"""
Core log analysis engine for LogSentry

Created by Anthony Frederick, 2025
This module contains the main analysis engine that orchestrates log parsing,
threat detection, IP analysis, and result generation. It provides the primary
interface for analyzing individual files, directories, and text data for
security threats and generates comprehensive analysis reports.
"""

import os
import gzip
from typing import Dict, List, Any, Optional, Tuple, Generator
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import json

from .parsers import LogParserManager, LogEntry
from .rules import RuleEngine, Detection, Severity
from .utils import (
    is_valid_ip, is_private_ip, extract_ips_from_text,
    get_geolocation_info, format_bytes
)


@dataclass
class AnalysisResult:
    """
    Comprehensive result data structure for log analysis operations
    
    Contains all analysis results including detections, statistics, timelines,
    and metadata for a single log analysis operation. This is the primary
    output format returned by LogSentry's analysis functions.
    
    Attributes:
        file_path (str): Path to the analyzed log file or source identifier
        total_lines (int): Total number of lines processed
        parsed_lines (int): Number of lines successfully parsed
        detections (List[Detection]): All security threats detected
        summary (Dict[str, Any]): Summary statistics and aggregated data
        analysis_time (float): Time taken to complete analysis (seconds)
        log_types (Dict[str, int]): Count of entries by log format type
        ip_analysis (Dict[str, Any]): IP address analysis results
        timeline (List[Dict[str, Any]]): Chronological timeline of events
    """
    file_path: str                              # Source file path or identifier
    total_lines: int                            # Total lines processed
    parsed_lines: int                           # Successfully parsed lines
    detections: List[Detection]                 # All detected security threats
    summary: Dict[str, Any]                     # Analysis summary statistics
    analysis_time: float                        # Processing time in seconds
    log_types: Dict[str, int]                   # Log format distribution
    ip_analysis: Dict[str, Any]                 # IP address analysis results
    timeline: List[Dict[str, Any]]              # Event timeline data


@dataclass
class IPAnalysis:
    """
    Data structure for individual IP address analysis results
    
    Contains comprehensive information about a specific IP address found
    in the log data, including activity patterns, threat associations,
    and geolocation information.
    
    Attributes:
        ip (str): The IP address being analyzed
        count (int): Number of times this IP appears in logs
        is_private (bool): Whether IP is in private address space
        first_seen (Optional[datetime]): First occurrence timestamp
        last_seen (Optional[datetime]): Last occurrence timestamp
        detections (List[Detection]): Security threats associated with this IP
        geolocation (Dict[str, Any]): Geographic and network information
    """
    ip: str                                     # IP address string
    count: int                                  # Frequency count in logs
    is_private: bool                            # Private vs public IP flag
    first_seen: Optional[datetime]              # First seen timestamp
    last_seen: Optional[datetime]               # Last seen timestamp
    detections: List[Detection]                 # Associated threat detections
    geolocation: Dict[str, Any]                 # Geographic/network metadata


