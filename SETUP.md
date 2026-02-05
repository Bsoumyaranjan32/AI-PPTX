# 🚀 Quick Setup Guide - Run AI-PPTX on Localhost

This guide provides step-by-step instructions with exact git commands to run the Gamma AI project on your local machine.

**🇮🇳 हिंदी में पढ़ें:** [SETUP-HI.md](SETUP-HI.md) | **⚡ Need just the commands?** [Visual Quick Reference](docs/VISUAL-SETUP-GUIDE.md)

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] **Python 3.9 or higher** installed ([Download](https://www.python.org/downloads/))
- [ ] **MySQL 8.0 or higher** installed ([Download](https://dev.mysql.com/downloads/))
- [ ] **Git** installed ([Download](https://git-scm.com/downloads))
- [ ] **Google Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey))

---

## 🔧 Step-by-Step Setup

### Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
# Clone the repository
git clone https://github.com/Bsoumyaranjan32/AI-PPTX.git

# Navigate into the project directory
cd AI-PPTX

# Verify you're in the correct directory
pwd  # On Windows use: cd
```

### Step 2: Create Python Virtual Environment

**For Windows:**
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) prefix in your terminal
```

**For Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) prefix in your terminal
```

### Step 3: Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

**Note:** Installation may take 2-5 minutes depending on your internet speed.

### Step 4: Setup Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# For Windows (if cp doesn't work):
copy .env.example .env
```

Now edit the `.env` file with your favorite text editor:

```bash
# Use nano, vim, or any text editor
nano .env

# Or on Windows:
notepad .env
```

**Required Configuration in .env:**

```bash
# Database Settings
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=gamma_ai
DB_PORT=3306

# Generate secret keys (run command below and paste results)
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Google Gemini API Key (Get from: https://makersuite.google.com/app/apikey)
GOOGLE_GEMINI_API_KEY=your_gemini_api_key

# OpenRouter API Key (Optional, for DeepSeek)
OPENROUTER_API_KEY=your_openrouter_api_key

# Windows users: Keep this line
GRPC_DNS_RESOLVER=native
```

**Generate secure secret keys:**

```bash
# Run this to generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Run this again to generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Copy and paste each result into your .env file
```

### Step 5: Setup MySQL Database

#### Option 1: Automated Setup (Recommended)

```bash
# Make the script executable (Linux/Mac only)
chmod +x database/init_db.sh

# Run the database setup script
./database/init_db.sh

# For Windows, use Git Bash or follow Option 2
```

#### Option 2: Manual Setup

**Step 5a: Start MySQL**

```bash
# Check if MySQL is running
mysql --version

# If MySQL is not running, start it:
# Windows: Open Services and start MySQL
# Linux: sudo systemctl start mysql
# Mac: brew services start mysql
```

**Step 5b: Create Database**

```bash
# Log into MySQL
mysql -u root -p
# Enter your MySQL password when prompted
```

Once in MySQL shell:

```sql
-- Create the database
CREATE DATABASE gamma_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verify database was created
SHOW DATABASES;

-- Exit MySQL
EXIT;
```

**Step 5c: Import Schema**

```bash
# Import the database schema
mysql -u root -p gamma_ai < database/schema.sql

# Verify tables were created
mysql -u root -p gamma_ai -e "SHOW TABLES;"
```

You should see tables: `users`, `presentations`, `presentation_shares`, `api_usage_log`

### Step 6: Verify Setup

Let's verify everything is configured correctly:

```bash
# Check Python version
python --version

# Check if virtual environment is active (should see venv)
which python  # Windows: where python

# Check if .env file exists
ls -la .env  # Windows: dir .env

# Check database connection
mysql -u root -p gamma_ai -e "SELECT 'Connection successful!' as Status;"
```

### Step 7: Run the Application

```bash
# Make sure virtual environment is active
# You should see (venv) in your terminal

# Start the Flask application
python run.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Step 8: Access the Application

Open your web browser and go to:

```
http://localhost:5000
```

or

```
http://127.0.0.1:5000
```

You should see the Gamma AI homepage! 🎉

---

## 🧪 Test the Application

1. **Create an account:**
   - Click "Sign Up"
   - Enter username, email, and password
   - Click "Register"

2. **Log in:**
   - Use your credentials to log in
   - You should see the dashboard

3. **Create a presentation:**
   - Click "Create New Presentation"
   - Enter a topic (e.g., "Artificial Intelligence")
   - Select number of slides (e.g., 5)
   - Choose a theme (e.g., "dialogue")
   - Click "Generate"
   - Wait 10-30 seconds

4. **Export presentation:**
   - View your generated presentation
   - Click "Export" and choose PDF, DOCX, or PPTX
   - File will download to your computer

---

## 🐛 Common Issues and Solutions

### Issue 1: "python: command not found"

**Solution:**
```bash
# Try using python3 instead
python3 --version

# Or install Python from python.org
```

### Issue 2: "pip: command not found"

**Solution:**
```bash
# Install pip
python -m ensurepip --upgrade

# Or use python3
python3 -m ensurepip --upgrade
```

### Issue 3: "Access denied for user 'root'@'localhost'"

**Solution:**
```bash
# Reset MySQL password or use correct password
# Check your DB_PASSWORD in .env matches MySQL password

# Test connection manually:
mysql -u root -p
```

### Issue 4: "Can't connect to MySQL server"

**Solution:**
```bash
# Check if MySQL is running
# Windows: Check Services
# Linux: sudo systemctl status mysql
# Mac: brew services list

# Start MySQL if not running
# Linux: sudo systemctl start mysql
# Mac: brew services start mysql
```

### Issue 5: "Module not found" errors

**Solution:**
```bash
# Ensure virtual environment is active
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 6: Port 5000 already in use

**Solution:**
```bash
# Find and kill the process using port 5000
# Linux/Mac:
lsof -ti:5000 | xargs kill -9

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Or change port in .env:
FLASK_RUN_PORT=5001
```

### Issue 7: "DNS resolution failed" (Windows)

**Solution:**
Make sure your `.env` file has:
```bash
GRPC_DNS_RESOLVER=native
```

### Issue 8: "Invalid API key" or "API key not set"

**Solution:**
```bash
# Verify your .env file has the correct API key
# Get a new key from: https://makersuite.google.com/app/apikey

# Make sure no extra spaces around the key
GOOGLE_GEMINI_API_KEY=your_key_here
```

### Issue 9: Virtual environment won't activate (Windows)

**Solution:**
```powershell
# If you get execution policy error, run PowerShell as Administrator:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again:
venv\Scripts\activate
```

---

## 📝 Quick Reference Commands

### Daily Development Workflow

```bash
# 1. Navigate to project
cd AI-PPTX

# 2. Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Pull latest changes
git pull origin main

# 4. Install any new dependencies
pip install -r requirements.txt

# 5. Run the application
python run.py

# 6. When done, deactivate virtual environment
deactivate
```

### Git Commands

```bash
# Check current branch
git branch

# Pull latest code
git pull origin main

# Check repository status
git status

# View commit history
git log --oneline -10

# Create a new branch
git checkout -b feature/my-feature

# Switch branches
git checkout main

# Update from remote
git fetch origin
```

### Database Commands

```bash
# Login to MySQL
mysql -u root -p

# Backup database
mysqldump -u root -p gamma_ai > backup.sql

# Restore database
mysql -u root -p gamma_ai < backup.sql

# View tables
mysql -u root -p gamma_ai -e "SHOW TABLES;"

# View users
mysql -u root -p gamma_ai -e "SELECT id, username, email FROM users;"
```

---

## 🎯 Next Steps

After successful setup:

1. **Read the documentation:**
   - Check [README.md](README.md) for features and API documentation
   - Review [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute

2. **Customize your setup:**
   - Configure Google Custom Search for images
   - Set up OpenRouter for DeepSeek AI model
   - Adjust themes and layouts

3. **Deploy to production:**
   - Use Gunicorn for production server
   - Set up HTTPS with SSL certificates
   - Configure production database

---

## 💡 Tips

- **Keep your API keys secure**: Never commit `.env` file to git
- **Update regularly**: Run `git pull` to get latest features
- **Backup your data**: Export presentations regularly
- **Use virtual environment**: Always activate venv before running
- **Check logs**: Review `pptx_service.log` for errors

---

## 📞 Need Help?

If you're still stuck:

1. **Check existing issues**: [GitHub Issues](https://github.com/Bsoumyaranjan32/AI-PPTX/issues)
2. **Create new issue**: Describe your problem with error messages
3. **Join discussions**: [GitHub Discussions](https://github.com/Bsoumyaranjan32/AI-PPTX/discussions)

---

## ✅ Verification Checklist

Before asking for help, verify:

- [ ] Python 3.9+ is installed: `python --version`
- [ ] MySQL is running: `mysql --version`
- [ ] Virtual environment is active: `(venv)` prefix visible
- [ ] Dependencies installed: `pip list | grep Flask`
- [ ] .env file exists and is configured: `cat .env`
- [ ] Database created: `mysql -u root -p -e "SHOW DATABASES;"`
- [ ] Tables exist: `mysql -u root -p gamma_ai -e "SHOW TABLES;"`
- [ ] API key is set: Check `.env` file
- [ ] Port 5000 is free: `lsof -i:5000` (should be empty)

---

**Happy Coding! 🚀**

If you found this guide helpful, please ⭐ star the repository!
