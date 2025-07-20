#!/usr/bin/env python3
"""
LogSentry Web Interface Executable Entry Point
Created by Anthony Frederick, 2025

Main entry point for creating standalone web interface executables of LogSentry.
This provides a clean interface for PyInstaller to build web executables.
"""

import sys
import os
import argparse

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """Main entry point for LogSentry Web Interface executable"""
    
    parser = argparse.ArgumentParser(
        description='LogSentry Web Interface - Standalone Executable',
        epilog='Created by Anthony Frederick, 2025'
    )
    
    parser.add_argument(
        '--host', 
        default='0.0.0.0',
        help='Host to bind to (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port', 
        type=int,
        default=5000,
        help='Port to listen on (default: 5000)'
    )
    
    parser.add_argument(
        '--debug', 
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--no-browser',
        action='store_true',
        help='Do not automatically open browser'
    )
    
    args = parser.parse_args()
    
    print("🛡️  LogSentry Security Log Analyzer")
    print("🌐 Web Interface - Standalone Executable")
    print("Created by Anthony Frederick, 2025")
    print("=" * 50)
    print()
    
    try:
        # Import the web application
        from logsentry.web_app import run_web_app
        
        # Display startup information
        print(f"🌐 Starting LogSentry web server...")
        print(f"   Host: {args.host}")
        print(f"   Port: {args.port}")
        print(f"   Debug: {'Enabled' if args.debug else 'Disabled'}")
        print()
        print(f"🔗 Access LogSentry at: http://{args.host}:{args.port}")
        print("💡 Use Ctrl+C to stop the server")
        print()
        
        # Optionally open browser
        if not args.no_browser:
            try:
                import webbrowser
                webbrowser.open(f"http://localhost:{args.port}")
                print("🌐 Opening LogSentry in your default browser...")
            except Exception:
                print("⚠️  Could not open browser automatically")
        
        print("🚀 LogSentry web server starting...")
        print()
        
        # Start the web application
        run_web_app(host=args.host, port=args.port, debug=args.debug)
        
    except ImportError as e:
        print(f"❌ Failed to import LogSentry modules: {e}")
        print("💡 Please ensure all dependencies are installed")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n👋 LogSentry web server stopped by user")
        
    except Exception as e:
        print(f"❌ Failed to start web server: {e}")
        print("💡 Check that the port is not already in use")
        print(f"💡 Try a different port: {sys.argv[0]} --port 8080")
        sys.exit(1)

if __name__ == '__main__':
    main()