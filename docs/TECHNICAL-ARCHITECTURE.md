# Mystic.ai - Technical Architecture Document

**Version:** 1.0
**Date:** January 12, 2026
**Status:** MVP Architecture
**Document Owner:** Engineering Team

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Diagrams](#architecture-diagrams)
4. [Frontend Architecture](#frontend-architecture)
5. [Backend Architecture](#backend-architecture)
6. [AI/ML Infrastructure](#aiml-infrastructure)
7. [Database Design](#database-design)
8. [API Specifications](#api-specifications)
9. [Authentication & Authorization](#authentication--authorization)
10. [Payment Integration](#payment-integration)
11. [Internationalization (i18n)](#internationalization-i18n)
12. [Performance & Scalability](#performance--scalability)
13. [Security](#security)
14. [DevOps & CI/CD](#devops--cicd)
15. [Monitoring & Analytics](#monitoring--analytics)

---

## 1. System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  React Native App (iOS + Android)                               │
│  - TypeScript                                                    │
│  - Redux Toolkit (State Management)                             │
│  - React Navigation (Routing)                                   │
│  - Lottie (Animations)                                          │
└────────────┬────────────────────────────────────────────────────┘
             │ HTTPS / REST API + WebSocket
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  AWS API Gateway / Nginx                                         │
│  - Rate Limiting                                                 │
│  - Request Validation                                            │
│  - JWT Verification                                              │
│  - Load Balancing                                                │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI Backend (Python 3.11+)                                 │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐ │
│  │ Auth Service │ Reading Svc  │ Chat Service │ Payment Svc  │ │
│  │              │              │              │              │ │
│  │ - Login/Reg  │ - Coffee AI  │ - Personas   │ - Stripe     │ │
│  │ - JWT tokens │ - Tarot      │ - Memory     │ - IAP verify │ │
│  │ - Profile    │ - Palmistry  │ - Context    │ - Subs mgmt  │ │
│  └──────────────┴──────────────┴──────────────┴──────────────┘ │
│                                                                  │
│  ┌──────────────┬──────────────┬──────────────┐                │
│  │Journal Svc   │Analytics Svc │Notification  │                │
│  │              │              │Service       │                │
│  │- Entries     │- Events      │- Push (FCM)  │                │
│  │- Sentiment   │- Metrics     │- Email       │                │
│  └──────────────┴──────────────┴──────────────┘                │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       AI/ML LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┬──────────────────────┐               │
│  │   OpenAI API         │  Anthropic Claude    │               │
│  │                      │                      │               │
│  │  - GPT-4 Turbo       │  - Claude 3.5 Sonnet │               │
│  │  - GPT-4 Vision      │  - Vision support    │               │
│  │  - Embeddings        │  - Long context      │               │
│  └──────────────────────┴──────────────────────┘               │
│                                                                  │
│  ┌──────────────────────┬──────────────────────┐               │
│  │  Vector Database     │  Image Processing    │               │
│  │                      │                      │               │
│  │  - Pinecone          │  - OpenCV            │               │
│  │  - User embeddings   │  - PIL/Pillow        │               │
│  │  - Semantic search   │  - TensorFlow Lite   │               │
│  └──────────────────────┴──────────────────────┘               │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┬──────────────────────┐               │
│  │  PostgreSQL 15       │  Redis 7             │               │
│  │                      │                      │               │
│  │  - User data         │  - Session cache     │               │
│  │  - Readings          │  - Rate limiting     │               │
│  │  - Subscriptions     │  - Queue (BullMQ)    │               │
│  │  - Journal entries   │                      │               │
│  └──────────────────────┴──────────────────────┘               │
│                                                                  │
│  ┌──────────────────────┬──────────────────────┐               │
│  │  AWS S3              │  CDN (CloudFront)    │               │
│  │                      │                      │               │
│  │  - User images       │  - Static assets     │               │
│  │  - Reading exports   │  - Tarot images      │               │
│  └──────────────────────┴──────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Example: Coffee Cup Reading

```
1. User captures 3 photos (App)
2. Photos uploaded to S3 (App → Backend → S3)
3. Backend triggers AI processing job (FastAPI → Celery Queue)
4. Worker retrieves images from S3 (Celery Worker)
5. Worker sends images to GPT-4 Vision API (Worker → OpenAI)
6. Vision API returns detected symbols (OpenAI → Worker)
7. Worker enriches with user context (PostgreSQL query)
8. Worker generates reading prompt (Template + Context)
9. Worker sends to GPT-4 Turbo (Worker → OpenAI)
10. GPT-4 returns narrative reading (OpenAI → Worker)
11. Worker saves to database (Worker → PostgreSQL)
12. Worker notifies app via WebSocket (Worker → App)
13. App displays reading (App UI)

Total time: 8-12 seconds
```

---

## 2. Technology Stack

### Frontend (Mobile)

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Framework** | React Native | 0.73+ | Cross-platform iOS/Android |
| **Language** | TypeScript | 5.3+ | Type safety, better DX |
| **State Management** | Redux Toolkit | 2.0+ | Global state, caching |
| **Data Fetching** | RTK Query | 2.0+ | API calls, caching, optimistic updates |
| **Navigation** | React Navigation | 6.x | Stack, tab, drawer navigation |
| **UI Components** | React Native Paper | 5.x | Material Design components |
| **Styling** | Styled Components | 6.x | CSS-in-JS |
| **Animations** | React Native Reanimated | 3.x | 60fps animations |
| **Lottie** | lottie-react-native | 6.x | JSON animations |
| **Forms** | React Hook Form | 7.x | Form validation |
| **Camera** | react-native-vision-camera | 3.x | High-quality photo capture |
| **Auth** | @react-native-firebase/auth | 19.x | Firebase Auth SDK |
| **Payments** | react-native-purchases | 7.x | RevenueCat SDK for IAP |
| **i18n** | react-i18next | 14.x | Internationalization |
| **Icons** | react-native-vector-icons | 10.x | Icon sets |
| **Haptics** | react-native-haptic-feedback | 2.x | Vibration feedback |
| **Push** | @react-native-firebase/messaging | 19.x | Firebase Cloud Messaging |
| **Analytics** | @segment/analytics-react-native | 2.x | Segment for analytics |

### Backend

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Framework** | FastAPI | 0.109+ | High-performance Python web framework |
| **Language** | Python | 3.11+ | Backend logic |
| **ORM** | SQLAlchemy | 2.0+ | Database ORM |
| **Migrations** | Alembic | 1.13+ | Database migrations |
| **Validation** | Pydantic | 2.5+ | Data validation |
| **Auth** | python-jose | 3.3+ | JWT handling |
| **Password** | passlib + bcrypt | 1.7+ | Password hashing |
| **HTTP Client** | httpx | 0.26+ | Async HTTP requests |
| **Task Queue** | Celery | 5.3+ | Background jobs |
| **Message Broker** | Redis | 7.2+ | Celery broker |
| **WebSockets** | FastAPI WebSockets | Built-in | Real-time updates |
| **CORS** | fastapi-cors | Built-in | Cross-origin requests |
| **Rate Limiting** | slowapi | 0.1.9+ | API rate limiting |
| **Image Processing** | Pillow | 10.x | Image manipulation |
| **Computer Vision** | OpenCV | 4.9+ | Image analysis |
| **Testing** | pytest | 8.x | Unit/integration tests |
| **API Docs** | Swagger UI | Built-in | Auto-generated API docs |

### AI/ML

| Service | Model | Purpose |
|---------|-------|---------|
| **OpenAI** | GPT-4 Turbo | Text generation (readings, chat) |
| **OpenAI** | GPT-4 Vision | Image analysis (coffee, palm, tarot) |
| **OpenAI** | text-embedding-3-small | Text embeddings for semantic search |
| **Anthropic** | Claude 3.5 Sonnet | Alternative LLM (A/B testing) |
| **Pinecone** | Vector DB | Store user embeddings, semantic memory |
| **TensorFlow Lite** | On-device ML | Palm line detection (offline fallback) |

### Database & Storage

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Primary DB** | PostgreSQL 15 | Relational data (users, readings, subscriptions) |
| **Cache** | Redis 7 | Session cache, rate limiting, queue |
| **Vector DB** | Pinecone | User history embeddings, semantic search |
| **Object Storage** | AWS S3 | User-uploaded images, reading exports |
| **CDN** | AWS CloudFront | Static assets (tarot images, audio) |

### Infrastructure

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Cloud Provider** | AWS / GCP | Hosting |
| **Container** | Docker | Containerization |
| **Orchestration** | Kubernetes (EKS) | Container orchestration |
| **CI/CD** | GitHub Actions | Automated deployments |
| **Monitoring** | Sentry | Error tracking |
| **Monitoring** | DataDog | Performance monitoring |
| **Analytics** | Mixpanel | Product analytics |
| **Logging** | AWS CloudWatch | Application logs |
| **API Gateway** | AWS API Gateway | Request routing, throttling |

---

## 3. Architecture Diagrams

### Microservices Architecture (Text-Based)

```
┌─────────────────────────────────────────────────────────────────┐
│                        API GATEWAY                               │
│                      (Kong / AWS API GW)                         │
└─────────┬───────────────────────────────────────────────────────┘
          │
          ├─────────► Auth Service (Port 8001)
          │           ├─── POST /auth/register
          │           ├─── POST /auth/login
          │           ├─── POST /auth/refresh
          │           └─── GET /auth/profile
          │
          ├─────────► Reading Service (Port 8002)
          │           ├─── POST /readings/coffee
          │           ├─── POST /readings/tarot
          │           ├─── POST /readings/palm
          │           └─── GET /readings/{id}
          │
          ├─────────► Chat Service (Port 8003)
          │           ├─── POST /chat/message
          │           ├─── GET /chat/history
          │           └─── WebSocket /chat/stream
          │
          ├─────────► Journal Service (Port 8004)
          │           ├─── POST /journal/entries
          │           ├─── GET /journal/entries
          │           └─── GET /journal/insights
          │
          ├─────────► Payment Service (Port 8005)
          │           ├─── POST /payments/subscribe
          │           ├─── POST /payments/verify-receipt
          │           └─── GET /payments/status
          │
          └─────────► Notification Service (Port 8006)
                      ├─── POST /notifications/push
                      └─── POST /notifications/schedule
```

### Database Entity Relationship Diagram

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │───┐
│ email           │   │
│ name            │   │
│ birth_date      │   │
│ zodiac_sign     │   │
│ language        │   │
│ created_at      │   │
└─────────────────┘   │
                      │
                      │  1:N
                      │
┌─────────────────────▼──────┐
│      readings              │
├────────────────────────────┤
│ id (PK)                    │
│ user_id (FK)               │───┐
│ type (coffee/tarot/palm)   │   │
│ input_data (JSONB)         │   │
│ ai_response (TEXT)         │   │
│ symbols_detected (JSONB)   │   │
│ created_at                 │   │
│ rating (1-5)               │   │
└────────────────────────────┘   │
                                 │
                                 │  1:1
                                 │
┌────────────────────────────────▼───┐
│      reading_images               │
├────────────────────────────────────┤
│ id (PK)                            │
│ reading_id (FK)                    │
│ image_url (S3 path)                │
│ image_type (cup/saucer/palm)       │
│ uploaded_at                        │
└────────────────────────────────────┘

┌─────────────────┐
│ chat_messages   │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │────────────┐
│ persona         │            │
│ role            │            │  N:1
│ content         │            │
│ created_at      │            │
└─────────────────┘            │
                               │
                               │
┌──────────────────────────────▼─┐
│       subscriptions            │
├────────────────────────────────┤
│ id (PK)                        │
│ user_id (FK)                   │
│ tier (weekly/monthly)          │
│ status (active/canceled)       │
│ platform (ios/android)         │
│ original_transaction_id        │
│ expires_at                     │
│ auto_renew                     │
│ created_at                     │
└────────────────────────────────┘

┌─────────────────┐
│ journal_entries │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │─────────┐
│ content         │         │
│ mood            │         │  N:1
│ tags (ARRAY)    │         │
│ sentiment       │         │
│ chakra_scores   │         │
│ created_at      │         │
└─────────────────┘         │
                            │
                            │
┌───────────────────────────▼─┐
│      user_stats             │
├─────────────────────────────┤
│ id (PK)                     │
│ user_id (FK)                │
│ karma_points                │
│ readings_count              │
│ journal_streak              │
│ badges (JSONB)              │
│ last_active                 │
└─────────────────────────────┘
```

---

## 4. Frontend Architecture

### Project Structure

```
mystic-ai-app/
├── src/
│   ├── api/                      # API layer (RTK Query)
│   │   ├── authApi.ts
│   │   ├── readingApi.ts
│   │   ├── chatApi.ts
│   │   └── paymentApi.ts
│   │
│   ├── components/               # Reusable components
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Loading.tsx
│   │   │   └── Modal.tsx
│   │   ├── reading/
│   │   │   ├── CameraOverlay.tsx
│   │   │   ├── SymbolAnnotation.tsx
│   │   │   └── ReadingCard.tsx
│   │   ├── chat/
│   │   │   ├── PersonaSelector.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   └── ChatInput.tsx
│   │   └── journal/
│   │       ├── EntryEditor.tsx
│   │       ├── MoodPicker.tsx
│   │       └── ChakraWheel.tsx
│   │
│   ├── screens/                  # Screen components
│   │   ├── auth/
│   │   │   ├── WelcomeScreen.tsx
│   │   │   ├── LoginScreen.tsx
│   │   │   └── OnboardingScreen.tsx
│   │   ├── home/
│   │   │   └── HomeScreen.tsx
│   │   ├── readings/
│   │   │   ├── CoffeeReadingScreen.tsx
│   │   │   ├── TarotReadingScreen.tsx
│   │   │   ├── PalmReadingScreen.tsx
│   │   │   └── ReadingDetailScreen.tsx
│   │   ├── chat/
│   │   │   └── ChatScreen.tsx
│   │   ├── journal/
│   │   │   └── JournalScreen.tsx
│   │   └── profile/
│   │       ├── ProfileScreen.tsx
│   │       └── SubscriptionScreen.tsx
│   │
│   ├── navigation/               # Navigation setup
│   │   ├── RootNavigator.tsx
│   │   ├── AuthNavigator.tsx
│   │   └── MainNavigator.tsx
│   │
│   ├── store/                    # Redux store
│   │   ├── index.ts
│   │   ├── slices/
│   │   │   ├── authSlice.ts
│   │   │   ├── readingSlice.ts
│   │   │   └── uiSlice.ts
│   │   └── middleware.ts
│   │
│   ├── hooks/                    # Custom hooks
│   │   ├── useAuth.ts
│   │   ├── useCamera.ts
│   │   ├── useHaptics.ts
│   │   └── useLocalization.ts
│   │
│   ├── services/                 # Business logic services
│   │   ├── authService.ts
│   │   ├── cameraService.ts
│   │   ├── paymentService.ts
│   │   └── notificationService.ts
│   │
│   ├── utils/                    # Utility functions
│   │   ├── zodiac.ts
│   │   ├── astrology.ts
│   │   ├── validation.ts
│   │   └── formatting.ts
│   │
│   ├── theme/                    # Theme configuration
│   │   ├── colors.ts
│   │   ├── typography.ts
│   │   ├── spacing.ts
│   │   └── index.ts
│   │
│   ├── locales/                  # i18n translations
│   │   ├── en.json
│   │   ├── tr.json
│   │   └── de.json
│   │
│   ├── assets/                   # Static assets
│   │   ├── images/
│   │   ├── animations/           # Lottie JSON files
│   │   ├── sounds/
│   │   └── fonts/
│   │
│   ├── types/                    # TypeScript types
│   │   ├── api.types.ts
│   │   ├── reading.types.ts
│   │   └── user.types.ts
│   │
│   └── App.tsx                   # Root component
│
├── ios/                          # iOS native code
├── android/                      # Android native code
├── package.json
├── tsconfig.json
└── app.json
```

### State Management Architecture

```typescript
// Redux Store Structure

interface RootState {
  auth: {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
  };

  reading: {
    current: Reading | null;
    history: Reading[];
    isProcessing: boolean;
  };

  chat: {
    activePersona: 'sage' | 'witch' | 'astrologer';
    messages: Message[];
    isTyping: boolean;
  };

  journal: {
    entries: JournalEntry[];
    currentEntry: JournalEntry | null;
    insights: ChakraInsights | null;
  };

  subscription: {
    tier: 'free' | 'weekly' | 'monthly';
    status: 'active' | 'expired';
    expiresAt: Date | null;
    usageCount: {
      readings: number;
      chatMessages: number;
    };
  };

  ui: {
    theme: 'light' | 'dark';
    language: 'en' | 'tr' | 'de';
    notifications: Notification[];
  };
}
```

### Component Design Pattern

```typescript
// Example: CoffeeReadingScreen.tsx

import React, { useState } from 'react';
import { View, StyleSheet } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useCreateReadingMutation } from '@/api/readingApi';
import { CameraOverlay } from '@/components/reading/CameraOverlay';
import { Button, Loading } from '@/components/common';
import { useHaptics } from '@/hooks/useHaptics';
import { colors, spacing } from '@/theme';

export const CoffeeReadingScreen: React.FC = () => {
  const [photos, setPhotos] = useState<string[]>([]);
  const [createReading, { isLoading }] = useCreateReadingMutation();
  const { triggerSuccess } = useHaptics();
  const navigation = useNavigation();

  const handleCaptureComplete = async (capturedPhotos: string[]) => {
    setPhotos(capturedPhotos);

    try {
      const result = await createReading({
        type: 'coffee',
        images: capturedPhotos,
      }).unwrap();

      triggerSuccess();
      navigation.navigate('ReadingDetail', { readingId: result.id });
    } catch (error) {
      // Error handled by RTK Query middleware
    }
  };

  if (isLoading) {
    return <Loading message="The Oracle is reading your cup..." />;
  }

  return (
    <View style={styles.container}>
      <CameraOverlay
        instructionSteps={['Cup Interior', 'Saucer', 'Side View']}
        onComplete={handleCaptureComplete}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
});
```

---

## 5. Backend Architecture

### Project Structure

```
mystic-ai-backend/
├── app/
│   ├── main.py                   # FastAPI app entry
│   ├── config.py                 # Configuration (env vars)
│   │
│   ├── api/                      # API routes
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── readings.py
│   │   │   ├── chat.py
│   │   │   ├── journal.py
│   │   │   └── payments.py
│   │   └── deps.py               # Dependencies (auth, db session)
│   │
│   ├── models/                   # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── reading.py
│   │   ├── chat.py
│   │   ├── journal.py
│   │   └── subscription.py
│   │
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── reading.py
│   │   ├── chat.py
│   │   └── payment.py
│   │
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── reading_service.py
│   │   ├── ai_service.py
│   │   ├── vision_service.py
│   │   ├── chat_service.py
│   │   ├── payment_service.py
│   │   └── notification_service.py
│   │
│   ├── ai/                       # AI-specific logic
│   │   ├── __init__.py
│   │   ├── prompts/
│   │   │   ├── coffee_reading.py
│   │   │   ├── tarot_reading.py
│   │   │   ├── palm_reading.py
│   │   │   └── personas.py
│   │   ├── vision.py             # Image analysis
│   │   ├── embeddings.py         # Vector embeddings
│   │   └── memory.py             # Long-term memory
│   │
│   ├── workers/                  # Celery tasks
│   │   ├── __init__.py
│   │   ├── reading_worker.py
│   │   └── notification_worker.py
│   │
│   ├── db/                       # Database utilities
│   │   ├── __init__.py
│   │   ├── session.py
│   │   └── migrations/           # Alembic migrations
│   │
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── astrology.py
│   │   ├── image.py
│   │   ├── security.py
│   │   └── validation.py
│   │
│   └── tests/                    # Tests
│       ├── test_auth.py
│       ├── test_readings.py
│       └── test_ai.py
│
├── alembic.ini                   # Alembic config
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

### FastAPI Application Setup

```python
# app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.v1 import auth, readings, chat, journal, payments
from app.config import settings
from app.db.session import engine
from app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# FastAPI app
app = FastAPI(
    title="Mystic.ai API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(readings.router, prefix="/api/v1/readings", tags=["readings"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(journal.router, prefix="/api/v1/journal", tags=["journal"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["payments"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Example: Reading Service

```python
# app/services/reading_service.py

from typing import List
from sqlalchemy.orm import Session
from app.models.reading import Reading
from app.models.user import User
from app.services.vision_service import VisionService
from app.services.ai_service import AIService
from app.schemas.reading import ReadingCreate, ReadingResponse
from app.utils.astrology import get_current_transits
import logging

logger = logging.getLogger(__name__)

class ReadingService:
    def __init__(self, db: Session):
        self.db = db
        self.vision_service = VisionService()
        self.ai_service = AIService()

    async def create_coffee_reading(
        self,
        user: User,
        image_urls: List[str]
    ) -> ReadingResponse:
        """
        Process coffee cup reading

        1. Analyze images with Vision AI
        2. Get user context (zodiac, recent readings)
        3. Generate personalized reading
        4. Save to database
        """

        logger.info(f"Creating coffee reading for user {user.id}")

        # Step 1: Vision analysis
        symbols = []
        for idx, image_url in enumerate(image_urls):
            detected = await self.vision_service.detect_coffee_symbols(image_url)
            symbols.extend(detected)

        logger.info(f"Detected {len(symbols)} symbols")

        # Step 2: Get user context
        context = {
            "user_name": user.name,
            "zodiac_sign": user.zodiac_sign,
            "recent_readings": self._get_recent_readings_summary(user),
            "current_transits": get_current_transits(),
            "language": user.language,
        }

        # Step 3: Generate reading
        reading_text = await self.ai_service.generate_coffee_reading(
            symbols=symbols,
            context=context
        )

        # Step 4: Save to database
        reading = Reading(
            user_id=user.id,
            type="coffee",
            input_data={"image_urls": image_urls, "symbols": symbols},
            ai_response=reading_text,
            symbols_detected=symbols,
        )
        self.db.add(reading)
        self.db.commit()
        self.db.refresh(reading)

        logger.info(f"Coffee reading {reading.id} created successfully")

        return ReadingResponse.from_orm(reading)

    def _get_recent_readings_summary(self, user: User, limit: int = 3) -> str:
        """Get summary of user's recent readings for context"""
        recent = self.db.query(Reading)\
            .filter(Reading.user_id == user.id)\
            .order_by(Reading.created_at.desc())\
            .limit(limit)\
            .all()

        if not recent:
            return "This is the user's first reading."

        summaries = []
        for r in recent:
            summaries.append(f"{r.type.capitalize()} reading on {r.created_at.date()}")

        return f"Recent activity: " + ", ".join(summaries)
```

---

## 6. AI/ML Infrastructure

### OpenAI Integration

```python
# app/services/ai_service.py

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from app.config import settings
from app.ai.prompts.coffee_reading import COFFEE_READING_PROMPT
from app.ai.prompts.personas import PERSONA_PROMPTS
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def generate_coffee_reading(
        self,
        symbols: List[Dict],
        context: Dict
    ) -> str:
        """
        Generate coffee cup reading using GPT-4
        """

        # Build prompt
        prompt = COFFEE_READING_PROMPT.format(
            symbols_json=symbols,
            user_name=context["user_name"],
            zodiac_sign=context["zodiac_sign"],
            recent_readings=context["recent_readings"],
            current_transits=context["current_transits"],
            language=context["language"],
        )

        logger.info(f"Generating reading with GPT-4 ({len(symbols)} symbols)")

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a master coffee fortune teller."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,  # Slightly creative
                max_tokens=1000,
            )

            reading_text = response.choices[0].message.content
            logger.info(f"Reading generated: {len(reading_text)} chars")

            return reading_text

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

    async def chat_with_persona(
        self,
        persona: str,
        user_message: str,
        chat_history: List[Dict],
        user_context: Dict
    ) -> str:
        """
        Chat with one of the mystical personas
        """

        system_prompt = PERSONA_PROMPTS[persona].format(
            user_name=user_context["user_name"],
            zodiac_sign=user_context["zodiac_sign"],
            recent_reading=user_context.get("recent_reading", "None yet"),
            language=user_context["language"],
        )

        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Add chat history (last 10 messages)
        for msg in chat_history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Add current message
        messages.append({"role": "user", "content": user_message})

        response = await self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=0.9 if persona == "witch" else 0.7,
            max_tokens=300,
        )

        return response.choices[0].message.content
```

### Vision AI Service

```python
# app/services/vision_service.py

from openai import AsyncOpenAI
from app.config import settings
from typing import List, Dict
import base64
import logging

logger = logging.getLogger(__name__)

class VisionService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def detect_coffee_symbols(self, image_url: str) -> List[Dict]:
        """
        Analyze coffee cup image and detect symbols
        """

        logger.info(f"Analyzing image: {image_url}")

        prompt = """
        You are an expert in Turkish coffee cup reading (Tasseography).

        Analyze this coffee cup image and identify:
        1. All visible shapes and symbols
        2. Their positions (top/middle/bottom, left/right)
        3. Clarity/prominence (1-10 scale)

        Common symbols to look for:
        - Animals (bird, fish, snake, cat, dog, horse)
        - Objects (heart, key, tree, mountain, road, stairs, ring)
        - Nature (cloud, sun, moon, star, flower, water)
        - Abstract (lines, circles, triangles, arrows)

        Return as JSON array:
        [
          {
            "symbol": "bird",
            "position": "top-right",
            "clarity": 8,
            "description": "Bird with wings spread, facing upward"
          },
          ...
        ]
        """

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]
                    }
                ],
                max_tokens=500,
            )

            # Parse JSON response
            import json
            symbols = json.loads(response.choices[0].message.content)

            logger.info(f"Detected {len(symbols)} symbols")
            return symbols

        except Exception as e:
            logger.error(f"Vision API error: {str(e)}")
            return []

    async def analyze_palm_lines(self, image_url: str) -> Dict:
        """
        Analyze palm image and detect major lines
        """

        prompt = """
        You are a palmistry expert. Analyze this hand image and identify:

        1. Life Line: Length, depth, breaks, chains
        2. Heart Line: Curvature, length, ending point
        3. Head Line: Angle, length, clarity
        4. Fate Line: Presence, strength, direction
        5. Hand Shape: Square/rectangular palm, finger length

        Return as JSON:
        {
          "life_line": {"length": "long", "depth": "deep", "breaks": []},
          "heart_line": {"curve": "high", "length": "long", "ending": "between_fingers"},
          "head_line": {"angle": "straight", "length": "medium"},
          "fate_line": {"present": true, "strength": "strong"},
          "hand_shape": {"element": "earth", "description": "Square palm, short fingers"}
        }
        """

        response = await self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            max_tokens=600,
        )

        import json
        return json.loads(response.choices[0].message.content)
```

### Prompt Templates

```python
# app/ai/prompts/coffee_reading.py

COFFEE_READING_PROMPT = """
You are Mystic.ai's Coffee Fortune Oracle, a master of Turkish coffee cup reading (Tasseography).

USER INFORMATION:
- Name: {user_name}
- Zodiac Sign: {zodiac_sign}
- Recent Activity: {recent_readings}

CURRENT ASTROLOGICAL CONTEXT:
{current_transits}

DETECTED SYMBOLS:
{symbols_json}

TASK:
Generate a personalized, story-driven coffee fortune reading in {language}.

STRUCTURE:
1. **Opening** (2-3 sentences): Warmly greet the user and acknowledge the symbols you see
2. **The Past** (~100 words): Interpret symbols at the bottom of the cup
3. **The Present** (~100 words): Interpret symbols on the sides
4. **The Future** (~150 words): Interpret symbols at the top and on the saucer
5. **Guidance** (~50 words): Practical, actionable advice based on the reading

TONE & STYLE:
- Mystical yet warm and personal
- Use the user's name naturally
- Weave in their zodiac sign's traits
- Tell a story, don't just list meanings
- Be specific, avoid generic statements like "you will find love"
- End on a hopeful, empowering note

SYMBOL MEANINGS (use these as guidance):
- Bird: Freedom, messages, travel, spiritual ascension
- Heart: Love, emotions, relationships, compassion
- Key: Solutions, unlocking potential, secrets revealed
- Tree: Growth, stability, family roots
- Mountain: Challenges, obstacles, goals to climb
- Road/Path: Journey, life direction, choices ahead
- Star: Hope, wishes coming true, guidance
- Fish: Abundance, prosperity, intuition
- Snake: Transformation, healing, hidden wisdom (or betrayal depending on context)
- Ring: Commitment, completion, cycles
- Cloud: Confusion, temporary obstacles, need for clarity
- Moon: Feminine energy, intuition, cycles, emotions

POSITION MEANINGS:
- Bottom of cup: The past (what has led you here)
- Sides of cup: The present (current situation, influences)
- Top of cup & saucer: The future (what's coming, potential outcomes)
- Left side: Negative influences or departing energies
- Right side: Positive influences or arriving energies

EXAMPLE OPENING:
"{user_name}, as I gaze into your coffee cup, I see a powerful story unfolding. A bird takes flight from a mountain peak—a symbol of liberation earned through perseverance. The grounds have spoken, and they reveal much about your journey..."

Now generate the full reading for {user_name}.
"""

# app/ai/prompts/personas.py

PERSONA_PROMPTS = {
    "sage": """
You are The Sage—a wise, stoic philosopher and spiritual guide within Mystic.ai.

YOUR CHARACTER:
- Calm, measured, and deeply thoughtful
- You draw from Stoicism (Marcus Aurelius, Epictetus), Buddhism (Thich Nhat Hanh), and Taoism
- You ask reflective questions to help users find their own wisdom
- You believe obstacles are teachers, not enemies
- You speak in simple yet profound truths

USER CONTEXT:
- Name: {user_name}
- Zodiac: {zodiac_sign}
- Recent Reading: {recent_reading}
- Language: {language}

YOUR APPROACH:
- Listen deeply to the user's question or concern
- Reflect it back with added perspective
- Ask a question that invites self-discovery
- Offer a philosophical insight or practice (meditation, journaling prompt)
- Keep responses under 150 words unless the user asks for depth

EXAMPLE RESPONSES:
User: "I'm anxious about a job interview tomorrow."
Sage: "{user_name}, anxiety is the mind's way of rehearsing the future. But consider this: the interview is simply a conversation, not a judgment of your worth. What if you viewed it as an opportunity to learn, rather than a test to pass? Tonight, try this: Write down three qualities you bring to this role, then breathe deeply and trust in your preparation. Remember, as Marcus Aurelius said, 'You have power over your mind—not outside events. Realize this, and you will find strength.' How are you preparing your mind, not just your answers?"

Now respond to the user's message in {language}.
""",

    "witch": """
You are The Witch—an earthy, practical mystic who works with nature, crystals, herbs, and lunar magic within Mystic.ai.

YOUR CHARACTER:
- Grounded yet magical, like a forest herbalist
- You know the properties of crystals, herbs, moon phases, and simple rituals
- You speak with warmth and a touch of playful mystery
- You believe in the power of intention + natural elements
- You offer tangible practices (carry this stone, burn this herb, do this ritual)

USER CONTEXT:
- Name: {user_name}
- Zodiac: {zodiac_sign}
- Recent Reading: {recent_reading}
- Language: {language}

YOUR APPROACH:
- Acknowledge the user's situation with empathy
- Suggest a crystal, herb, or ritual that aligns with their need
- Explain the "why" behind your suggestion (e.g., "Rose quartz opens the heart chakra")
- Include moon phase guidance if relevant
- Keep it accessible—no complex spells, just simple magic

EXAMPLE RESPONSES:
User: "I need more confidence at work."
Witch: "Ah, {user_name}, confidence is like a fire—it needs tending. For you, a Leo, I'd suggest carrying a Citrine stone in your pocket. Citrine is the 'success stone'—it amplifies personal power and attracts abundance. Each morning, hold it and say: 'I am capable, I am worthy.' Also, the New Moon in three days is perfect for setting intentions. Write your goal on bay leaves and burn them safely—release the wish to the universe. Your inner fire will respond. 🔥🌙"

Now respond to the user's message in {language}.
""",

    "astrologer": """
You are The Astrologer—a cosmic guide who interprets planetary movements and their influence on human life within Mystic.ai.

YOUR CHARACTER:
- Knowledgeable about natal charts, transits, retrogrades, and aspects
- You speak the language of the stars: "Venus in your 7th house," "Mercury retrograde"
- You're analytical yet mystical—you see patterns in the cosmos
- You connect current planetary movements to the user's situation
- You offer both warnings and opportunities based on transits

USER CONTEXT:
- Name: {user_name}
- Zodiac: {zodiac_sign}
- Recent Reading: {recent_reading}
- Language: {language}

CURRENT TRANSITS: (You have access to real-time astrological data)
- Moon Phase: Waxing Crescent (growth phase)
- Mercury: Direct in Capricorn (clear communication, practical thinking)
- Venus: In Pisces (dreamy love, artistic inspiration)

YOUR APPROACH:
- Reference the user's zodiac sign and current transits
- Explain what's happening in the cosmos and how it affects them
- Offer timing advice ("Wait until Friday when..." or "Act now while...")
- Use astrological terms but explain them simply
- Keep responses focused and actionable

EXAMPLE RESPONSES:
User: "Should I start a new project now?"
Astrologer: "{user_name}, as a {zodiac_sign}, you're currently experiencing a powerful moment. Mars is transiting your 10th house of career—this is your cosmic green light for bold professional moves. The Waxing Moon also supports growth and initiation. However, I'd suggest finalizing details by January 20th, before Mercury enters its shadow period. Harness this fiery energy: start your project, but build in flexibility for mid-February adjustments. The stars are aligned for your ambition. ✨"

Now respond to the user's message in {language}.
"""
}
```

---

## 7. Database Design

### PostgreSQL Schema (SQLAlchemy Models)

```python
# app/models/user.py

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime
import enum

class LanguageEnum(str, enum.Enum):
    ENGLISH = "en"
    TURKISH = "tr"
    GERMAN = "de"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for social logins
    name = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=True)
    zodiac_sign = Column(String, nullable=True)
    language = Column(Enum(LanguageEnum), default=LanguageEnum.ENGLISH)

    # OAuth
    google_id = Column(String, unique=True, nullable=True)
    apple_id = Column(String, unique=True, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    readings = relationship("Reading", back_populates="user", cascade="all, delete-orphan")
    journal_entries = relationship("JournalEntry", back_populates="user")
    chat_messages = relationship("ChatMessage", back_populates="user")
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    stats = relationship("UserStats", back_populates="user", uselist=False)
```

```python
# app/models/reading.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Reading type: coffee, tarot, palm
    type = Column(String, nullable=False, index=True)

    # Input data (images, card selections, etc.)
    input_data = Column(JSON, nullable=False)

    # AI-generated reading
    ai_response = Column(Text, nullable=False)

    # Detected symbols/patterns
    symbols_detected = Column(JSON, nullable=True)

    # User feedback
    rating = Column(Integer, nullable=True)  # 1-5 stars

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    processing_time = Column(Integer, nullable=True)  # milliseconds

    # Relationships
    user = relationship("User", back_populates="readings")
    images = relationship("ReadingImage", back_populates="reading")
```

```python
# app/models/subscription.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime
import enum

class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ANNUAL = "annual"

class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELED = "canceled"
    TRIAL = "trial"

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)

    # Platform (ios, android, web)
    platform = Column(String, nullable=True)

    # Store receipt/transaction data
    original_transaction_id = Column(String, unique=True, nullable=True)
    latest_receipt = Column(Text, nullable=True)

    # Dates
    started_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)

    # Auto-renewal
    auto_renew = Column(Boolean, default=True)

    # Usage tracking (for free tier limits)
    readings_this_month = Column(Integer, default=0)
    chat_messages_today = Column(Integer, default=0)
    last_reset = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="subscription")
```

### Redis Cache Structure

```python
# Cache keys structure

# Session cache
"session:{user_id}" → {
    "token": "jwt_token",
    "expires_at": 1234567890,
    "device_id": "device123"
}

# Rate limiting
"rate_limit:readings:{user_id}" → "3"  # Count
"rate_limit:chat:{user_id}" → "15"

# Chat context (short-term)
"chat:history:{user_id}" → [
    {"role": "user", "content": "...", "timestamp": 123},
    {"role": "assistant", "content": "...", "timestamp": 124}
]

# Processing queue
"queue:readings" → [reading_id_1, reading_id_2, ...]
```

### Pinecone Vector Database

```python
# Vector embeddings for semantic memory

# Structure
{
    "id": "reading_123",
    "values": [0.123, 0.456, ...],  # 1536-dim embedding
    "metadata": {
        "user_id": 42,
        "type": "coffee",
        "date": "2026-01-12",
        "summary": "Travel and new opportunities",
        "symbols": ["bird", "key", "road"]
    }
}

# Query: "Tell me about my past readings related to career"
# → Embed query → Search Pinecone → Return top 5 relevant readings
```

---

## 8. API Specifications

### Authentication Endpoints

```
POST /api/v1/auth/register
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "Luna",
  "birth_date": "1995-08-15",
  "language": "en"
}

Response:
{
  "user": {
    "id": 42,
    "email": "user@example.com",
    "name": "Luna",
    "zodiac_sign": "Leo",
    "language": "en"
  },
  "token": "eyJhbGc...",
  "refresh_token": "def50200..."
}

---

POST /api/v1/auth/login
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123"
}

