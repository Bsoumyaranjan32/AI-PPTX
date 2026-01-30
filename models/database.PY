"""
Database Connection and Initialization
MySQL Connection Pool with Error Handling
Author: GuptaSigma | Date: 2025-11-23
"""

import mysql.connector
from mysql.connector import pooling
from flask import current_app
import os

# ============================================
# DATABASE CONNECTION POOL
# ============================================
connection_pool = None

def get_db_config():
    """Get database configuration"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'gamma_ai'),
        'pool_name': 'gamma_pool',
        'pool_size': 5,
        'pool_reset_session': True,
        'autocommit': False
    }

def get_connection():
    """Get database connection from pool"""
    global connection_pool
    
    if connection_pool is None:
        try:
            config = get_db_config()
            connection_pool = pooling.MySQLConnectionPool(**config)
            print("✅ Database connection pool created")
        except mysql.connector.Error as err:
            print(f"❌ Error creating connection pool: {err}")
            raise
    
    try:
        return connection_pool.get_connection()
    except mysql.connector.Error as err:
        print(f"❌ Error getting connection: {err}")
        raise

def init_db():
    """Initialize database tables"""
    
    print("\n" + "="*60)
    print("📊 INITIALIZING DATABASE")
    print("="*60)
    
    conn = None
    cursor = None
    
    try:
        # Get database config
        config = get_db_config()
        print(f"📍 Host: {config['host']}")
        print(f"📍 Database: {config['database']}")
        
        # Connect to MySQL server (without database)
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password']
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
        cursor.execute(f"USE {config['database']}")
        print(f"✅ Database '{config['database']}' ready")
        
        # ============================================
        # CREATE USERS TABLE
        # ============================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_email (email),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Table 'users' ready")
        
        # ============================================
        # CREATE PRESENTATIONS TABLE
        # ============================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS presentations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                title VARCHAR(500) NOT NULL,
                prompt TEXT NOT NULL,
                slides_count INT DEFAULT 10,
                output_type VARCHAR(50) DEFAULT 'presentation',
                style VARCHAR(50) DEFAULT 'business',
                theme VARCHAR(50) DEFAULT 'alien',
                language VARCHAR(10) DEFAULT 'en-uk',
                image_style VARCHAR(50) DEFAULT 'illustration',
                text_amount VARCHAR(20) DEFAULT 'moderate',
                ai_model VARCHAR(100) DEFAULT 'gemini-2.0-flash',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id),
                INDEX idx_created_at (created_at),
                INDEX idx_output_type (output_type)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Table 'presentations' ready")
        
        # ============================================
        # CREATE SLIDES TABLE
        # ============================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS slides (
                id INT AUTO_INCREMENT PRIMARY KEY,
                presentation_id INT NOT NULL,
                slide_number INT NOT NULL,
                title VARCHAR(500),
                content TEXT,
                layout JSON,
                image_url VARCHAR(1000),
                background VARCHAR(500),
                animation VARCHAR(50),
                notes TEXT,
                metadata JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (presentation_id) REFERENCES presentations(id) ON DELETE CASCADE,
                INDEX idx_presentation_id (presentation_id),
                INDEX idx_slide_number (slide_number)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Table 'slides' ready")
        
        conn.commit()
        print("="*60)
        print("✅ Database tables created successfully!")
        print("="*60 + "\n")
        
    except mysql.connector.Error as err:
        print(f"\n❌ Database error: {err}")
        if conn:
            conn.rollback()
        raise
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def execute_query(query, params=None, fetch=False):
    """Execute database query with error handling"""
    
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return cursor.lastrowid
    
    except mysql.connector.Error as err:
        print(f"❌ Query error: {err}")
        if conn:
            conn.rollback()
        raise
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()