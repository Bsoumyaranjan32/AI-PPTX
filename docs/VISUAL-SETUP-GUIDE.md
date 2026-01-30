# 📸 Visual Setup Guide - Screenshots & Quick Reference

This is a companion guide to [SETUP.md](SETUP.md) with visual aids and a condensed command reference.

---

## ⚡ Super Quick Start (TL;DR)

For experienced developers who just need the commands:

```bash
# 1. Clone & Setup
git clone https://github.com/Bsoumyaranjan32/AI-PPTX.git
cd AI-PPTX
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install & Configure
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys

# 3. Database
mysql -u root -p -e "CREATE DATABASE gamma_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p gamma_ai < database/schema.sql

# 4. Run
python run.py
# Open http://localhost:5000
```

---

## 🗺️ Step-by-Step Visual Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Prerequisites                                       │
│  ✓ Python 3.9+  ✓ MySQL 8.0+  ✓ Git  ✓ API Key            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Clone Repository                                    │
│  $ git clone https://github.com/Bsoumyaranjan32/AI-PPTX.git│
│  $ cd AI-PPTX                                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 3: Virtual Environment                                 │
│  $ python -m venv venv                                      │
│  $ source venv/bin/activate                                 │
│  (venv) ← You should see this                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 4: Install Dependencies                                │
│  (venv) $ pip install -r requirements.txt                   │
│  Installing... [████████████████] 100%                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 5: Configure Environment                               │
│  $ cp .env.example .env                                     │
│  $ nano .env  # Edit with your API keys                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 6: Setup Database                                      │
│  $ mysql -u root -p < database/schema.sql                   │
│  Database 'gamma_ai' created ✓                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 7: Run Application                                     │
│  (venv) $ python run.py                                     │
│  * Running on http://127.0.0.1:5000 ✓                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 8: Access in Browser                                   │
│  🌐 http://localhost:5000                                   │
│  Welcome to Gamma AI! 🎉                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Command Cheat Sheet

### Git Commands
```bash
# Clone repository
git clone https://github.com/Bsoumyaranjan32/AI-PPTX.git

# Navigate to directory
cd AI-PPTX

# Check current status
git status

# Pull latest changes
git pull origin main

# View branches
git branch -a
```

### Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv                    # Linux/Mac/Windows
python3 -m venv venv                   # Explicit Python 3

# Activate virtual environment
source venv/bin/activate               # Linux/Mac
venv\Scripts\activate                  # Windows CMD
venv\Scripts\Activate.ps1              # Windows PowerShell

# Deactivate virtual environment
deactivate                             # All platforms

# Check if active (should show venv path)
which python                           # Linux/Mac
where python                           # Windows
```

### Package Management
```bash
# Install all dependencies
pip install -r requirements.txt

# Install specific package
pip install flask

# Upgrade pip
pip install --upgrade pip

# List installed packages
pip list

# Check for outdated packages
pip list --outdated

# Freeze current packages
pip freeze > requirements.txt
```

### Environment Configuration
```bash
# Copy example environment file
cp .env.example .env                   # Linux/Mac
copy .env.example .env                 # Windows

# Edit .env file
nano .env                              # Linux/Mac (nano)
vim .env                               # Linux/Mac (vim)
notepad .env                           # Windows
code .env                              # VS Code

# View .env content (be careful with sensitive data!)
cat .env                               # Linux/Mac
type .env                              # Windows

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

### MySQL Database
```bash
# Check MySQL version
mysql --version

# Login to MySQL
mysql -u root -p

# Create database (from MySQL shell)
CREATE DATABASE gamma_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Import schema
mysql -u root -p gamma_ai < database/schema.sql

# Run SQL command from terminal
mysql -u root -p gamma_ai -e "SHOW TABLES;"

# Backup database
mysqldump -u root -p gamma_ai > backup.sql

# Restore database
mysql -u root -p gamma_ai < backup.sql

# Drop database (careful!)
mysql -u root -p -e "DROP DATABASE gamma_ai;"
```

### Running the Application
```bash
# Standard run
python run.py

# Run with specific Python version
python3 run.py

# Run on different port (edit .env first)
# Set FLASK_RUN_PORT=8080 in .env
python run.py

# Run in production mode (with gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Process Management
```bash
# Find process on port 5000
lsof -i:5000                           # Linux/Mac
netstat -ano | findstr :5000           # Windows

# Kill process by port
lsof -ti:5000 | xargs kill -9          # Linux/Mac
taskkill /PID <PID> /F                 # Windows (replace <PID>)

# Check if server is running
curl http://localhost:5000             # Linux/Mac
Invoke-WebRequest http://localhost:5000  # Windows PowerShell
```

---

## 🎯 Expected Outputs

### Successful Virtual Environment Activation
```bash
$ source venv/bin/activate
(venv) $  ← Notice the (venv) prefix
```

### Successful Dependency Installation
```bash
$ pip install -r requirements.txt
Collecting Flask==3.0.0
  Downloading Flask-3.0.0-py3-none-any.whl
