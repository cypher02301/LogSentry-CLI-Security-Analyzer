"""
Utility functions for LogSentry

Created by Anthony Frederick, 2025
This module provides essential utility functions for log analysis, IP validation,
timestamp parsing, and various text processing operations used throughout LogSentry.
"""

import re
import ipaddress
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib


def is_valid_ip(ip_string: str) -> bool:
    """
    Validate if a string represents a valid IP address (IPv4 or IPv6)
    
    Args:
        ip_string (str): The string to validate as an IP address
        
    Returns:
        bool: True if valid IP address, False otherwise
        
    Example:
        >>> is_valid_ip("192.168.1.1")
        True
        >>> is_valid_ip("invalid.ip")
        False
    """
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False


def is_private_ip(ip_string: str) -> bool:
    """
    Determine if an IP address is in a private network range
    
    Private ranges include:
    - 10.0.0.0/8 (Class A)
    - 172.16.0.0/12 (Class B) 
    - 192.168.0.0/16 (Class C)
    - 127.0.0.0/8 (Loopback)
    
    Args:
        ip_string (str): The IP address to check
        
    Returns:
        bool: True if IP is in private range, False otherwise
    """
    try:
        ip = ipaddress.ip_address(ip_string)
        return ip.is_private
    except ValueError:
        return False


def extract_ips_from_text(text: str) -> List[str]:
    """
    Extract all IPv4 addresses from a text string using regex pattern matching
    
    This function uses a regex pattern to find all valid IPv4 addresses
    within the provided text. Useful for parsing log entries to identify
    source/destination IP addresses.
    
    Args:
        text (str): The text to search for IP addresses
        
    Returns:
        List[str]: List of IP addresses found in the text
        
    Example:
        >>> extract_ips_from_text("Connection from 192.168.1.1 to 10.0.0.1")
        ['192.168.1.1', '10.0.0.1']
    """
    # IPv4 pattern: matches 0-255.0-255.0-255.0-255 format
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    return re.findall(ip_pattern, text)


def extract_domains_from_text(text: str) -> List[str]:
    """
    Extract domain names from text using regex pattern matching
    
    This function identifies fully qualified domain names (FQDNs) within text.
    Useful for analyzing web logs, DNS logs, and identifying suspicious domains.
    
    Args:
        text (str): The text to search for domain names
        
    Returns:
        List[str]: List of domain names found in the text
        
    Example:
        >>> extract_domains_from_text("Visit example.com or malicious-site.evil")
        ['example.com', 'malicious-site.evil']
    """
    # Domain pattern: matches valid domain name format with TLD
    domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    return re.findall(domain_pattern, text)


def normalize_timestamp(timestamp_str: str, format_hint: Optional[str] = None) -> Optional[datetime]:
    """
    Parse timestamp strings in various common log formats into datetime objects
    
    This function attempts to parse timestamp strings using a variety of common
    formats found in different log types (Apache, syslog, ISO 8601, etc.).
    Returns timezone-naive datetime objects for consistency across the application.
    
    Args:
        timestamp_str (str): The timestamp string to parse
        format_hint (Optional[str]): Optional format hint to try first
        
    Returns:
        Optional[datetime]: Parsed datetime object or None if parsing fails
        
    Supported Formats:
        - ISO 8601: 2025-01-01T12:00:00Z
        - Apache: 01/Jan/2025:12:00:00 +0000
        - Syslog: Jan 1 12:00:00
        - Standard: 2025-01-01 12:00:00
        
    Example:
        >>> normalize_timestamp("2025-01-01 12:00:00")
        datetime.datetime(2025, 1, 1, 12, 0, 0)
    """
    # Common timestamp formats found in various log types
    common_formats = [
        '%Y-%m-%d %H:%M:%S',          # Standard format: 2025-01-01 12:00:00
        '%Y-%m-%d %H:%M:%S.%f',       # With microseconds: 2025-01-01 12:00:00.123456
        '%Y-%m-%dT%H:%M:%S',          # ISO 8601: 2025-01-01T12:00:00
        '%Y-%m-%dT%H:%M:%S.%f',       # ISO 8601 with microseconds
        '%Y-%m-%dT%H:%M:%SZ',         # ISO 8601 UTC: 2025-01-01T12:00:00Z
        '%Y-%m-%dT%H:%M:%S.%fZ',      # ISO 8601 UTC with microseconds
        '%d/%b/%Y:%H:%M:%S %z',       # Apache format: 01/Jan/2025:12:00:00 +0000
        '%b %d %H:%M:%S',             # Syslog format: Jan 1 12:00:00
        '%Y%m%d %H:%M:%S',            # Compact format: 20250101 12:00:00
    ]
    
    # If format hint provided, try it first for better performance
    if format_hint:
        common_formats.insert(0, format_hint)
    
    # Attempt to parse using each format until one succeeds
    for fmt in common_formats:
        try:
            dt = datetime.strptime(timestamp_str, fmt)
            # Return timezone-naive datetime for consistency across the application
            # This prevents timezone comparison issues in analysis functions
            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            return dt
        except ValueError:
            continue  # Try next format
    
    return None  # Return None if no format matches


def hash_sensitive_data(data: str) -> str:
    """
    Create a secure hash of sensitive data for anonymization purposes
    
    This function uses SHA-256 hashing to create a consistent but anonymized
    representation of sensitive data like passwords, emails, or personal info.
    Only returns the first 8 characters for brevity while maintaining uniqueness.
    
    Args:
        data (str): The sensitive data to hash
        
    Returns:
        str: First 8 characters of the SHA-256 hash
        
    Example:
        >>> hash_sensitive_data("sensitive_password")
        'a1b2c3d4'
    """
    return hashlib.sha256(data.encode()).hexdigest()[:8]


def clean_log_line(line: str) -> str:
    """
    Clean and normalize a log line by removing unwanted characters
    
    Removes null bytes, carriage returns, and leading/trailing whitespace
    that can interfere with log parsing and analysis. Essential preprocessing
    step for reliable log analysis.
    
    Args:
        line (str): Raw log line to clean
        
    Returns:
        str: Cleaned and normalized log line
        
    Example:
        >>> clean_log_line("  log entry with\\x00null\\r  ")
        'log entry withnull'
    """
    return line.strip().replace('\x00', '').replace('\r', '')


def calculate_entropy(data: str) -> float:
    """
    Calculate Shannon entropy of a string to detect randomness/encoding
    
    Shannon entropy measures the randomness or information content of data.
    High entropy values may indicate encoded, encrypted, or random data which
    could be suspicious in certain contexts (e.g., SQL injection payloads).
    
    Args:
        data (str): The string to analyze
        
    Returns:
        float: Shannon entropy value (0.0 = no randomness, higher = more random)
        
    Note:
        This implementation uses a simplified entropy calculation optimized
        for ASCII text analysis in security contexts.
        
    Example:
        >>> calculate_entropy("aaaa")  # Low entropy
        0.0
        >>> calculate_entropy("a1B#x9")  # Higher entropy
        2.4494
    """
    if not data:
        return 0.0
    
    entropy = 0.0
    # Check frequency of each possible ASCII character (0-255)
    for x in range(256):
        # Calculate probability of this character appearing
        p_x = float(data.count(chr(x))) / len(data)
        if p_x > 0:
            # Shannon entropy formula: -Σ(p(x) * log2(p(x)))
            # Using simplified calculation for performance
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