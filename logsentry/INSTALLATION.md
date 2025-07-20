# LogSentry Installation Guide

**Created by Anthony Frederick, 2025**

This guide provides multiple installation methods for LogSentry CLI Security Analyzer to handle different Python environments and operating systems.

## 🚨 **Quick Fix for setuptools Error**

If you're getting the error: `ModuleNotFoundError: No module named 'setuptools'`, here are solutions:

### **Method 1: Install setuptools directly**
```bash
# Option A: With system packages override (if allowed)
pip install --break-system-packages setuptools wheel

# Option B: User installation
pip install --user setuptools wheel

# Option C: Using Python module syntax
python -m pip install --user setuptools wheel
```

### **Method 2: Use Virtual Environment (Recommended)**
```bash
# Create virtual environment
python -m venv logsentry_env

# Activate virtual environment
# On Windows:
logsentry_env\Scripts\activate
# On Linux/Mac:
source logsentry_env/bin/activate

# Install setuptools and LogSentry
pip install setuptools wheel
pip install -e .
```

### **Method 3: Use System Package Manager**
```bash
# Ubuntu/Debian:
sudo apt update
sudo apt install python3-setuptools python3-pip python3-venv

# CentOS/RHEL/Fedora:
sudo yum install python3-setuptools python3-pip
# or
sudo dnf install python3-setuptools python3-pip

# macOS (with Homebrew):
brew install python
```

## 📦 **Complete Installation Methods**

### **1. Virtual Environment Installation (Recommended)**

This is the safest method that won't interfere with your system Python:

```bash
# Step 1: Create virtual environment
python -m venv logsentry_env

# Step 2: Activate virtual environment
# Windows:
logsentry_env\Scripts\activate
# Linux/Mac:
source logsentry_env/bin/activate

# Step 3: Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Step 4: Install LogSentry
cd logsentry
pip install -e .

# Step 5: Verify installation
logsentry --help
```

### **2. User Installation (No Admin Rights)**

If you can't create virtual environments:

```bash
# Install setuptools for user
pip install --user setuptools wheel

# Install LogSentry dependencies
cd logsentry
pip install --user -r requirements.txt

# Run LogSentry directly
python -m logsentry.cli --help
```

### **3. System-wide Installation (Admin Rights)**

If you have administrator privileges:

```bash
# Install setuptools system-wide
pip install --break-system-packages setuptools wheel

# Install LogSentry
cd logsentry
pip install --break-system-packages -e .

# Verify installation
logsentry --help
```

### **4. Development Installation**

For development work with testing capabilities:

```bash
# Create development environment
python -m venv logsentry_dev
source logsentry_dev/bin/activate  # Linux/Mac
# or
logsentry_dev\Scripts\activate     # Windows

# Install with development dependencies
cd logsentry
pip install -e ".[dev]"

# Run tests
pytest tests/
```

## 🐍 **IDE-Specific Solutions**

### **Wing IDE 101**
Since your error mentions Wing IDE, here's a specific solution:

1. **Configure Python Interpreter:**
   - Go to `Project` → `Project Properties`
   - Set `Python Executable` to your Python installation with setuptools
   - Or create a virtual environment and point to that Python

2. **Install in Wing's Python Environment:**
   ```bash
   # Find Wing's Python path
   import sys
   print(sys.executable)
   
   # Use that path to install setuptools
   /path/to/wing/python -m pip install setuptools wheel
   ```

### **PyCharm**
1. Open `File` → `Settings` → `Project` → `Python Interpreter`
2. Click the gear icon → `Add` → `Virtual Environment`
3. Create new environment or use existing one with setuptools

### **VS Code**
1. Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
2. Type "Python: Select Interpreter"
3. Choose interpreter with setuptools or create virtual environment

## 🛠 **Troubleshooting Common Issues**

### **Issue 1: Permission Denied**
```bash
# Solution: Use --user flag
pip install --user setuptools wheel
```

### **Issue 2: Externally Managed Environment**
```bash
# Solution A: Use virtual environment (recommended)
python -m venv myenv
source myenv/bin/activate
pip install setuptools

# Solution B: Override (use cautiously)
pip install --break-system-packages setuptools
```

### **Issue 3: Old pip version**
```bash
# Upgrade pip first
python -m pip install --upgrade pip
pip install setuptools wheel
```

### **Issue 4: Multiple Python versions**
```bash
# Use specific Python version
python3.9 -m pip install setuptools
python3.10 -m pip install setuptools
```

## 📋 **Installation Verification**

After installation, verify LogSentry works:

```bash
# Test 1: Check CLI help
logsentry --help

# Test 2: Run version command
logsentry --version

# Test 3: Test rule detection
logsentry test-rules "GET /admin/../../../etc/passwd HTTP/1.1"

# Test 4: Generate and analyze sample data
logsentry generate-sample --count 50 --include-attacks
logsentry analyze sample_logs.txt
```

## 🔧 **Alternative Installation Script**

If manual installation fails, use this automated script:

**install_logsentry.py:**
```python
#!/usr/bin/env python3
"""
LogSentry Installation Script
Created by Anthony Frederick, 2025
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🛡️  LogSentry Installation Script")
    print("Created by Anthony Frederick, 2025\n")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print("❌ Python 3.8+ required. Current version:", 
              f"{python_version.major}.{python_version.minor}")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor} detected")
    
    # Install setuptools
    commands = [
        ("pip install --user setuptools wheel", "Installing setuptools"),
        ("pip install --user click python-dateutil colorama rich pyyaml regex", 
         "Installing dependencies"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            # Try alternative method
            alt_command = command.replace("--user", "--break-system-packages")
            print(f"🔄 Trying alternative method...")
            if not run_command(alt_command, description):
                print(f"❌ Failed to {description.lower()}")
                return False
    
    print("\n🎉 LogSentry installation completed!")
    print("\n📖 Usage examples:")
    print("   python -m logsentry.cli --help")
    print("   python -m logsentry.cli test-rules 'suspicious log entry'")
    
    return True

if __name__ == "__main__":
    main()
```

## 📞 **Getting Help**

If you continue having installation issues:

1. **Check Python Installation:**
   ```bash
   python --version
   pip --version
   ```

2. **Check Available Packages:**
   ```bash
   pip list | grep setuptools
   ```

3. **Create Issue Report:**
   - Python version: `python --version`
   - Operating system: Windows/Linux/Mac
   - Error message: Full error text
   - Installation method attempted

## 🏆 **Recommended Approach**

For most users, we recommend:

1. **Virtual Environment** (safest and cleanest)
2. **User Installation** (if virtual env not possible)
3. **System Installation** (only if you have admin rights and understand risks)

The virtual environment approach ensures LogSentry doesn't interfere with other Python projects and provides the most reliable installation experience.