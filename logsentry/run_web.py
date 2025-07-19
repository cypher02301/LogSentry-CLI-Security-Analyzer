#!/usr/bin/env python3
"""
LogSentry Web Interface Launcher
Created by Anthony Frederick, 2025

Standalone script to launch the LogSentry security log analyzer web interface.
This provides a convenient way to start the web application without using CLI.
"""

import sys
import os
import argparse

# Add the current directory to path so we can import logsentry modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function to launch LogSentry web interface"""
    
    parser = argparse.ArgumentParser(
        description='LogSentry Web Interface Launcher',
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
    print("📱 Web Interface Launcher")
    print("Created by Anthony Frederick, 2025")
    print("=" * 50)
    print()
    
    try:
        # Import the web application
        from logsentry.web_app import run_web_app
        
        # Display startup information
        print(f"🌐 Starting web server...")
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
        print("💡 Make sure you're running from the correct directory")
        print("💡 Try: cd logsentry && python3 run_web.py")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n👋 LogSentry web server stopped by user")
        
    except Exception as e:
        print(f"❌ Failed to start web server: {e}")
        print("💡 Check that the port is not already in use")
        print("💡 Try a different port: python3 run_web.py --port 8080")
        sys.exit(1)


if __name__ == '__main__':
    main()