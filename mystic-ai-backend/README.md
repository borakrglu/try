# Mystic.ai Backend API

AI-powered mystical guidance platform backend built with FastAPI, PostgreSQL, and OpenAI.

## 🌟 Features

### Core Features
- **AI-Powered Readings** - Coffee cup, Tarot, Palm reading, and Astrology interpretations
- **Intelligent Chat System** - 3 AI personas (Sage, Witch, Astrologer) with long-term memory
- **Journal System** - AI sentiment analysis with 7-chakra scoring and personalized affirmations
- **Moon Phase & Astrology** - Real-time lunar calculations and astrological insights
- **Push Notifications** - Firebase Cloud Messaging with user preferences and quiet hours
- **Subscription Management** - RevenueCat integration for iOS/Android/Web payments
- **Admin Panel** - User management, system statistics, and content moderation
- **Analytics Dashboard** - Time-series data, cohort analysis, revenue forecasting

### Technical Features
- JWT authentication with refresh tokens
- Role-based access control (Admin/User)
- Rate limiting and security middleware
- Image upload to AWS S3
- Vector database integration (Pinecone)
- Webhook handling for payment events
- Comprehensive error tracking (Sentry)
- Data export (CSV/JSON)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (recommended)
- OpenAI API key

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd mystic-ai-backend

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f api

# Access the API
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# Database UI: http://localhost:8080 (Adminer)
```

### Option 2: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and configure database + API keys
nano .env

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

### Interactive Docs

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints Summary

#### Authentication (`/api/v1/auth`)
- `POST /register` - Register new user
- `POST /login` - Login with email/password
- `POST /google-login` - Login with Google
- `POST /refresh` - Refresh access token

#### Readings (`/api/v1/readings`)
- `POST /coffee` - Coffee cup reading
- `POST /tarot` - Tarot card reading
- `POST /palm` - Palm reading with image
- `POST /astrology` - Astrological reading
- `GET /` - Get user's reading history
- `GET /{reading_id}` - Get specific reading

#### Chat (`/api/v1/chat`)
- `POST /message` - Send message to AI persona
- `GET /history` - Get chat history
- `DELETE /history` - Clear chat history
- `GET /personas` - List available personas
- `GET /memory-stats` - Get memory statistics

#### Journal (`/api/v1/journal`)
- `POST /entries` - Create journal entry with AI analysis
- `GET /entries` - Get journal entries
- `GET /entries/{id}` - Get specific entry
- `PUT /entries/{id}` - Update entry
- `DELETE /entries/{id}` - Delete entry
- `GET /insights` - Get 7-day insights and trends
- `GET /calendar/{year}/{month}` - Get calendar view
- `GET /affirmation` - Get daily affirmation

#### Astrology (`/api/v1/astrology`)
- `GET /moon/current` - Current moon phase
- `GET /moon/phase` - Moon phase for specific date
- `GET /moon/calendar` - Monthly moon calendar
- `GET /transits` - Current planetary transits
- `GET /zodiac/compatibility` - Zodiac compatibility
- `GET /moon/ritual-guide` - Ritual guide for current phase

#### Notifications (`/api/v1/notifications`)
- `POST /tokens` - Register device for notifications
- `GET /tokens` - Get registered devices
- `DELETE /tokens/{token}` - Unregister device
- `GET /preferences` - Get notification preferences
- `PUT /preferences` - Update notification preferences
- `POST /send` - Send custom notification (admin)
- `GET /history` - Get notification history
- `POST /history/{id}/opened` - Mark as opened
- `GET /status` - Get notification system status

#### Admin (`/api/v1/admin`) 🔐
- `GET /users` - List users with filters
- `GET /users/{user_id}` - Get user details
- `POST /users/{user_id}/ban` - Ban user
- `POST /users/{user_id}/unban` - Unban user
- `DELETE /users/{user_id}` - Delete user
- `POST /users/{user_id}/promote` - Promote to admin
- `GET /stats` - System statistics
- `GET /stats/revenue` - Revenue metrics
- `GET /stats/growth` - Growth metrics
- `GET /moderation/flagged` - Flagged content
- `GET /health` - System health check

#### Analytics (`/api/v1/analytics`) 🔐
- `GET /timeseries` - Time-series data for charts
- `GET /cohorts` - Cohort retention analysis
- `GET /funnel` - Conversion funnel data
- `GET /engagement` - Engagement patterns
- `GET /revenue/forecast` - Revenue forecasting
- `GET /export` - Export data (CSV/JSON)

## 🗄️ Database

### Running Migrations

```bash
# Generate new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history
```

### Database Schema

Main tables:
- `users` - User accounts and profiles
- `subscriptions` - Subscription tiers and status
- `readings` - All reading types (coffee, tarot, palm, astrology)
- `reading_images` - Uploaded images for palm readings
- `chat_messages` - Chat conversations with AI personas
- `journal_entries` - User journal entries with AI analysis
- `notification_tokens` - FCM device tokens
- `notification_history` - Notification delivery tracking
- `notification_preferences` - User notification settings
- `webhooks` - Payment webhook events
- `user_stats` - User statistics and gamification

## 🔧 Configuration

### Required Environment Variables

```env
# Essential
DATABASE_URL=postgresql://user:password@localhost:5432/mystic_ai
SECRET_KEY=your-secret-key
OPENAI_API_KEY=sk-your-openai-key

