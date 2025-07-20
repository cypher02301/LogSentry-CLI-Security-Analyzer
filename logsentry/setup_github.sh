#!/bin/bash

# LogSentry GitHub Setup Script
# Created by Anthony Frederick, 2025
# 
# This script automates the process of setting up LogSentry for GitHub upload

echo "🛡️  LogSentry GitHub Setup Script"
echo "=================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    echo "   Download from: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git is installed"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "🔧 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Set up user configuration (will prompt if not set)
echo ""
echo "🔧 Checking git configuration..."

# Check if user.name is set
if [ -z "$(git config user.name)" ]; then
    echo "⚠️  Git user name not set"
    read -p "Enter your name: " username
    git config user.name "$username"
    echo "✅ Git user name set to: $username"
else
    echo "✅ Git user name: $(git config user.name)"
fi

# Check if user.email is set
if [ -z "$(git config user.email)" ]; then
    echo "⚠️  Git user email not set"
    read -p "Enter your email: " useremail
    git config user.email "$useremail"
    echo "✅ Git user email set to: $useremail"
else
    echo "✅ Git user email: $(git config user.email)"
fi

echo ""
echo "📁 Checking project files..."

# Check for important files
files_to_check=("README.md" "pyproject.toml" "logsentry/__init__.py" ".gitignore")
missing_files=()

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ Found: $file"
    else
        echo "❌ Missing: $file"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  Some important files are missing. Please ensure all files are present before continuing."
    exit 1
fi

echo ""
echo "📦 Adding files to git..."

# Add all files to git
git add .

# Check git status
echo ""
echo "📊 Git status:"
git status --short

echo ""
echo "💾 Creating initial commit..."

# Create initial commit
commit_message="🛡️ Initial LogSentry release

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

git commit -m "$commit_message"

echo "✅ Initial commit created"

echo ""
echo "🌐 GitHub Repository Setup"
echo "========================="
echo ""
echo "📝 Next steps to upload to GitHub:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: logsentry"
echo "   - Description: 🛡️ LogSentry - Advanced CLI Security Log Analyzer with Web Interface"
echo "   - Set to Public or Private"
echo "   - DO NOT initialize with README, .gitignore, or license"
echo ""
echo "2. Connect this repository to GitHub:"
echo "   Replace YOUR_USERNAME with your actual GitHub username:"
echo ""
echo "   git branch -M main"
echo "   git remote add origin https://github.com/YOUR_USERNAME/logsentry.git"
echo "   git push -u origin main"
echo ""
echo "3. After uploading, create a release:"
echo "   - Go to your repository → Releases → Create a new release"
echo "   - Tag: v1.0.0"
echo "   - Title: LogSentry v1.0.0 - Initial Release"
echo "   - Upload the executable files from dist/ folder"
echo ""

# Check if executables exist
echo "📋 Available executables:"
if [ -d "dist" ]; then
    ls -la dist/*.exe 2>/dev/null || echo "   No .exe files found in dist/"
    ls -la dist/LogSentry-* 2>/dev/null || echo "   No LogSentry executables found in dist/"
else
    echo "   No dist/ directory found"
    echo "   Run build_executables.py to create executables"
fi

echo ""
echo "📚 Documentation files ready:"
echo "   ✅ README.md - Main documentation"
echo "   ✅ INSTALLATION.md - Installation guide"  
echo "   ✅ WEB_INTERFACE.md - Web interface guide"
echo "   ✅ WINDOWS_CLI_TROUBLESHOOTING.md - Windows troubleshooting"
echo "   ✅ GITHUB_UPLOAD_GUIDE.md - Detailed GitHub instructions"

echo ""
echo "🎯 Repository Topics to add on GitHub:"
echo "   security, log-analysis, cybersecurity, cli-tool, python,"
echo "   flask, threat-detection, windows-executable, pyinstaller"

echo ""
echo "✅ LogSentry is ready for GitHub upload!"
echo ""
echo "📖 For detailed instructions, see: GITHUB_UPLOAD_GUIDE.md"
echo ""
echo "🚀 Happy coding!"