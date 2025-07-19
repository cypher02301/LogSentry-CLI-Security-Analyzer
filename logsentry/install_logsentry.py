#!/usr/bin/env python3
"""
LogSentry Installation Script
Created by Anthony Frederick, 2025

This script automatically installs LogSentry CLI Security Analyzer
and handles common installation issues including missing setuptools.
"""

import subprocess
import sys
import os
import platform

def print_header():
    """Print the installation header"""
    print("🛡️  LogSentry CLI Security Analyzer")
    print("📦 Automated Installation Script")
    print("Created by Anthony Frederick, 2025")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro} detected")
    
    if version < (3, 8):
        print("❌ ERROR: Python 3.8+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again")
        return False
    
    print("✅ Python version compatible")
    return True

def run_command(command, description, allow_failure=False):
    """Run a command and handle errors gracefully"""
    print(f"\n🔄 {description}...")
    
    try:
        # Use shell=True for cross-platform compatibility
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
        
    except subprocess.CalledProcessError as e:
        if allow_failure:
            print(f"⚠️  {description} failed (continuing anyway)")
            print(f"   Error: {e.stderr.strip() if e.stderr else 'Unknown error'}")
            return False
        else:
            print(f"❌ {description} failed")
            print(f"   Error: {e.stderr.strip() if e.stderr else 'Unknown error'}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {description} timed out after 2 minutes")
        return False
    except Exception as e:
        print(f"❌ {description} failed with unexpected error: {e}")
        return False

def detect_installation_method():
    """Detect the best installation method for this system"""
    print("\n🔍 Detecting best installation method...")
    
    # Check if we can use virtual environments
    venv_available = run_command(
        "python -m venv --help", 
        "Checking virtual environment support", 
        allow_failure=True
    )
    
    # Check if we have pip
    pip_available = run_command(
        "pip --version", 
        "Checking pip availability", 
        allow_failure=True
    )
    
    # Check system permissions
    system_writable = platform.system() != "Linux"  # Assume non-Linux systems are more permissive
    
    if venv_available:
        print("✅ Virtual environment method recommended")
        return "venv"
    elif pip_available:
        print("✅ User installation method available")
        return "user"
    else:
        print("⚠️  Limited installation options detected")
        return "basic"

def install_with_venv():
    """Install using virtual environment (recommended)"""
    print("\n📦 Installing with Virtual Environment Method")
    
    commands = [
        ("python -m venv logsentry_env", "Creating virtual environment"),
    ]
    
    # Platform-specific activation
    if platform.system() == "Windows":
        activate_cmd = "logsentry_env\\Scripts\\activate"
        pip_cmd = "logsentry_env\\Scripts\\pip"
    else:
        activate_cmd = "source logsentry_env/bin/activate"
        pip_cmd = "logsentry_env/bin/pip"
    
    commands.extend([
        (f"{pip_cmd} install --upgrade pip", "Upgrading pip in virtual environment"),
        (f"{pip_cmd} install setuptools wheel", "Installing build tools"),
        (f"{pip_cmd} install click python-dateutil colorama rich pyyaml regex", "Installing dependencies"),
    ])
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("\n🎉 Virtual environment installation completed!")
    print(f"\n📖 To use LogSentry, activate the environment:")
    if platform.system() == "Windows":
        print("   logsentry_env\\Scripts\\activate")
    else:
        print("   source logsentry_env/bin/activate")
    print("   python -m logsentry.cli --help")
    
    return True

def install_with_user():
    """Install using user installation method"""
    print("\n📦 Installing with User Installation Method")
    
    commands = [
        ("pip install --user --upgrade pip", "Upgrading pip"),
        ("pip install --user setuptools wheel", "Installing build tools"),
        ("pip install --user click python-dateutil colorama rich pyyaml regex", "Installing dependencies"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            # Try alternative method
            alt_command = command.replace("--user", "--break-system-packages")
            print(f"🔄 Trying alternative method...")
            if not run_command(alt_command, description):
                return False
    
    print("\n🎉 User installation completed!")
    print("\n📖 Usage:")
    print("   python -m logsentry.cli --help")
    
    return True

def install_basic():
    """Basic installation fallback"""
    print("\n📦 Installing with Basic Method")
    
    commands = [
        ("python -m pip install setuptools wheel", "Installing build tools"),
        ("python -m pip install click python-dateutil colorama rich pyyaml regex", "Installing dependencies"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("\n🎉 Basic installation completed!")
    print("\n📖 Usage:")
    print("   python -m logsentry.cli --help")
    
    return True

def verify_installation():
    """Verify that LogSentry was installed correctly"""
    print("\n🔍 Verifying installation...")
    
    # Test importing core modules
    try:
        import importlib
        modules = ['click', 'rich', 'yaml', 'regex']
        
        for module in modules:
            importlib.import_module(module)
            print(f"✅ {module} module available")
            
    except ImportError as e:
        print(f"❌ Module import failed: {e}")
        return False
    
    print("✅ All required modules available")
    
    # Test LogSentry CLI
    if os.path.exists("logsentry"):
        test_success = run_command(
            "python -m logsentry.cli --help", 
            "Testing LogSentry CLI", 
            allow_failure=True
        )
        
        if test_success:
            print("✅ LogSentry CLI working correctly")
        else:
            print("⚠️  LogSentry CLI test failed (may need to cd to logsentry directory)")
    
    return True

def print_usage_examples():
    """Print usage examples and next steps"""
    print("\n" + "=" * 50)
    print("🎉 LogSentry Installation Complete!")
    print("=" * 50)
    
    print("\n📖 Quick Start Examples:")
    print("   # Get help")
    print("   python -m logsentry.cli --help")
    
    print("\n   # Test threat detection")
    print('   python -m logsentry.cli test-rules "GET /admin/../../../etc/passwd"')
    
    print("\n   # Generate sample data and analyze")
    print("   python -m logsentry.cli generate-sample --include-attacks --count 100")
    print("   python -m logsentry.cli analyze sample_logs.txt")
    
    print("\n   # Analyze real log file")
    print("   python -m logsentry.cli analyze /path/to/your/logfile.log --verbose")
    
    print("\n   # Scan directory for log files")
    print("   python -m logsentry.cli scan /var/log --pattern '*.log'")
    
    print("\n🔧 Troubleshooting:")
    print("   If you encounter issues, check INSTALLATION.md for detailed solutions")
    
    print("\n📧 Created by Anthony Frederick, 2025")
    print("🛡️  Happy log hunting with LogSentry!")

def main():
    """Main installation function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Detect best installation method
    method = detect_installation_method()
    
    # Install based on detected method
    success = False
    
    if method == "venv":
        success = install_with_venv()
    elif method == "user":
        success = install_with_user()
    else:
        success = install_basic()
    
    if not success:
        print("\n❌ Installation failed!")
        print("📖 Please check INSTALLATION.md for manual installation instructions")
        sys.exit(1)
    
    # Verify installation
    verify_installation()
    
    # Print usage examples
    print_usage_examples()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during installation: {e}")
        print("📖 Please check INSTALLATION.md for manual installation instructions")
        sys.exit(1)