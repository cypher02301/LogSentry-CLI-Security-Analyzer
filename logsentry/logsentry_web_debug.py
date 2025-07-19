#!/usr/bin/env python3
"""
LogSentry Web Interface - Debug Standalone Executable Entry Point
Created by Anthony Frederick, 2025

This is the main entry point for the standalone web interface executable.
Includes debug output to help troubleshoot template and static file issues.
"""

import os
import sys
import argparse
import webbrowser
from threading import Timer

def debug_paths():
    """Debug function to check paths and files."""
    print("🔧 Debug Information:")
    
    # Check if running as executable
    try:
        base_path = sys._MEIPASS
        print(f"   🎯 Running as executable, base path: {base_path}")
        is_executable = True
    except AttributeError:
        print("   🐍 Running from Python source")
        is_executable = False
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Check important paths
    important_paths = [
        'frontend',
        'frontend/templates',
        'frontend/static',
        'frontend/templates/index.html',
        'frontend/templates/404.html',
        'frontend/static/css/style.css',
        'frontend/static/js/app.js',
    ]
    
    print("   📁 Path Status:")
    for path in important_paths:
        if is_executable:
            full_path = os.path.join(base_path, path)
        else:
            full_path = os.path.join(base_path, '..', path)
        exists = os.path.exists(full_path)
        status = "✅" if exists else "❌"
        print(f"      {status} {path} -> {full_path}")

def open_browser(url):
    """Open browser after a short delay."""
    webbrowser.open(url)

def main():
    """Main entry point for the web interface executable."""
    print("🛡️  LogSentry Security Log Analyzer")
    print("🌐 Web Interface - Debug Standalone Executable")
    print("Created by Anthony Frederick, 2025")
    print("=" * 50)
    print()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='LogSentry Web Interface - Debug Standalone Executable')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Port to listen on (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--no-browser', action='store_true', help='Do not automatically open browser')
    
    args = parser.parse_args()
    
    # Debug path information
    debug_paths()
    print()
    
    print("🌐 Starting LogSentry web server...")
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   Debug: {'Enabled' if args.debug else 'Disabled'}")
    print()
    
    print(f"🔗 Access LogSentry at: http://{args.host}:{args.port}")
    print("💡 Use Ctrl+C to stop the server")
    print()
    
    # Open browser automatically unless disabled
    if not args.no_browser:
        print("🌐 Opening LogSentry in your default browser...")
        Timer(2.0, open_browser, [f"http://localhost:{args.port}"]).start()
    
    print("🚀 LogSentry web server starting...")
    print()
    
    try:
        # Import and run the Flask application
        from logsentry.web_app import app
        
        print("🛡️  LogSentry Web Application")
        print("Created by Anthony Frederick, 2025")
        print(f"Starting server on http://{args.host}:{args.port}")
        print("=" * 50)
        
        # Run the Flask application
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            use_reloader=False,  # Disable reloader for executable
            threaded=True        # Enable threading for better performance
        )
        
    except ImportError as e:
        print(f"❌ Failed to import LogSentry web application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n💡 LogSentry web server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Failed to start LogSentry web server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()