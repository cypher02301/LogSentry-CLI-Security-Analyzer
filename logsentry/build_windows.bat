@echo off
REM LogSentry Windows Executable Builder
REM Created by Anthony Frederick, 2025
REM
REM Simple batch file to build LogSentry Windows executables

echo.
echo ==========================================
echo LogSentry Windows Executable Builder
echo Created by Anthony Frederick, 2025
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if PyInstaller is available
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Building LogSentry CLI executable...
python -m PyInstaller --clean --noconfirm logsentry_cli.spec
if errorlevel 1 (
    echo ERROR: Failed to build CLI executable
    pause
    exit /b 1
)

echo.
echo Building LogSentry Web Interface executable...
python -m PyInstaller --clean --noconfirm logsentry_web.spec
if errorlevel 1 (
    echo ERROR: Failed to build Web executable
    pause
    exit /b 1
)

echo.
echo Creating release package...
if not exist "dist\LogSentry-Release" mkdir "dist\LogSentry-Release"

copy "dist\LogSentry-CLI.exe" "dist\LogSentry-Release\" >nul
copy "dist\LogSentry-Web.exe" "dist\LogSentry-Release\" >nul
copy "README.md" "dist\LogSentry-Release\" >nul
copy "LICENSE" "dist\LogSentry-Release\" >nul
if exist "WEB_INTERFACE.md" copy "WEB_INTERFACE.md" "dist\LogSentry-Release\" >nul

echo.
echo ==========================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ==========================================
echo.
echo Executables created:
echo - LogSentry-CLI.exe (Command Line Interface)
echo - LogSentry-Web.exe (Web Interface)
echo.
echo Location: dist\LogSentry-Release\
echo.
echo Usage:
echo   LogSentry-CLI.exe --help
echo   LogSentry-Web.exe
echo.
echo Created by Anthony Frederick, 2025
echo.
pause