Response:
{
  "user": {...},
  "token": "jwt_token",
  "refresh_token": "refresh_token"
}

---

POST /api/v1/auth/social
Request:
{
  "provider": "google",
  "id_token": "google_id_token"
}

Response:
{
  "user": {...},
  "token": "jwt_token",
  "is_new_user": false
}
```

### Reading Endpoints

```
POST /api/v1/readings/coffee
Headers:
  Authorization: Bearer {token}

Request (multipart/form-data):
{
  "cup_image": <file>,
  "saucer_image": <file>,
  "side_image": <file>
}

Response:
{
  "id": 123,
  "type": "coffee",
  "status": "processing",
  "estimated_time": 10  // seconds
}

---

GET /api/v1/readings/{reading_id}
Headers:
  Authorization: Bearer {token}

Response:
{
  "id": 123,
  "type": "coffee",
  "status": "completed",
  "created_at": "2026-01-12T10:30:00Z",
  "reading": {
    "text": "Luna, as I gaze into your cup...",
    "sections": {
      "past": "...",
      "present": "...",
      "future": "..."
    },
    "symbols": [
      {
        "name": "bird",
        "position": "top-right",
        "meaning": "Freedom and new messages"
      }
    ]
  },
  "images": [
    {
      "url": "https://cdn.mystic.ai/readings/123/cup.jpg",
      "type": "cup",
      "annotated_url": "https://cdn.mystic.ai/readings/123/cup_annotated.jpg"
    }
  ]
}

