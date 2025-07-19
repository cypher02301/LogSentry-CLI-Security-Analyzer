"""
Utility functions for LogSentry
"""

import re
import ipaddress
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib


def is_valid_ip(ip_string: str) -> bool:
    """Check if a string is a valid IP address"""
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False


def is_private_ip(ip_string: str) -> bool:
    """Check if an IP address is private"""
    try:
        ip = ipaddress.ip_address(ip_string)
        return ip.is_private
    except ValueError:
        return False


def extract_ips_from_text(text: str) -> List[str]:
    """Extract all IP addresses from text"""
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    return re.findall(ip_pattern, text)


def extract_domains_from_text(text: str) -> List[str]:
    """Extract domain names from text"""
    domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    return re.findall(domain_pattern, text)


def normalize_timestamp(timestamp_str: str, format_hint: Optional[str] = None) -> Optional[datetime]:
    """Try to parse various timestamp formats"""
    common_formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%d/%b/%Y:%H:%M:%S %z',
        '%b %d %H:%M:%S',
        '%Y%m%d %H:%M:%S',
    ]
    
    if format_hint:
        common_formats.insert(0, format_hint)
    
    for fmt in common_formats:
        try:
            dt = datetime.strptime(timestamp_str, fmt)
            # Return timezone-naive datetime for consistency
            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            return dt
        except ValueError:
            continue
    
    return None


def hash_sensitive_data(data: str) -> str:
    """Hash sensitive data for anonymization"""
    return hashlib.sha256(data.encode()).hexdigest()[:8]


def clean_log_line(line: str) -> str:
    """Clean and normalize log line"""
    return line.strip().replace('\x00', '').replace('\r', '')


def calculate_entropy(data: str) -> float:
    """Calculate Shannon entropy of a string"""
    if not data:
        return 0.0
    
    entropy = 0.0
    for x in range(256):
        p_x = float(data.count(chr(x))) / len(data)
        if p_x > 0:
            entropy += - p_x * (p_x ** 0.5)
    
    return entropy


def detect_encoding_attempts(text: str) -> List[str]:
    """Detect potential encoding/obfuscation attempts"""
    patterns = []
    
    # Base64-like patterns
    if re.search(r'[A-Za-z0-9+/]{20,}={0,2}', text):
        patterns.append('base64')
    
    # Hex encoding
    if re.search(r'[0-9a-fA-F]{20,}', text):
        patterns.append('hex')
    
    # URL encoding
    if re.search(r'%[0-9a-fA-F]{2}', text):
        patterns.append('url_encoding')
    
    # Unicode escapes
    if re.search(r'\\u[0-9a-fA-F]{4}', text):
        patterns.append('unicode')
    
    return patterns


def is_suspicious_user_agent(user_agent: str) -> bool:
    """Check if user agent looks suspicious"""
    suspicious_patterns = [
        r'bot|crawler|spider|scraper',
        r'python|curl|wget|powershell',
        r'nmap|sqlmap|nikto|burp',
        r'masscan|zmap',
    ]
    
    user_agent_lower = user_agent.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, user_agent_lower):
            return True
    
    return False


def format_bytes(bytes_count: int) -> str:
    """Format byte count in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} TB"


def get_geolocation_info(ip: str) -> Dict[str, Any]:
    """Get basic geolocation info (placeholder for external service)"""
    # In a real implementation, this would query a geolocation service
    return {
        'country': 'Unknown',
        'city': 'Unknown',
        'asn': 'Unknown',
        'is_tor': False,
        'is_vpn': False
    }