class LogAnalyzer:
    """
    Main log analysis engine that orchestrates the complete analysis process
    
    This is the central component of LogSentry that coordinates log parsing,
    threat detection, IP analysis, and result generation. It supports analysis
    of individual files, directories, compressed files, and raw text data.
    
    Key Features:
    - Multi-format log parsing (Apache, syslog, JSON, etc.)
    - Real-time threat detection using security rules
    - IP address analysis and geolocation
    - Performance optimization with chunk-based processing
    - Comprehensive reporting and export capabilities
    - Support for custom security rules
    
    Performance Characteristics:
    - Memory efficient: Processes large files in configurable chunks
    - Fast: Compiled regex patterns for efficient threat detection
    - Scalable: Handles multiple files and directory scanning
    """
    
    def __init__(self, custom_rules: Optional[List] = None):
        """
        Initialize the LogAnalyzer with parsers, rules, and configuration
        
        Sets up the complete analysis pipeline including log parsers for
        different formats, security detection rules, and performance settings.
        Optionally accepts custom rules to extend the built-in detection
        capabilities.
        
        Args:
            custom_rules (Optional[List]): List of custom DetectionRule objects
                                          to add to the built-in rule set
        
        Example:
            >>> analyzer = LogAnalyzer()  # Use built-in rules only
            >>> 
            >>> # Or with custom rules
            >>> custom_rule = DetectionRule(name="my_rule", ...)
            >>> analyzer = LogAnalyzer(custom_rules=[custom_rule])
        """
        # Initialize log format parsers (Apache, syslog, JSON, etc.)
        self.parser_manager = LogParserManager()
        
        # Initialize security detection rule engine
        self.rule_engine = RuleEngine()
        
        # Performance tuning: process logs in chunks to manage memory usage
        # Larger chunks = faster processing but more memory usage
        self.chunk_size = 10000  # Process 10,000 lines at a time
        
        # Add custom security rules if provided by user
        if custom_rules:
            for rule in custom_rules:
                self.rule_engine.rules.add_custom_rule(rule)
            # Recompile regex patterns after adding custom rules for performance
            self.rule_engine._compile_patterns()
    
    def analyze_file(self, file_path: str, max_lines: Optional[int] = None) -> AnalysisResult:
        """Analyze a single log file"""
        start_time = datetime.now()
        
        detections = []
        log_entries = []
        total_lines = 0
        parsed_lines = 0
        
        try:
            # Determine if file is compressed
            open_func = gzip.open if file_path.endswith('.gz') else open
            mode = 'rt' if file_path.endswith('.gz') else 'r'
            
            with open_func(file_path, mode, encoding='utf-8', errors='ignore') as f:
                for chunk in self._read_in_chunks(f, max_lines):
                    chunk_entries = self.parser_manager.parse_lines(chunk, total_lines + 1)
                    chunk_detections = self.rule_engine.analyze_log_chunk(chunk)
                    
                    log_entries.extend(chunk_entries)
                    detections.extend(chunk_detections)
                    
                    total_lines += len(chunk)
                    parsed_lines += len(chunk_entries)
        
        except Exception as e:
            raise Exception(f"Error analyzing file {file_path}: {str(e)}")
        
        # Generate analysis results
        analysis_time = (datetime.now() - start_time).total_seconds()
        
        # Get log type statistics
        log_types = self.parser_manager.get_parser_stats(log_entries)
        
        # Perform IP analysis
        ip_analysis = self._analyze_ips(log_entries, detections)
        
        # Generate timeline
        timeline = self._generate_timeline(detections)
        
        # Generate summary
        summary = self._generate_summary(detections, log_entries, ip_analysis)
        
        return AnalysisResult(
            file_path=file_path,
            total_lines=total_lines,
            parsed_lines=parsed_lines,
            detections=detections,
            summary=summary,
            analysis_time=analysis_time,
            log_types=log_types,
            ip_analysis=ip_analysis,
            timeline=timeline
        )
    
    def analyze_directory(self, directory: str, pattern: str = "*.log") -> List[AnalysisResult]:
        """Analyze all log files in a directory"""
        import glob
        
        results = []
        log_files = glob.glob(os.path.join(directory, pattern))
        
        for file_path in log_files:
            try:
                result = self.analyze_file(file_path)
                results.append(result)
            except Exception as e:
                print(f"Warning: Failed to analyze {file_path}: {e}")
        
        return results
    
    def analyze_text(self, text: str, source_name: str = "text_input") -> AnalysisResult:
        """Analyze log text directly"""
        start_time = datetime.now()
        
        lines = text.strip().split('\n')
        log_entries = self.parser_manager.parse_lines(lines)
        detections = self.rule_engine.analyze_log_chunk(lines)
        
        analysis_time = (datetime.now() - start_time).total_seconds()
        log_types = self.parser_manager.get_parser_stats(log_entries)
        ip_analysis = self._analyze_ips(log_entries, detections)
        timeline = self._generate_timeline(detections)
        summary = self._generate_summary(detections, log_entries, ip_analysis)
        
        return AnalysisResult(
            file_path=source_name,
            total_lines=len(lines),
            parsed_lines=len(log_entries),
            detections=detections,
            summary=summary,
            analysis_time=analysis_time,
            log_types=log_types,
            ip_analysis=ip_analysis,
            timeline=timeline
        )
    
    def _read_in_chunks(self, file_obj, max_lines: Optional[int] = None) -> Generator[List[str], None, None]:
        """Read file in chunks to manage memory usage"""
        chunk = []
        lines_read = 0
        
        for line in file_obj:
            if max_lines and lines_read >= max_lines:
                break
            
            chunk.append(line.rstrip('\n\r'))
            lines_read += 1
            
            if len(chunk) >= self.chunk_size:
                yield chunk
                chunk = []
        
        if chunk:
            yield chunk
    
    def _analyze_ips(self, log_entries: List[LogEntry], detections: List[Detection]) -> Dict[str, Any]:
        """Analyze IP addresses found in logs"""
        ip_stats = defaultdict(lambda: {
            'count': 0,
            'first_seen': None,
            'last_seen': None,
            'detections': [],
            'is_private': False,
            'geolocation': {}
        })
        
        # Collect IP statistics from log entries
        for entry in log_entries:
            if entry.source_ip and is_valid_ip(entry.source_ip):
                ip = entry.source_ip
                ip_stats[ip]['count'] += 1
                ip_stats[ip]['is_private'] = is_private_ip(ip)
                
                if entry.timestamp:
                    if not ip_stats[ip]['first_seen'] or entry.timestamp < ip_stats[ip]['first_seen']:
                        ip_stats[ip]['first_seen'] = entry.timestamp
                    if not ip_stats[ip]['last_seen'] or entry.timestamp > ip_stats[ip]['last_seen']:
                        ip_stats[ip]['last_seen'] = entry.timestamp
        
        # Associate detections with IPs
        for detection in detections:
            ips_in_detection = extract_ips_from_text(detection.matched_text)
            for ip in ips_in_detection:
                if ip in ip_stats:
                    ip_stats[ip]['detections'].append(detection)
        
        # Get geolocation for external IPs (placeholder)
        for ip, stats in ip_stats.items():
            if not stats['is_private']:
                stats['geolocation'] = get_geolocation_info(ip)
        
        # Convert to final format
        result = {
            'total_unique_ips': len(ip_stats),
            'private_ips': sum(1 for stats in ip_stats.values() if stats['is_private']),
            'public_ips': sum(1 for stats in ip_stats.values() if not stats['is_private']),
            'top_ips': sorted(
                [{'ip': ip, **stats} for ip, stats in ip_stats.items()],
                key=lambda x: x['count'],
                reverse=True
            )[:20],
            'suspicious_ips': [
                {'ip': ip, **stats} for ip, stats in ip_stats.items()
                if len(stats['detections']) > 0
            ]
        }
        
        return result
    
    def _generate_timeline(self, detections: List[Detection]) -> List[Dict[str, Any]]:
        """Generate timeline of security events"""
        if not detections:
            return []
        
        # Group detections by hour
        timeline = defaultdict(lambda: {
            'timestamp': None,
            'total_detections': 0,
            'by_severity': Counter(),
            'by_category': Counter(),
            'events': []
        })
        
        for detection in detections:
            if detection.timestamp:
                try:
                    # Parse timestamp if it's a string
                    if isinstance(detection.timestamp, str):
                        from .utils import normalize_timestamp
                        dt = normalize_timestamp(detection.timestamp)
                    else:
                        dt = detection.timestamp
                    
                    if dt:
                        # Round to nearest hour - ensure timezone naive
                        if dt.tzinfo is not None:
                            dt = dt.replace(tzinfo=None)
                        hour_key = dt.replace(minute=0, second=0, microsecond=0)
                        timeline[hour_key]['timestamp'] = hour_key
                        timeline[hour_key]['total_detections'] += 1
                        timeline[hour_key]['by_severity'][detection.severity.value] += 1
                        timeline[hour_key]['by_category'][detection.category] += 1
                        timeline[hour_key]['events'].append({
                            'rule': detection.rule_name,
                            'severity': detection.severity.value,
                            'category': detection.category,
                            'line': detection.line_number
                        })
                except Exception:
                    continue  # Skip detections with unparseable timestamps
        
        # Convert to sorted list
        sorted_timeline = sorted(timeline.values(), key=lambda x: x['timestamp'] or datetime.min)
        
        return sorted_timeline
    
    def _generate_summary(self, detections: List[Detection], log_entries: List[LogEntry], ip_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive analysis summary"""
        summary = self.rule_engine.get_detection_summary(detections)
        
        # Add additional summary information
        summary.update({
            'log_entries_parsed': len(log_entries),
            'unique_ips': ip_analysis['total_unique_ips'],
            'private_ips': ip_analysis['private_ips'],
            'public_ips': ip_analysis['public_ips'],
            'suspicious_ips': len(ip_analysis['suspicious_ips']),
        })
        
        # Top threats
        if detections:
            summary['top_threats'] = [
                {
                    'rule': rule_name,
                    'count': count,
                    'severity': next(d.severity.value for d in detections if d.rule_name == rule_name)
                }
                for rule_name, count in summary.get('by_rule', {}).items()
            ]
            summary['top_threats'].sort(key=lambda x: x['count'], reverse=True)
            summary['top_threats'] = summary['top_threats'][:10]
        else:
            summary['top_threats'] = []
        
        # Risk score calculation
        risk_score = self._calculate_risk_score(detections, ip_analysis)
        summary['risk_score'] = risk_score
        
        return summary
    
    def _calculate_risk_score(self, detections: List[Detection], ip_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall risk score based on detections and indicators"""
        if not detections:
            return {'score': 0, 'level': 'low', 'factors': []}
        
        base_score = 0
        factors = []
        
        # Score based on detection severity
        severity_weights = {
            Severity.LOW: 1,
            Severity.MEDIUM: 3,
            Severity.HIGH: 7,
            Severity.CRITICAL: 15
        }
        
        for detection in detections:
            base_score += severity_weights.get(detection.severity, 1) * detection.confidence
        
        # Additional risk factors
        if ip_analysis['suspicious_ips']:
            suspicious_count = len(ip_analysis['suspicious_ips'])
            base_score += suspicious_count * 2
            factors.append(f"{suspicious_count} suspicious IP(s) detected")
        
        if ip_analysis['public_ips'] > 50:
            base_score += 5
            factors.append("High number of external IPs")
        
        # Normalize score to 0-100 range
        normalized_score = min(100, int(base_score / max(1, len(detections)) * 10))
        
        # Determine risk level
        if normalized_score >= 80:
            level = 'critical'
        elif normalized_score >= 60:
            level = 'high'
        elif normalized_score >= 30:
            level = 'medium'
        else:
            level = 'low'
        
        return {
            'score': normalized_score,
            'level': level,
            'factors': factors
        }
    
    def export_results(self, result: AnalysisResult, output_file: str, format_type: str = 'json'):
        """Export analysis results to file"""
        if format_type.lower() == 'json':
            self._export_json(result, output_file)
        elif format_type.lower() == 'csv':
            self._export_csv(result, output_file)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _export_json(self, result: AnalysisResult, output_file: str):
        """Export results as JSON"""
        # Convert result to dict, handling datetime serialization
        data = asdict(result)
        
        # Convert datetime objects to strings
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {k: convert_datetime(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_datetime(item) for item in obj]
            return obj
        
        data = convert_datetime(data)
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _export_csv(self, result: AnalysisResult, output_file: str):
        """Export detections as CSV"""
        import csv
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Line Number', 'Timestamp', 'Severity', 'Rule Name',
                'Category', 'Description', 'Matched Text', 'Confidence'
            ])
            
            for detection in result.detections:
                writer.writerow([
                    detection.line_number,
                    detection.timestamp or '',
                    detection.severity.value,
                    detection.rule_name,
                    detection.category,
                    detection.description,
                    detection.matched_text[:100],  # Truncate for readability
                    f"{detection.confidence:.2f}"
                ])


def merge_analysis_results(results: List[AnalysisResult]) -> Dict[str, Any]:
    """Merge multiple analysis results into a comprehensive report"""
    if not results:
        return {}
    
    merged = {
        'total_files': len(results),
        'total_lines': sum(r.total_lines for r in results),
        'total_detections': sum(len(r.detections) for r in results),
        'total_analysis_time': sum(r.analysis_time for r in results),
        'files': [r.file_path for r in results],
        'combined_summary': {},
        'top_threats_across_files': Counter(),
        'timeline': []
    }
    
    # Combine all detections
    all_detections = []
    for result in results:
        all_detections.extend(result.detections)
    
    # Generate combined summary
    if all_detections:
        rule_engine = RuleEngine()  # Temporary instance for summary
        merged['combined_summary'] = rule_engine.get_detection_summary(all_detections)
        
        # Count threats across all files
        for detection in all_detections:
            merged['top_threats_across_files'][detection.rule_name] += 1
    
    # Combine timelines
    all_timeline_events = []
    for result in results:
        all_timeline_events.extend(result.timeline)
    
    merged['timeline'] = sorted(all_timeline_events, key=lambda x: x.get('timestamp', datetime.min))
    
    return merged