---

GET /api/v1/readings
Headers:
  Authorization: Bearer {token}

Query Params:
  ?type=coffee&limit=10&offset=0

Response:
{
  "readings": [...],
  "total": 25,
  "has_more": true
}
```

### Chat Endpoints

```
POST /api/v1/chat/message
Headers:
  Authorization: Bearer {token}

Request:
{
  "persona": "sage",
  "message": "I'm feeling anxious about tomorrow"
}

Response:
{
  "message_id": 456,
  "persona": "sage",
  "response": "Luna, anxiety is the mind's way...",
  "created_at": "2026-01-12T11:00:00Z"
}

---

WebSocket /api/v1/chat/stream
Headers:
  Authorization: Bearer {token}

Client → Server:
{
  "type": "message",
  "persona": "witch",
  "content": "What crystal should I use for confidence?"
}

Server → Client (streaming):
{
  "type": "chunk",
  "content": "Ah, Luna"
}
{
  "type": "chunk",
  "content": ", confidence is like a fire..."
}
{
  "type": "done"
}
```

### Subscription Endpoints

```
POST /api/v1/payments/verify-receipt
Headers:
  Authorization: Bearer {token}

Request:
{
  "platform": "ios",
  "receipt_data": "base64_encoded_receipt"
}

Response:
{
  "subscription": {
    "tier": "monthly",
    "status": "active",
    "expires_at": "2026-02-12T10:00:00Z"
  },
  "features_unlocked": true
}

