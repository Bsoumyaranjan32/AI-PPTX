"""
Gamma AI - Flask Application Factory
Complete Version with MySQL Database
Author: GuptaSigma | Date: 2026-01-30
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config=None):
    """Create and configure the Flask application.
    
    Args:
        config (dict, optional): Configuration dictionary to override defaults
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static',
        static_url_path='/static'
    )
    
    # ============================================
    # CONFIGURATION
    # ============================================
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-in-production')
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:"
        f"{os.getenv('DB_PASSWORD', '')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME', 'gamma_ai')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    
    # File upload configuration
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')
    
    # CORS configuration
    app.config['CORS_HEADERS'] = 'Content-Type'
    
    # JWT configuration
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    # Override with custom config if provided
    if config:
        app.config.update(config)
    
    # ============================================
    # INITIALIZE EXTENSIONS
    # ============================================
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    print("✅ Flask extensions initialized")
    
    # ============================================
    # REGISTER BLUEPRINTS
    # ============================================
    try:
        # Import blueprints from root-level routes directory
        import sys
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from routes.main import main_bp
        from routes.auth import auth_bp
        from routes.presentations import presentations_bp
        
        # Register blueprints
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(presentations_bp, url_prefix='/api/presentations')
        
        print("✅ Blueprints registered:")
        print("   - Main routes (frontend pages)")
        print("   - Auth API (/api/auth)")
        print("   - Presentations API (/api/presentations)")
        
    except ImportError as e:
        print(f"⚠️  Blueprint import error: {e}")
        print("   Some routes may not be available")
    
    # ============================================
    # ERROR HANDLERS
    # ============================================
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return {
            "success": False,
            "error": "Resource not found",
            "message": str(error)
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return {
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }, 500
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handle file too large errors"""
        return {
            "success": False,
            "error": "File too large",
            "message": "Maximum file size is 16MB"
        }, 413
    
    # ============================================
    # HEALTH CHECK ROUTE
    # ============================================
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "Gamma AI",
            "version": "1.0.0"
        }, 200
    
    return app
