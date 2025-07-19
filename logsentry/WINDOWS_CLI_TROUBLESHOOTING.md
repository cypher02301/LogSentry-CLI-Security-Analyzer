# 🛠️ LogSentry CLI Windows Troubleshooting Guide

**Created by Anthony Frederick, 2025**

## 🚨 **Problem: CLI Executable Closes Immediately**

If your `LogSentry-CLI.exe` file "loads for a couple seconds then auto closes," this guide will help you diagnose and fix the issue.

## 🔍 **Quick Diagnosis Steps**

### **Step 1: Use the Debug Version**
I've created a special debug version that shows detailed error information:

1. **Download**: `LogSentry-CLI-Debug.exe` 
2. **Run from Command Prompt**: 
   ```cmd
   LogSentry-CLI-Debug.exe --help
   ```
3. **Check Output**: The debug version will show:
   - ✅ What modules are loading successfully
   - ❌ What modules are missing or failing
   - 🔍 Detailed error messages
   - 📁 File paths and environment info

### **Step 2: Run from Command Prompt**
**Never double-click the executable!** Always run from Command Prompt:

```cmd
# Open Command Prompt (Windows + R, type "cmd", press Enter)
cd "C:\path\to\your\logsentry\folder"
LogSentry-CLI.exe --help
```

### **Step 3: Use the Debug Batch File**
Run the `debug_cli_windows.bat` file I created:

1. Place `debug_cli_windows.bat` in the same folder as `LogSentry-CLI.exe`
2. Double-click `debug_cli_windows.bat`
3. It will automatically test the executable and show results

## 🧩 **Common Issues and Solutions**

### **Issue 1: Missing Python Dependencies**

**Symptoms**: Debug version shows missing modules like `yaml` or `regex`

**Solutions**:
```cmd
# Option A: Use the Fixed CLI Version (if available)
LogSentry-CLI-Fixed.exe --help

# Option B: Install missing dependencies (if you have Python)
pip install pyyaml regex python-dateutil

# Option C: Re-download the complete package
# Make sure you have the full LogSentry package with all files
```

### **Issue 2: Windows Security/Antivirus Blocking**

**Symptoms**: File starts but immediately closes, or "Access Denied" errors

**Solutions**:
1. **Temporarily disable antivirus** and test
2. **Add exception** for LogSentry folder in antivirus
3. **Run as Administrator**:
   ```cmd
   # Right-click Command Prompt, select "Run as Administrator"
   cd "C:\path\to\logsentry"
   LogSentry-CLI.exe --help
   ```

### **Issue 3: Missing Visual C++ Redistributables**

**Symptoms**: Error about missing DLLs or runtime components

**Solutions**:
1. **Download and install**: [Microsoft Visual C++ Redistributables](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. **Restart computer** after installation
3. **Test again**: `LogSentry-CLI.exe --help`

### **Issue 4: Corrupted Download**

**Symptoms**: File won't run at all, or random errors

**Solutions**:
1. **Re-download** the executable
2. **Check file size**: Should be ~15-17MB
3. **Verify integrity**: Compare with known good version

### **Issue 5: Path/Directory Issues**

**Symptoms**: "File not found" or path-related errors

**Solutions**:
```cmd
# Make sure you're in the right directory
dir LogSentry-CLI.exe

# Use full path if needed
"C:\full\path\to\LogSentry-CLI.exe" --help

# Avoid spaces in folder names, or use quotes
cd "C:\Program Files\LogSentry"
```

## 🐛 **Advanced Debugging**

### **Check Windows Event Viewer**
1. Press `Windows + R`, type `eventvwr.msc`, press Enter
2. Navigate to `Windows Logs` → `Application`
3. Look for recent errors related to LogSentry or Python
4. Note the error code and description

### **Command Prompt Debug Session**
```cmd
# Run with verbose output (if supported)
LogSentry-CLI-Debug.exe --help > debug_output.txt 2>&1

# Check the output file
type debug_output.txt

# Test specific commands
LogSentry-CLI-Debug.exe list-rules
LogSentry-CLI-Debug.exe --version
```

### **Test Basic Functionality**
```cmd
# These commands should work if the executable is functioning:
LogSentry-CLI.exe --help
LogSentry-CLI.exe --version
LogSentry-CLI.exe list-rules
LogSentry-CLI.exe test-rules "GET /admin HTTP/1.1"
```

## 🔧 **Environment-Specific Fixes**

### **Windows 10/11**
- ✅ Should work out of the box
- May need Visual C++ Redistributables
- Check Windows Defender exceptions

### **Windows 8.1/8**
- May need additional .NET Framework
- Install latest Windows updates
- Check compatibility mode

### **Windows 7**
- ⚠️ Limited support for Python 3.13
- May need Python 3.8 version instead
- Install all available Windows updates

### **Corporate/Enterprise Windows**
- Check Group Policy restrictions
- May need IT administrator approval
- Test in a temporary folder (like Desktop)

## 📝 **Error Message Reference**

### **"The system cannot execute the specified program"**
- Missing Visual C++ Redistributables
- Corrupted executable file
- Antivirus interference

### **"Access is denied"**
- Insufficient permissions
- Antivirus blocking
- File in use by another process

### **"This app can't run on your PC"**
- Wrong architecture (32-bit vs 64-bit)
- Incompatible Windows version
- Missing system dependencies

### **"The application was unable to start correctly (0xc000007b)"**
- Missing or incompatible DLLs
- Needs Visual C++ Redistributables
- System file corruption

## 🎯 **Step-by-Step Diagnostic Checklist**

```
□ 1. Downloaded correct version (Windows, 64-bit)
□ 2. File size is approximately 15-17MB
□ 3. Running from Command Prompt (not double-clicking)
□ 4. Tested LogSentry-CLI-Debug.exe first
□ 5. Checked antivirus isn't blocking
□ 6. Tried running as Administrator
□ 7. Installed Visual C++ Redistributables
□ 8. Checked Windows Event Viewer for errors
□ 9. Tested in a simple folder path (no spaces)
□ 10. Verified Windows version compatibility
```

## ✅ **Expected Working Output**

When LogSentry CLI is working correctly, you should see:

```cmd
C:\> LogSentry-CLI.exe --help

Usage: LogSentry-CLI [OPTIONS] COMMAND [ARGS]...

  LogSentry - A CLI Security Log Analyzer
  
  Created by Anthony Frederick, 2025
  
  [... rest of help text ...]

Commands:
  analyze          Analyze a single log file for security threats.
  generate-sample  Generate sample log data for testing.
  list-rules       List all available security detection rules.
  scan             Scan a directory for log files and analyze them.
  test-rules       Test security rules against a text string.
  web              Launch the LogSentry web interface
```

## 🆘 **If Nothing Works**

### **Alternative Options**:

1. **Use the Web Interface**:
   ```cmd
   LogSentry-Web.exe
   # Then open browser to http://localhost:5000
   ```

2. **Install Python and run from source**:
   ```cmd
   pip install logsentry
   logsentry --help
   ```

3. **Use Online Tools**: (if available)

### **Report the Issue**:
If you're still having problems, please provide:
- ✅ Windows version and architecture
- ✅ Output from `LogSentry-CLI-Debug.exe`
- ✅ Any error messages from Windows Event Viewer
- ✅ Antivirus software being used
- ✅ Whether you have Administrator privileges

---

**🛡️ LogSentry Windows CLI Troubleshooting**  
**Created by Anthony Frederick, 2025**

*This guide helps resolve common issues with LogSentry CLI executables on Windows systems.*