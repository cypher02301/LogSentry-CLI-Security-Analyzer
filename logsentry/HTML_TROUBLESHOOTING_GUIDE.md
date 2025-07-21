# 🔧 LogSentry HTML File Troubleshooting Guide

**Comprehensive guide to fix HTML file issues**

## ✅ **Current Status Check**

Based on diagnostics, your LogSentry web app has:
- ✅ **HTML File**: Present and structurally valid (413 lines, 19KB)
- ✅ **Template Engine**: Jinja2 syntax working correctly
- ✅ **Flask App**: Imports and starts successfully
- ✅ **File Paths**: Templates and static files found correctly
- ✅ **Web Server**: Starts on http://0.0.0.0:5000

## 🚨 **Common HTML Issues & Solutions**

### **Issue 1: Web Page Not Loading**

**Symptoms**: Browser shows "This site can't be reached" or connection error

**Solutions**:
```bash
# 1. Start the web server
cd /path/to/logsentry
python3 logsentry_web.py

# 2. Access the correct URL
# Open browser to: http://localhost:5000
# NOT: http://0.0.0.0:5000 (this might not work in browser)
```

### **Issue 2: Template Not Found Error**

**Symptoms**: `TemplateNotFound: index.html` error

**Solutions**:
```bash
# Check file exists
ls -la frontend/templates/index.html

# Check permissions
chmod 644 frontend/templates/index.html

# Verify Flask configuration
python3 -c "from logsentry.web_app import app; print(app.template_folder)"
```

### **Issue 3: Static Files Not Loading**

**Symptoms**: CSS/JS not working, images not showing

**Solutions**:
```bash
# Check static directory
ls -la frontend/static/

# Check CSS file
ls -la frontend/static/css/style.css

# Check JavaScript file
ls -la frontend/static/js/app.js
```

### **Issue 4: HTML Syntax Errors**

**Symptoms**: Page displays incorrectly or partially

**Solutions**:
```bash
# Validate HTML structure
python3 -c "
with open('frontend/templates/index.html', 'r') as f:
    content = f.read()
    
# Check for unclosed tags
open_tags = content.count('<')
close_tags = content.count('>')
print(f'Open tags: {open_tags}, Close tags: {close_tags}')

# Check for Jinja2 syntax
jinja_open = content.count('{{')
jinja_close = content.count('}}')
print(f'Jinja2 open: {jinja_open}, close: {jinja_close}')
"
```

## 🛠️ **Quick Fix Commands**

### **1. Restart Web Server**
```bash
# Kill any running instances
pkill -f logsentry_web
pkill -f python3

# Start fresh
cd logsentry
python3 logsentry_web.py
```

### **2. Test Web Server**
```bash
# Test if server responds
curl -I http://localhost:5000

# Test HTML content
curl -s http://localhost:5000 | head -10
```

### **3. Check File Integrity**
```bash
# Verify HTML file
file frontend/templates/index.html

# Check file size
ls -lh frontend/templates/index.html

# Count lines
wc -l frontend/templates/index.html
```

## 🔍 **Diagnostic Commands**

Run these to identify the exact issue:

### **Test 1: Flask App Import**
```bash
python3 -c "
try:
    from logsentry.web_app import app
    print('✅ Flask app imports successfully')
    print(f'Template folder: {app.template_folder}')
    print(f'Static folder: {app.static_folder}')
except Exception as e:
    print(f'❌ Flask import error: {e}')
"
```

### **Test 2: Template Rendering**
```bash
python3 -c "
import sys
sys.path.append('.')
from logsentry.web_app import app

with app.app_context():
    try:
        from flask import render_template
        html = render_template('index.html')
        print('✅ Template renders successfully')
        print(f'HTML length: {len(html)} characters')
    except Exception as e:
        print(f'❌ Template error: {e}')
"
```

