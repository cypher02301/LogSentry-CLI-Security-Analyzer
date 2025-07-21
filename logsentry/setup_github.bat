@echo off
REM LogSentry GitHub Setup Script for Windows
REM Created by Anthony Frederick, 2025
REM 
REM This script automates the process of setting up LogSentry for GitHub upload

echo 🛡️  LogSentry GitHub Setup Script (Windows)
echo ============================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    echo    Download from: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo ✅ Git is installed

REM Check if we're in a git repository
if not exist ".git" (
    echo 🔧 Initializing git repository...
    git init
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already exists
)

echo.
echo 🔧 Checking git configuration...

REM Check git user configuration
for /f "tokens=*" %%i in ('git config user.name') do set gitname=%%i
for /f "tokens=*" %%i in ('git config user.email') do set gitemail=%%i

if "%gitname%"=="" (
    echo ⚠️  Git user name not set
    set /p gitname="Enter your name: "
    git config user.name "%gitname%"
    echo ✅ Git user name set to: %gitname%
) else (
    echo ✅ Git user name: %gitname%
)

if "%gitemail%"=="" (
    echo ⚠️  Git user email not set  
    set /p gitemail="Enter your email: "
    git config user.email "%gitemail%"
    echo ✅ Git user email set to: %gitemail%
) else (
    echo ✅ Git user email: %gitemail%
)

echo.
echo 📁 Checking project files...

REM Check for important files
set missing_files=0

if exist "README.md" (
    echo ✅ Found: README.md
) else (
    echo ❌ Missing: README.md
    set missing_files=1
)

if exist "pyproject.toml" (
    echo ✅ Found: pyproject.toml
) else (
    echo ❌ Missing: pyproject.toml
    set missing_files=1
)

if exist "logsentry\__init__.py" (
    echo ✅ Found: logsentry\__init__.py
) else (
    echo ❌ Missing: logsentry\__init__.py
    set missing_files=1
)

if exist ".gitignore" (
    echo ✅ Found: .gitignore
) else (
    echo ❌ Missing: .gitignore
    set missing_files=1
)

if %missing_files%==1 (
    echo.
    echo ⚠️  Some important files are missing. Please ensure all files are present before continuing.
    pause
    exit /b 1
)

echo.
echo 📦 Adding files to git...

REM Add all files to git
git add .

REM Check git status
echo.
echo 📊 Git status:
git status --short

echo.
echo 💾 Creating initial commit...

REM Create initial commit
git commit -m "🛡️ Initial LogSentry release

Features:
- CLI security log analyzer with 20+ detection rules  
- Modern web interface with interactive charts
- Windows/Linux executables included
- Comprehensive documentation and troubleshooting
- Fixed CLI executable issues (yaml/regex dependencies)
- Multiple output formats (JSON, CSV, terminal)
- Web interface with Bootstrap UI and Chart.js
- PyInstaller build configurations
- Debug tools and Windows troubleshooting guides

Created by Anthony Frederick, 2025"

echo ✅ Initial commit created

echo.
echo 🌐 GitHub Repository Setup
echo =========================
echo.
echo 📝 Next steps to upload to GitHub:
echo.
echo 1. Create a new repository on GitHub:
echo    - Go to: https://github.com/new
echo    - Repository name: logsentry
echo    - Description: 🛡️ LogSentry - Advanced CLI Security Log Analyzer with Web Interface
echo    - Set to Public or Private
echo    - DO NOT initialize with README, .gitignore, or license
echo.
echo 2. Connect this repository to GitHub:
echo    Replace YOUR_USERNAME with your actual GitHub username:
echo.
echo    git branch -M main
echo    git remote add origin https://github.com/YOUR_USERNAME/logsentry.git
echo    git push -u origin main
echo.
echo 3. After uploading, create a release:
echo    - Go to your repository → Releases → Create a new release
echo    - Tag: v1.0.0
echo    - Title: LogSentry v1.0.0 - Initial Release
echo    - Upload the executable files from dist\ folder
echo.

REM Check if executables exist
echo 📋 Available executables:
if exist "dist" (
    if exist "dist\*.exe" (
        dir /b dist\*.exe
    ) else (
        echo    No .exe files found in dist\
    )
    if exist "dist\LogSentry-*" (
        dir /b dist\LogSentry-*
    ) else (
        echo    No LogSentry executables found in dist\
    )
) else (
    echo    No dist\ directory found
    echo    Run build_executables.py to create executables
)

echo.
echo 📚 Documentation files ready:
echo    ✅ README.md - Main documentation
echo    ✅ INSTALLATION.md - Installation guide  
echo    ✅ WEB_INTERFACE.md - Web interface guide
echo    ✅ WINDOWS_CLI_TROUBLESHOOTING.md - Windows troubleshooting
echo    ✅ GITHUB_UPLOAD_GUIDE.md - Detailed GitHub instructions

echo.
echo 🎯 Repository Topics to add on GitHub:
echo    security, log-analysis, cybersecurity, cli-tool, python,
echo    flask, threat-detection, windows-executable, pyinstaller

echo.
echo ✅ LogSentry is ready for GitHub upload!
echo.
echo 📖 For detailed instructions, see: GITHUB_UPLOAD_GUIDE.md
echo.
echo 🚀 Happy coding!
echo.
pause