---

GET /api/v1/payments/status
Headers:
  Authorization: Bearer {token}

Response:
{
  "tier": "free",
  "status": "active",
  "usage": {
    "readings_this_month": 2,
    "readings_limit": 3,
    "chat_messages_today": 5,
    "chat_messages_limit": 10
  },
  "can_upgrade": true
}
```

---

## 9. Authentication & Authorization

### JWT Token Structure

```json
{
  "sub": "42",  // user_id
  "email": "user@example.com",
  "name": "Luna",
  "tier": "monthly",
  "iat": 1234567890,
  "exp": 1234654290
}
```

### Authentication Flow

```
1. User signs up/logs in
2. Backend generates JWT + Refresh Token
3. JWT stored in secure storage (iOS Keychain, Android Keystore)
4. Every API request includes: Authorization: Bearer {jwt}
5. Backend middleware validates JWT
6. If expired, client uses refresh token to get new JWT
```

### Authorization Middleware

```python
# app/api/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import settings
from app.db.session import get_db
from app.models.user import User
from sqlalchemy.orm import Session

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Validate JWT and return current user
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def require_premium(user: User = Depends(get_current_user)):
    """
    Require premium subscription
    """
    if user.subscription.tier == "free":
        raise HTTPException(
            status_code=403,
            detail="Premium subscription required"
        )
    return user
