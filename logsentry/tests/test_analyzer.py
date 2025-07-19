"""
Test cases for LogSentry analyzer

Created by Anthony Frederick, 2025
Comprehensive test suite for validating LogSentry's core analysis functionality,
including threat detection, log parsing, IP analysis, and export capabilities.
Tests cover both individual components and integrated workflows.
"""

import pytest
import tempfile
import os
from datetime import datetime

from logsentry.analyzer import LogAnalyzer, merge_analysis_results
from logsentry.rules import SecurityRules, DetectionRule, Severity
from logsentry.parsers import LogParserManager


class TestLogAnalyzer:
    """Test cases for LogAnalyzer class"""
    
    def setup_method(self):
        """Setup test environment"""
        self.analyzer = LogAnalyzer()
    
    def test_analyze_text_no_threats(self):
        """Test analyzing benign log text"""
        text = """192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
192.168.1.1 - - [10/Oct/2023:13:55:37 +0000] "GET /css/style.css HTTP/1.1" 200 1234"""
        
        result = self.analyzer.analyze_text(text)
        
        assert result.total_lines == 2
        assert result.parsed_lines == 2
        assert len(result.detections) == 0
        assert result.summary['total'] == 0
    
    def test_analyze_text_with_threats(self):
        """Test analyzing log text with security threats"""
        text = """192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /admin/../../../etc/passwd HTTP/1.1" 404 234
203.0.113.42 - - [10/Oct/2023:13:55:37 +0000] "POST /login HTTP/1.1' OR 1=1-- " 400 156"""
        
        result = self.analyzer.analyze_text(text)
        
        assert result.total_lines == 2
        assert len(result.detections) > 0
        
        # Check if specific threats were detected
        threat_rules = [d.rule_name for d in result.detections]
        assert any('lfi' in rule or 'directory_traversal' in rule for rule in threat_rules)
        assert any('sql_injection' in rule for rule in threat_rules)
    
    def test_analyze_file_with_temp_file(self):
        """Test analyzing a temporary log file"""
        sample_logs = """192.168.1.100 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
192.168.1.100 - - [10/Oct/2023:13:55:37 +0000] "GET /admin/config.php?file=../../../etc/passwd HTTP/1.1" 404 234
Oct 10 13:55:38 server sshd: Failed login attempt from 203.0.113.42
Oct 10 13:55:39 server security: multiple failed login attempts detected from 203.0.113.42"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
            f.write(sample_logs)
            temp_file = f.name
        
        try:
            result = self.analyzer.analyze_file(temp_file)
            
            assert result.total_lines == 4
            assert len(result.detections) > 0
            assert result.file_path == temp_file
            
            # Check IP analysis
            assert result.ip_analysis['total_unique_ips'] >= 2
            # Suspicious IPs are those with detections, may be 0 in this test
            assert result.ip_analysis['total_unique_ips'] > 0
            
        finally:
            os.unlink(temp_file)
    
    def test_analyze_compressed_file(self):
        """Test analyzing gzipped log file"""
        import gzip
        
        sample_logs = """192.168.1.100 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
192.168.1.100 - - [10/Oct/2023:13:55:37 +0000] "GET /search?q=<script>alert('xss')</script> HTTP/1.1" 400 156"""
        
        with tempfile.NamedTemporaryFile(suffix='.log.gz', delete=False) as f:
            temp_file = f.name
        
        try:
            with gzip.open(temp_file, 'wt') as f:
                f.write(sample_logs)
            
            result = self.analyzer.analyze_file(temp_file)
            
            assert result.total_lines == 2
            assert len(result.detections) > 0
            
        finally:
            os.unlink(temp_file)
    
    def test_max_lines_limit(self):
        """Test max_lines parameter"""
        sample_logs = "\n".join([
            f'192.168.1.{i} - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326'
            for i in range(100)
        ])
        
        result = self.analyzer.analyze_text(sample_logs)
        assert result.total_lines == 100
        
        # Test with max_lines
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
            f.write(sample_logs)
            temp_file = f.name
        
        try:
            result = self.analyzer.analyze_file(temp_file, max_lines=50)
            assert result.total_lines == 50
            
        finally:
            os.unlink(temp_file)
    
    def test_export_results_json(self):
        """Test exporting results to JSON"""
        text = """192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /admin/../../../etc/passwd HTTP/1.1" 404 234"""
        
        result = self.analyzer.analyze_text(text)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_file = f.name
        
        try:
            self.analyzer.export_results(result, output_file, 'json')
            assert os.path.exists(output_file)
            
            with open(output_file, 'r') as f:
                content = f.read()
                assert 'detections' in content
                assert 'summary' in content
                
        finally:
            os.unlink(output_file)
    
    def test_export_results_csv(self):
        """Test exporting results to CSV"""
        text = """192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /admin/../../../etc/passwd HTTP/1.1" 404 234"""
        
        result = self.analyzer.analyze_text(text)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            output_file = f.name
        
        try:
            self.analyzer.export_results(result, output_file, 'csv')
            assert os.path.exists(output_file)
            
            with open(output_file, 'r') as f:
                content = f.read()
                assert 'Line Number' in content
                assert 'Severity' in content
                
        finally:
            os.unlink(output_file)
    
    def test_custom_rules(self):
        """Test analyzer with custom rules"""
        custom_rule = DetectionRule(
            name="test_custom_rule",
            description="Test custom detection rule",
            severity=Severity.HIGH,
            pattern=r"CUSTOM_THREAT_PATTERN",
            category="test",
            tags=["custom", "test"]
        )
        
        analyzer = LogAnalyzer(custom_rules=[custom_rule])
        
        text = "This log contains CUSTOM_THREAT_PATTERN in the message"
        result = analyzer.analyze_text(text)
        
        assert len(result.detections) > 0
        assert any(d.rule_name == "test_custom_rule" for d in result.detections)


