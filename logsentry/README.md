# LogSentry CLI Security Analyzer

![LogSentry Logo](https://img.shields.io/badge/LogSentry-Security%20Analyzer-blue)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-green)](tests/)
[![Creator](https://img.shields.io/badge/Created%20by-Anthony%20Frederick-orange)](https://github.com/anthony-frederick)

**Created by Anthony Frederick, 2025**

LogSentry is a powerful Python-based command-line tool for analyzing log files and detecting security incidents. It provides comprehensive threat detection capabilities across multiple log formats with beautiful, colorized output and detailed reporting.

## 🚀 Features

### 🌐 **Modern Web Interface**
- **Drag & Drop Upload**: Easy file upload with progress indicators
- **Real-time Analysis**: Live threat detection with interactive feedback
- **Interactive Charts**: Beautiful visualizations with Chart.js (pie charts, bar charts)
- **Export Capabilities**: Download results in JSON/CSV formats
- **Mobile Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **Dark Mode Support**: Automatic theme switching based on system preferences
- **Rule Testing**: Test individual log entries against detection rules in real-time

### 🔍 **Core Analysis Features**
- **Multi-format Log Parsing**: Supports Apache/Nginx access logs, syslog, Windows Event Logs, firewall logs, JSON logs, and more
- **Advanced Threat Detection**: Over 20 built-in security rules detecting SQL injection, XSS, directory traversal, brute force attacks, privilege escalation, and more
- **IP Analysis**: Automatic geolocation, suspicious IP detection, and traffic pattern analysis
- **Risk Scoring**: Intelligent risk assessment with confidence scoring
- **Beautiful Output**: Rich, colorized console output with tables and progress indicators
- **Multiple Export Formats**: JSON and CSV export options for further analysis
- **High Performance**: Efficient chunk-based processing for large log files
- **Extensible**: Easy to add custom detection rules
- **Compressed File Support**: Handles gzipped log files automatically

## 📦 Installation

### 🚨 **Quick Fix for setuptools Error**

If you get `ModuleNotFoundError: No module named 'setuptools'`, run this:

```bash
# Quick fix script
python3 quick_start.py

# Or manual fix
pip install --break-system-packages setuptools wheel
# OR
pip install --user setuptools wheel
```

### From PyPI (Recommended)
```bash
pip install logsentry
```

### From Source (Modern Method)
```bash
git clone https://github.com/anthony-frederick/logsentry.git
cd logsentry
pip install -e .[dev]
```

### Legacy Installation (Deprecated)
If you see deprecation warnings about `setup.py develop`, use the modern method above or see [SETUP_MIGRATION.md](SETUP_MIGRATION.md) for migration guide.

### Development Installation (Full Setup)
```bash
git clone https://github.com/anthony-frederick/logsentry.git
cd logsentry

# Install with all features (dev tools, web interface, build tools)
pip install -e .[dev,web,build]

# Or install specific feature groups:
pip install -e .[dev]    # Development tools only
pip install -e .[web]    # Web interface dependencies
pip install -e .[build]  # Executable building tools
```

### Alternative Installation Methods

**For Wing IDE / IDE Users:**
```bash
# Use the automated installer
python3 install_logsentry.py

# Or run directly without installation
python3 -m logsentry.cli --help
```

**For Virtual Environments:**
```bash
python -m venv logsentry_env
source logsentry_env/bin/activate  # Linux/Mac
# or logsentry_env\Scripts\activate  # Windows
pip install setuptools wheel
pip install -e .
```

## 🎯 Quick Start

### 🌐 **Web Interface (New!)**
```bash
# Launch the modern web interface
python3 -m logsentry.cli web

# Or use the standalone launcher
python3 run_web.py

# Access at http://localhost:5000
```

### Analyze a Single Log File
```bash
logsentry analyze /var/log/apache2/access.log
```

### Scan a Directory for Log Files
```bash
logsentry scan /var/log --pattern "*.log"
```

### Generate Sample Data for Testing
```bash
logsentry generate-sample --include-attacks --count 1000
logsentry analyze sample_logs.txt
```

### View All Available Detection Rules
```bash
logsentry list-rules
```

### Test Rules Against Specific Text
```bash
logsentry test-rules "GET /admin/../../../etc/passwd HTTP/1.1"
```

## 🔧 Usage Examples

### Basic Analysis
```bash
# Analyze a log file with verbose output
logsentry analyze access.log --verbose

# Filter by severity level
logsentry analyze access.log --severity high

# Limit analysis to first 10,000 lines
logsentry analyze large.log --max-lines 10000
```

### Export Results
```bash
# Export to JSON
logsentry analyze access.log --output results.json --format json

# Export to CSV
logsentry analyze access.log --output detections.csv --format csv
```

### Directory Scanning
```bash
# Scan directory with custom pattern
logsentry scan /var/log --pattern "*.log*" --output scan_results.json

# Scan with severity filtering
logsentry scan /var/log --severity medium --verbose
```

## 📊 Detection Categories

LogSentry detects various types of security threats:

### Web Attacks
- **SQL Injection**: Detects various SQLi patterns and techniques
- **Cross-Site Scripting (XSS)**: Identifies script injection attempts
- **Directory Traversal**: Path traversal and file inclusion attacks
- **Command Injection**: OS command injection attempts

### Authentication Attacks
- **Failed Login Attempts**: Brute force detection
- **Credential Stuffing**: Automated login attempts
- **Multiple Failed Logins**: Repeated failure patterns

### Network Attacks
- **Port Scanning**: Network reconnaissance activities
- **Suspicious User Agents**: Automated tools and scanners
- **DNS Tunneling**: Data exfiltration via DNS

### System Attacks
- **Privilege Escalation**: Unauthorized permission elevation
- **Suspicious File Access**: Access to sensitive system files
- **Reverse Shells**: Backdoor establishment attempts

### Malware & Data Exfiltration
- **Cryptocurrency Mining**: Cryptojacking detection
- **Large Data Transfers**: Potential data theft
- **Suspicious Network Activity**: Unusual traffic patterns

## 🎨 Sample Output

```
┌─ Analysis Summary ──────────────────────────────────────────┐
│ File: /var/log/apache2/access.log                          │
│ Total lines: 45,234                                        │
│ Parsed lines: 45,180                                       │
│ Analysis time: 2.34s                                       │
│ Risk Score: 73/100 (high)                                  │
└─────────────────────────────────────────────────────────────┘

┌─ Detection Summary ─────────────────────────────────────────┐
│ Metric           │ Count                                    │
├──────────────────┼──────────────────────────────────────────┤
│ Total Detections │ 127                                      │
│ Unique IPs       │ 1,203                                    │
│ Suspicious IPs   │ 23                                       │
│ High Severity    │ 45                                       │
│ Critical Severity│ 12                                       │
└─────────────────────────────────────────────────────────────┘

┌─ Top Threats ───────────────────────────────────────────────┐
│ Rule                    │ Count │ Severity                   │
├─────────────────────────┼───────┼────────────────────────────┤
│ sql_injection          │    34 │ high                       │
│ directory_traversal    │    28 │ high                       │
│ failed_login_attempt   │    23 │ medium                     │
│ xss_attempt           │    18 │ high                       │
│ command_injection     │    12 │ critical                   │
└─────────────────────────────────────────────────────────────┘
```

## ⚙️ Configuration

### Custom Rules
You can extend LogSentry with custom detection rules:

```python
from logsentry.rules import DetectionRule, Severity
from logsentry.analyzer import LogAnalyzer

# Define custom rule
custom_rule = DetectionRule(
    name="custom_threat",
    description="Detects custom threat pattern",
    severity=Severity.HIGH,
    pattern=r"SUSPICIOUS_PATTERN",
    category="custom",
    tags=["custom", "threat"]
)

# Use with analyzer
analyzer = LogAnalyzer(custom_rules=[custom_rule])
```

### Supported Log Formats

LogSentry automatically detects and parses various log formats:

- **Apache/Nginx Access Logs**: Common and Combined Log Format
- **Syslog**: RFC3164 format with facility/severity parsing
- **Windows Event Logs**: Structured Windows event format
- **Firewall Logs**: iptables and similar firewall logs
- **JSON Logs**: Structured JSON log entries
- **Generic Logs**: Unstructured text logs with timestamp extraction

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=logsentry tests/
```

Generate sample data for testing:
```bash
# Generate clean sample logs
logsentry generate-sample --count 1000

# Generate logs with attack patterns
logsentry generate-sample --include-attacks --count 1000
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/logsentry/logsentry.git
cd logsentry
pip install -e ".[dev]"
pre-commit install
```

### Adding New Detection Rules
1. Add rule definition in `logsentry/rules.py`
2. Add test cases in `tests/test_analyzer.py`
3. Update documentation

### Adding New Log Parsers
1. Create parser class in `logsentry/parsers.py`
2. Register in `LogParserManager`
3. Add comprehensive tests

## 📚 Documentation

- [API Documentation](https://logsentry.readthedocs.io)
- [Detection Rules Reference](docs/rules.md)
- [Parser Development Guide](docs/parsers.md)
- [Examples and Tutorials](docs/examples.md)

## 🔒 Security

LogSentry is designed with security in mind:

- **No Network Access**: Operates entirely offline on local files
- **Safe Pattern Matching**: Uses compiled regex with safeguards
- **Data Privacy**: Supports data anonymization and hashing
- **Resource Limits**: Built-in protections against resource exhaustion

Report security vulnerabilities to: security@logsentry.dev

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Created by Anthony Frederick in 2025** - Inspired by the need for accessible security log analysis
- Built with Python, Click, Rich, and other amazing open-source libraries
- Thanks to the cybersecurity community for threat intelligence and patterns
- Special thanks to the open-source security tools that inspire this project

## 📈 Roadmap

- [ ] Machine learning-based anomaly detection
- [ ] Real-time log monitoring capabilities
- [ ] Web dashboard for visualization
- [ ] Integration with SIEM systems
- [ ] Additional log format support
- [ ] Cloud deployment options

---

**LogSentry** - Making security log analysis accessible to everyone 🛡️