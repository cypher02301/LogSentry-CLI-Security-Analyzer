#!/usr/bin/env python3
"""
LogSentry Setup Verification Script
Created by Anthony Frederick, 2025

Verifies that LogSentry is installed correctly with all dependencies.
"""

import sys
import importlib
from typing import List, Tuple

def check_python_version() -> bool:
    """Check if Python version is compatible."""
    version = sys.version_info
    if version >= (3, 8):
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def check_package(package_name: str, optional: bool = False) -> bool:
    """Check if a package is installed."""
    try:
        importlib.import_module(package_name)
        status = "✅" if not optional else "✅ (optional)"
        print(f"   {status} {package_name}")
        return True
    except ImportError:
        status = "❌" if not optional else "⚠️  (optional)"
        print(f"   {status} {package_name}")
        return not optional  # Return True for optional packages even if missing

def main():
    """Main verification function."""
    print("🛡️  LogSentry Setup Verification")
    print("Created by Anthony Frederick, 2025")
    print("=" * 50)
    print()
    
    # Check Python version
    print("🐍 Python Version Check:")
    python_ok = check_python_version()
    print()
    
    # Check core LogSentry installation
    print("📦 LogSentry Core:")
    try:
        import logsentry
        print("   ✅ logsentry")
        
        from logsentry.cli import cli
        print("   ✅ logsentry.cli")
        
        from logsentry.analyzer import LogAnalyzer
        print("   ✅ logsentry.analyzer")
        
        from logsentry.rules import SecurityRules
        print("   ✅ logsentry.rules")
        
        core_ok = True
    except ImportError as e:
        print(f"   ❌ LogSentry core modules: {e}")
        core_ok = False
    print()
    
    # Check core dependencies
    print("🔧 Core Dependencies:")
    core_deps = [
        "click", "rich", "colorama", "dateutil", 
        "yaml", "regex"
    ]
    core_deps_ok = all(check_package(dep) for dep in core_deps)
    print()
    
    # Check web dependencies
    print("🌐 Web Interface Dependencies:")
    web_deps = [
        "flask", "werkzeug", "jinja2", "markupsafe", 
        "itsdangerous", "blinker"
    ]
    web_deps_ok = all(check_package(dep, optional=True) for dep in web_deps)
    print()
    
    # Check development dependencies
    print("🔧 Development Dependencies:")
    dev_deps = [
        "pytest", "coverage", "black", "flake8", "mypy"
    ]
    dev_deps_ok = all(check_package(dep, optional=True) for dep in dev_deps)
    print()
    
    # Check build dependencies
    print("🏗️  Build Dependencies:")
    build_deps = ["PyInstaller"]
    build_deps_ok = all(check_package(dep, optional=True) for dep in build_deps)
    print()
    
    # Test CLI functionality
    print("🧪 Functionality Tests:")
    try:
        # Test CLI import
        from logsentry.cli import cli
        print("   ✅ CLI framework")
        
        # Test analyzer
        analyzer = LogAnalyzer()
        print("   ✅ LogAnalyzer initialization")
        
        # Test rules
        rules = SecurityRules()
        print(f"   ✅ Security rules ({len(rules.rules)} rules loaded)")
        
        # Test web app (if available)
        try:
            from logsentry.web_app import app
            print("   ✅ Web application")
        except ImportError:
            print("   ⚠️  Web application (optional)")
        
        functionality_ok = True
    except Exception as e:
        print(f"   ❌ Functionality test failed: {e}")
        functionality_ok = False
    print()
    
    # Summary
    print("📊 Verification Summary:")
    print(f"   Python Version: {'✅ Pass' if python_ok else '❌ Fail'}")
    print(f"   LogSentry Core: {'✅ Pass' if core_ok else '❌ Fail'}")
    print(f"   Core Dependencies: {'✅ Pass' if core_deps_ok else '❌ Fail'}")
    print(f"   Web Dependencies: {'✅ Pass' if web_deps_ok else '⚠️  Optional'}")
    print(f"   Dev Dependencies: {'✅ Pass' if dev_deps_ok else '⚠️  Optional'}")
    print(f"   Build Dependencies: {'✅ Pass' if build_deps_ok else '⚠️  Optional'}")
    print(f"   Functionality: {'✅ Pass' if functionality_ok else '❌ Fail'}")
    print()
    
    # Overall status
    required_ok = python_ok and core_ok and core_deps_ok and functionality_ok
    
    if required_ok:
        print("🎉 LogSentry is properly installed and ready to use!")
        print()
        print("Quick Start Commands:")
        print("   logsentry --help")
        print("   logsentry list-rules")
        print("   logsentry test-rules 'GET /admin/../etc/passwd'")
        if web_deps_ok:
            print("   logsentry web")
        print()
        return True
    else:
        print("❌ LogSentry installation has issues!")
        print()
        print("Recommended Fix:")
        print("   pip uninstall logsentry")
        print("   pip install -e .[dev,web,build]")
        print()
        print("For help, see: SETUP_MIGRATION.md")
        print()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)