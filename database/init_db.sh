#!/bin/bash
# Gamma AI - Database Initialization Script

echo "==========================================="
echo "🗄️  Gamma AI - Database Setup"
echo "==========================================="

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_USER="${DB_USER:-root}"
DB_NAME="${DB_NAME:-gamma_ai}"

echo ""
echo "Database Configuration:"
echo "  Host: $DB_HOST"
echo "  User: $DB_USER"
echo "  Database: $DB_NAME"
echo ""

# Check if MySQL is available
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL client not found. Please install MySQL first."
    exit 1
fi

echo "✅ MySQL client found"
echo ""

# Prompt for password
read -sp "Enter MySQL password for user '$DB_USER': " DB_PASSWORD
echo ""
echo ""

# Test connection
echo "🔄 Testing database connection..."
if mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1;" &> /dev/null; then
    echo "✅ Database connection successful"
else
    echo "❌ Database connection failed. Please check your credentials."
    exit 1
fi

echo ""
echo "🔄 Creating database schema..."

# Execute schema
if mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" < database/schema.sql; then
    echo "✅ Database schema created successfully!"
    echo ""
    echo "You can now start the application with: python run.py"
else
    echo "❌ Failed to create database schema"
    exit 1
fi
