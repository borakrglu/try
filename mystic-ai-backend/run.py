"""
Simple runner for Replit
"""
import uvicorn
import os

# Set environment defaults if not in Replit Secrets
os.environ.setdefault('DATABASE_URL', 'sqlite:///./mystic.db')
os.environ.setdefault('APP_ENV', 'production')
os.environ.setdefault('DEBUG', 'false')
os.environ.setdefault('ALLOWED_ORIGINS', '*')
os.environ.setdefault('SECRET_KEY', 'mystic_ai_secret_key_2024')

if __name__ == "__main__":
    print("🌟 Starting Mystic.ai Backend...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
