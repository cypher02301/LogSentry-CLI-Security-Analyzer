#!/usr/bin/env python3
"""
LogSentry Web App Path Testing Script
Created by Anthony Frederick, 2025

Tests that all paths are correctly configured for the web application.
"""

import os
import sys
from pathlib import Path

def test_paths():
    """Test all web app paths and configurations."""
    print("🔧 LogSentry Web App Path Testing")
    print("=" * 50)
    print()
    
    # Test current working directory
    cwd = os.getcwd()
    print(f"📂 Current Working Directory: {cwd}")
    
    # Test if we're in an executable
    try:
        base_path = sys._MEIPASS
        print(f"🎯 Running as executable, base path: {base_path}")
        is_executable = True
    except AttributeError:
        print("🐍 Running from Python source")
        is_executable = False
    
    print()
    
    # Test template and static folders
    if is_executable:
        template_folder = os.path.join(sys._MEIPASS, 'frontend', 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'frontend', 'static')
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(current_dir, 'frontend', 'templates')
        static_folder = os.path.join(current_dir, 'frontend', 'static')
    
    print(f"📁 Template Folder: {template_folder}")
    print(f"   Exists: {os.path.exists(template_folder)}")
    
    if os.path.exists(template_folder):
        try:
            templates = os.listdir(template_folder)
            print(f"   Files: {templates}")
        except Exception as e:
            print(f"   Error listing: {e}")
    
    print()
    print(f"📁 Static Folder: {static_folder}")
    print(f"   Exists: {os.path.exists(static_folder)}")
    
    if os.path.exists(static_folder):
        try:
            static_files = os.listdir(static_folder)
            print(f"   Contents: {static_files}")
            
            # Check subdirectories
            for item in static_files:
                item_path = os.path.join(static_folder, item)
                if os.path.isdir(item_path):
                    subfiles = os.listdir(item_path)
                    print(f"   {item}/: {subfiles}")
        except Exception as e:
            print(f"   Error listing: {e}")
    
    print()
    
    # Test key files
    key_files = [
        ('index.html', template_folder),
        ('404.html', template_folder),
        ('style.css', os.path.join(static_folder, 'css')),
        ('app.js', os.path.join(static_folder, 'js')),
    ]
    
    print("🔍 Key File Checks:")
    for filename, folder in key_files:
        if os.path.exists(folder):
            file_path = os.path.join(folder, filename)
            exists = os.path.exists(file_path)
            status = "✅" if exists else "❌"
            print(f"   {status} {filename} ({file_path})")
        else:
            print(f"   ❌ {filename} (folder missing: {folder})")
    
    print()
    
    # Test Flask app import
    try:
        from logsentry.web_app import app
        print("✅ Flask app import successful")
        print(f"   Template folder: {app.template_folder}")
        print(f"   Static folder: {app.static_folder}")
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
    
    print()
    print("🏁 Path testing complete!")

if __name__ == "__main__":
    test_paths()