# 🎨 Gamma AI - AI-Powered Presentation Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Create stunning presentations powered by Google Gemini 2.5 Flash and DeepSeek AI**

[🚀 Setup Guide](SETUP.md) • [Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Configuration](#️-configuration) • [Usage](#-usage) • [API](#-api-endpoints) • [Troubleshooting](#-troubleshooting)

</div>

---

## 📋 Overview

Gamma AI is a powerful web application that uses artificial intelligence to generate professional presentations automatically. Simply provide a topic, and the AI will create a complete presentation with relevant content, images, and layouts.

### ✨ Features

- 🤖 **Dual AI Models**: Powered by Google Gemini 2.5 Flash and DeepSeek R1
- 🎨 **Multiple Themes**: Choose from 7+ professional themes (Dialogue, Alien, Wine, Snowball, etc.)
- 📊 **Smart Layouts**: 8+ different slide layouts including centered, split, grid, and roadmap views
- 🖼️ **Automatic Images**: Integration with Google Custom Search for relevant images
- 📥 **Multiple Export Formats**: Export to PDF, DOCX, and PPTX
- 🔐 **User Authentication**: Secure JWT-based authentication with bcrypt password hashing
- 💾 **MySQL Database**: Persistent storage for users and presentations
- 🌍 **Multi-language Support**: Generate presentations in multiple languages
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

---

## 🚀 Quick Start

> **👉 New to the project? Check out our [Detailed Setup Guide](SETUP.md) with step-by-step instructions and troubleshooting!**
> 
> **🇮🇳 हिंदी में सेटअप गाइड:** [SETUP-HI.md](SETUP-HI.md)

```bash
# Clone the repository
git clone https://github.com/Bsoumyaranjan32/AI-PPTX.git
cd AI-PPTX

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Initialize MySQL database
mysql -u root -p < database/schema.sql

# Run the application
python run.py
```

Visit **http://localhost:5000** in your browser!

**Need detailed instructions?** See [SETUP.md](SETUP.md) for comprehensive setup guide with git commands and troubleshooting.

---

## 📦 Installation

### Prerequisites

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **MySQL 8.0+** - [Download](https://dev.mysql.com/downloads/)
- **pip** - Python package installer

### Step-by-Step Installation

#### 1. Clone and Setup

```bash
git clone https://github.com/Bsoumyaranjan32/AI-PPTX.git
cd AI-PPTX
```

#### 2. Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Database Setup

**Create Database:**
```sql
CREATE DATABASE gamma_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Import Schema:**
```bash
mysql -u root -p gamma_ai < database/schema.sql
```

Or manually create tables:
```sql
USE gamma_ai;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE presentations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content JSON NOT NULL,
    theme VARCHAR(50) DEFAULT 'dialogue',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### 5. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your actual values (see [Configuration](#️-configuration) section).

---

## ⚙️ Configuration

### Environment Variables

Edit the `.env` file with your credentials:

```bash
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=gamma_ai
DB_PORT=3306

# Flask Secrets (Generate with: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Google Gemini API Key (Get from: https://makersuite.google.com/app/apikey)
GOOGLE_GEMINI_API_KEY=your_gemini_api_key

# OpenRouter API Key (Get from: https://openrouter.ai/keys)
OPENROUTER_API_KEY=your_openrouter_api_key

# Google Custom Search (Optional - for images)
GOOGLE_API_KEY=your_google_search_api_key
GOOGLE_CX_ID=your_custom_search_engine_id

# Network Fix for Windows
GRPC_DNS_RESOLVER=native
```

### Getting API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy and paste into `.env`

#### OpenRouter API Key (Optional)
1. Visit [OpenRouter](https://openrouter.ai/keys)
2. Sign up or log in
3. Generate a new API key
4. Copy and paste into `.env`

#### Google Custom Search (Optional)
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Custom Search API
3. Create credentials (API key)
4. Set up a [Custom Search Engine](https://programmablesearchengine.google.com/)
5. Copy API key and Search Engine ID to `.env`

---

## 🎯 Usage

### Starting the Server

```bash
python run.py
```

The server will start on **http://localhost:5000**

### Creating Your First Presentation

1. **Sign Up**: Create a new account at http://localhost:5000/signup
2. **Log In**: Access your dashboard
3. **New Presentation**: Click "Create New Presentation"
4. **Configure**:
   - Enter your topic (e.g., "Climate Change Solutions")
   - Select number of slides (3-20)
   - Choose theme
   - Select AI model (Gemini or DeepSeek)
   - Set text amount (minimal/concise/detailed)
5. **Generate**: Click "Generate" and wait 10-30 seconds
6. **Edit & Export**: Review, edit, and export to PDF/DOCX/PPTX

### Themes Available

- **Dialogue** - Clean white professional theme
- **Alien** - Dark blue futuristic theme
- **Wine** - Elegant burgundy theme
- **Snowball** - Light blue fresh theme
- **Petrol** - Modern grey theme
- **Piano** - Black and white contrast theme
- **Business** - Professional blue gradient theme

---

## 🔌 API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}
```

### Presentations

#### Generate Presentation
```http
POST /api/presentations/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "prompt": "Artificial Intelligence in Healthcare",
  "slides_count": 8,
  "language": "English",
  "theme": "dialogue",
  "text_amount": "concise",
  "ai_model": "gemini"
}
```

#### Get All Presentations
```http
GET /api/presentations
Authorization: Bearer <token>
```

#### Get Specific Presentation
```http
GET /api/presentations/<id>
Authorization: Bearer <token>
```

#### Update Presentation
```http
PUT /api/presentations/<id>
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": {...}
}
```

#### Delete Presentation
```http
DELETE /api/presentations/<id>
Authorization: Bearer <token>
```

#### Export Presentation
```http
GET /api/presentations/<id>/export/<format>
Authorization: Bearer <token>

# format: pdf, docx, or pptx
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. **DNS Resolution Failed Error (Windows)**
**Solution:** The `.env` file should have `GRPC_DNS_RESOLVER=native`

#### 2. **Database Connection Error**
```
Error: Can't connect to MySQL server
```
**Solution:**
- Verify MySQL is running: `mysql --version`
- Check credentials in `.env`
- Ensure database exists: `CREATE DATABASE gamma_ai;`

#### 3. **Missing API Key Error**
```
WARNING: GOOGLE_GEMINI_API_KEY not set
```
**Solution:** Add your API key to `.env` file

#### 4. **Import Error: No module named 'app'**
**Solution:** Make sure you're in the project root directory and run:
```bash
pip install -r requirements.txt
```

#### 5. **Port Already in Use**
```
OSError: [Errno 48] Address already in use
```
**Solution:** Kill the process using port 5000:
```bash
# Linux/macOS
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Debug Mode

To enable detailed error messages, set in `.env`:
```bash
FLASK_ENV=development
```

### Logs

Check application logs:
- **Console output**: Real-time logs in terminal
- **pptx_service.log**: PPTX generation logs

---

## 🏗️ Project Structure

```
AI-PPTX/
├── models/              # Database models
│   ├── user.py         # User model
│   ├── presentation.py # Presentation model
│   └── database.py     # Database configuration
├── routes/             # API routes
│   ├── auth.py        # Authentication endpoints
│   ├── main.py        # Frontend routes
│   └── presentations.py # Presentation CRUD
├── services/          # Business logic
│   ├── ai_service.py  # AI generation service
│   └── pptx_service.py # Export service
├── templates/         # HTML templates
│   ├── index.html     # Landing page
│   ├── dashboard.html # User dashboard
│   ├── editor.html    # Presentation editor
│   └── presentation.html # Viewer
├── css/               # Stylesheets
│   └── style.css
├── js/                # JavaScript
│   ├── api.js        # API helper
│   ├── auth.js       # Authentication
│   └── editor.js     # Editor logic
├── .env.example       # Environment template
├── .gitignore        # Git ignore rules
├── requirements.txt   # Python dependencies
├── run.py            # Application entry point
└── README.md         # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**GuptaSigma**
- GitHub: [@Bsoumyaranjan32](https://github.com/Bsoumyaranjan32)

---

## 🙏 Acknowledgments

- **Google Gemini** - AI model for content generation
- **DeepSeek** - Alternative AI model via OpenRouter
- **Flask** - Web framework
- **python-pptx** - PowerPoint generation
- **ReportLab** - PDF generation

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search [existing issues](https://github.com/Bsoumyaranjan32/AI-PPTX/issues)
3. Create a [new issue](https://github.com/Bsoumyaranjan32/AI-PPTX/issues/new)

---

<div align="center">

**Made with ❤️ by GuptaSigma**

⭐ Star this repository if you find it helpful!

</div>