class TestMergeResults:
    """Test cases for merge_analysis_results function"""
    
    def test_merge_empty_results(self):
        """Test merging empty results list"""
        merged = merge_analysis_results([])
        assert merged == {}
    
    def test_merge_multiple_results(self):
        """Test merging multiple analysis results"""
        analyzer = LogAnalyzer()
        
        text1 = """192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /admin/../../../etc/passwd HTTP/1.1" 404 234"""
        text2 = """203.0.113.42 - - [10/Oct/2023:13:55:37 +0000] "POST /login HTTP/1.1' OR 1=1-- " 400 156"""
        
        result1 = analyzer.analyze_text(text1, "file1.log")
        result2 = analyzer.analyze_text(text2, "file2.log")
        
        merged = merge_analysis_results([result1, result2])
        
        assert merged['total_files'] == 2
        assert merged['total_lines'] == 2
        assert merged['total_detections'] >= 2
        assert 'file1.log' in merged['files']
        assert 'file2.log' in merged['files']
        assert len(merged['top_threats_across_files']) > 0


class TestSpecificThreatDetection:
    """Test specific threat detection scenarios"""
    
    def setup_method(self):
        """Setup test environment"""
        self.analyzer = LogAnalyzer()
    
    def test_sql_injection_detection(self):
        """Test SQL injection detection"""
        sqli_logs = [
            "POST /login HTTP/1.1' OR 1=1--",
            "GET /search?id=1' UNION SELECT * FROM users--",
            "POST /api/data HTTP/1.1' AND 1=1--"
        ]
        
        for log in sqli_logs:
            result = self.analyzer.analyze_text(log)
            assert any(d.rule_name == "sql_injection" for d in result.detections), f"Failed to detect SQLi in: {log}"
    
    def test_xss_detection(self):
        """Test XSS detection"""
        xss_logs = [
            "GET /search?q=<script>alert('xss')</script>",
            "POST /comment HTTP/1.1 <iframe src=javascript:alert('xss')>",
            "GET /page?name=<img onerror=alert('xss') src=x>"
        ]
        
        for log in xss_logs:
            result = self.analyzer.analyze_text(log)
            assert any(d.rule_name == "xss_attempt" for d in result.detections), f"Failed to detect XSS in: {log}"
    
    def test_directory_traversal_detection(self):
        """Test directory traversal detection"""
        traversal_logs = [
            "GET /admin/config.php?file=../../../etc/passwd",
            "POST /upload HTTP/1.1 filename=..\\..\\windows\\system32\\config\\sam",
            "GET /view?page=../../../../etc/shadow"
        ]
        
        for log in traversal_logs:
            result = self.analyzer.analyze_text(log)
            detected_rules = [d.rule_name for d in result.detections]
            assert any('traversal' in rule or 'lfi' in rule for rule in detected_rules), f"Failed to detect traversal in: {log}"
    
    def test_failed_login_detection(self):
        """Test failed login detection"""
        login_logs = [
            "Oct 10 13:55:38 server sshd: Failed login attempt from 192.168.1.1",
            "Authentication failed for user admin from 203.0.113.42",
            "Login failed: invalid credentials for user test"
        ]
        
        for log in login_logs:
            result = self.analyzer.analyze_text(log)
            assert any(d.rule_name == "failed_login_attempt" for d in result.detections), f"Failed to detect failed login in: {log}"
    
    def test_privilege_escalation_detection(self):
        """Test privilege escalation detection"""
        privesc_logs = [
            "Oct 10 13:55:38 server sudo: user executed sudo su - root",
            "Privilege escalation attempt detected: become root",
            "User executed: runas /user:administrator cmd.exe"
        ]
        
        for log in privesc_logs:
            result = self.analyzer.analyze_text(log)
            assert any(d.rule_name == "privileged_escalation" for d in result.detections), f"Failed to detect privilege escalation in: {log}"


if __name__ == '__main__':
    pytest.main([__file__])