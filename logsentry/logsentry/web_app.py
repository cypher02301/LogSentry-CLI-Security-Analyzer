"""
LogSentry Web Application
Created by Anthony Frederick, 2025

Flask-based web frontend for LogSentry CLI Security Analyzer.
Provides a user-friendly web interface for log analysis, threat detection,
and security monitoring with real-time results and beautiful visualizations.
"""

import os
import json
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import io
import base64

from .analyzer import LogAnalyzer, AnalysisResult
from .rules import SecurityRules, Severity
from .parsers import LogParserManager

# Initialize Flask application
app = Flask(__name__, 
           template_folder='../frontend/templates',
           static_folder='../frontend/static')
app.secret_key = 'logsentry_2025_anthony_frederick'  # Change in production

# Configuration
UPLOAD_FOLDER = '../frontend/static/uploads'
ALLOWED_EXTENSIONS = {'log', 'txt', 'csv', 'json', 'gz'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global analyzer instance
analyzer = LogAnalyzer()
security_rules = SecurityRules()


def allowed_file(filename: str) -> bool:
    """
    Check if uploaded file has allowed extension
    
    Args:
        filename (str): Name of the uploaded file
        
    Returns:
        bool: True if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def format_analysis_for_web(result: AnalysisResult) -> Dict[str, Any]:
    """
    Format analysis result for web display
    
    Converts the analysis result into a JSON-serializable format
    suitable for web frontend consumption with additional formatting
    for charts and visualizations.
    
    Args:
        result (AnalysisResult): Raw analysis result from LogSentry
        
    Returns:
        Dict[str, Any]: Web-formatted analysis data
    """
    # Convert detections to serializable format
    detections_data = []
    for detection in result.detections:
        detections_data.append({
            'rule_name': detection.rule_name,
            'severity': detection.severity.value,
            'description': detection.description,
            'matched_text': detection.matched_text[:200],  # Truncate for display
            'line_number': detection.line_number,
            'timestamp': detection.timestamp,
            'category': detection.category,
            'tags': detection.tags,
            'confidence': round(detection.confidence, 2)
        })
    
    # Prepare data for charts
    severity_chart_data = []
    for severity, count in result.summary.get('by_severity', {}).items():
        severity_chart_data.append({
            'label': severity.title(),
            'value': count,
            'color': get_severity_color(severity)
        })
    
    category_chart_data = []
    for category, count in result.summary.get('by_category', {}).items():
        category_chart_data.append({
            'label': category.replace('_', ' ').title(),
            'value': count
        })
    
    # Timeline data for time-series chart
    timeline_data = []
    for entry in result.timeline:
        if entry.get('timestamp'):
            timeline_data.append({
                'timestamp': entry['timestamp'].isoformat() if hasattr(entry['timestamp'], 'isoformat') else str(entry['timestamp']),
                'count': entry['total_detections']
            })
    
    return {
        'file_info': {
            'file_path': os.path.basename(result.file_path),
            'total_lines': result.total_lines,
            'parsed_lines': result.parsed_lines,
            'analysis_time': round(result.analysis_time, 2)
        },
        'summary': {
            'total_detections': len(result.detections),
            'risk_score': result.summary.get('risk_score', {}),
            'unique_ips': result.summary.get('unique_ips', 0),
            'suspicious_ips': result.summary.get('suspicious_ips', 0),
            'top_threats': result.summary.get('top_threats', [])[:10]
        },
        'detections': detections_data,
        'charts': {
            'severity_distribution': severity_chart_data,
            'category_distribution': category_chart_data,
            'timeline': timeline_data
        },
        'ip_analysis': result.ip_analysis,
        'log_types': result.log_types
    }


def get_severity_color(severity: str) -> str:
    """
    Get color code for severity level
    
    Args:
        severity (str): Severity level string
        
    Returns:
        str: Hex color code for the severity
    """
    colors = {
        'low': '#28a745',      # Green
        'medium': '#ffc107',   # Yellow
        'high': '#fd7e14',     # Orange
        'critical': '#dc3545'  # Red
    }
    return colors.get(severity.lower(), '#6c757d')


@app.route('/')
def index():
    """
    Main dashboard page
    
    Displays the LogSentry web interface with upload form,
    analysis options, and results display area.
    """
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and analysis
    
    Processes uploaded log files, runs security analysis,
    and returns formatted results for web display.
    """
    try:
        # Check if file was uploaded
        if 'logfile' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['logfile']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Supported: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Get analysis options
        max_lines = request.form.get('max_lines', type=int)
        severity_filter = request.form.get('severity_filter')
        
        # Save uploaded file securely
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Analyze the log file
        result = analyzer.analyze_file(filepath, max_lines)
        
        # Filter results if requested
        if severity_filter and severity_filter != 'all':
            filtered_detections = []
            severity_levels = ['low', 'medium', 'high', 'critical']
            min_level_index = severity_levels.index(severity_filter.lower())
            
            for detection in result.detections:
                detection_level_index = severity_levels.index(detection.severity.value)
                if detection_level_index >= min_level_index:
                    filtered_detections.append(detection)
            
            result.detections = filtered_detections
        
        # Format for web display
        web_result = format_analysis_for_web(result)
        
        # Clean up uploaded file (optional - keep for download)
        # os.remove(filepath)
        
        return jsonify({
            'success': True,
            'result': web_result
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    """
    Analyze text input directly without file upload
    
    Processes raw log text provided through the web interface
    and returns analysis results.
    """
    try:
        data = request.get_json()
        log_text = data.get('text', '')
        
        if not log_text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze the text
        result = analyzer.analyze_text(log_text, 'web_input')
        
        # Format for web display
        web_result = format_analysis_for_web(result)
        
        return jsonify({
            'success': True,
            'result': web_result
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@app.route('/test_rule', methods=['POST'])
def test_rule():
    """
    Test a single rule against provided text
    
    Allows users to test specific log entries against
    LogSentry's detection rules in real-time.
    """
    try:
        data = request.get_json()
        test_text = data.get('text', '')
        
        if not test_text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        # Test the text against rules
        detections = analyzer.rule_engine.analyze_line(test_text, 1)
        
        # Format detections for response
        result_detections = []
        for detection in detections:
            result_detections.append({
                'rule_name': detection.rule_name,
                'severity': detection.severity.value,
                'description': detection.description,
                'category': detection.category,
                'confidence': round(detection.confidence, 2),
                'tags': detection.tags
            })
        
        return jsonify({
            'success': True,
            'detections': result_detections,
            'total_matches': len(result_detections)
        })
        
    except Exception as e:
        return jsonify({'error': f'Rule test failed: {str(e)}'}), 500


@app.route('/rules')
def get_rules():
    """
    Get all available security rules
    
    Returns the complete list of LogSentry security detection rules
    with their categories, descriptions, and severity levels.
    """
    try:
        rules_data = []
        
        # Group rules by category
        rules_by_category = {}
        for rule in security_rules.rules:
            category = rule.category
            if category not in rules_by_category:
                rules_by_category[category] = []
            
            rules_by_category[category].append({
                'name': rule.name,
                'description': rule.description,
                'severity': rule.severity.value,
                'tags': rule.tags,
                'pattern': rule.pattern  # Be careful about exposing patterns
            })
        
        return jsonify({
            'success': True,
            'rules_by_category': rules_by_category,
            'total_rules': len(security_rules.rules)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get rules: {str(e)}'}), 500


@app.route('/generate_sample', methods=['POST'])
def generate_sample():
    """
    Generate sample log data for testing
    
    Creates sample log entries with optional attack patterns
    for demonstration and testing purposes.
    """
    try:
        data = request.get_json()
        count = data.get('count', 100)
        include_attacks = data.get('include_attacks', True)
        
        # Import the sample generation function from CLI
        from .cli import _generate_sample_logs
        
        # Create temporary file for sample data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
            sample_file = f.name
        
        # Generate sample data
        _generate_sample_logs(sample_file, count, include_attacks)
        
        # Read the generated data
        with open(sample_file, 'r') as f:
            sample_content = f.read()
        
        # Clean up
        os.unlink(sample_file)
        
        return jsonify({
            'success': True,
            'sample_data': sample_content,
            'line_count': count
        })
        
    except Exception as e:
        return jsonify({'error': f'Sample generation failed: {str(e)}'}), 500


@app.route('/export/<format_type>')
def export_results(format_type):
    """
    Export analysis results in various formats
    
    Args:
        format_type (str): Export format ('json', 'csv', 'pdf')
    """
    try:
        # This would need to store the last analysis result
        # For now, return a placeholder
        return jsonify({'error': 'Export functionality coming soon'}), 501
        
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500


@app.route('/health')
def health_check():
    """
    Health check endpoint for monitoring
    
    Returns the status of the LogSentry web application
    and its components.
    """
    try:
        # Test analyzer functionality
        test_result = analyzer.analyze_text("test log entry", "health_check")
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'analyzer': 'operational',
            'rules_loaded': len(security_rules.rules),
            'creator': 'Anthony Frederick, 2025'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


def run_web_app(host='0.0.0.0', port=5000, debug=True):
    """
    Run the LogSentry web application
    
    Args:
        host (str): Host to bind to (default: 0.0.0.0)
        port (int): Port to listen on (default: 5000)
        debug (bool): Enable debug mode (default: True)
    """
    print("🛡️  LogSentry Web Application")
    print("Created by Anthony Frederick, 2025")
    print(f"Starting server on http://{host}:{port}")
    print("=" * 50)
    
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_web_app()