```

---

## 10. Payment Integration

### RevenueCat Setup

```typescript
// Frontend: services/paymentService.ts

import Purchases, { PurchasesOffering } from 'react-native-purchases';
import { Platform } from 'react-native';

const REVENUECAT_API_KEY = Platform.select({
  ios: 'appl_xxx',
  android: 'goog_xxx',
});

export class PaymentService {
  static async initialize(userId: string) {
    await Purchases.configure({
      apiKey: REVENUECAT_API_KEY!,
      appUserID: userId,
    });
  }

  static async getOfferings(): Promise<PurchasesOffering | null> {
    const offerings = await Purchases.getOfferings();
    return offerings.current;
  }

  static async purchasePackage(pkg: any) {
    try {
      const { customerInfo } = await Purchases.purchasePackage(pkg);
      return this.checkSubscriptionStatus(customerInfo);
    } catch (error) {
      if (error.userCancelled) {
        return null;
      }
      throw error;
    }
  }

  static async restorePurchases() {
    const customerInfo = await Purchases.restorePurchases();
    return this.checkSubscriptionStatus(customerInfo);
  }

  static checkSubscriptionStatus(customerInfo: any) {
    const activeEntitlements = customerInfo.entitlements.active;

    if (activeEntitlements['premium']) {
      return {
        isPremium: true,
        tier: 'monthly',  // Determine from product ID
        expiresAt: activeEntitlements['premium'].expirationDate,
      };
    }

    return {
      isPremium: false,
      tier: 'free',
    };
  }
}
```

### Backend Webhook Handler

```python
# app/api/v1/payments.py

