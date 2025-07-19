# 🌐 LogSentry Web Interface

**Created by Anthony Frederick, 2025**

A modern, responsive web interface for the LogSentry security log analyzer that provides an intuitive way to upload, analyze, and visualize security threats in log files.

## 🚀 **Quick Start**

### **Method 1: Using CLI Command**
```bash
cd logsentry
python3 -m logsentry.cli web
```

### **Method 2: Using Standalone Launcher**
```bash
cd logsentry
python3 run_web.py
```

### **Method 3: Direct Import**
```python
from logsentry.web_app import run_web_app
run_web_app()
```

## 📖 **Features**

### **🔍 Core Analysis Features**
- **File Upload**: Drag & drop or browse for log files (.log, .txt, .csv, .json, .gz)
- **Text Analysis**: Paste log data directly for immediate analysis
- **Real-time Processing**: Live progress indicators and status updates
- **Multi-format Support**: Apache, Nginx, syslog, Windows Event Logs, firewall logs

### **📊 Visualization & Reporting**
- **Interactive Charts**: Pie charts for severity distribution, bar charts for categories
- **Summary Dashboard**: Key metrics cards with threat counts and risk scores
- **Detailed Tables**: Sortable, searchable tables of detected threats
- **Export Options**: Download results in JSON or CSV format

### **🛡️ Security Features**
- **Rule Testing**: Test individual log entries against detection rules
- **Real-time Detection**: Immediate threat identification as you type
- **Severity Filtering**: Filter results by threat severity levels
- **IP Analysis**: Automatic IP geolocation and reputation checking

### **🎨 User Experience**
- **Modern UI**: Clean, professional design with Bootstrap 5
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark Mode Support**: Automatic dark theme based on system preferences
- **Accessibility**: Full keyboard navigation and screen reader support

## 🖥️ **Interface Overview**

### **Navigation Sections**
1. **Upload**: File upload and text analysis
2. **Rules**: Browse and explore security detection rules
3. **Test**: Test individual log entries against rules
4. **About**: Information about LogSentry and its creator

### **Main Dashboard**
- **Hero Section**: Welcome banner with LogSentry branding
- **Upload Cards**: Side-by-side file upload and text analysis
- **Progress Indicator**: Shows analysis progress with animated bars
- **Results Section**: Comprehensive analysis results with charts and tables

### **Results Display**
- **Summary Cards**: Total threats, risk score, unique IPs, suspicious IPs
- **Charts**: Visual representation of threat distribution
- **Detections Table**: Detailed list of all detected threats
- **Export Controls**: Download results in multiple formats

## 🛠️ **Configuration Options**

### **Server Configuration**
```bash
# Basic startup
python3 -m logsentry.cli web

# Custom host and port
python3 -m logsentry.cli web --host 127.0.0.1 --port 8080

# Debug mode
python3 -m logsentry.cli web --debug

# Production mode
python3 -m logsentry.cli web --host 0.0.0.0 --port 80
```

### **Environment Variables**
```bash
export LOGSENTRY_HOST=0.0.0.0
export LOGSENTRY_PORT=5000
export LOGSENTRY_DEBUG=false
export LOGSENTRY_SECRET_KEY=your-secret-key-here
```

### **Advanced Configuration**
Edit `logsentry/web_app.py` to customize:
- Upload file size limits
- Allowed file extensions
- Session configuration
- Security settings

## 📡 **API Endpoints**

The web interface exposes several REST API endpoints:

### **Analysis Endpoints**
- `POST /upload` - Upload and analyze log files
- `POST /analyze_text` - Analyze raw log text
- `POST /test_rule` - Test rules against text

### **Data Endpoints**
- `GET /rules` - Get all security rules
- `POST /generate_sample` - Generate sample log data
- `GET /health` - Health check endpoint

### **Export Endpoints**
- `GET /export/json` - Export results as JSON
- `GET /export/csv` - Export results as CSV

## 🎨 **Customization**

### **Styling**
Modify `frontend/static/css/style.css` to customize:
- Color schemes and themes
- Animation effects
- Layout and spacing
- Responsive breakpoints

### **Functionality**
Extend `frontend/static/js/app.js` to add:
- Custom chart types
- Additional export formats
- Enhanced user interactions
- Real-time features

