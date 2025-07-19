"""
Security detection rules for LogSentry

Created by Anthony Frederick, 2025
This module defines the security detection rules engine that powers LogSentry's
threat detection capabilities. It includes rule definitions, severity levels,
detection logic, and analysis engines for identifying security threats in log data.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """
    Enumeration of threat severity levels used throughout LogSentry
    
    These levels help prioritize security incidents and determine response urgency:
    - LOW: Informational events, potential reconnaissance
    - MEDIUM: Suspicious activity requiring monitoring
    - HIGH: Likely security incidents requiring investigation
    - CRITICAL: Active attacks requiring immediate response
    """
    LOW = "low"           # Informational/reconnaissance activity
    MEDIUM = "medium"     # Suspicious activity worth monitoring
    HIGH = "high"         # Likely security incident
    CRITICAL = "critical" # Active attack requiring immediate response


@dataclass
class DetectionRule:
    """
    Data class representing a single security detection rule
    
    Each rule defines a pattern to match against log entries, along with
    metadata about the threat type, severity, and categorization. Rules
    are compiled into regex patterns for efficient matching.
    
    Attributes:
        name (str): Unique identifier for the rule
        description (str): Human-readable description of what the rule detects
        severity (Severity): Threat severity level (LOW, MEDIUM, HIGH, CRITICAL)
        pattern (str): Regex pattern to match against log entries
        category (str): Threat category (e.g., 'web_attack', 'authentication')
        tags (List[str]): List of tags for classification and filtering
        regex_flags (int): Regex compilation flags (default: re.IGNORECASE)
    """
    name: str                                    # Unique rule identifier
    description: str                             # Human-readable description
    severity: Severity                           # Threat severity level
    pattern: str                                 # Regex pattern for matching
    category: str                                # Threat category
    tags: List[str]                             # Classification tags
    regex_flags: int = re.IGNORECASE            # Regex compilation flags


@dataclass
class Detection:
    """
    Data class representing a security threat detection instance
    
    Created when a rule matches against a log entry. Contains all relevant
    information about the detected threat including context, confidence,
    and metadata for analysis and reporting.
    
    Attributes:
        rule_name (str): Name of the rule that triggered
        severity (Severity): Severity level of the detected threat
        description (str): Description of the threat
        matched_text (str): Text that matched the rule pattern
        line_number (int): Line number where threat was detected
        timestamp (Optional[str]): Timestamp of the log entry
        category (str): Threat category
        tags (List[str]): Rule tags for classification
        confidence (float): Confidence score (0.0-1.0) of the detection
    """
    rule_name: str                               # Name of triggered rule
    severity: Severity                           # Threat severity level
    description: str                             # Threat description
    matched_text: str                            # Matching text portion
    line_number: int                             # Line number in log file
    timestamp: Optional[str]                     # Log entry timestamp
    category: str                                # Threat category
    tags: List[str]                             # Classification tags
    confidence: float = 1.0                     # Detection confidence (0.0-1.0)


class SecurityRules:
    """
    Collection and management of security detection rules
    
    This class maintains the complete set of detection rules used by LogSentry
    to identify security threats. It includes built-in rules for common attack
    patterns and provides methods to add custom rules, filter rules, and
    manage the rule set.
    
    The built-in rules cover major threat categories:
    - Web attacks (SQL injection, XSS, directory traversal)
    - Authentication attacks (brute force, credential stuffing)
    - Network attacks (port scans, suspicious user agents)
    - System attacks (privilege escalation, file access)
    - Malware and data exfiltration
    """
    
    def __init__(self):
        """
        Initialize the SecurityRules with default built-in detection rules
        
        Loads and configures all the standard security detection rules that
        ship with LogSentry. These rules cover the most common attack patterns
        and security threats found in typical enterprise environments.
        """
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> List[DetectionRule]:
        """
        Initialize and return the complete set of built-in security detection rules
        
        This method defines all the default rules that LogSentry uses to detect
        security threats. Rules are organized by category and cover various
        attack vectors and threat types commonly seen in log data.
        
        Returns:
            List[DetectionRule]: Complete list of initialized detection rules
            
        Rule Categories:
            - Authentication: Failed logins, brute force, credential stuffing
            - Web Attacks: SQL injection, XSS, directory traversal, command injection
            - Network: Port scanning, suspicious user agents, DNS tunneling
            - System: Privilege escalation, file access, reverse shells
            - Data Exfiltration: Large transfers, suspicious downloads
        """
        return [
            # Authentication attacks
            DetectionRule(
                name="failed_login_attempt",
                description="Failed login attempt detected",
                severity=Severity.MEDIUM,
                pattern=r"(failed login|authentication failed|invalid credentials|login failed|auth.*fail)",
                category="authentication",
                tags=["bruteforce", "authentication"]
            ),
            
            DetectionRule(
                name="multiple_failed_logins",
                description="Multiple failed login attempts from same source",
                severity=Severity.HIGH,
                pattern=r"(\d+\.\d+\.\d+\.\d+).*failed.*login.*(\1.*failed.*login.*){2,}",
                category="authentication",
                tags=["bruteforce", "authentication", "repeated"]
            ),
            
            DetectionRule(
                name="privileged_escalation",
                description="Potential privilege escalation attempt",
                severity=Severity.HIGH,
                pattern=r"(sudo|su |runas|privilege.*escalat|become.*root)",
                category="privilege_escalation",
                tags=["privilege_escalation", "admin"]
            ),
            
            # Web attacks
            DetectionRule(
                name="sql_injection",
                description="SQL injection attempt detected",
                severity=Severity.HIGH,
                pattern=r"('.*(union|select|insert|delete|drop|alter|exec|script).*'|'.*or.*1.*=.*1|'.*and.*1.*=.*1|(union|select|insert|delete|drop|alter).*from)",
                category="web_attack",
                tags=["sqli", "injection", "web"]
            ),
            
            DetectionRule(
                name="xss_attempt",
                description="Cross-Site Scripting (XSS) attempt",
                severity=Severity.HIGH,
                pattern=r"(<script|javascript:|onload=|onerror=|<iframe|eval\(|document\.cookie)",
                category="web_attack",
                tags=["xss", "injection", "web"]
            ),
            
            DetectionRule(
                name="lfi_rfi_attempt",
                description="Local/Remote File Inclusion attempt",
                severity=Severity.HIGH,
                pattern=r"(\.\./|\.\.\\|/etc/passwd|/etc/shadow|/windows/system32|\\windows\\system32|php://|file://|http://.*\?.*=http)",
                category="web_attack",
                tags=["lfi", "rfi", "file_inclusion"]
            ),
            
            DetectionRule(
                name="command_injection",
                description="Command injection attempt",
                severity=Severity.CRITICAL,
                pattern=r"(;|\||&|`|\$\(|%0a|%0d|%3b|%7c)(cat |ls |id |whoami |nc |netcat |wget |curl |python |perl |bash |sh )",
                category="web_attack",
                tags=["command_injection", "rce"]
            ),
            
            # Network attacks
            DetectionRule(
                name="port_scan",
                description="Port scanning activity detected",
                severity=Severity.MEDIUM,
                pattern=r"(nmap|masscan|zmap|port.*scan|connection.*refused.*(\d+\.\d+\.\d+\.\d+).*){3,}",
                category="network_attack",
                tags=["port_scan", "reconnaissance"]
            ),
            
            DetectionRule(
                name="suspicious_user_agent",
                description="Suspicious user agent detected",
                severity=Severity.MEDIUM,
                pattern=r"user.agent.*(sqlmap|nikto|nmap|burp|dirb|gobuster|wfuzz|hydra|medusa)",
                category="network_attack",
                tags=["suspicious_ua", "scanning"]
            ),
            
            # Malware and suspicious activity
            DetectionRule(
                name="suspicious_file_access",
                description="Access to suspicious files",
                severity=Severity.HIGH,
                pattern=r"(/etc/passwd|/etc/shadow|/windows/system32/sam|\.ssh/id_rsa|\.aws/credentials)",
                category="file_access",
                tags=["sensitive_files", "credential_access"]
            ),
            
            DetectionRule(
                name="crypto_mining",
                description="Cryptocurrency mining activity",
                severity=Severity.MEDIUM,
                pattern=r"(stratum\+tcp|pool\..*\.com|xmrig|ccminer|cryptonight|monero|bitcoin|ethereum)",
                category="malware",
                tags=["cryptomining", "malware"]
            ),
            
            DetectionRule(
                name="reverse_shell",
                description="Reverse shell attempt",
                severity=Severity.CRITICAL,
                pattern=r"(nc.*-e|/bin/sh|/bin/bash.*-i|python.*socket.*exec|perl.*socket)",
                category="malware",
                tags=["reverse_shell", "backdoor"]
            ),
            
            # Data exfiltration
            DetectionRule(
                name="data_exfiltration",
                description="Potential data exfiltration",
                severity=Severity.HIGH,
                pattern=r"(wget|curl|scp|rsync|ftp).*-O.*\.(sql|db|backup|dump|csv|xlsx?)",
                category="data_exfiltration",
                tags=["exfiltration", "data_theft"]
            ),
            
            DetectionRule(
                name="large_data_transfer",
                description="Large data transfer detected",
                severity=Severity.MEDIUM,
                pattern=r"(POST|PUT).*content-length:\s*([1-9]\d{7,})",  # 10MB+
                category="data_exfiltration",
                tags=["large_transfer", "exfiltration"]
            ),
            
            # Error conditions that might indicate attacks
            DetectionRule(
                name="http_error_spike",
                description="HTTP error response (potential attack)",
                severity=Severity.LOW,
                pattern=r"HTTP/1\.[01].*[45]\d{2}",
                category="web_error",
                tags=["http_error", "web"]
            ),
            
            DetectionRule(
                name="directory_traversal",
                description="Directory traversal attempt",
                severity=Severity.HIGH,
                pattern=r"(\.\./|\.\.\\|%2e%2e%2f|%2e%2e%5c|\\\.\.\\)",
                category="web_attack",
                tags=["directory_traversal", "path_traversal"]
            ),
            
            # DNS attacks
            DetectionRule(
                name="dns_tunneling",
                description="Potential DNS tunneling",
                severity=Severity.HIGH,
                pattern=r"[a-f0-9]{20,}\..*\.(com|net|org)",
                category="network_attack",
                tags=["dns_tunneling", "exfiltration"]
            ),
            
            # Credential stuffing
            DetectionRule(
                name="credential_stuffing",
                description="Credential stuffing attack",
                severity=Severity.HIGH,
                pattern=r"(\d+\.\d+\.\d+\.\d+).*POST.*/login.*(\1.*POST.*/login.*){5,}",
                category="authentication",
                tags=["credential_stuffing", "bruteforce"]
            ),
        ]
    
    def add_custom_rule(self, rule: DetectionRule):
        """Add a custom detection rule"""
        self.rules.append(rule)
    
    def remove_rule(self, rule_name: str):
        """Remove a rule by name"""
        self.rules = [rule for rule in self.rules if rule.name != rule_name]
    
    def get_rules_by_category(self, category: str) -> List[DetectionRule]:
        """Get rules filtered by category"""
        return [rule for rule in self.rules if rule.category == category]
    
    def get_rules_by_severity(self, severity: Severity) -> List[DetectionRule]:
        """Get rules filtered by severity"""
        return [rule for rule in self.rules if rule.severity == severity]
    
    def get_rule_by_name(self, name: str) -> Optional[DetectionRule]:
        """Get a specific rule by name"""
        for rule in self.rules:
            if rule.name == name:
                return rule
        return None


class RuleEngine:
    """Engine for applying security rules to log data"""
    
    def __init__(self, rules: Optional[SecurityRules] = None):
        self.rules = rules or SecurityRules()
        self.compiled_patterns = {}
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Pre-compile regex patterns for better performance"""
        for rule in self.rules.rules:
            try:
                self.compiled_patterns[rule.name] = re.compile(rule.pattern, rule.regex_flags)
            except re.error as e:
                print(f"Warning: Failed to compile pattern for rule '{rule.name}': {e}")
    
    def analyze_line(self, line: str, line_number: int, timestamp: Optional[str] = None) -> List[Detection]:
        """Analyze a single log line against all rules"""
        detections = []
        
        for rule in self.rules.rules:
            pattern = self.compiled_patterns.get(rule.name)
            if not pattern:
                continue
            
            matches = pattern.findall(line)
            if matches:
                # Calculate confidence based on match quality
                confidence = self._calculate_confidence(rule, line, matches)
                
                detection = Detection(
                    rule_name=rule.name,
                    severity=rule.severity,
                    description=rule.description,
                    matched_text=str(matches[0]) if matches else line[:100],
                    line_number=line_number,
                    timestamp=timestamp,
                    category=rule.category,
                    tags=rule.tags,
                    confidence=confidence
                )
                detections.append(detection)
        
        return detections
    
    def _calculate_confidence(self, rule: DetectionRule, line: str, matches: List) -> float:
        """Calculate confidence score for a detection"""
        base_confidence = 0.7
        
        # Adjust based on rule severity
        severity_boost = {
            Severity.LOW: 0.0,
            Severity.MEDIUM: 0.1,
            Severity.HIGH: 0.2,
            Severity.CRITICAL: 0.3
        }
        
        confidence = base_confidence + severity_boost.get(rule.severity, 0.0)
        
        # Boost confidence for multiple matches
        if len(matches) > 1:
            confidence += 0.1
        
        # Reduce confidence for very short matches
        if matches and len(str(matches[0])) < 5:
            confidence -= 0.1
        
        return min(1.0, max(0.1, confidence))
    
    def analyze_log_chunk(self, lines: List[str], start_line: int = 1) -> List[Detection]:
        """Analyze a chunk of log lines"""
        all_detections = []
        
        for i, line in enumerate(lines):
            line_number = start_line + i
            detections = self.analyze_line(line, line_number)
            all_detections.extend(detections)
        
        return all_detections
    
    def get_detection_summary(self, detections: List[Detection]) -> Dict[str, Any]:
        """Generate summary statistics for detections"""
        if not detections:
            return {"total": 0, "by_severity": {}, "by_category": {}}
        
        summary = {
            "total": len(detections),
            "by_severity": {},
            "by_category": {},
            "by_rule": {},
            "confidence_avg": sum(d.confidence for d in detections) / len(detections)
        }
        
        for detection in detections:
            # Count by severity
            severity_key = detection.severity.value
            summary["by_severity"][severity_key] = summary["by_severity"].get(severity_key, 0) + 1
            
            # Count by category
            summary["by_category"][detection.category] = summary["by_category"].get(detection.category, 0) + 1
            
            # Count by rule
            summary["by_rule"][detection.rule_name] = summary["by_rule"].get(detection.rule_name, 0) + 1
        
        return summary