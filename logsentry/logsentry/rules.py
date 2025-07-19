"""
Security detection rules for LogSentry
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DetectionRule:
    name: str
    description: str
    severity: Severity
    pattern: str
    category: str
    tags: List[str]
    regex_flags: int = re.IGNORECASE


@dataclass
class Detection:
    rule_name: str
    severity: Severity
    description: str
    matched_text: str
    line_number: int
    timestamp: Optional[str]
    category: str
    tags: List[str]
    confidence: float = 1.0


class SecurityRules:
    """Collection of security detection rules"""
    
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> List[DetectionRule]:
        """Initialize default security rules"""
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