### **Templates**
Edit `frontend/templates/index.html` to modify:
- Page structure and layout
- UI components and sections
- Branding and content

## 🔧 **Development Setup**

### **Prerequisites**
```bash
pip install flask werkzeug
```

### **Development Mode**
```bash
# Enable debug mode for development
python3 -m logsentry.cli web --debug

# Or set environment variable
export FLASK_DEBUG=1
python3 run_web.py
```

### **File Structure**
```
frontend/
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   └── app.js             # JavaScript application
│   └── uploads/               # File upload directory
├── templates/
│   ├── index.html             # Main page template
│   └── 404.html               # Error page template
├── web_app.py                 # Flask application
└── run_web.py                 # Standalone launcher
```

## 🚀 **Production Deployment**

### **Using Gunicorn**
```bash
pip install gunicorn
cd logsentry
gunicorn -w 4 -b 0.0.0.0:5000 logsentry.web_app:app
```

### **Using uWSGI**
```bash
pip install uwsgi
uwsgi --http :5000 --module logsentry.web_app:app
```

### **Using Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY logsentry/ .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "-m", "logsentry.cli", "web"]
```

### **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🛡️ **Security Considerations**

### **File Upload Security**
- File size limits (16MB default)
- Extension validation
- Secure filename handling
- Upload directory isolation

### **Input Validation**
- XSS prevention with HTML escaping
- CSRF protection with secure forms
- SQL injection prevention
- Input sanitization

### **Production Security**
```python
# In production, update these settings:
app.secret_key = 'secure-random-key'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
```

## 📱 **Mobile Experience**

The web interface is fully responsive and optimized for mobile devices:

- **Touch-friendly**: Large buttons and touch targets
- **Adaptive Layout**: Cards stack vertically on small screens
- **Mobile Charts**: Touch-enabled charts with zoom/pan
- **Fast Loading**: Optimized assets and lazy loading

## 🧪 **Testing**

### **Manual Testing**
1. Upload various log file formats
2. Test text analysis with sample data
3. Verify rule testing functionality
4. Check export functionality
5. Test mobile responsiveness

### **Automated Testing**
```bash
# Test web endpoints
python3 -m pytest tests/test_web.py

# Test JavaScript functionality
npm test  # If you add JS testing
```

## 🔍 **Troubleshooting**

### **Common Issues**

**Port Already in Use**
```bash
# Use different port
python3 -m logsentry.cli web --port 8080
```

**Permission Denied**
```bash
# Use port >1024 or run with sudo
python3 -m logsentry.cli web --port 8080
```

**Import Errors**
```bash
# Make sure you're in the right directory
cd logsentry
python3 -m logsentry.cli web
```

**File Upload Issues**
- Check file size (16MB limit)
- Verify file extension is allowed
- Ensure upload directory is writable

### **Debug Mode**
Enable debug mode for detailed error messages:
```bash
python3 -m logsentry.cli web --debug
```

## 📈 **Performance Tips**

### **Optimization**
- Use production WSGI server (Gunicorn/uWSGI)
- Enable gzip compression
- Serve static files with Nginx
- Use CDN for external libraries

### **Monitoring**
- Check `/health` endpoint for status
- Monitor memory usage during analysis
- Track request response times
- Log analysis performance metrics

## 🤝 **Contributing**

To contribute to the web interface:

1. **Frontend**: Modify HTML/CSS/JS files
2. **Backend**: Update Flask routes and functions
3. **Features**: Add new analysis capabilities
4. **Testing**: Write tests for new functionality

## 📞 **Support**

If you encounter issues with the web interface:

1. Check the console for JavaScript errors
2. Verify server logs for backend issues
3. Test with sample data first
4. Ensure all dependencies are installed

## 🎯 **Future Enhancements**

Planned features for future releases:

- **Real-time Monitoring**: Live log streaming and analysis
- **User Authentication**: Multi-user support with login
- **Advanced Visualizations**: Timeline charts, heatmaps, network graphs
- **API Integration**: Connect to SIEM systems and log aggregators
- **Machine Learning**: AI-powered threat detection
- **Collaboration**: Share analyses and create custom dashboards

---

**Created by Anthony Frederick, 2025**  
🛡️ LogSentry CLI Security Analyzer - Web Interface

For more information, visit the main [README.md](README.md) or check the [CLI documentation](CLI.md).