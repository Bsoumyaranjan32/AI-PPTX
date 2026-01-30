"""
Authentication Routes - Signup, Login, JWT
Author: GuptaSigma
Date: 2025-11-23
"""

from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
import os
from app.models.database import execute_query

auth_bp = Blueprint('auth', __name__)

print("✅ auth_bp Blueprint created")

# =====================================================================
# JWT CONFIG
# =====================================================================

JWT_SECRET = os.getenv('JWT_SECRET_KEY', 'gamma-ai-jwt-secret-key-production-2025')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


# =====================================================================
# PASSWORD HELPERS
# =====================================================================

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


# =====================================================================
# TOKEN HELPERS
# =====================================================================

def generate_token(user_id: int, email: str, name: str) -> str:
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'email': email,
        'name': name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception:
        return None


# =====================================================================
# ROUTES
# =====================================================================

@auth_bp.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    """Register new user"""
    if request.method == 'OPTIONS':
        return '', 204

    try:
        print("📝 Signup request")
        data = request.get_json()

        # Basic validation
        if not data or not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({'success': False, 'error': 'Name, email, and password required'}), 400

        email = data['email'].lower().strip()
        password = data['password']
        name = data['name'].strip()

        print(f"   Name: {name}, Email: {email}")

        # Email format check
        if '@' not in email or '.' not in email:
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400

        # Password length check
        if len(password) < 6:
            return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400

        # Check if user already exists
        existing_user = execute_query(
            "SELECT id FROM users WHERE email = %s",
            (email,),
            fetch=True
        )

        if existing_user:
            print(f"❌ Email exists: {email}")
            return jsonify({'success': False, 'error': 'Email already registered'}), 409

        # Hash password
        hashed_password = hash_password(password)

        # Insert user (ONLY name, email, password – matches your table)
        user_id = execute_query(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )

        # Generate token
        token = generate_token(user_id, email, name)

        print(f"✅ User registered: {email} (ID: {user_id})")

        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'token': token,
            'user': {'id': user_id, 'name': name, 'email': email}
        }), 201

    except Exception as e:
        print(f"❌ Signup error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': 'Registration failed'}), 500


@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """Login user"""
    if request.method == 'OPTIONS':
        return '', 204

    try:
        print("🔐 Login request")
        data = request.get_json()

        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'error': 'Email and password required'}), 400

        email = data['email'].lower().strip()
        password = data['password']

        print(f"   Email: {email}")

        # Fetch user with password hash
        users = execute_query(
            "SELECT id, name, email, password FROM users WHERE email = %s",
            (email,),
            fetch=True
        )

        if not users:
            print(f"❌ User not found: {email}")
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401

        user = users[0]

        # Verify password
        if not verify_password(password, user['password']):
            print(f"❌ Invalid password: {email}")
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401

        token = generate_token(user['id'], user['email'], user['name'])

        print(f"✅ User logged in: {email}")

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': {'id': user['id'], 'name': user['name'], 'email': user['email']}
        }), 200

    except Exception as e:
        print(f"❌ Login error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': 'Login failed'}), 500


@auth_bp.route('/verify', methods=['GET', 'OPTIONS'])
def verify_route():
    """Verify JWT token"""
    if request.method == 'OPTIONS':
        return '', 204

    try:
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'No token provided'}), 401

        token = auth_header.split(' ')[1]
        payload = verify_token(token)

        if not payload:
            return jsonify({'success': False, 'error': 'Invalid or expired token'}), 401

        return jsonify({
            'success': True,
            'user': {
                'id': payload['user_id'],
                'email': payload['email'],
                'name': payload['name']
            }
        }), 200

    except Exception as e:
        print(f"❌ Verify error: {e}")
        return jsonify({'success': False, 'error': 'Token verification failed'}), 500


@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    """Logout user"""
    if request.method == 'OPTIONS':
        return '', 204

    # For JWT-based stateless auth, logout is client-side (delete token)
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200


print("✅ Auth routes: /signup, /login, /verify, /logout")