from fastapi import APIRouter, Request, HTTPException
from app.services.payment_service import PaymentService

router = APIRouter()

@router.post("/webhook/revenuecat")
async def revenuecat_webhook(request: Request):
    """
    Handle RevenueCat webhooks for subscription events
    """
    payload = await request.json()
    event_type = payload.get("type")

    if event_type == "INITIAL_PURCHASE":
        # New subscription
        await PaymentService.activate_subscription(payload)

    elif event_type == "RENEWAL":
        # Subscription renewed
        await PaymentService.renew_subscription(payload)

    elif event_type == "CANCELLATION":
        # Subscription canceled
        await PaymentService.cancel_subscription(payload)

    elif event_type == "EXPIRATION":
        # Subscription expired
        await PaymentService.expire_subscription(payload)

    return {"status": "ok"}
```

---

## 11. Internationalization (i18n)

### Translation Files

```json
// locales/en.json
{
  "common": {
    "loading": "Loading...",
    "error": "Something went wrong",
    "retry": "Try again"
  },
  "auth": {
    "signIn": "Sign In",
    "signUp": "Sign Up",
    "emailPlaceholder": "Enter your email",
    "passwordPlaceholder": "Enter your password"
  },
  "readings": {
    "coffee": {
      "title": "Coffee Cup Reading",
      "instruction1": "Photograph the interior of your cup",
      "instruction2": "Photograph the saucer",
      "instruction3": "Photograph the side view",
      "processing": "The Oracle is reading your cup..."
    },
    "tarot": {
      "title": "Tarot Reading",
      "shufflePrompt": "Shuffle the cards and focus on your question",
      "selectCards": "Select {{count}} cards"
    }
  }
}
```

```json
// locales/tr.json
{
  "readings": {
    "coffee": {
      "title": "Kahve Falı",
      "instruction1": "Fincanınızın içini fotoğraflayın",
      "processing": "Falınız bakılıyor..."
    }
  }
}
```

### Backend i18n

```python
# app/utils/i18n.py

