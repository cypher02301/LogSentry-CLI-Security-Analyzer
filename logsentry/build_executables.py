#!/usr/bin/env python3
"""
LogSentry Executable Builder
Created by Anthony Frederick, 2025

Automated script to build Windows executables for LogSentry using PyInstaller.
Creates both CLI and Web interface executables with all dependencies bundled.
"""

import os
import sys
import shutil
import subprocess
import time
from pathlib import Path

def print_header():
    """Print the build script header"""
    print("🛡️  LogSentry Executable Builder")
    print("Created by Anthony Frederick, 2025")
    print("=" * 50)
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'pyinstaller',
        'flask',
        'click',
        'rich',
        'colorama',
        'python-dateutil',
        'pyyaml',
        'regex'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("💡 Install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies found")
    return True

def clean_build_directories():
    """Clean previous build directories"""
    print("\n🧹 Cleaning previous builds...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"   🗑️  Removed {dir_name}/")
            except Exception as e:
                print(f"   ⚠️  Could not remove {dir_name}/: {e}")
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                except:
                    pass
    
    print("✅ Build directories cleaned")

def build_executable(spec_file, executable_name):
    """Build an executable using PyInstaller"""
    print(f"\n🔨 Building {executable_name}...")
    print(f"   Spec file: {spec_file}")
    
    start_time = time.time()
    
    try:
        # Run PyInstaller
        cmd = ['pyinstaller', '--clean', '--noconfirm', spec_file]
        print(f"   Command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        build_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"   ✅ {executable_name} built successfully in {build_time:.1f}s")
            
            # Check if executable exists
            exe_path = Path('dist') / f"{executable_name}.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"   📦 Executable size: {size_mb:.1f} MB")
                print(f"   📁 Location: {exe_path.absolute()}")
                return True
            else:
                print(f"   ❌ Executable not found at {exe_path}")
                return False
        else:
            print(f"   ❌ Build failed for {executable_name}")
            print(f"   Error output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ❌ Build timed out for {executable_name}")
        return False
    except Exception as e:
        print(f"   ❌ Build error for {executable_name}: {e}")
        return False

def create_release_package():
    """Create a release package with both executables"""
    print("\n📦 Creating release package...")
    
    release_dir = Path('dist/LogSentry-Release')
    release_dir.mkdir(exist_ok=True)
    
    # Copy executables
    exe_files = list(Path('dist').glob('*.exe'))
    for exe_file in exe_files:
        if exe_file.name not in ['LogSentry-CLI.exe', 'LogSentry-Web.exe']:
            continue
        
        dest = release_dir / exe_file.name
        try:
            shutil.copy2(exe_file, dest)
            print(f"   ✅ Copied {exe_file.name}")
        except Exception as e:
            print(f"   ❌ Failed to copy {exe_file.name}: {e}")
    
    # Copy documentation
    doc_files = ['README.md', 'WEB_INTERFACE.md', 'INSTALLATION.md', 'LICENSE']
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            try:
                shutil.copy2(doc_file, release_dir / doc_file)
                print(f"   ✅ Copied {doc_file}")
            except Exception as e:
                print(f"   ❌ Failed to copy {doc_file}: {e}")
    
    # Create usage instructions
    usage_file = release_dir / 'USAGE.txt'
    with open(usage_file, 'w') as f:
        f.write("""LogSentry Security Log Analyzer - Standalone Executables
Created by Anthony Frederick, 2025

USAGE INSTRUCTIONS:

1. CLI Interface:
   - Run: LogSentry-CLI.exe --help
   - Example: LogSentry-CLI.exe analyze logfile.txt
   - Example: LogSentry-CLI.exe scan C:\\logs --pattern "*.log"

2. Web Interface:
   - Run: LogSentry-Web.exe
   - Open browser to: http://localhost:5000
   - Upload log files via web interface
   - View interactive charts and results

3. Command Line Options:
   - LogSentry-CLI.exe analyze [file] --verbose --severity high
   - LogSentry-Web.exe --port 8080 --no-browser

4. Supported Log Formats:
   - Apache/Nginx access logs
   - Windows Event Logs
   - Syslog files
   - Firewall logs
   - JSON logs
   - CSV files
   - Compressed (.gz) files

5. Security Features:
   - SQL injection detection
   - XSS attack detection
   - Directory traversal detection
   - Brute force detection
   - Privilege escalation detection
   - And many more...

For full documentation, see README.md and WEB_INTERFACE.md

Created by Anthony Frederick, 2025
""")
    
    print(f"   ✅ Created usage instructions")
    print(f"   📁 Release package: {release_dir.absolute()}")
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in release_dir.rglob('*') if f.is_file())
    total_size_mb = total_size / (1024 * 1024)
    print(f"   📊 Total package size: {total_size_mb:.1f} MB")
    
    return release_dir

def main():
    """Main build function"""
    print_header()
    
    # Check if we're in the right directory
    if not os.path.exists('logsentry'):
        print("❌ Error: Must run from the logsentry project root directory")
        print("💡 Change to the directory containing the 'logsentry' folder")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Clean previous builds
    clean_build_directories()
    
    # Build executables
    builds = [
        ('logsentry_cli.spec', 'LogSentry-CLI'),
        ('logsentry_web.spec', 'LogSentry-Web'),
    ]
    
    successful_builds = 0
    total_builds = len(builds)
    
    for spec_file, exe_name in builds:
        if build_executable(spec_file, exe_name):
            successful_builds += 1
    
    # Summary
    print(f"\n📊 Build Summary:")
    print(f"   ✅ Successful: {successful_builds}/{total_builds}")
    print(f"   ❌ Failed: {total_builds - successful_builds}/{total_builds}")
    
    if successful_builds > 0:
        # Create release package
        release_dir = create_release_package()
        
        print(f"\n🎉 Build completed successfully!")
        print(f"📦 Executables available in: {Path('dist').absolute()}")
        print(f"📁 Release package: {release_dir}")
        print(f"\n💡 Next steps:")
        print(f"   1. Test the executables")
        print(f"   2. Distribute the release package")
        print(f"   3. Share LogSentry with the world!")
        
    else:
        print(f"\n❌ Build failed!")
        print(f"💡 Check the error messages above and fix any issues")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)