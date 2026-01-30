#!/bin/bash
# Gamma AI - Development Startup Script

echo "==========================================="
echo "🎨 Gamma AI - Starting Development Server"
echo "==========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your API keys!"
    echo ""
    exit 1
fi

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Run the application
echo ""
echo "🚀 Starting Flask server..."
python run.py
