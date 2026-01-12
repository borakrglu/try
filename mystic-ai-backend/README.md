# Mystic.ai Backend API

FastAPI backend for Mystic.ai - AI-powered mystical guidance platform.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15
- Redis 7
- OpenAI API key

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
# Required: DATABASE_URL, REDIS_URL, OPENAI_API_KEY
```

### Database Setup

```bash
# Run migrations
alembic upgrade head

# Create a new migration (after model changes)
alembic revision --autogenerate -m "description"
```

### Run Development Server

```bash
# Option 1: Direct run
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Docker Compose (recommended)
cd ..
docker-compose up

# API will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

## 📁 Project Structure

```
mystic-ai-backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── api/                    # API routes
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── readings.py
│   │       ├── chat.py
│   │       ├── journal.py
│   │       └── payments.py
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── reading.py
│   │   ├── chat.py
│   │   ├── journal.py
│   │   ├── subscription.py
│   │   └── user_stats.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── reading.py
│   │   ├── chat.py
│   │   ├── journal.py
│   │   └── subscription.py
│   ├── services/               # Business logic
│   │   ├── auth_service.py
│   │   ├── reading_service.py
│   │   ├── ai_service.py
│   │   └── ...
│   ├── ai/                     # AI-specific code
│   │   ├── prompts/
│   │   ├── vision.py
│   │   └── embeddings.py
│   ├── workers/                # Celery tasks
│   ├── db/                     # Database utilities
│   │   ├── base.py
│   │   └── session.py
│   └── utils/                  # Utility functions
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── tests/                      # Tests
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🗄 Database Models

### Users
- User accounts (email, password, OAuth)
- Birth date and zodiac sign
- Language preference (EN, TR, DE)

### Readings
- Coffee, Tarot, Palm readings
- AI-generated interpretations
- User ratings and feedback
- Associated images

### Chat
- Conversation history
- 3 personas (Sage, Witch, Astrologer)
- Long-term memory integration

### Journal
- Daily entries
- AI sentiment analysis
- Chakra scores
- Generated affirmations

### Subscriptions
- Free, Weekly, Monthly, Annual tiers
- Usage tracking (readings, chat messages)
- Auto-renewal management

### User Stats (Gamification)
- Karma points
- Badges
- Streaks
- Daily quests

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register with email/password
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/oauth` - OAuth login (Google, Apple)
- `POST /api/v1/auth/refresh` - Refresh access token

### Readings
- `POST /api/v1/readings/coffee` - Create coffee reading
- `POST /api/v1/readings/tarot` - Create tarot reading
- `POST /api/v1/readings/palm` - Create palm reading
- `GET /api/v1/readings/{id}` - Get reading by ID
- `GET /api/v1/readings` - List user's readings

### Chat
- `POST /api/v1/chat/message` - Send chat message
- `GET /api/v1/chat/history` - Get chat history
- `WebSocket /api/v1/chat/stream` - Streaming chat

### Journal
- `POST /api/v1/journal/entries` - Create journal entry
- `GET /api/v1/journal/entries` - List entries
- `GET /api/v1/journal/insights` - Get insights (chakra, mood)
- `GET /api/v1/journal/calendar` - Mood calendar

### Subscriptions
- `POST /api/v1/payments/verify-receipt` - Verify IAP receipt
- `GET /api/v1/payments/status` - Get subscription status
- `POST /api/v1/payments/cancel` - Cancel subscription

## 🤖 AI Integration

### OpenAI GPT-4
- Text generation for readings
- Chat conversations with personas
- Sentiment analysis for journal

### OpenAI GPT-4 Vision
- Coffee cup symbol detection
- Palm line analysis
- Tarot card recognition (physical cards)

### Pinecone
- Vector storage for user reading history
- Semantic search for context-aware responses

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## 📊 Monitoring

- **Sentry**: Error tracking and performance monitoring
- **Logs**: Available in CloudWatch (production) or console (dev)
- **Health Check**: `GET /health`

## 🔐 Security

- JWT authentication with refresh tokens
- Password hashing with bcrypt
- Rate limiting on all endpoints
- CORS configuration
- SQL injection prevention (SQLAlchemy ORM)
- Input validation (Pydantic)

## 📦 Deployment

### Docker

```bash
# Build image
docker build -t mystic-backend .

# Run container
docker run -p 8000:8000 --env-file .env mystic-backend
```

### Production

```bash
# With Gunicorn + Uvicorn workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## 🔄 Database Migrations

```bash
# Create migration after model changes
alembic revision --autogenerate -m "add user stats table"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Check current version
alembic current

# View migration history
alembic history
```

## 📝 Environment Variables

See `.env.example` for all required environment variables.

**Critical:**
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET` - Secret key for JWT tokens
- `OPENAI_API_KEY` - OpenAI API key
- `SENTRY_DSN` - Sentry error tracking DSN

## 👥 Contributing

This is a private project. For questions, contact the repository owner.

## 📄 License

© 2026 Mystic.ai. All rights reserved.