...
Successfully installed Flask-3.0.0 ... [many more packages]
```

### Successful Database Import
```bash
$ mysql -u root -p gamma_ai < database/schema.sql
Enter password: ********
+-------------------------------------------+
| Status                                     |
+-------------------------------------------+
| Database schema created successfully!     |
+-------------------------------------------+
```

### Successful Application Start
```bash
$ python run.py

================================================================================
🔧 GAMMA AI - INITIALIZATION
================================================================================
📂 Project Root: /path/to/AI-PPTX
🔍 Loading .env from: /path/to/AI-PPTX/.env
✅ .env file loaded successfully
✅ GOOGLE_GEMINI_API_KEY: AIzaSyDXXX... (Hidden)
✅ Database: localhost/gamma_ai
================================================================================

🚀 Creating Flask application...
✅ Flask app created successfully

================================================================================
🎨 GAMMA AI - Python Flask Edition
================================================================================
🚀 Server starting on http://localhost:5000
📊 Database: MySQL
🤖 AI: Google Gemini 2.0 Flash
📄 Export: PDF/DOCX/PPTX
👤 Author: GuptaSigma
📅 Date: 2025-11-23
================================================================================

💡 Access the app:
   🌐 Local:   http://localhost:5000

💡 Press CTRL+C to stop the server

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.xxx:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```

---

## 🔍 Troubleshooting Quick Reference

| Problem | Quick Fix |
|---------|-----------|
| `python: command not found` | Use `python3` instead or install Python |
| `pip: command not found` | Use `python -m pip` or install pip |
| `(venv)` not showing | Virtual environment not activated |
| `Access denied` MySQL error | Check username/password in `.env` |
| `Can't connect to MySQL` | Start MySQL service |
| `Port 5000 already in use` | Kill existing process or change port |
| `Module not found` | Activate venv and reinstall: `pip install -r requirements.txt` |
| `Invalid API key` | Check `.env` file has correct API key |
| DNS resolution error (Windows) | Add `GRPC_DNS_RESOLVER=native` to `.env` |

---

## 📊 Directory Structure After Setup

```
AI-PPTX/
├── venv/                    # ← Virtual environment (created by you)
│   ├── bin/                 # Scripts (Linux/Mac)
│   ├── Scripts/             # Scripts (Windows)
│   ├── lib/                 # Python libraries
│   └── ...
├── app/                     # Application code
│   ├── __init__.py
│   ├── routes/
│   ├── models/
│   └── ...
├── database/
│   ├── schema.sql          # Database schema
│   └── init_db.sh          # Setup script
├── templates/              # HTML templates
├── css/                    # Stylesheets
├── js/                     # JavaScript files
├── .env                    # ← Environment config (created by you)
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
├── run.py                  # Main entry point
├── README.md               # Project documentation
├── SETUP.md                # Detailed setup guide
└── SETUP-HI.md            # Hindi setup guide
```

---

## 💻 Platform-Specific Notes

### Windows Users

**PowerShell Execution Policy:**
If you get an error activating venv, run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Path Separators:**
Windows uses backslashes `\` instead of forward slashes `/`:
```cmd
cd AI-PPTX\database
venv\Scripts\activate
```

### Linux Users

**Permission Issues:**
Make scripts executable:
```bash
chmod +x database/init_db.sh
chmod +x start.sh
```

**MySQL Socket Error:**
If you get socket errors, specify socket path:
```bash
mysql -u root -p --socket=/var/run/mysqld/mysqld.sock
```

### macOS Users

**Homebrew MySQL:**
Start/stop MySQL with brew:
```bash
brew services start mysql
brew services stop mysql
brew services list
```

**Python Version:**
macOS may have Python 2.7 as `python`, use `python3`:
```bash
python3 -m venv venv
python3 run.py
```

---

## 🚦 Pre-Flight Checklist

Before running `python run.py`, verify:

```bash
# 1. Virtual environment is active
echo $VIRTUAL_ENV  # Should show path to venv

# 2. Dependencies are installed
pip list | grep Flask  # Should show Flask

# 3. .env file exists
ls -la .env  # Should exist

# 4. Database is accessible
mysql -u root -p gamma_ai -e "SELECT 1;"  # Should return 1

# 5. Port 5000 is free
lsof -i:5000  # Should return nothing (Linux/Mac)
netstat -ano | findstr :5000  # Should return nothing (Windows)
```

If all checks pass ✅, you're ready to run!

---

## 📚 Additional Resources

- **Full Setup Guide:** [SETUP.md](SETUP.md)
- **Hindi Guide:** [SETUP-HI.md](SETUP-HI.md)
- **Contributing Guide:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Main Documentation:** [README.md](README.md)

---

## 🎓 Learning Resources

**New to Git?**
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Guide](https://guides.github.com/activities/hello-world/)

**New to Python?**
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pip Package Manager](https://pip.pypa.io/en/stable/)

**New to MySQL?**
- [MySQL Tutorial](https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/)
- [MySQL Workbench](https://www.mysql.com/products/workbench/)

**New to Flask?**
- [Flask Quickstart](https://flask.palletsprojects.com/en/3.0.x/quickstart/)
- [Flask Tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/)

---

**Need help? Check [SETUP.md](SETUP.md) for detailed troubleshooting or open an issue on GitHub!**
