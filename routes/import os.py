import os
from dotenv import load_dotenv

# Print initialization banner
print("=" * 80)
print("🔧 GAMMA AI - INITIALIZATION")
print("=" * 80)
print(f"📂 Project Root: {os. getcwd()}")

# Load environment variables
env_path = os.path.join(os.getcwd(), '.env')
print(f"🔍 Loading .env from: {env_path}")
load_dotenv(env_path)
print("✅ .env file loaded successfully")

# Show API key (partially hidden)
api_key = os.getenv('GOOGLE_GEMINI_API_KEY', '')
if api_key:
    print(f"✅ GOOGLE_GEMINI_API_KEY:  {api_key[:10]}...  (Hidden)")

# Show database
db_url = os.getenv('DATABASE_URL', 'sqlite: ///gamma_ai.db')
print(f"✅ Database: {db_url}")
print("=" * 80)
print()

try:
    from app import create_app
    
    app = create_app()
    
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)
        
except ImportError as e:
    print(f"❌ Import error:  {e}")
    print("\n💡 Make sure you have these folders:")
    print("   - app/")
    print("   - app/__init__.py")
    print("   - app/routes/")
    print("   - app/models/")
    print("   - app/services/")