TRANSLATIONS = {
    "en": {
        "reading_intro": "{name}, as I gaze into your cup, I see...",
        "error_no_symbols": "No clear symbols were detected. Please try again with better lighting."
    },
    "tr": {
        "reading_intro": "{name}, fincanınıza baktığımda görüyorum ki...",
        "error_no_symbols": "Net semboller tespit edilemedi. Lütfen daha iyi aydınlatma ile tekrar deneyin."
    },
    "de": {
        "reading_intro": "{name}, wenn ich in deine Tasse schaue, sehe ich...",
        "error_no_symbols": "Es wurden keine klaren Symbole erkannt. Bitte versuchen Sie es mit besserer Beleuchtung erneut."
    }
}

def t(key: str, language: str, **kwargs) -> str:
    """Translate a key"""
    text = TRANSLATIONS.get(language, {}).get(key, TRANSLATIONS["en"][key])
    return text.format(**kwargs)
```

---

## 12. Performance & Scalability

### Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| **App Launch** | <2s | TBD |
| **API Response (simple)** | <200ms | TBD |
| **Reading Generation** | <10s | TBD |
| **Image Upload** | <3s (10MB) | TBD |
| **Chat Response** | <3s | TBD |
| **App Size** | <100MB | TBD |

### Optimization Strategies

**Frontend**:
- Code splitting (lazy load screens)
- Image optimization (WebP, compression)
- Memoization (React.memo, useMemo)
- Virtualized lists (FlatList for long lists)
- Offline support (cached readings)

**Backend**:
- Database indexing (user_id, created_at)
- Query optimization (N+1 prevention)
- Caching (Redis for hot data)
- CDN for static assets
- Connection pooling (PostgreSQL)

**AI**:
- Batch requests where possible
- Stream responses (chat)
- Cache common queries
- Fallback to smaller models for simple tasks

### Scalability Plan

**Phase 1: Single Server** (0-10K users)
- Single EC2 instance or App Engine
- Single PostgreSQL instance
- Redis for caching

**Phase 2: Horizontal Scaling** (10K-100K users)
- Load balancer (ALB)
- Auto-scaling group (3-10 instances)
- Read replicas for PostgreSQL
- ElastiCache for Redis

**Phase 3: Microservices** (100K+ users)
- Separate services for Auth, Readings, Chat
- Kubernetes orchestration
- Message queue (RabbitMQ/SQS) for async jobs
- Multi-region deployment

---

## 13. Security

### Security Checklist

✅ **Authentication**:
- JWT with expiration (15 min access, 7 day refresh)
- Secure password hashing (bcrypt, 12 rounds)
- Rate limiting (5 login attempts per 15 min)
- HTTPS only (TLS 1.3)

✅ **Authorization**:
- Role-based access control
- Premium feature checks
- User can only access their own data

✅ **Data Protection**:
- AES-256 encryption for journal entries
- Encrypted at rest (database)
- Encrypted in transit (TLS)
- PII anonymization for analytics

✅ **Input Validation**:
- Pydantic schemas on backend
- React Hook Form validation on frontend
- File upload limits (10MB max)
- Content type validation (images only)

✅ **API Security**:
- Rate limiting (100 req/min per user)
- CORS whitelist
- SQL injection prevention (ORM)
- XSS prevention (sanitize inputs)

✅ **Compliance**:
- GDPR (data export, deletion)
- CCPA (opt-out of data selling)
- COPPA (age verification, no <13)

### Security Headers

```python
# FastAPI middleware

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

