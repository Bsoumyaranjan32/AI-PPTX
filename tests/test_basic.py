"""
Basic tests for Flask application
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_app_import():
    """Test that the app module can be imported"""
    try:
        from app import create_app
        assert create_app is not None
    except ImportError as e:
        assert False, f"Failed to import app: {e}"


def test_app_creation():
    """Test that the Flask app can be created"""
    try:
        from app import create_app
        app = create_app()
        assert app is not None
        assert app.config is not None
    except Exception as e:
        assert False, f"Failed to create app: {e}"


def test_health_endpoint():
    """Test the health check endpoint"""
    from app import create_app
    
    app = create_app()
    client = app.test_client()
    
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'service' in data


def test_index_route():
    """Test the index route"""
    from app import create_app
    
    app = create_app()
    client = app.test_client()
    
    response = client.get('/')
    assert response.status_code == 200


if __name__ == '__main__':
    # Run tests manually
    print("Running basic tests...")
    
    try:
        test_app_import()
        print("✅ App import test passed")
    except AssertionError as e:
        print(f"❌ App import test failed: {e}")
    
    try:
        test_app_creation()
        print("✅ App creation test passed")
    except AssertionError as e:
        print(f"❌ App creation test failed: {e}")
    
    try:
        test_health_endpoint()
        print("✅ Health endpoint test passed")
    except AssertionError as e:
        print(f"❌ Health endpoint test failed: {e}")
    
    try:
        test_index_route()
        print("✅ Index route test passed")
    except AssertionError as e:
        print(f"❌ Index route test failed: {e}")
    
    print("\nAll basic tests completed!")
