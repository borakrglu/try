#!/bin/bash

echo "🌟 Starting Mystic.ai Backend on Replit..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements-replit.txt

# Run database migrations (with SQLite)
echo "🗄️  Running database migrations..."
export DATABASE_URL="sqlite:///./mystic.db"
alembic upgrade head

# Start the server
echo "🚀 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
