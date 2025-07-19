#!/usr/bin/env python3
"""
Debug script to check what files are available when running as executable
"""

import os
import sys

def main():
    print("🔍 Executable Debug Information")
    print("=" * 50)
    
    # Check if running as executable
    try:
        base_path = sys._MEIPASS
        print(f"🎯 Running as executable")
        print(f"   Base path: {base_path}")
        is_executable = True
    except AttributeError:
        print("🐍 Running from Python source")
        is_executable = False
        return
    
    print()
    
    # List all files in the base path
    print("📁 Files in executable:")
    try:
        for root, dirs, files in os.walk(base_path):
            level = root.replace(base_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            sub_indent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{sub_indent}{file}")
    except Exception as e:
        print(f"❌ Error listing files: {e}")
    
    print()
    
    # Check specific paths
    important_paths = [
        'frontend',
        'frontend/templates',
        'frontend/static',
        'frontend/templates/index.html',
        'frontend/templates/404.html',
        'frontend/static/css/style.css',
        'frontend/static/js/app.js',
    ]
    
    print("🔍 Important Path Checks:")
    for path in important_paths:
        full_path = os.path.join(base_path, path)
        exists = os.path.exists(full_path)
        status = "✅" if exists else "❌"
        print(f"   {status} {path}")
    
    print()
    
    # Try to import and test Flask app
    try:
        from logsentry.web_app import app
        print("✅ Flask app imported successfully")
        print(f"   Template folder: {app.template_folder}")
        print(f"   Static folder: {app.static_folder}")
        print(f"   Template folder exists: {os.path.exists(app.template_folder)}")
        print(f"   Static folder exists: {os.path.exists(app.static_folder)}")
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")

if __name__ == "__main__":
    main()