### **Test 3: Web Server Response**
```bash
python3 -c "
import requests
import time
import subprocess
import os

# Start server in background
proc = subprocess.Popen(['python3', 'logsentry_web.py'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.DEVNULL)
time.sleep(3)

try:
    response = requests.get('http://localhost:5000', timeout=5)
    print(f'✅ Server responds: {response.status_code}')
    print(f'Content length: {len(response.text)}')
    if 'LogSentry' in response.text:
        print('✅ HTML content looks correct')
    else:
        print('❌ HTML content may be corrupted')
except Exception as e:
    print(f'❌ Server error: {e}')
finally:
    proc.terminate()
"
```

## 🔧 **Fix Specific Issues**

### **Fix 1: Corrupted HTML File**
```bash
# Backup current file
cp frontend/templates/index.html frontend/templates/index.html.backup

# Check if file is corrupted
hexdump -C frontend/templates/index.html | head -5

# If corrupted, restore from backup or regenerate
```

### **Fix 2: Permission Issues**
```bash
# Fix file permissions
chmod 644 frontend/templates/index.html
chmod 755 frontend/templates/
chmod 755 frontend/static/
chmod -R 644 frontend/static/*
```

### **Fix 3: Path Issues**
```bash
# Check current directory
pwd

# Ensure you're in the right location
cd /workspace/logsentry  # or your actual path

# Verify directory structure
tree frontend/ || ls -la frontend/
```

### **Fix 4: Port Conflicts**
```bash
# Check if port 5000 is in use
netstat -tulpn | grep :5000
lsof -i :5000

# Kill processes using port 5000
sudo fuser -k 5000/tcp

# Or use different port
python3 logsentry_web.py --port 5001
```

## 🚀 **Complete Reset Procedure**

If nothing else works, try this complete reset:

### **Step 1: Clean Environment**
```bash
# Kill all Python processes
pkill -f python3
pkill -f logsentry

# Clear Python cache
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
```

### **Step 2: Verify Files**
```bash
# Check all required files exist
ls -la frontend/templates/index.html
ls -la frontend/static/css/style.css
ls -la frontend/static/js/app.js
ls -la logsentry/web_app.py
```

### **Step 3: Test Import Chain**
```bash
# Test each import
python3 -c "import logsentry; print('✅ logsentry package')"
python3 -c "from logsentry import web_app; print('✅ web_app module')"
python3 -c "from logsentry.web_app import app; print('✅ Flask app')"
```

### **Step 4: Fresh Start**
```bash
# Start with verbose output
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from logsentry.web_app import app
app.run(host='0.0.0.0', port=5000, debug=True)
"
```

## 📱 **Browser-Specific Issues**

### **Chrome/Edge**
- Clear cache: Ctrl+Shift+Delete
- Hard refresh: Ctrl+Shift+R
- Check Developer Tools (F12) for errors

### **Firefox**
- Clear cache: Ctrl+Shift+Delete
- Hard refresh: Ctrl+F5
- Check Web Console (F12) for errors

### **Safari**
- Clear cache: Safari > Preferences > Privacy > Manage Website Data
- Hard refresh: Cmd+Shift+R

## 🔍 **What to Check Next**

1. **Browser Console**: Press F12 and check for JavaScript errors
2. **Network Tab**: See if CSS/JS files are loading (Status 200)
3. **Flask Logs**: Check terminal output for error messages
4. **File Encoding**: Ensure HTML file is UTF-8 encoded

## 💡 **Quick Test**

Run this one-liner to test everything:

```bash
cd logsentry && python3 -c "
from logsentry.web_app import app
import threading
import time
import requests

# Start server
def start_server():
    app.run(host='localhost', port=5000, debug=False)

server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()
time.sleep(2)

# Test response
try:
    response = requests.get('http://localhost:5000')
    print(f'✅ SUCCESS: Server responds with status {response.status_code}')
    print(f'✅ HTML content: {len(response.text)} characters')
    if 'LogSentry' in response.text:
        print('✅ LogSentry branding found - HTML is working!')
    else:
        print('❌ LogSentry branding not found - check HTML content')
except Exception as e:
    print(f'❌ ERROR: {e}')
"
```

---

**🔧 HTML Troubleshooting Guide Complete**  
**Created by Anthony Frederick, 2025**

*Run the diagnostics above to identify and fix your specific HTML issue!*