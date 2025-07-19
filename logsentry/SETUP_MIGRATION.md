# 🔄 LogSentry Setup Migration Guide

**Created by Anthony Frederick, 2025**

## 🚨 **Deprecation Warning Resolution**

You're seeing this warning because the legacy `setup.py develop` method is being deprecated in favor of modern Python packaging standards. This guide will help you migrate to the new `pyproject.toml` based setup.

```
DEPRECATION: Legacy editable install of logsentry[dev]==1.0.0 from file:///C:/Users/Lexus/OneDrive/Desktop/logsentry (setup.py develop) is deprecated. pip 25.3 will enforce this behaviour change.
```

## ✅ **Quick Fix - Use These Commands Instead**

### **🔧 Modern Installation Methods**

#### **Method 1: Editable Install with pyproject.toml (Recommended)**
```bash
# Uninstall old version first
pip uninstall logsentry

# Install with modern method
pip install -e .[dev]
```

#### **Method 2: Direct Installation**
```bash
# Clean install
pip uninstall logsentry
pip install .
```

#### **Method 3: Development Install with All Features**
```bash
# Install with all optional dependencies
pip install -e .[dev,web,build]
```

## 📦 **What Changed**

### **✅ Modern pyproject.toml Added**
I've created a comprehensive `pyproject.toml` file that replaces the legacy `setup.py` method with:

- **Modern build system** using setuptools>=64
- **Proper dependency management** with version constraints
- **Optional dependencies** for dev, web, and build features
- **Tool configurations** for Black, MyPy, Pytest, Coverage
- **Better metadata** and project information

### **🔧 Key Improvements**

1. **PEP 517/518 Compliance**: Uses modern Python packaging standards
2. **Better Dependency Management**: Clear separation of core vs optional deps
3. **Tool Configuration**: All dev tools configured in one place
4. **Future-Proof**: Compatible with upcoming pip versions

## 🛠️ **Step-by-Step Migration**

### **Step 1: Clean Existing Installation**
```bash
# Remove old installation
pip uninstall logsentry

# Clean build artifacts (optional)
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/
```

### **Step 2: Install with Modern Method**
```bash
# Navigate to project directory
cd C:\Users\Lexus\OneDrive\Desktop\logsentry

# Install in editable mode with dev dependencies
pip install -e .[dev]
```

### **Step 3: Verify Installation**
```bash
# Test CLI
logsentry --help

# Test web interface
logsentry web --help

# Test Python import
python -c "import logsentry; print('✅ LogSentry installed successfully')"
```

## 📋 **Available Installation Options**

### **Core Package Only**
```bash
pip install -e .
```

### **With Development Tools**
```bash
pip install -e .[dev]
```

### **With Web Interface**
```bash
pip install -e .[web]
```

### **With Build Tools**
```bash
pip install -e .[build]
```

### **Everything (Full Development Setup)**
```bash
pip install -e .[dev,web,build]
```

## 🔍 **Dependency Groups Explained**

### **Core Dependencies (Always Installed)**
- `click` - CLI framework
- `rich` - Terminal formatting
- `colorama` - Cross-platform colors
- `python-dateutil` - Date parsing
- `pyyaml` - Configuration files
- `regex` - Advanced pattern matching

### **Web Dependencies (`[web]`)**
- `flask` - Web framework
- `werkzeug` - WSGI utilities
- `jinja2` - Template engine
- `markupsafe` - Safe string handling
- `itsdangerous` - Secure signatures
- `blinker` - Signal library

### **Development Dependencies (`[dev]`)**
- `pytest` - Testing framework
- `pytest-cov` - Coverage testing
- `black` - Code formatter
- `flake8` - Linting
- `mypy` - Type checking
- `coverage` - Coverage reporting

### **Build Dependencies (`[build]`)**
- `pyinstaller` - Executable building
- `setuptools` - Build system
- `wheel` - Package format

## 🚀 **Verification Commands**

After installation, verify everything works:

```bash
# Test basic functionality
logsentry --version
logsentry list-rules

# Test web interface
logsentry web --help

# Test sample generation
logsentry generate-sample --count 5 --output test.log

# Test analysis
logsentry analyze test.log

# Test rule testing
logsentry test-rules "GET /admin/../../../etc/passwd HTTP/1.1"
```

## ⚠️ **Troubleshooting**

### **Issue: "No module named 'logsentry'"**
```bash
# Solution: Reinstall in editable mode
pip uninstall logsentry
pip install -e .[dev]
```

### **Issue: "Command 'logsentry' not found"**
```bash
# Solution: Check if scripts are installed
pip show logsentry
# Then reinstall
pip install -e .[dev]
```

### **Issue: "Permission denied" on Windows**
```bash
# Solution: Run as administrator or use --user flag
pip install -e .[dev] --user
```

### **Issue: Still getting deprecation warning**
```bash
# Solution: Force uninstall and clean install
pip uninstall logsentry --yes
pip cache purge
pip install -e .[dev]
```

## 🔧 **For Development**

### **Setting Up Development Environment**
```bash
# Clone/navigate to project
cd C:\Users\Lexus\OneDrive\Desktop\logsentry

# Install full development setup
pip install -e .[dev,web,build]

# Run tests
pytest

# Format code
black logsentry/

# Type check
mypy logsentry/

# Lint code
flake8 logsentry/
```

### **Building Executables**
```bash
# Install build dependencies
pip install -e .[build]

# Build executables
python build_executables.py
```

## 📊 **Benefits of Migration**

### **✅ Advantages of pyproject.toml**
1. **Future-Proof**: Compatible with pip 25.3+
2. **Better Dependency Management**: Clear separation of requirements
3. **Tool Integration**: All dev tools configured in one place
4. **Standard Compliance**: Follows PEP 517/518 standards
5. **Easier Maintenance**: Single configuration file

### **🔄 Backward Compatibility**
- All existing functionality preserved
- Same CLI commands and options
- Same web interface features
- Same executable building process

## 🎯 **Recommended Actions**

### **For Users**
1. **Uninstall old version**: `pip uninstall logsentry`
2. **Install with modern method**: `pip install -e .[dev]`
3. **Verify functionality**: `logsentry --help`

### **For Developers**
1. **Use pyproject.toml**: Delete setup.py (if desired)
2. **Install dev dependencies**: `pip install -e .[dev,web,build]`
3. **Configure IDE**: Point to new installation
4. **Update CI/CD**: Use modern pip commands

## 📞 **Support**

If you encounter any issues during migration:

1. **Check Python version**: Ensure Python 3.8+
2. **Update pip**: `python -m pip install --upgrade pip`
3. **Clear cache**: `pip cache purge`
4. **Reinstall cleanly**: Follow steps above
5. **Check installation**: `pip show logsentry`

---

**🛡️ LogSentry Modern Packaging Migration**  
**Created by Anthony Frederick, 2025**

*Keeping LogSentry up-to-date with modern Python packaging standards while maintaining full functionality.*