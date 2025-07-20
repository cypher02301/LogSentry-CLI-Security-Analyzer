/**
 * LogSentry Web Application JavaScript
 * Created by Anthony Frederick, 2025
 * 
 * Main JavaScript application for the LogSentry security log analyzer web interface.
 * Handles file uploads, analysis requests, chart rendering, and user interactions.
 */

class LogSentryApp {
    constructor() {
        this.charts = {};
        this.currentAnalysisResult = null;
        this.init();
    }

    /**
     * Initialize the application
     * Sets up event listeners and initial UI state
     */
    init() {
        console.log('🛡️ LogSentry Web App Initializing...');
        console.log('Created by Anthony Frederick, 2025');
        
        this.setupEventListeners();
        this.loadInitialData();
        this.showWelcomeMessage();
    }

    /**
     * Set up all event listeners for the application
     */
    setupEventListeners() {
        // File upload form
        document.getElementById('upload-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFileUpload();
        });

        // Text analysis form
        document.getElementById('text-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleTextAnalysis();
        });

        // Rule testing form
        document.getElementById('test-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleRuleTesting();
        });

        // Generate sample button
        document.getElementById('generate-sample-btn').addEventListener('click', () => {
            this.generateSampleData();
        });

        // Load rules button
        document.getElementById('load-rules-btn').addEventListener('click', () => {
            this.loadSecurityRules();
        });

        // Export buttons
        document.getElementById('export-json-btn').addEventListener('click', () => {
            this.exportResults('json');
        });

        document.getElementById('export-csv-btn').addEventListener('click', () => {
            this.exportResults('csv');
        });

        // File drag and drop
        this.setupFileDragDrop();

        // Smooth scrolling for navigation
        this.setupSmoothScrolling();
    }

    /**
     * Set up file drag and drop functionality
     */
    setupFileDragDrop() {
        const uploadArea = document.getElementById('logfile').parentElement;
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('file-drop-zone', 'dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('dragover');
            }, false);
        });

        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                document.getElementById('logfile').files = files;
                this.showStatus(`File "${files[0].name}" ready for analysis`, 'info');
            }
        }, false);
    }

    /**
     * Set up smooth scrolling for navigation links
     */
    setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    /**
     * Prevent default drag and drop behavior
     */
    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    /**
     * Load initial data when the app starts
     */
    loadInitialData() {
        // Load rules count in background
        this.getSecurityRulesCount();
    }

    /**
     * Show welcome message
     */
    showWelcomeMessage() {
        this.showStatus('Welcome to LogSentry! Upload a log file or paste log data to begin analysis.', 'info');
    }

    /**
     * Handle file upload and analysis
     */
    async handleFileUpload() {
        const form = document.getElementById('upload-form');
        const formData = new FormData(form);
        const fileInput = document.getElementById('logfile');

        if (!fileInput.files.length) {
            this.showStatus('Please select a file to upload', 'warning');
            return;
        }

        try {
            this.showProgress();
            this.showStatus('Uploading and analyzing file...', 'info');

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.displayAnalysisResults(result.result);
                this.showStatus(`Analysis complete! Found ${result.result.summary.total_detections} threats.`, 'success');
            } else {
                this.showStatus(`Analysis failed: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.showStatus(`Upload failed: ${error.message}`, 'danger');
        } finally {
            this.hideProgress();
        }
    }

    /**
     * Handle text analysis
     */
    async handleTextAnalysis() {
        const textArea = document.getElementById('log-text');
        const logText = textArea.value.trim();

        if (!logText) {
            this.showStatus('Please enter some log data to analyze', 'warning');
            return;
        }

        try {
            this.showProgress();
            this.showStatus('Analyzing log text...', 'info');

            const response = await fetch('/analyze_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: logText })
            });

            const result = await response.json();

            if (result.success) {
                this.displayAnalysisResults(result.result);
                this.showStatus(`Analysis complete! Found ${result.result.summary.total_detections} threats.`, 'success');
            } else {
                this.showStatus(`Analysis failed: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Text analysis error:', error);
            this.showStatus(`Analysis failed: ${error.message}`, 'danger');
        } finally {
            this.hideProgress();
        }
    }

    /**
     * Handle rule testing
     */
    async handleRuleTesting() {
        const testInput = document.getElementById('test-text');
        const testText = testInput.value.trim();

        if (!testText) {
            this.showStatus('Please enter text to test against rules', 'warning');
            return;
        }

        try {
            this.showStatus('Testing rules...', 'info');

            const response = await fetch('/test_rule', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: testText })
            });

            const result = await response.json();

            if (result.success) {
                this.displayTestResults(result.detections);
                this.showStatus(`Rule test complete! Found ${result.total_matches} matches.`, 'success');
            } else {
                this.showStatus(`Rule test failed: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Rule test error:', error);
            this.showStatus(`Rule test failed: ${error.message}`, 'danger');
        }
    }

    /**
     * Generate sample log data
     */
    async generateSampleData() {
        try {
            this.showStatus('Generating sample data...', 'info');

            const response = await fetch('/generate_sample', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    count: 100,
                    include_attacks: true
                })
            });

            const result = await response.json();

            if (result.success) {
                document.getElementById('log-text').value = result.sample_data;
                this.showStatus(`Generated ${result.line_count} sample log entries with attacks`, 'success');
                
                // Scroll to text analysis section
                document.getElementById('log-text').scrollIntoView({ behavior: 'smooth' });
            } else {
                this.showStatus(`Sample generation failed: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Sample generation error:', error);
            this.showStatus(`Sample generation failed: ${error.message}`, 'danger');
        }
    }

    /**
     * Load security rules
     */
    async loadSecurityRules() {
        try {
            this.showStatus('Loading security rules...', 'info');

            const response = await fetch('/rules');
            const result = await response.json();

            if (result.success) {
                this.displaySecurityRules(result.rules_by_category);
                this.showStatus(`Loaded ${result.total_rules} security rules`, 'success');
            } else {
                this.showStatus(`Failed to load rules: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Rules loading error:', error);
            this.showStatus(`Failed to load rules: ${error.message}`, 'danger');
        }
    }

    /**
     * Get security rules count for display
     */
    async getSecurityRulesCount() {
        try {
            const response = await fetch('/rules');
            const result = await response.json();
            
            if (result.success) {
                // Update any rule count displays
                console.log(`📋 ${result.total_rules} security rules available`);
            }
        } catch (error) {
            console.warn('Could not fetch rules count:', error);
        }
    }

    /**
     * Display analysis results
     */
    displayAnalysisResults(result) {
        this.currentAnalysisResult = result;

        // Update summary cards
        this.updateSummaryCards(result.summary);

        // Create charts
        this.createCharts(result.charts);

        // Populate detections table
        this.populateDetectionsTable(result.detections);

        // Show results section
        const resultsSection = document.getElementById('results-section');
        resultsSection.classList.remove('d-none');
        resultsSection.classList.add('fade-in-up');

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    /**
     * Update summary cards with analysis data
     */
    updateSummaryCards(summary) {
        document.getElementById('total-detections').textContent = summary.total_detections || 0;
        document.getElementById('risk-score').textContent = summary.risk_score?.overall || 0;
        document.getElementById('unique-ips').textContent = summary.unique_ips || 0;
        document.getElementById('suspicious-ips').textContent = summary.suspicious_ips || 0;
    }

    /**
     * Create charts for data visualization
     */
    createCharts(chartData) {
        // Destroy existing charts
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });

        // Severity distribution pie chart
        if (chartData.severity_distribution && chartData.severity_distribution.length > 0) {
            this.charts.severity = this.createPieChart(
                'severity-chart',
                'Threat Severity Distribution',
                chartData.severity_distribution
            );
        }

        // Category distribution bar chart
        if (chartData.category_distribution && chartData.category_distribution.length > 0) {
            this.charts.category = this.createBarChart(
                'category-chart',
                'Threat Categories',
                chartData.category_distribution
            );
        }
    }

    /**
     * Create a pie chart
     */
    createPieChart(canvasId, title, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(item => item.label),
                datasets: [{
                    data: data.map(item => item.value),
                    backgroundColor: data.map(item => item.color || this.getRandomColor()),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: title,
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        position: 'bottom',
                        labels: { padding: 20 }
                    }
                },
                animation: {
                    animateRotate: true,
                    duration: 1000
                }
            }
        });
    }

    /**
     * Create a bar chart
     */
    createBarChart(canvasId, title, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(item => item.label),
                datasets: [{
                    label: 'Count',
                    data: data.map(item => item.value),
                    backgroundColor: 'rgba(13, 110, 253, 0.8)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: title,
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    /**
     * Populate the detections table
     */
    populateDetectionsTable(detections) {
        const tbody = document.getElementById('detections-tbody');
        tbody.innerHTML = '';

        if (!detections || detections.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No threats detected</td></tr>';
            return;
        }

        detections.forEach(detection => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${detection.line_number || 'N/A'}</td>
                <td><code>${this.escapeHtml(detection.rule_name)}</code></td>
                <td><span class="badge severity-${detection.severity}">${detection.severity.toUpperCase()}</span></td>
                <td>${this.escapeHtml(detection.category.replace('_', ' '))}</td>
                <td>${this.escapeHtml(detection.description)}</td>
                <td>${detection.confidence}%</td>
                <td><code class="text-break">${this.escapeHtml(detection.matched_text)}</code></td>
            `;
            row.classList.add('slide-in-right');
            tbody.appendChild(row);
        });
    }

    /**
     * Display rule test results
     */
    displayTestResults(detections) {
        const resultsDiv = document.getElementById('test-results');
        const detectionsDiv = document.getElementById('test-detections');

        if (!detections || detections.length === 0) {
            detectionsDiv.innerHTML = '<div class="alert alert-info">No rule matches found.</div>';
        } else {
            let html = '<div class="row">';
            detections.forEach(detection => {
                html += `
                    <div class="col-md-6 mb-3">
                        <div class="card border-${this.getSeverityColor(detection.severity)}">
                            <div class="card-body">
                                <h6 class="card-title">
                                    <span class="badge severity-${detection.severity}">${detection.severity.toUpperCase()}</span>
                                    ${this.escapeHtml(detection.rule_name)}
                                </h6>
                                <p class="card-text">${this.escapeHtml(detection.description)}</p>
                                <small class="text-muted">
                                    Category: ${detection.category} | Confidence: ${detection.confidence}%
                                </small>
                            </div>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            detectionsDiv.innerHTML = html;
        }

        resultsDiv.classList.remove('d-none');
        resultsDiv.classList.add('fade-in-up');
    }

    /**
     * Display security rules
     */
    displaySecurityRules(rulesByCategory) {
        const rulesContent = document.getElementById('rules-content');
        let html = '';

        Object.entries(rulesByCategory).forEach(([category, rules]) => {
            html += `
                <div class="mb-4">
                    <h6 class="text-primary">
                        <i class="fas fa-shield-alt"></i>
                        ${category.replace('_', ' ').toUpperCase()}
                        <span class="badge bg-secondary ms-2">${rules.length}</span>
                    </h6>
                    <div class="row">
            `;

            rules.forEach(rule => {
                html += `
                    <div class="col-lg-6 mb-3">
                        <div class="card h-100">
                            <div class="card-body">
                                <h6 class="card-title">
                                    <span class="badge severity-${rule.severity}">${rule.severity.toUpperCase()}</span>
                                    ${this.escapeHtml(rule.name)}
                                </h6>
                                <p class="card-text">${this.escapeHtml(rule.description)}</p>
                                ${rule.tags ? `<div class="small text-muted">Tags: ${rule.tags.join(', ')}</div>` : ''}
                            </div>
                        </div>
                    </div>
                `;
            });

            html += '</div></div>';
        });

        rulesContent.innerHTML = html;
    }

    /**
     * Export analysis results
     */
    exportResults(format) {
        if (!this.currentAnalysisResult) {
            this.showStatus('No analysis results to export', 'warning');
            return;
        }

        try {
            let data, filename, mimeType;

            if (format === 'json') {
                data = JSON.stringify(this.currentAnalysisResult, null, 2);
                filename = `logsentry-analysis-${new Date().toISOString().split('T')[0]}.json`;
                mimeType = 'application/json';
            } else if (format === 'csv') {
                data = this.convertToCSV(this.currentAnalysisResult.detections);
                filename = `logsentry-detections-${new Date().toISOString().split('T')[0]}.csv`;
                mimeType = 'text/csv';
            }

            this.downloadFile(data, filename, mimeType);
            this.showStatus(`Exported results as ${format.toUpperCase()}`, 'success');
        } catch (error) {
            console.error('Export error:', error);
            this.showStatus(`Export failed: ${error.message}`, 'danger');
        }
    }

    /**
     * Convert detections to CSV format
     */
    convertToCSV(detections) {
        const headers = ['Line', 'Rule', 'Severity', 'Category', 'Description', 'Confidence', 'Matched Text'];
        const csvRows = [headers.join(',')];

        detections.forEach(detection => {
            const row = [
                detection.line_number || 'N/A',
                `"${detection.rule_name}"`,
                detection.severity,
                detection.category,
                `"${detection.description}"`,
                detection.confidence,
                `"${detection.matched_text}"`
            ];
            csvRows.push(row.join(','));
        });

        return csvRows.join('\n');
    }

    /**
     * Download file to user's computer
     */
    downloadFile(data, filename, mimeType) {
        const blob = new Blob([data], { type: mimeType });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }

    /**
     * Show status message
     */
    showStatus(message, type = 'info') {
        const alert = document.getElementById('status-alert');
        const messageSpan = document.getElementById('status-message');
        
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        messageSpan.textContent = message;
        alert.classList.remove('d-none');

        // Auto-hide after 5 seconds for non-error messages
        if (type !== 'danger') {
            setTimeout(() => {
                alert.classList.add('d-none');
            }, 5000);
        }
    }

    /**
     * Show progress indicator
     */
    showProgress() {
        document.getElementById('progress-section').classList.remove('d-none');
    }

    /**
     * Hide progress indicator
     */
    hideProgress() {
        document.getElementById('progress-section').classList.add('d-none');
    }

    /**
     * Get severity color class
     */
    getSeverityColor(severity) {
        const colors = {
            'low': 'success',
            'medium': 'warning',
            'high': 'warning',
            'critical': 'danger'
        };
        return colors[severity] || 'secondary';
    }

    /**
     * Generate random color for charts
     */
    getRandomColor() {
        const colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
            '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new LogSentryApp();
});

// Health check function
async function checkAppHealth() {
    try {
        const response = await fetch('/health');
        const result = await response.json();
        console.log('🛡️ LogSentry Health Check:', result);
        return result.status === 'healthy';
    } catch (error) {
        console.error('Health check failed:', error);
        return false;
    }
}

// Run health check on load
checkAppHealth();