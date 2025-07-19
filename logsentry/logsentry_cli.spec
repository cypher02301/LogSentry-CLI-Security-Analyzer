# -*- mode: python ; coding: utf-8 -*-
"""
LogSentry CLI PyInstaller Specification
Created by Anthony Frederick, 2025

PyInstaller specification file for creating LogSentry CLI executable.
This creates a standalone Windows executable with all dependencies bundled.
"""

import os
import sys
from pathlib import Path

# Get the current directory
current_dir = Path.cwd().absolute()

# Define the analysis
a = Analysis(
    ['logsentry_cli.py'],  # Main script
    pathex=[str(current_dir)],  # Path to search for modules
    binaries=[],  # No additional binaries needed
    datas=[
        # Include template files for web interface (if needed)
        ('frontend/templates', 'frontend/templates'),
        ('frontend/static', 'frontend/static'),
        # Include any data files that might be needed
        ('*.md', '.'),  # Include documentation
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
        # Required dependencies
        'click',
        'rich',
        'colorama',
        'python_dateutil',
        'yaml',
        'regex',
        'flask',
        'werkzeug',
        'jinja2',
        'markupsafe',
        'itsdangerous',
        'blinker',
        # Standard library modules that might be missed
        'socket',
        'threading',
        'json',
        'csv',
        'gzip',
        'tempfile',
        'urllib',
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
    name='LogSentry-CLI',  # Executable name
    debug=False,  # Set to True for debugging
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress executable (if UPX is available)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path here if you have one
    # Executable metadata
    version_file=None,  # Can add version info file here
)