# Payment
REVENUECAT_API_KEY=your-key
REVENUECAT_WEBHOOK_SECRET=your-secret

# Optional but recommended
FIREBASE_CREDENTIALS_PATH=/path/to/firebase.json
PINECONE_API_KEY=your-pinecone-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET_NAME=your-bucket
SENTRY_DSN=your-sentry-dsn
```

### Creating an Admin User

```python
# Connect to your database and run:
UPDATE users SET is_admin = true WHERE email = 'admin@example.com';
```

Or use the API after creating a user:
```bash
# First, manually set is_admin in database, then use:
POST /api/v1/admin/users/{user_id}/promote
```

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

### Application Metrics

- Sentry for error tracking
- Database query performance monitoring
- API endpoint response times
- Rate limit tracking

## 🔐 Security

### Best Practices

1. **Never commit sensitive data**
   - Use `.env` files (gitignored)
   - Use secrets management in production

2. **API Keys**
   - Rotate keys regularly
   - Use different keys for dev/staging/production
   - Restrict API key permissions

3. **Database**
   - Use strong passwords
   - Enable SSL connections in production
   - Regular backups

4. **CORS**
   - Configure allowed origins properly
   - Don't use wildcards in production

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG=false`
- [ ] Set `APP_ENV=production`
- [ ] Configure proper `ALLOWED_ORIGINS`
- [ ] Use strong `SECRET_KEY`
- [ ] Enable database SSL
- [ ] Configure Sentry for error tracking
- [ ] Set up database backups
- [ ] Configure reverse proxy (nginx)
- [ ] Enable HTTPS
- [ ] Set up monitoring and alerts
- [ ] Configure auto-scaling (if needed)
- [ ] Run security audit
- [ ] Load testing

### Docker Production Build

```bash
# Build production image
docker build -t mystic-ai-backend:latest .

# Run with production settings
docker run -d \
  --name mystic-api \
  -p 8000:8000 \
  --env-file .env.production \
  mystic-ai-backend:latest
```

### Platform-Specific Guides

- **AWS ECS/Fargate**: Use provided task definitions
- **Google Cloud Run**: Deploy with `gcloud run deploy`
- **Heroku**: Use `Procfile` and configure buildpacks
- **DigitalOcean App Platform**: Connect GitHub and auto-deploy
- **Kubernetes**: Use provided manifests in `/k8s`

## 🤝 Development

### Project Structure

```
mystic-ai-backend/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependencies (auth, db)
│   │   └── v1/                  # API routes
│   │       ├── auth.py
│   │       ├── readings.py
│   │       ├── chat.py
│   │       ├── journal.py
│   │       ├── astrology.py
│   │       ├── notifications.py
│   │       ├── admin.py
│   │       └── analytics.py
│   ├── models/                  # Database models
│   ├── schemas/                 # Pydantic schemas
│   ├── services/                # Business logic
│   │   ├── auth_service.py
│   │   ├── reading_service.py
│   │   ├── chat_service.py
│   │   ├── journal_service.py
│   │   ├── moon_phase.py
│   │   ├── notification_service.py
│   │   ├── admin_service.py
│   │   └── analytics_service.py
│   ├── ai/                      # AI prompts and logic
│   │   └── prompts/
│   ├── db/                      # Database configuration
│   ├── config.py                # App configuration
│   └── main.py                  # FastAPI app
├── alembic/                     # Database migrations
├── tests/                       # Test files
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public methods
- Keep functions focused and small
- Use meaningful variable names

### Commit Conventions

```
feat: Add new feature
fix: Bug fix
docs: Documentation changes
style: Code formatting
refactor: Code refactoring
test: Add or update tests
chore: Maintenance tasks
```

## 📝 License

[Your License Here]

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- OpenAI for GPT-4 API
- RevenueCat for subscription management
- Firebase for push notifications
- Pinecone for vector database
- PostgreSQL for robust data storage

## 📧 Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Email: support@mystic.ai
- Documentation: [docs-url]

---

**Built with ❤️ for the Mystic.ai platform**