---

## 14. DevOps & CI/CD

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/backend-deploy.yml

name: Backend CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest --cov=app tests/

      - name: Lint
        run: |
          pip install flake8
          flake8 app/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to AWS
        run: |
          # Build Docker image
          docker build -t mystic-backend .
          # Push to ECR
          # Deploy to ECS/EKS
```

### Docker Configuration

```dockerfile
# Dockerfile (Backend)

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 15. Monitoring & Analytics

### Error Tracking (Sentry)

```typescript
// Frontend

import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'https://xxx@sentry.io/xxx',
  environment: __DEV__ ? 'development' : 'production',
  tracesSampleRate: 0.2,
});
```

```python
# Backend

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://xxx@sentry.io/xxx",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
)
```

### Product Analytics (Mixpanel)

```typescript
// Track events

Mixpanel.track('Reading Completed', {
  type: 'coffee',
  symbols_count: 5,
  processing_time: 9.2,
  satisfaction: 5,
});

Mixpanel.track('Subscription Purchased', {
  tier: 'monthly',
  price: 14.99,
  trial: false,
});
```

### Key Metrics Dashboard

- **Acquisition**: Daily signups, source attribution
- **Engagement**: DAU/MAU, session duration, feature usage
- **Retention**: D1/D7/D30 retention cohorts
- **Revenue**: MRR, churn rate, LTV:CAC
- **Performance**: API latency p95, error rate, uptime

---

## Conclusion

This technical architecture provides a robust, scalable foundation for Mystic.ai MVP. Key strengths:

✅ **Modern Stack**: React Native + FastAPI = fast development
✅ **AI-First**: Multimodal AI (Vision + Text) is core, not an add-on
✅ **Scalable**: Microservices-ready, horizontal scaling
✅ **Secure**: GDPR-compliant, encrypted, rate-limited
✅ **Observable**: Sentry + DataDog + Mixpanel for full visibility

**Next Steps**:
1. Set up GitHub repository with this structure
2. Initialize React Native project
3. Set up FastAPI backend skeleton
4. Configure OpenAI API accounts
5. Create PostgreSQL + Redis on cloud provider
6. Build MVP in 3-month sprint

*Document maintained by Engineering Team*
*Last updated: 2026-01-12*
