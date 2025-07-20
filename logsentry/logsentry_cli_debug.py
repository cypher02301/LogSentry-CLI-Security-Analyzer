#!/usr/bin/env python3
"""
LogSentry CLI - Debug Standalone Executable Entry Point
Created by Anthony Frederick, 2025

This is the main entry point for the standalone CLI executable with enhanced debugging.
This version includes comprehensive error handling and debug output to help diagnose issues.
"""

import os
import sys
import traceback
from pathlib import Path

def debug_environment():
    """Print debug information about the execution environment."""
    print("🔧 LogSentry CLI Debug Information")
    print("=" * 50)
    
    # Basic environment info
    print(f"🐍 Python Version: {sys.version}")
    print(f"📁 Current Working Directory: {os.getcwd()}")
    print(f"🖥️  Platform: {sys.platform}")
    
    # Check if running as executable
    try:
        base_path = sys._MEIPASS
        print(f"🎯 Running as executable, base path: {base_path}")
        is_executable = True
    except AttributeError:
        print("🐍 Running from Python source")
        is_executable = False
    
    print()
    
    # Check Python path
    print("📦 Python Path:")
    for i, path in enumerate(sys.path):
        print(f"   {i}: {path}")
    print()
    
    # Check LogSentry module import
    print("🔍 Module Import Tests:")
    modules_to_test = [
        'logsentry',
        'logsentry.cli',
        'logsentry.analyzer',
        'logsentry.rules',
        'logsentry.parsers',
        'click',
        'rich',
        'colorama',
        'yaml',
        'regex'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
    
    print()
    return is_executable

def main():
    """Main entry point with comprehensive error handling."""
    try:
        # Print debug information
        is_executable = debug_environment()
        
        print("🚀 Starting LogSentry CLI...")
        print()
        
        # Import and run the main CLI
        from logsentry.cli import cli
        
        print("✅ LogSentry CLI imported successfully")
        print("🎯 Executing CLI command...")
        print()
        
        # Run the CLI
        cli()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print(f"📍 This usually means a required module is missing.")
        print(f"💡 Try reinstalling LogSentry or check dependencies.")
        print()
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print(f"📍 Error Type: {type(e).__name__}")
        print()
        print("🔍 Full Traceback:")
        traceback.print_exc()
        print()
        input("Press Enter to exit...")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n💡 LogSentry CLI stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()