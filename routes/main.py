"""
Main Routes - Frontend Pages (ULTRA PRODUCTION v2.0)
Complete with Error Handling, Logging, and Multiple Route Aliases
Author: GuptaSigma | Date: 2026-01-15
"""

from flask import Blueprint, render_template, send_from_directory, jsonify, redirect, url_for
import os
import traceback
from datetime import datetime

main_bp = Blueprint('main', __name__)

print("=" * 70)
print("✅ MAIN BLUEPRINT INITIALIZED")
print("=" * 70)

# ==========================================
# LOGGING HELPER
# ==========================================
def log_request(route_name, template_name=None):
    """Log incoming requests with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if template_name:
        print(f"📄 [{timestamp}] {route_name} → Serving {template_name}")
    else:
        print(f"🔀 [{timestamp}] {route_name} → Redirect")

# ==========================================
# ROOT & AUTH ROUTES
# ==========================================
@main_bp.route('/')
def index():
    """Landing page - Login/Signup"""
    try:
        log_request("ROOT", "index.html")
        return render_template('index.html')
    except Exception as e: 
        print(f"❌ Error serving index.html: {e}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error":  str(e),
            "file":  "index.html",
            "timestamp": datetime.now().isoformat()
        }), 500

@main_bp.route('/login')
def login():
    """Login page"""
    try:
        log_request("LOGIN", "index.html")
        return render_template('index.html')
    except Exception as e:
        print(f"❌ Error:  {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/signup')
def signup():
    """Signup page"""
    try:
        log_request("SIGNUP", "index.html")
        return render_template('index.html')
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error":  str(e)}), 500

@main_bp.route('/logout')
def logout():
    """Logout redirect"""
    log_request("LOGOUT")
    return redirect(url_for('main.index'))

# ==========================================
# DASHBOARD
# ==========================================
@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page"""
    try:
        log_request("DASHBOARD", "dashboard.html")
        return render_template('dashboard.html')
    except Exception as e:
        print(f"❌ Dashboard Error: {e}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "file": "dashboard.html",
            "timestamp": datetime.now().isoformat()
        }), 500

# ==========================================
# EDITOR/CREATOR
# ==========================================
@main_bp.route('/editor')
@main_bp.route('/create')
@main_bp.route('/new')
@main_bp.route('/generator')  # ✅ FIXED: Added this route to prevent 404
def editor():
    """Editor/Creation page (multiple aliases)"""
    try:
        log_request("EDITOR", "editor.html")
        return render_template('editor.html')
    except Exception as e:
        print(f"❌ Editor Error: {e}")
        traceback.print_exc()
        return jsonify({
            "success":  False,
            "error": str(e),
            "file":  "editor.html",
            "timestamp": datetime.now().isoformat()
        }), 500

# ==========================================
# PRESENTATION VIEWER (Multiple URL Patterns)
# ==========================================
@main_bp.route('/presentations/<int:presentation_id>')
@main_bp.route('/presentation/<int:presentation_id>')
@main_bp.route('/view/<int:presentation_id>')
def view_presentation(presentation_id):
    """View presentation (primary route)"""
    try:
        log_request(f"VIEW_PRESENTATION (ID: {presentation_id})", "presentation.html")
        return render_template('presentation.html')
    except Exception as e: 
        print(f"❌ Error loading presentation {presentation_id}: {e}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "file": "presentation.html",
            "presentation_id": presentation_id,
            "timestamp": datetime.now().isoformat()
        }), 500

@main_bp.route('/editor/<int:presentation_id>')
@main_bp.route('/edit/<int:presentation_id>')
def editor_view(presentation_id):
    """Editor view (alias for presentations)"""
    try:
        log_request(f"EDITOR_VIEW (ID:  {presentation_id})", "presentation.html")
        return render_template('presentation.html')
    except Exception as e:
        print(f"❌ Error loading editor for {presentation_id}: {e}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "presentation_id": presentation_id,
            "timestamp": datetime.now().isoformat()
        }), 500

# ==========================================
# STATIC FILES
# ==========================================
@main_bp.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    try:
        return send_from_directory('../static', filename)
    except FileNotFoundError:
        print(f"⚠️ Static file not found: {filename}")
        return jsonify({
            "error": "File not found",
            "filename": filename
        }), 404
    except Exception as e:
        print(f"❌ Static file error: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    try:
        return send_from_directory('../static', 'favicon.ico')
    except: 
        return '', 204

# ==========================================
# ERROR HANDLERS
# ==========================================
@main_bp.app_errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    print(f"❌ 404 Error: {error}")
    return jsonify({
        "error": "Page not found",
        "status": 404,
        "message": "The requested URL was not found on the server.",
        "timestamp": datetime.now().isoformat()
    }), 404

@main_bp.app_errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    print(f"❌ 500 Error:  {error}")
    traceback.print_exc()
    return jsonify({
        "error": "Internal server error",
        "status": 500,
        "message": "An unexpected error occurred.",
        "timestamp": datetime.now().isoformat()
    }), 500

# ==========================================
# HEALTH CHECK
# ==========================================
@main_bp.route('/health')
@main_bp.route('/ping')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status":  "healthy",
        "service": "Gamma Pro",
        "timestamp": datetime.now().isoformat(),
        "routes": {
            "root": "/",
            "dashboard": "/dashboard",
            "editor": "/editor",
            "presentations": "/presentations/<id>"
        }
    }), 200

# ==========================================
# STARTUP SUMMARY
# ==========================================
print("\n✅ MAIN ROUTES REGISTERED:")
print("   🏠 GET  /                      → index.html (Login/Signup)")
print("   🔐 GET  /login                 → index.html")
print("   📝 GET  /signup                → index.html")
print("   📊 GET  /dashboard             → dashboard.html")
print("   ✨ GET  /editor                → editor.html")
print("   🎨 GET  /create                → editor.html (alias)")
print("   ⚙️ GET  /generator             → editor.html (FIXED)")
print("   📄 GET  /presentations/<id>    → presentation.html")
print("   📝 GET  /editor/<id>           → presentation.html (alias)")
print("   🔧 GET  /health                → Health check")
print("=" * 70)
print()