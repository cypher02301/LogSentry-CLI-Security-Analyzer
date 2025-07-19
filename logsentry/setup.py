"""
Setup script for LogSentry CLI Security Analyzer

Created by Anthony Frederick, 2025
Package configuration and installation script for LogSentry, a comprehensive
Python-based log analysis tool for detecting security incidents and threats.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_file(filename):
    """Read file contents for use as long description"""
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name="logsentry",
    version="1.0.0",
    author="Anthony Frederick",
    author_email="anthony.frederick@logsentry.dev",
    description="A Python-based log analysis tool for detecting security incidents",
    long_description=read_file('README.md') if os.path.exists('README.md') else '',
    long_description_content_type="text/markdown",
    url="https://github.com/logsentry/logsentry",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "python-dateutil>=2.8.2",
        "colorama>=0.4.4",
        "rich>=13.0.0",
        "pyyaml>=6.0",
        "regex>=2023.3.23",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.900",
        ],
    },
    entry_points={
        "console_scripts": [
            "logsentry=logsentry.cli:cli",
        ],
    },
    keywords="security log analysis threat detection cybersecurity",
    project_urls={
        "Bug Reports": "https://github.com/logsentry/logsentry/issues",
        "Source": "https://github.com/logsentry/logsentry",
        "Documentation": "https://logsentry.readthedocs.io",
    },
)