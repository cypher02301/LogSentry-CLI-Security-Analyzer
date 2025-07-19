# 🔧 LogSentry setuptools Error Fix Guide

**Created by Anthony Frederick, 2025**

## 🚨 **The Error**

```
ModuleNotFoundError: No module named 'setuptools'
```

This error occurs when Python's `setuptools` package is not installed or not accessible in your current environment.

## ⚡ **Quick Fixes (Choose One)**

### **Method 1: Use Quick Start Script (Recommended)**
```bash
cd logsentry
python3 quick_start.py
```

### **Method 2: Manual Command**
```bash
# Try these in order until one works:
pip install --break-system-packages setuptools wheel
# OR
pip install --user setuptools wheel
# OR
python3 -m pip install --user setuptools wheel
```

### **Method 3: Automated Installer**
```bash
cd logsentry
python3 install_logsentry.py
```

## 📋 **Detailed Solutions by Environment**

### **Windows Users**
```cmd
# Method 1: User installation
pip install --user setuptools wheel

# Method 2: If you have admin rights
pip install setuptools wheel

# Method 3: Using Python module syntax
python -m pip install --user setuptools wheel
```

### **Linux/Ubuntu Users**
```bash
# Method 1: System package manager (recommended)
sudo apt update
sudo apt install python3-setuptools python3-pip python3-wheel

# Method 2: Override external management
pip install --break-system-packages setuptools wheel

# Method 3: User installation
pip install --user setuptools wheel
```

### **macOS Users**
```bash
# Method 1: Using Homebrew
brew install python
pip3 install setuptools wheel

# Method 2: User installation
pip install --user setuptools wheel

# Method 3: Using Python module syntax
python3 -m pip install --user setuptools wheel
```

## 🐍 **IDE-Specific Solutions**

### **Wing IDE 101**
Your error mentioned Wing IDE specifically. Here's how to fix it:

1. **Find Wing's Python Path:**
   ```python
   import sys
   print(sys.executable)
   ```

2. **Install setuptools for Wing's Python:**
   ```bash
   # Replace /path/to/wing/python with actual path from step 1
   /path/to/wing/python -m pip install setuptools wheel
   ```

3. **Configure Wing Project:**
   - Go to `Project` → `Project Properties`
   - Set `Python Executable` to a Python installation with setuptools
   - Or create a virtual environment and point Wing to that

### **PyCharm**
1. Open `File` → `Settings` → `Project` → `Python Interpreter`
2. Click gear icon → `Add` → `Virtual Environment`
3. Create new environment with setuptools included

### **VS Code**
1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. Type "Python: Select Interpreter"
3. Choose an interpreter with setuptools or create virtual environment

### **Jupyter Notebook**
```bash
# Install in current kernel
!pip install setuptools wheel

# Or install for specific Python version
!python3 -m pip install setuptools wheel
```

## 🔄 **Virtual Environment Solution (Safest)**

This is the most reliable method that won't affect your system Python:

```bash
# Step 1: Create virtual environment
python3 -m venv logsentry_env

# Step 2: Activate (choose your platform)
# Windows:
logsentry_env\Scripts\activate
# Linux/Mac:
source logsentry_env/bin/activate

# Step 3: Install setuptools and LogSentry dependencies
pip install --upgrade pip setuptools wheel
pip install click python-dateutil colorama rich pyyaml regex

# Step 4: Use LogSentry
cd logsentry
python -m logsentry.cli --help
```

## 🛠 **Troubleshooting Common Issues**

### **Issue: "externally-managed-environment"**
**Solution:** Use `--break-system-packages` flag:
```bash
pip install --break-system-packages setuptools wheel
```

### **Issue: "Permission denied"**
**Solution:** Use `--user` flag:
```bash
pip install --user setuptools wheel
```

### **Issue: "pip not found"**
**Solution:** Install pip first:
```bash
# Ubuntu/Debian:
sudo apt install python3-pip

# CentOS/RHEL:
sudo yum install python3-pip

# macOS:
python3 -m ensurepip --upgrade
```

### **Issue: Multiple Python versions**
**Solution:** Use specific Python version:
```bash
# For Python 3.9
python3.9 -m pip install setuptools wheel

# For Python 3.10
python3.10 -m pip install setuptools wheel
```

### **Issue: Old pip version**
**Solution:** Upgrade pip first:
```bash
python3 -m pip install --upgrade pip
pip install setuptools wheel
```

## ✅ **Verification Steps**

After installation, verify setuptools is working:

```bash
# Test 1: Check if setuptools is installed
python3 -c "import setuptools; print('setuptools version:', setuptools.__version__)"

# Test 2: Check pip can see setuptools
pip list | grep setuptools

# Test 3: Test LogSentry
python3 -m logsentry.cli --help

# Test 4: Run a quick security test
python3 -m logsentry.cli test-rules "GET /admin/../../../etc/passwd"
```

## 🎯 **For Your Specific Case (Wing IDE)**

Since your error mentions Wing IDE, here's the exact sequence for you:

1. **Quick Fix:**
   ```bash
   cd logsentry
   python3 quick_start.py
   ```

2. **Test LogSentry:**
   ```bash
   python3 -m logsentry.cli test-rules "suspicious log entry"
   ```

3. **If Still Having Issues:**
   - Check Wing IDE's Python interpreter settings
   - Use virtual environment within Wing IDE
   - Run LogSentry directly without installing: `python3 -m logsentry.cli`

## 📞 **Still Need Help?**

If none of these solutions work:

1. **Check your Python setup:**
   ```bash
   python3 --version
   pip --version
   which python3
   which pip
   ```

2. **Create an issue with this information:**
   - Operating system and version
   - Python version
   - IDE being used (Wing IDE 101 in your case)
   - Complete error message
   - Commands you've tried

## 🏆 **Best Practices**

1. **Always use virtual environments** for Python projects
2. **Keep pip and setuptools updated**
3. **Use `--user` flag** when you don't have admin rights
4. **Avoid `--break-system-packages`** unless necessary

---

**Created by Anthony Frederick, 2025**  
🛡️ LogSentry CLI Security Analyzer