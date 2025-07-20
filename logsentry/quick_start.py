#!/usr/bin/env python3
"""
LogSentry Quick Start Script
Created by Anthony Frederick, 2025

Simple script to quickly fix setuptools issues and get LogSentry running.
Use this if you're getting "ModuleNotFoundError: No module named 'setuptools'"
"""

import subprocess
import sys

def print_banner():
    print("🛡️  LogSentry Quick Start")
    print("Created by Anthony Frederick, 2025")
    print("Fixing setuptools issues...\n")

def run_command(cmd, description):
    """Run command and report status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr.strip()}")
        return False

def main():
    print_banner()
    
    # Try multiple methods to install setuptools
    methods = [
        ("pip install --user setuptools wheel", "Installing setuptools (user)"),
        ("pip install --break-system-packages setuptools wheel", "Installing setuptools (system override)"),
        ("python3 -m pip install --user setuptools wheel", "Installing setuptools (python3 -m pip)"),
    ]
    
    success = False
    for cmd, desc in methods:
        if run_command(cmd, desc):
            success = True
            break
    
    if not success:
        print("\n❌ All installation methods failed!")
        print("Please check INSTALLATION.md for detailed solutions")
        return
    
    # Install LogSentry dependencies
    deps_cmd = "pip install --break-system-packages click python-dateutil colorama rich pyyaml regex"
    if not run_command(deps_cmd, "Installing LogSentry dependencies"):
        alt_cmd = "pip install --user click python-dateutil colorama rich pyyaml regex"
        run_command(alt_cmd, "Installing dependencies (user mode)")
    
    print("\n🎉 Quick setup complete!")
    print("\n📖 Test LogSentry:")
    print('   python3 -m logsentry.cli test-rules "GET /admin/../../../etc/passwd"')
    print("\n📖 Get help:")
    print("   python3 -m logsentry.cli --help")

if __name__ == "__main__":
    main()