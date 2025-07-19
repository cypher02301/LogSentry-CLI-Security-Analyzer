# -*- mode: python ; coding: utf-8 -*-
"""
LogSentry Web Interface PyInstaller Specification
Created by Anthony Frederick, 2025

PyInstaller specification file for creating LogSentry Web Interface executable.
This creates a standalone Windows executable with web server capabilities.
"""

import os
import sys
from pathlib import Path

# Get the current directory
current_dir = Path(__file__).parent.absolute()

# Define the analysis
a = Analysis(
    ['logsentry_web.py'],  # Main script
    pathex=[str(current_dir)],  # Path to search for modules
    binaries=[],  # No additional binaries needed
    datas=[
        # Include web interface files (critical for web app)
        ('frontend/templates', 'frontend/templates'),
        ('frontend/static', 'frontend/static'),
        # Include documentation
        ('*.md', '.'),
        # Include any sample data files
        ('tests/test_data', 'tests/test_data'),
    ],
    hiddenimports=[
        # Ensure all LogSentry modules are included
        'logsentry',
        'logsentry.cli',
        'logsentry.analyzer',
        'logsentry.parsers',
        'logsentry.rules',
        'logsentry.utils',
        'logsentry.web_app',
        # Flask and web dependencies
        'flask',
        'werkzeug',
        'jinja2',
        'markupsafe',
        'itsdangerous',
        'blinker',
        'werkzeug.utils',
        'werkzeug.security',
        'werkzeug.serving',
        'flask.helpers',
        'flask.json',
        # Required core dependencies
        'click',
        'rich',
        'colorama',
        'python_dateutil',
        'yaml',
        'regex',
        # Standard library modules
        'socket',
        'threading',
        'json',
        'csv',
        'gzip',
        'tempfile',
        'urllib',
        'urllib.parse',
        'urllib.request',
        'hashlib',
        'base64',
        'datetime',
        'math',
        'statistics',
        're',
        'os',
        'sys',
        'pathlib',
        'collections',
        'dataclasses',
        'enum',
        'typing',
        'io',
        'webbrowser',
        'mimetypes',
        'secrets',
        'uuid',
        # Network and web related
        'http',
        'http.server',
        'socketserver',
        'email',
        'email.utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude packages we don't need to reduce size
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'wx',
        'IPython',
        'jupyter',
        'notebook',
    ],
    noarchive=False,
)

# Create the PYZ file (Python archive)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LogSentry-Web',  # Executable name
    debug=False,  # Set to True for debugging
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress executable (if UPX is available)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console application (shows server output)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path here if you have one
    # Executable metadata
    version_file=None,  # Can add version info file here
)