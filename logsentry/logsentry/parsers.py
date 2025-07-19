"""
Log format parsers for different log types
"""

import re
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod
from .utils import normalize_timestamp, extract_ips_from_text, clean_log_line


@dataclass
class LogEntry:
    raw_line: str
    timestamp: Optional[datetime]
    source_ip: Optional[str]
    message: str
    fields: Dict[str, Any]
    log_type: str
    line_number: int = 0


class LogParser(ABC):
    """Abstract base class for log parsers"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def can_parse(self, line: str) -> bool:
        """Check if this parser can handle the given log line"""
        pass
    
    @abstractmethod
    def parse(self, line: str, line_number: int = 0) -> Optional[LogEntry]:
        """Parse a log line into a LogEntry"""
        pass


class ApacheAccessLogParser(LogParser):
    """Parser for Apache/Nginx access logs"""
    
    def __init__(self):
        super().__init__("apache_access")
        # Common Log Format pattern
        self.clf_pattern = re.compile(
            r'(\S+)\s+\S+\s+\S+\s+\[([^\]]+)\]\s+"([^"]+)"\s+(\d+)\s+(\d+|-)'
        )
        # Combined Log Format pattern
        self.combined_pattern = re.compile(
            r'(\S+)\s+\S+\s+\S+\s+\[([^\]]+)\]\s+"([^"]+)"\s+(\d+)\s+(\d+|-)\s+"([^"]*)"\s+"([^"]*)"'
        )
    
    def can_parse(self, line: str) -> bool:
        return bool(self.clf_pattern.match(line) or self.combined_pattern.match(line))
    
    def parse(self, line: str, line_number: int = 0) -> Optional[LogEntry]:
        line = clean_log_line(line)
        
        # Try combined format first (more detailed)
        match = self.combined_pattern.match(line)
        if match:
            ip, timestamp_str, request, status, size, referer, user_agent = match.groups()
            fields = {
                'request': request,
                'status_code': int(status),
                'response_size': int(size) if size != '-' else 0,
                'referer': referer,
                'user_agent': user_agent
            }
        else:
            # Try common log format
            match = self.clf_pattern.match(line)
            if not match:
                return None
            
            ip, timestamp_str, request, status, size = match.groups()
            fields = {
                'request': request,
                'status_code': int(status),
                'response_size': int(size) if size != '-' else 0
            }
        
        # Parse timestamp
        timestamp = normalize_timestamp(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')
        # Ensure timezone naive for consistency
        if timestamp and timestamp.tzinfo is not None:
            timestamp = timestamp.replace(tzinfo=None)
        
        # Extract method and URL from request
        request_parts = request.split(' ')
        if len(request_parts) >= 2:
            fields['method'] = request_parts[0]
            fields['url'] = request_parts[1]
            if len(request_parts) >= 3:
                fields['protocol'] = request_parts[2]
        
        return LogEntry(
            raw_line=line,
            timestamp=timestamp,
            source_ip=ip,
            message=request,
            fields=fields,
            log_type=self.name,
            line_number=line_number
        )


class SyslogParser(LogParser):
    """Parser for syslog format logs"""
    
    def __init__(self):
        super().__init__("syslog")
        # RFC3164 syslog pattern
        self.pattern = re.compile(
            r'<(\d+)>([A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+([^:]+):\s*(.*)'
        )
        # Alternative pattern without priority
        self.alt_pattern = re.compile(
            r'([A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+([^:]+):\s*(.*)'
        )
    
    def can_parse(self, line: str) -> bool:
        return bool(self.pattern.match(line) or self.alt_pattern.match(line))
    
    def parse(self, line: str, line_number: int = 0) -> Optional[LogEntry]:
        line = clean_log_line(line)
        
        match = self.pattern.match(line)
        if match:
            priority, timestamp_str, hostname, process, message = match.groups()
            fields = {
                'priority': int(priority),
                'hostname': hostname,
                'process': process,
                'facility': int(priority) >> 3,
                'severity': int(priority) & 7
            }
        else:
            match = self.alt_pattern.match(line)
            if not match:
                return None
            
            timestamp_str, hostname, process, message = match.groups()
            fields = {
                'hostname': hostname,
                'process': process
            }
        
        # Parse timestamp
        timestamp = normalize_timestamp(timestamp_str, '%b %d %H:%M:%S')
        
        # Extract IPs from message
        ips = extract_ips_from_text(message)
        source_ip = ips[0] if ips else None
        
        return LogEntry(
            raw_line=line,
            timestamp=timestamp,
            source_ip=source_ip,
            message=message,
            fields=fields,
            log_type=self.name,
            line_number=line_number
        )


class WindowsEventLogParser(LogParser):
    """Parser for Windows Event Log format"""
    
    def __init__(self):
        super().__init__("windows_event")
        self.pattern = re.compile(
            r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(\w+)\s+(\d+)\s+(\d+)\s+(.*)'
        )
    
    def can_parse(self, line: str) -> bool:
        return bool(self.pattern.match(line))
    
    def parse(self, line: str, line_number: int = 0) -> Optional[LogEntry]:
        line = clean_log_line(line)
        match = self.pattern.match(line)
        
        if not match:
            return None
        
        timestamp_str, level, event_id, task_category, message = match.groups()
        
        fields = {
            'level': level,
            'event_id': int(event_id),
            'task_category': int(task_category)
        }
        
        timestamp = normalize_timestamp(timestamp_str)
        
        # Extract IPs from message
        ips = extract_ips_from_text(message)
        source_ip = ips[0] if ips else None
        
        return LogEntry(
            raw_line=line,
            timestamp=timestamp,
            source_ip=source_ip,
            message=message,
            fields=fields,
            log_type=self.name,
            line_number=line_number
        )


class FirewallLogParser(LogParser):
    """Parser for firewall logs (iptables, pf, etc.)"""
    
    def __init__(self):
        super().__init__("firewall")
        # iptables pattern
        self.iptables_pattern = re.compile(
            r'.*kernel:.*IN=(\S*)\s+OUT=(\S*)\s+.*SRC=(\S+)\s+DST=(\S+).*PROTO=(\S+).*SPT=(\d+).*DPT=(\d+)'
        )
    
    def can_parse(self, line: str) -> bool:
        return 'kernel:' in line and ('SRC=' in line or 'DST=' in line)
    
    def parse(self, line: str, line_number: int = 0) -> Optional[LogEntry]:
        line = clean_log_line(line)
        match = self.iptables_pattern.search(line)
        
        if not match:
            return None
        
        in_if, out_if, src_ip, dst_ip, protocol, src_port, dst_port = match.groups()
        
        fields = {
            'in_interface': in_if,
            'out_interface': out_if,
            'destination_ip': dst_ip,
            'protocol': protocol,
            'source_port': int(src_port),
            'destination_port': int(dst_port)
        }
        
        # Extract timestamp from beginning of line
        timestamp_match = re.search(r'([A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})', line)
        timestamp = None
        if timestamp_match:
            timestamp = normalize_timestamp(timestamp_match.group(1), '%b %d %H:%M:%S')
        
        return LogEntry(
            raw_line=line,
            timestamp=timestamp,
            source_ip=src_ip,
            message=line,
            fields=fields,
            log_type=self.name,
            line_number=line_number
        )


class JSONLogParser(LogParser):
    """Parser for JSON formatted logs"""
    
    def __init__(self):
        super().__init__("json")
    
    def can_parse(self, line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith('{') and stripped.endswith('}')
    
    def parse(self, line: str, line_number: int = 0) -> Optional[LogEntry]:
        import json
        
        line = clean_log_line(line)
        
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            return None
        
        # Common timestamp field names
        timestamp = None
        for ts_field in ['timestamp', 'time', '@timestamp', 'datetime', 'date']:
            if ts_field in data:
                timestamp = normalize_timestamp(str(data[ts_field]))
                break
        
        # Common IP field names
        source_ip = None
        for ip_field in ['src_ip', 'source_ip', 'client_ip', 'remote_addr', 'ip']:
            if ip_field in data:
                source_ip = str(data[ip_field])
                break
        
        # Common message field names
        message = ""
        for msg_field in ['message', 'msg', 'log', 'event', 'description']:
            if msg_field in data:
                message = str(data[msg_field])
                break
        
        if not message:
            message = line[:200]  # Fallback to truncated raw line
        
        return LogEntry(
            raw_line=line,
            timestamp=timestamp,
            source_ip=source_ip,
            message=message,
            fields=data,
            log_type=self.name,
            line_number=line_number
        )


class GenericLogParser(LogParser):
    """Generic parser for unstructured logs"""
    
    def __init__(self):
        super().__init__("generic")
    
    def can_parse(self, line: str) -> bool:
        return True  # This parser accepts any line
    
    def parse(self, line: str, line_number: int = 0) -> Optional[LogEntry]:
        line = clean_log_line(line)
        
        if not line:
            return None
        
        # Try to extract timestamp from beginning of line
        timestamp = None
        timestamp_patterns = [
            r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}',
            r'\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}',
            r'[A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}',
        ]
        
        for pattern in timestamp_patterns:
            match = re.search(pattern, line[:50])  # Look in first 50 chars
            if match:
                timestamp = normalize_timestamp(match.group(0))
                break
        
        # Extract IPs
        ips = extract_ips_from_text(line)
        source_ip = ips[0] if ips else None
        
        return LogEntry(
            raw_line=line,
            timestamp=timestamp,
            source_ip=source_ip,
            message=line,
            fields={},
            log_type=self.name,
            line_number=line_number
        )


class LogParserManager:
    """Manager for multiple log parsers"""
    
    def __init__(self):
        self.parsers = [
            ApacheAccessLogParser(),
            SyslogParser(),
            WindowsEventLogParser(),
            FirewallLogParser(),
            JSONLogParser(),
            GenericLogParser(),  # Keep this last as fallback
        ]
    
    def add_parser(self, parser: LogParser):
        """Add a custom parser"""
        # Insert before the generic parser (which should be last)
        self.parsers.insert(-1, parser)
    
    def parse_line(self, line: str, line_number: int = 0) -> Optional[LogEntry]:
        """Parse a line using the first compatible parser"""
        for parser in self.parsers:
            if parser.can_parse(line):
                return parser.parse(line, line_number)
        return None
    
    def parse_lines(self, lines: List[str], start_line: int = 1) -> List[LogEntry]:
        """Parse multiple lines"""
        entries = []
        for i, line in enumerate(lines):
            line_number = start_line + i
            entry = self.parse_line(line, line_number)
            if entry:
                entries.append(entry)
        return entries
    
    def get_parser_stats(self, entries: List[LogEntry]) -> Dict[str, int]:
        """Get statistics about which parsers were used"""
        stats = {}
        for entry in entries:
            stats[entry.log_type] = stats.get(entry.log_type, 0) + 1
        return stats