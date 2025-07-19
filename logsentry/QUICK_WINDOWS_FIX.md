# 🚀 Quick Windows CLI Fix

**LogSentry CLI closing immediately? Here's the fix!**

## 🎯 **Solution**

Your `LogSentry-CLI.exe` was missing dependencies. I've fixed it!

### **Step 1: Try the Fixed Executable**
```cmd
LogSentry-CLI.exe --help
```

✅ **Should now work perfectly!**

### **Step 2: If Still Having Issues**
```cmd
LogSentry-CLI-Debug.exe --help
```

This will show you exactly what's wrong.

### **Step 3: Use the Debug Script**
Double-click: `debug_cli_windows.bat`

## 📁 **What I Fixed**

- ✅ **Added missing `yaml` module**
- ✅ **Added missing `regex` module** 
- ✅ **Included all Python dependencies**
- ✅ **Created debug tools for troubleshooting**

## 🔧 **Available Files**

| File | Purpose |
|------|---------|
| `LogSentry-CLI.exe` | **Main CLI** (now fixed!) |
| `LogSentry-CLI-Debug.exe` | Shows detailed error info |
| `LogSentry-Web.exe` | Web interface version |
| `debug_cli_windows.bat` | Windows troubleshooting |

## 🆘 **Still Not Working?**

1. **Run as Administrator**
2. **Check antivirus** (add LogSentry folder to exceptions)
3. **Install**: [Visual C++ Redistributables](https://aka.ms/vs/17/release/vc_redist.x64.exe)
4. **Read**: `WINDOWS_CLI_TROUBLESHOOTING.md`

## ✅ **Test Commands**

```cmd
LogSentry-CLI.exe --help
LogSentry-CLI.exe --version  
LogSentry-CLI.exe list-rules
LogSentry-CLI.exe test-rules "test string"
```

**All should work now!** 🎉

---
*Fixed by Anthony Frederick, 2025*