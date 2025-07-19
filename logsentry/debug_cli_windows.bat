@echo off
echo ===============================================
echo LogSentry CLI Windows Debug Helper
echo Created by Anthony Frederick, 2025
echo ===============================================
echo.

echo 🔧 Running LogSentry CLI diagnostics...
echo.

echo 📁 Current Directory: %CD%
echo 🖥️  Windows Version: %OS%
echo 👤 User: %USERNAME%
echo.

echo 🎯 Testing LogSentry-CLI.exe...
echo ===============================================

REM Check if LogSentry-CLI.exe exists
if exist "LogSentry-CLI.exe" (
    echo ✅ LogSentry-CLI.exe found
) else (
    echo ❌ LogSentry-CLI.exe not found in current directory
    echo 💡 Make sure you're in the correct directory
    goto end
)

echo.
echo 🚀 Running LogSentry-CLI.exe --help...
echo ===============================================

REM Run with help flag to test basic functionality
LogSentry-CLI.exe --help

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Basic CLI test successful!
    echo.
    echo 🎯 Testing version command...
    LogSentry-CLI.exe --version
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ✅ Version command successful!
    ) else (
        echo.
        echo ❌ Version command failed with error code: %ERRORLEVEL%
    )
) else (
    echo.
    echo ❌ CLI test failed with error code: %ERRORLEVEL%
    echo.
    echo 🔍 Common issues and solutions:
    echo    1. Missing Visual C++ Redistributables
    echo    2. Antivirus blocking the executable
    echo    3. Corrupted download
    echo    4. Insufficient permissions
    echo.
    echo 💡 Try these solutions:
    echo    1. Run as Administrator
    echo    2. Add exception to antivirus
    echo    3. Download Microsoft Visual C++ Redistributables
    echo    4. Re-download the executable
)

echo.
echo 🎯 Testing list-rules command...
echo ===============================================

LogSentry-CLI.exe list-rules

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ List-rules command successful!
) else (
    echo.
    echo ❌ List-rules command failed with error code: %ERRORLEVEL%
)

:end
echo.
echo ===============================================
echo 🏁 Debug session complete
echo ===============================================
echo.
echo If the executable is still not working:
echo 1. Try running from Command Prompt as Administrator
echo 2. Check Windows Event Viewer for error details
echo 3. Temporarily disable antivirus
echo 4. Re-download the executable
echo.
pause