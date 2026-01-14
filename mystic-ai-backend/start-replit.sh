#!/bin/bash

echo "🌟 Starting Mystic.ai Backend on Replit..."

# Install dependencies
echo "📦 Installing dependencies..."
python3 -m pip install -q -r requirements-replit.txt

# Start the server (skip migrations for now - will create tables automatically)
echo "🚀 Starting FastAPI server..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
