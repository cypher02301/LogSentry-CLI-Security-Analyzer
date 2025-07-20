#!/usr/bin/env python3
"""
LogSentry CLI Executable Entry Point
Created by Anthony Frederick, 2025

Main entry point for creating standalone executables of LogSentry.
This provides a clean interface for PyInstaller to build executables.
"""

import sys
import os

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """Main entry point for LogSentry CLI executable"""
    try:
        # Import and run the CLI
        from logsentry.cli import cli
        cli()
    except ImportError as e:
        print(f"❌ Error importing LogSentry modules: {e}")
        print("💡 Please ensure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running LogSentry: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()