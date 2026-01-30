-- ============================================
-- Gamma AI Database Schema
-- MySQL 8.0+
-- Author: GuptaSigma
-- Date: 2026-01-30
-- ============================================

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS gamma_ai 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE gamma_ai;

-- ============================================
-- USERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    profile_image VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- PRESENTATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS presentations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content JSON NOT NULL,
    theme VARCHAR(50) DEFAULT 'dialogue',
    slides_count INT DEFAULT 8,
    language VARCHAR(50) DEFAULT 'English',
    ai_model VARCHAR(50) DEFAULT 'gemini',
    is_public BOOLEAN DEFAULT FALSE,
    views INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_theme (theme),
    INDEX idx_is_public (is_public),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- PRESENTATION SHARES TABLE (Optional)
-- ============================================
CREATE TABLE IF NOT EXISTS presentation_shares (
    id INT AUTO_INCREMENT PRIMARY KEY,
    presentation_id INT NOT NULL,
    share_token VARCHAR(100) UNIQUE NOT NULL,
    expires_at TIMESTAMP NULL,
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (presentation_id) REFERENCES presentations(id) ON DELETE CASCADE,
    
    INDEX idx_share_token (share_token),
    INDEX idx_presentation_id (presentation_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- API USAGE LOG TABLE (Optional)
-- ============================================
CREATE TABLE IF NOT EXISTS api_usage_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    endpoint VARCHAR(100) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INT,
    response_time_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_endpoint (endpoint),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- ADMIN USER (Optional - Comment out if not needed)
-- ============================================
-- Default password: 'admin123' (change after first login)
-- Password is bcrypt hashed
INSERT INTO users (username, email, password, full_name, is_admin) 
VALUES (
    'admin',
    'admin@gamma-ai.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5agyWw3MfXQUm',
    'Admin User',
    TRUE
) ON DUPLICATE KEY UPDATE username=username;

-- ============================================
-- VIEWS FOR ANALYTICS (Optional)
-- ============================================

-- User statistics view
CREATE OR REPLACE VIEW user_statistics AS
SELECT 
    u.id,
    u.username,
    u.email,
    COUNT(p.id) as total_presentations,
    SUM(p.views) as total_views,
    MAX(p.created_at) as last_presentation_date,
    u.created_at as user_since
FROM users u
LEFT JOIN presentations p ON u.id = p.user_id
GROUP BY u.id;

-- Popular presentations view
CREATE OR REPLACE VIEW popular_presentations AS
SELECT 
    p.id,
    p.title,
    p.theme,
    p.views,
    u.username,
    p.created_at
FROM presentations p
JOIN users u ON p.user_id = u.id
WHERE p.is_public = TRUE
ORDER BY p.views DESC
LIMIT 100;

-- ============================================
-- SAMPLE DATA (Optional - Comment out for production)
-- ============================================

-- Sample user: username=testuser, password=test123
-- INSERT INTO users (username, email, password, full_name) 
-- VALUES (
--     'testuser',
--     'test@example.com',
--     '$2b$12$7.XQHQvLqT7Z0wM3nxI5L.bwVz7J8.1.QH2Z9XQC0wM3nxI5L.bwV',
--     'Test User'
-- );

-- ============================================
-- SUCCESS MESSAGE
-- ============================================
SELECT 'Database schema created successfully!' AS Status;
SELECT COUNT(*) AS user_count FROM users;
SELECT COUNT(*) AS presentation_count FROM presentations;
