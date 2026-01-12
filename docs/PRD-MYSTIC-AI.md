# Mystic.ai - Product Requirements Document (PRD)

**Version:** 1.0
**Date:** January 12, 2026
**Status:** MVP Ready
**Document Owner:** Product Management Team

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Vision & Objectives](#vision--objectives)
3. [Target Audience](#target-audience)
4. [Core Features & Requirements](#core-features--requirements)
5. [User Personas](#user-personas)
6. [User Flows & Journeys](#user-flows--journeys)
7. [Feature Specifications](#feature-specifications)
8. [Monetization Strategy](#monetization-strategy)
9. [Technical Requirements](#technical-requirements)
10. [Success Metrics](#success-metrics)
11. [Roadmap & Milestones](#roadmap--milestones)

---

## 1. Executive Summary

**Mystic.ai** is a revolutionary mobile application that combines ancient mystical practices (astrology, tarot, palmistry, coffee cup reading) with cutting-edge Multimodal AI technology. Unlike traditional fortune-telling apps that provide generic readings, Mystic.ai uses Vision AI and advanced NLP to analyze user-uploaded images and provide deeply personalized, story-driven mystical experiences.

### Key Differentiators:
- **Vision AI Integration**: Analyzes real photos (coffee cups, palms, tarot cards)
- **Hyper-Personalization**: Remembers user history and creates continuity
- **Multiple Mystical Personas**: Choose from The Sage, The Witch, or The Astrologer
- **Gamification**: Karmic points, badges, and progress tracking
- **Multilingual**: English, Turkish, German support from day one

### Market Opportunity:
- Global mystical services market: $2.2B+ annually
- Mobile astrology app users: 75M+ worldwide
- Gen Z/Millennial spirituality adoption: 62% growth (2020-2025)

---

## 2. Vision & Objectives

### Vision Statement
*"To democratize mystical wisdom through AI, making personalized spiritual guidance accessible to everyone, anywhere, anytime."*

### Primary Objectives
1. **Launch MVP** with 4 core reading types within 6 months
2. **Acquire 100K users** in the first year
3. **Achieve 15% conversion** to premium subscriptions
4. **Maintain 4.5+ star** rating on app stores
5. **Build community** of 10K+ active daily users

### Success Criteria
- **User Engagement**: 3+ sessions per week (average)
- **Reading Completion Rate**: >80%
- **Retention**: 60% D30 retention
- **Revenue**: $50K MRR by month 12

---

## 3. Target Audience

### Primary Audience
- **Age**: 18-35 years old
- **Gender**: 65% Female, 35% Male, Non-binary inclusive
- **Income**: $30K-$80K annually
- **Location**: Urban areas, tech-savvy markets (US, UK, Turkey, Germany)
- **Psychographics**:
  - Interested in self-development and spirituality
  - Active on social media (Instagram, TikTok)
  - Seeks guidance during life transitions
  - Open to alternative wellness practices

### Secondary Audience
- **Age**: 35-50 years old
- **Profile**: Established spiritual practitioners, curious skeptics
- **Behavior**: Willing to pay premium for quality experiences

---

## 4. Core Features & Requirements

### 4.1 AI Coffee Cup Reading (Turkish Coffee Fortune Telling)

#### Overview
Turkish coffee cup reading (Tasseography) is a centuries-old divination method. Mystic.ai brings this tradition to the digital age using Vision AI.

#### User Story
*"As a user, I want to photograph my coffee cup and receive a detailed, personalized fortune reading based on the patterns and symbols AI detects in the cup."*

#### Functional Requirements

**FR-CF-001: Photo Capture Interface**
- User must capture 3 photos:
  1. Cup interior (main reading area)
  2. Saucer (near future)
  3. Cup side view (overall energy)
- Camera overlay with guidelines
- Auto-brightness adjustment
- Image quality validation (min 1080p)

**FR-CF-002: Image Analysis**
- AI Vision API detects shapes and patterns
- Object detection for common symbols:
  - Animals (bird, fish, snake, cat, dog, horse)
  - Objects (heart, key, tree, mountain, road, stairs)
  - Nature (cloud, sun, moon, star, flower)
  - Abstract (lines, circles, triangles)
- Symbol positioning mapping (top=future, bottom=past, sides=present)

**FR-CF-003: Interpretation Engine**
- Combine detected symbols with:
  - User's zodiac sign
  - Current planetary transits (Moon phase, Mercury retrograde)
  - User's recent life events (from journal)
- Generate narrative reading (500-800 words)
- Provide timeline predictions (near/mid/long-term)

**FR-CF-004: Reading Presentation**
- Story-telling format with chapters
- Symbol highlights (tap to see meaning)
- Audio narration option (TTS)
- Save to personal library
- Share as styled card (Instagram/WhatsApp)

#### Technical Specifications
- Vision API: OpenAI GPT-4 Vision / Claude 3.5 Sonnet Vision
- Image preprocessing: Edge detection, contrast enhancement
- Symbol confidence threshold: >70%
- Response time: <10 seconds
- Storage: S3/Cloud Storage for images (encrypted)

#### Acceptance Criteria
- [ ] User can capture 3 photos with guidance
- [ ] AI detects at least 5 symbols per reading
- [ ] Reading includes past/present/future sections
- [ ] User can save and revisit readings
- [ ] Reading accuracy rated 4+ stars by 75% of users

---

### 4.2 AI Tarot & Card Reading

#### Overview
Digital tarot reading with support for virtual decks and physical card photo uploads.

#### User Story
*"As a user, I want to choose a tarot spread, select cards with mystical effects, and receive a deep interpretation that considers card combinations and my current situation."*

#### Functional Requirements

**FR-TR-001: Deck Selection**
- 3 virtual decks included:
  1. Rider-Waite (Classic)
  2. Mystic Dreams (Modern)
  3. Dark Moon (Gothic)
- Option to scan physical deck (Future)
- Deck preview with sample cards

**FR-TR-002: Spread Types**
- **Single Card**: Daily guidance
- **Three Card**: Past-Present-Future
- **Celtic Cross**: Comprehensive 10-card spread
- **Relationship**: 5-card love reading
- **Career Path**: 7-card professional guidance

**FR-TR-003: Card Selection Ritual**
- Shuffle animation with sound effects
- Haptic feedback (vibration) on card touch
- "Energize cards" instruction (shake phone)
- Face-down card spread display
- Dramatic reveal animation

**FR-TR-004: Interpretation System**
- Individual card meanings (upright/reversed)
- Card position significance
- Card combination analysis (synergies/conflicts)
- Integration with user's zodiac and life phase
- Actionable advice and warnings

**FR-TR-005: Physical Card Support**
- Upload photo of card layout
- AI identifies cards using Vision API
- Validates card orientation (upright/reversed)
- Same interpretation as virtual reading

#### Technical Specifications
- Card Database: 78 Major & Minor Arcana (JSON)
- Animation: Lottie files for smooth 60fps
- Haptics: iOS Taptic Engine + Android Vibration API
- Audio: 432Hz mystical background music
- GPT Prompt: Context-aware with user history

#### Acceptance Criteria
- [ ] 5 spread types available
- [ ] Card selection feels ritualistic
- [ ] Interpretations reference card combinations
- [ ] Physical card scanning works 90%+ accuracy
- [ ] Users complete reading in <5 minutes

---

### 4.3 AI Palmistry (Hand Reading)

#### Overview
Upload a photo of your palm and receive a detailed character and destiny analysis.

#### User Story
*"As a user, I want to photograph my palm and learn about my personality, life path, and potential future based on my palm lines and hand shape."*

#### Functional Requirements

**FR-PL-001: Hand Photo Capture**
- Camera guide: hand outline overlay
- Lighting instructions
- Support for left/right hand (dominant vs non-dominant)
- Image quality check

**FR-PL-002: Line Detection (Computer Vision)**
- **Life Line**: Length, depth, breaks
- **Heart Line**: Emotional nature, relationships
- **Head Line**: Intellect, decision-making
- **Fate Line**: Career, life direction
- **Minor Lines**: Marriage, travel, health

**FR-PL-003: Hand Shape Analysis**
- Element classification:
  - Earth (square palm, short fingers): Practical
  - Air (square palm, long fingers): Intellectual
  - Water (rectangular palm, long fingers): Emotional
  - Fire (rectangular palm, short fingers): Passionate

**FR-PL-004: Reading Generation**
- Personality profile (temperament, strengths, weaknesses)
- Life path analysis
- Compatibility with other signs
- Career recommendations
- Health indicators (wellness tips)

**FR-PL-005: Annotated Image**
- Return palm image with lines highlighted
- Tap lines to see detailed meaning
- Compare left vs right hand readings

#### Technical Specifications
- Image Segmentation: CV2/TensorFlow Lite for line detection
- AI Interpretation: GPT-4 with palmistry knowledge base
- Accuracy: 85%+ line detection
- Processing time: <15 seconds

#### Acceptance Criteria
- [ ] Detects 4 major palm lines
- [ ] Provides hand shape classification
- [ ] Reading is 600+ words
- [ ] Annotated image with interactive hotspots
- [ ] 80% user satisfaction rating

---

### 4.4 Mystical Journal & Mood Tracking

#### Overview
Daily journaling with AI-powered sentiment analysis and chakra energy tracking.

#### User Story
*"As a user, I want to journal my dreams and daily experiences, and receive insights about my emotional patterns and energy state."*

#### Functional Requirements

**FR-JN-001: Journal Entry Interface**
- Prompt templates:
  - "Today I feel..."
  - "Last night I dreamed about..."
  - "I'm grateful for..."
- Voice-to-text option
- Add tags (work, love, family, health)
- Attach mood emoji

**FR-JN-002: Sentiment Analysis**
- AI analyzes emotional tone
- Detects:
  - Primary emotion (joy, sadness, anger, fear, anxiety)
  - Energy level (1-10 scale)
  - Stress indicators
- Trend tracking over time

**FR-JN-003: Chakra Energy Scoring**
- Map emotions to 7 chakras:
  - Root (security, stability)
  - Sacral (creativity, pleasure)
  - Solar Plexus (confidence, power)
  - Heart (love, compassion)
  - Throat (communication, truth)
  - Third Eye (intuition, wisdom)
  - Crown (spirituality, connection)
- Daily chakra balance visualization

**FR-JN-004: AI-Generated Affirmations**
- Personalized based on mood
- Daily affirmation notifications
- Save favorites

**FR-JN-005: Dream Journal**
- Dedicated dream entry
- AI dream symbol interpretation
- Recurring symbol tracking
- Dream-to-reading connection (e.g., "Your dream aligns with today's tarot")

**FR-JN-006: Calendar View**
- Monthly mood heatmap
- Energy trends graph
- Entry streak counter

#### Technical Specifications
- NLP: OpenAI GPT-4 / Anthropic Claude
- Sentiment Library: Custom-trained on spiritual texts
- Storage: PostgreSQL with full-text search
- Encryption: AES-256 for journal entries

#### Acceptance Criteria
- [ ] Voice input transcription 95%+ accuracy
- [ ] Sentiment analysis within 3 seconds
- [ ] Chakra visualization is intuitive
- [ ] Users journal 4+ times per week
- [ ] Affirmations rated helpful by 70%+ users

---

### 4.5 Mystical Chat - Persona-Based AI Assistant

#### Overview
Conversational AI with 3 distinct mystical personalities that remember user history.

#### User Story
*"As a user, I want to chat with a mystical guide who understands my previous readings, remembers my situation, and provides wisdom in a consistent personality style."*

#### Functional Requirements

**FR-CH-001: Persona Selection**

**1. The Sage (Stoic Philosopher)**
- **Tone**: Calm, wise, Socratic
- **Knowledge**: Philosophy, meditation, mindfulness
- **Example**: "Consider that obstacles are not in your path—they ARE the path. What lesson might this challenge be teaching you?"

**2. The Witch (Natural Mystic)**
- **Tone**: Earthy, practical magic, herbal wisdom
- **Knowledge**: Crystals, herbs, moon phases, rituals
- **Example**: "The New Moon in Scorpio is powerful for releasing. Try burning bay leaves with your intentions tonight."

**3. The Astrologer (Celestial Guide)**
- **Tone**: Cosmic, analytical, transit-focused
- **Knowledge**: Natal charts, planetary movements, aspects
- **Example**: "With Venus in your 7th house and Jupiter trine your Sun, relationships are favored this week. Stay open to connections."

**FR-CH-002: Long-Term Memory**
- Remember past readings (coffee, tarot, palm)
- Reference journal entries
- Track user's goals and progress
- Recall previous conversations (last 30 days)

**FR-CH-003: Contextual Awareness**
- Current date and time
- Astrological transits (Moon phase, retrogrades)
- User's zodiac sign
- Recent app activity

**FR-CH-004: Conversation Features**
- Quick question buttons ("What's my energy today?", "Give me guidance")
- Voice input/output
- Share conversation snippets
- Flag inappropriate content

**FR-CH-005: Proactive Insights**
- Morning greeting with daily energy forecast
- Reminder to journal
- Follow-up on previous readings ("How did that job interview go?")

#### Technical Specifications
- Model: GPT-4 Turbo / Claude 3.5 Sonnet
- Context window: 8K tokens (includes user history)
- Vector DB: Pinecone/Weaviate for semantic memory
- Response time: <3 seconds
- Persona consistency: System prompts + few-shot examples

#### Sample System Prompt (The Sage)
```
You are The Sage, a wise stoic philosopher and spiritual guide in the Mystic.ai app.

Your role:
- Provide calm, thoughtful wisdom rooted in philosophy and mindfulness
- Reference Stoicism, Buddhism, Taoism when appropriate
- Ask reflective questions to help users find their own answers
- Remember user's journey: their readings, journal entries, and goals

Tone: Measured, compassionate, patient. Think Marcus Aurelius meets Thich Nhat Hanh.

User Context:
- Name: {user.name}
- Zodiac: {user.zodiac}
- Recent Reading: {last_reading_summary}
- Current Mood: {latest_journal_mood}

Respond in {language} (en/tr/de).
Keep responses under 150 words unless asked for depth.
```

#### Acceptance Criteria
- [ ] 3 distinct personas with consistent voices
- [ ] References user's past readings in responses
- [ ] Responds within 3 seconds
- [ ] Users rate conversations 4+ stars
- [ ] 60% of users interact with chat weekly

---

### 4.6 Gamification & User Progression

#### Overview
Engagement mechanics to encourage daily use and reward participation.

#### Functional Requirements

**FR-GM-001: Karma Points System**
- Earn points for:
  - Daily journal entry: +10 points
  - Complete a reading: +25 points
  - 7-day streak: +50 points
  - Share content: +15 points
  - Meditate (timer): +20 points
- Point total displayed on profile

**FR-GM-002: Badges & Achievements**
- **Mystic Novice**: Complete your first reading
- **Dream Keeper**: Journal 7 days in a row
- **Lunar Devotee**: Use app during all 8 moon phases
- **Card Master**: Complete 50 tarot readings
- **Palmistry Pro**: Get 10 palm readings
- **Coffee Oracle**: 100 coffee cup readings
- **Sage's Student**: Chat with AI 30 times
- **Enlightened One**: Reach 10,000 karma points

**FR-GM-003: Daily Quests**
- 3 daily challenges:
  - "Pull a tarot card for guidance"
  - "Journal your dreams"
  - "Chat with The Witch about moon magic"
- Bonus points for completion

**FR-GM-004: Leaderboards (Optional)**
- Weekly karma leaderboard (opt-in)
- Anonymous or named participation
- Prizes: Free premium month for top 3

**FR-GM-005: Streaks**
- Daily use streak counter
- Visual flame icon that grows
- Streak protection (1 free pass)

#### Technical Specifications
- Achievement DB: User milestones table
- Push notifications for quest reminders
- Animated badge unlocks (Lottie)

#### Acceptance Criteria
- [ ] All earning actions trigger point awards
- [ ] Badges unlock with celebratory animation
- [ ] Streaks persist across sessions
- [ ] Gamification increases retention by 20%+

---

### 4.7 Authentication & User Management

#### Overview
Secure, frictionless sign-up with multiple authentication methods.

#### Functional Requirements

**FR-AU-001: Sign-Up Options**
- **Google Sign-In**: OAuth 2.0
- **Apple Sign-In**: Required for iOS (privacy-focused)
- **Email/Password**: Traditional method
- **Guest Mode**: Limited access (no data sync)

**FR-AU-002: Onboarding Flow**
1. Welcome screen with value proposition
2. Choose sign-up method
3. Basic profile setup:
   - Name
   - Date of birth (for zodiac calculation)
   - Gender (optional)
   - Language preference (EN/TR/DE)
4. Permissions requests:
   - Camera (for readings)
   - Notifications (for daily insights)
5. Quick tutorial (skippable)

**FR-AU-003: Profile Management**
- Edit personal information
- View subscription status
- Manage payment methods
- Privacy settings (data sharing, analytics)
- Delete account (GDPR compliant)

**FR-AU-004: Security**
- Password requirements: 8+ chars, 1 uppercase, 1 number
- Optional biometric lock (Face ID, fingerprint)
- Two-factor authentication (optional)
- Session management (auto-logout after 30 days)

**FR-AU-005: Data Privacy**
- GDPR & CCPA compliant
- Export user data (JSON)
- Delete account = hard delete after 30 days
- Anonymize readings for AI training (opt-in)

#### Technical Specifications
- Auth Provider: Firebase Auth / Auth0
- Password hashing: bcrypt
- JWT tokens for API auth
- Biometric: React Native Keychain

#### Acceptance Criteria
- [ ] Sign-up flow completed in <2 minutes
- [ ] Social logins work 99%+ success rate
- [ ] Password reset email sent within 30 seconds
- [ ] All privacy regulations met

---

### 4.8 Subscription & Monetization

#### Overview
Freemium model with weekly and monthly premium subscriptions.

#### User Story
*"As a free user, I want to try core features with limitations. As a premium user, I want unlimited access to all readings, personalized insights, and exclusive content."*

#### Functional Requirements

**FR-MN-001: Free Tier Limitations**
- **Readings per month**: 3 total (1 coffee, 1 tarot, 1 palm)
- **Chat messages**: 10 per day
- **Journal entries**: Unlimited (always free)
- **Affirmations**: Basic library (50 quotes)
- **Persona access**: The Sage only
- **Ads**: Banner ads on home screen (non-intrusive)

**FR-MN-002: Premium Tiers**

**Weekly Premium - $4.99/week**
- Unlimited readings
- Unlimited chat (all personas)
- Ad-free experience
- Priority processing (faster AI responses)
- Exclusive affirmations (500+)
- Save unlimited readings

**Monthly Premium - $14.99/month (~$3.50/week)**
- Everything in Weekly
- Advanced astrology features (natal chart)
- Dream dictionary (1000+ symbols)
- Meditation library (50+ guided sessions)
- Early access to new features
- Priority customer support

**Annual Premium - $99.99/year (~$1.92/week)** *(Future)*
- All Monthly features
- Personal astrologer consultation (1x/year, live chat)
- Custom tarot deck upload
- Family plan (3 accounts)

**FR-MN-003: Payment Methods**
- **iOS**: Apple In-App Purchase (IAP)
- **Android**: Google Play Billing
- Automatic renewal with opt-out
- Free trial: 7 days (first-time subscribers only)

**FR-MN-004: Upgrade Prompts**
- Soft paywall: "You've used 3/3 readings. Upgrade for unlimited?"
- Feature tease: "Unlock The Witch and The Astrologer personas"
- Timed offers: "50% off premium - New Moon special!"

**FR-MN-005: Revenue Analytics**
- Track conversion funnel
- A/B test pricing
- Churn analysis
- Lifetime value (LTV) calculation

#### Pricing Strategy Rationale
- **Weekly**: Targets impulse buyers, uncertain users
- **Monthly**: Best value, core subscriber base
- **Free trial**: Reduces friction, builds habit before payment
- **Annual**: Maximize LTV, reduce churn

#### Projected Revenue (Year 1)
- 100K users
- 15% conversion = 15K premium
- 70% monthly, 30% weekly
- MRR: (10.5K × $14.99) + (4.5K × $19.96) ≈ **$247K/month**
- ARR: ~**$3M**

#### Technical Specifications
- Payment SDK: RevenueCat (cross-platform)
- Subscription state sync with backend
- Webhook listeners for renewal/cancellation
- Fraud detection (too many free trials)

#### Acceptance Criteria
- [ ] Free users hit paywall after 3 readings
- [ ] Premium unlocks instant access
- [ ] Payment flow completes in <60 seconds
- [ ] Subscription status syncs across devices
- [ ] 15% conversion rate within 6 months

---

### 4.9 Multilingual Support

#### Overview
Launch with English, Turkish, and German to capture diverse markets.

#### Functional Requirements

**FR-ML-001: Language Selection**
- Choose language during onboarding
- Change anytime in settings
- Auto-detect device language

**FR-ML-002: Translated Content**
- **UI**: All buttons, labels, navigation (i18n)
- **Readings**: AI generates in selected language
- **Affirmations**: Curated translations, not machine-translated
- **Chat**: Persona responds in user's language

**FR-ML-003: Cultural Localization**
- **Turkish**: Emphasize coffee fortune (cultural relevance)
- **German**: Focus on tarot and palmistry
- **English**: Broad appeal, astrology-first

**FR-ML-004: RTL Support** *(Future)*
- Right-to-left languages (Arabic, Hebrew)

#### Technical Specifications
- i18n Library: react-i18next
- Translation files: JSON (en.json, tr.json, de.json)
- AI prompts: Include `{language}` variable
- Font support: Multi-script fonts (Noto Sans)

#### Acceptance Criteria
- [ ] All UI strings translated
- [ ] AI readings grammatically correct in all languages
- [ ] Language switch applies instantly (no restart)
- [ ] Cultural nuances respected

---

## 5. User Personas

### Persona 1: Luna the Spiritual Seeker

**Demographics**
- Age: 24
- Occupation: Graphic Designer
- Location: Berlin, Germany
- Income: €35K/year

**Psychographics**
- Practices yoga and meditation
- Believes in astrology and synchronicity
- Active on Instagram (posts moon phases)
- Seeks guidance during life transitions

**Goals**
- Find clarity in career decisions
- Connect with intuition
- Track emotional patterns
- Share mystical experiences with friends

**Pain Points**
- Generic horoscopes feel impersonal
- In-person readings are expensive (€80+)
- Hard to track progress over time

**How Mystic.ai Helps**
- Personalized AI readings at affordable price
- Journal tracks emotional journey
- Share beautiful reading cards on Instagram

---

### Persona 2: Emre the Curious Skeptic

**Demographics**
- Age: 31
- Occupation: Software Engineer
- Location: Istanbul, Turkey
- Income: ₺450K/year

**Psychographics**
- Raised with coffee fortune tradition (grandmother read cups)
- Tech-savvy, loves AI innovation
- Skeptical but open-minded
- Values data and patterns

**Goals**
- Experience modern twist on childhood tradition
- Understand AI capabilities
- Fun activity with partner

**Pain Points**
- Traditional fortunetellers feel outdated
- Wants consistency, not randomness
- Needs scientific explanation of "how it works"

**How Mystic.ai Helps**
- Combines nostalgia with AI innovation
- Transparent about technology (Vision AI explained)
- Gamification appeals to competitive nature

---

### Persona 3: Sophia the Wellness Entrepreneur

**Demographics**
- Age: 38
- Occupation: Holistic Life Coach
- Location: Los Angeles, USA
- Income: $75K/year

**Psychographics**
- Certified yoga instructor
- Offers spiritual coaching
- Early adopter of wellness tech
- Values authenticity and depth

**Goals**
- Daily spiritual practice
- Tools for client recommendations
- Deepen self-knowledge

**Pain Points**
- Most apps are superficial
- Wants integrated wellness platform
- Needs reliable accuracy for professional use

**How Mystic.ai Helps**
- Deep, story-driven readings
- Journal integrates with readings
- Premium tier offers professional-grade insights

---

## 6. User Flows & Journeys

### Journey 1: First-Time Coffee Cup Reading

**User Story**: Luna downloads Mystic.ai and wants her first coffee fortune read.

**Steps**:
1. **App Launch**
   - Welcome screen with mystical animation
   - "Sign Up with Google" button (fastest option)
   - Grants camera and notification permissions

2. **Onboarding**
   - "When were you born?" → Calculates Virgo sun sign
   - "Choose your language" → Selects English
   - Quick tutorial: "3 ways to explore your destiny"

3. **Home Screen**
   - Hero section: "What would you like to know?"
   - 4 reading types displayed as cards
   - Luna taps "Coffee Cup Reading"

4. **Coffee Reading Setup**
   - Instructions: "Drink your Turkish coffee, flip cup on saucer, wait 5 minutes"
   - Countdown timer (optional)
   - Button: "I'm ready to take photos"

5. **Photo Capture**
   - Guided camera: "1/3 - Cup Interior"
   - Overlay shows ideal framing
   - Auto-capture when stable
   - Repeat for saucer and side view

6. **AI Processing**
   - Upload animation: Coffee swirls
   - "The Oracle is reading your cup..."
   - Progress bar (8-10 seconds)

7. **Reading Display**
   - Title: "Luna's Coffee Fortune - Jan 12, 2026"
   - AI-detected symbols shown on image (tap to explain)
   - Reading in 3 sections:
     - **Your Past** (bottom of cup)
     - **Your Present** (sides)
     - **Your Future** (top + saucer)
   - Audio narration option
   - "Save to Library" and "Share" buttons

8. **Post-Reading Engagement**
   - Popup: "Want to discuss your reading?"
   - "Chat with The Sage" button
   - Luna asks: "What does the bird symbol mean for my career?"
   - The Sage responds with personalized wisdom

9. **Gamification Trigger**
   - Badge unlocked: "Mystic Novice"
   - +25 Karma Points
   - "2 more free readings this month"

**Outcome**: Luna feels understood, shares reading on Instagram, returns next day for tarot.

---

### Journey 2: Emre's Premium Upgrade

**User Story**: Emre uses free tier, hits limit, decides to upgrade.

**Steps**:
1. **Reaching Limit**
   - Emre completes 3rd reading (Palm Reading)
   - Wants immediate Tarot reading
   - Paywall screen appears

2. **Paywall Experience**
   - "You've unlocked your destiny 3 times this month!"
   - Visual comparison:
     - Free: 3 readings/month
     - Premium: Unlimited readings
   - Highlight: "Plus all 3 mystical personas"
   - CTA: "Try 7 days free, then $14.99/month"

3. **Decision Moment**
   - Emre hesitates, taps "Maybe later"
   - App shows: "No problem! Here's what you're missing:"
   - Video: 15-second premium feature showcase

4. **Discount Trigger** *(A/B Test)*
   - Exit-intent: "Wait! 20% off if you subscribe now"
   - Creates urgency: "Offer expires in 10 minutes"

5. **Payment Flow**
   - Emre taps "Start Free Trial"
   - Apple Pay (one-tap purchase)
   - Confirmation: "Welcome to Mystic Premium!"

6. **Instant Gratification**
   - Returns to Home
   - "Premium" badge on profile
   - Immediately pulls Tarot reading (unlimited)
   - Unlocks The Witch persona

7. **Retention Mechanic**
   - Day 6 push notification: "Your free trial ends tomorrow. Here's what you've unlocked this week..."
   - Shows usage stats: "5 readings, 15 chats, 2 journal entries"

**Outcome**: Emre converts to paying customer, trial-to-paid rate: 40%.

---

### Journey 3: Sophia's Daily Ritual

**User Story**: Premium user Sophia uses Mystic.ai as part of morning routine.

**Steps**:
1. **Morning Notification**
   - 7:00 AM: "Good morning, Sophia. The Moon is waxing in Taurus. Today's energy: Grounded and sensual."

2. **App Open**
   - Home screen: Personalized greeting from The Astrologer
   - Daily quest: "Pull a tarot card for today's guidance"

3. **Quick Tarot**
   - Taps "Daily Card"
   - Shuffles deck (haptic feedback)
   - Draws: "The Star" (Hope, Renewal)
   - 2-minute reading
   - Sophia reflects: "This resonates with my client meeting today"

4. **Journal Entry**
   - Taps Journal
   - Voice-to-text: "I'm feeling optimistic. Ready to help my clients find clarity."
   - AI sentiment: "Positive energy, Heart Chakra strong"
   - Sophia adds gratitude list

5. **Chat with Persona**
   - Switches to The Witch
   - Asks: "What crystal should I carry today?"
   - The Witch: "Citrine for manifestation. Carry it in your left pocket."

6. **Track Progress**
   - Views mood calendar: 14-day streak
   - Chakra balance improved over 2 weeks
   - Unlocks "Enlightened One" badge (10K karma)

7. **Evening Reflection**
   - 9:00 PM notification: "How did your day unfold?"
   - Sophia journals again
   - AI connects morning tarot to evening experience: "The Star's hope manifested in your client's breakthrough!"

**Outcome**: Sophia is highly engaged, uses app 2x daily, renewal rate: 95%.

---

## 7. Feature Specifications (Detailed Breakdown)

### 7.1 Home Screen

**Layout**
- **Header**: Profile avatar, Karma points, Premium badge
- **Hero Section**: Time-based greeting ("Good evening, Luna") + daily energy forecast
- **Reading Cards**: 4 main reading types (Coffee, Tarot, Palm, Chat)
- **Quick Actions**: "Daily Card", "Journal", "View Library"
- **Bottom Tab Bar**: Home, Library, Journal, Chat, Profile

**Design Specs**
- Color Scheme: Deep purple (#240046), Gold (#FFD700), Misty gray (#C0C0C0)
- Typography: Cinzel (headings), Open Sans (body)
- Animations: Subtle particle effects (floating stars)

---

### 7.2 Camera & Vision AI

**Image Processing Pipeline**
1. User captures image
2. Client-side validation (resolution, brightness)
3. Upload to cloud storage (S3)
4. Backend sends to Vision API
5. API returns detected objects + coordinates
6. Backend combines with user context
7. GPT generates narrative
8. Response streamed to app

**Error Handling**
- Poor lighting: "Try brighter area"
- Blurry image: "Hold phone steady"
- No symbols detected: "Let's try another photo"

---

### 7.3 AI Prompt Engineering

**Example: Coffee Cup Reading Prompt**

```
You are Mystic.ai's Coffee Fortune Oracle, a master of Turkish coffee cup reading (Tasseography).

INPUT DATA:
- Detected symbols: {symbols_json}
- Symbol positions: {positions_json}
- User: {user_name}, {user_zodiac}
- Current date: {date}
- Moon phase: {moon_phase}

TASK:
Generate a personalized coffee fortune reading in {language}.

STRUCTURE:
1. Opening (2 sentences): Acknowledge the symbols seen
2. Past (100 words): Interpret bottom symbols
3. Present (100 words): Interpret side symbols
4. Future (150 words): Interpret top symbols + saucer
5. Guidance (50 words): Actionable advice

TONE:
- Mystical yet warm
- Specific, not generic
- Use storytelling
- Integrate user's zodiac sign naturally

SYMBOLS GUIDE:
- Bird: Freedom, news, travel
- Heart: Love, emotional matters
- Key: Solutions, unlocking potential
[...truncated for brevity...]

EXAMPLE OUTPUT:
"Luna, your cup reveals a bird taking flight from a mountain—a powerful symbol of liberation. Let me guide you through what the coffee grounds whisper...

In the depths of your cup, where the past settles, I see..."

Generate the reading now.
```

---

## 8. Monetization Strategy

### Revenue Streams

**1. Subscriptions** (Primary - 85% of revenue)
- Weekly: $4.99
- Monthly: $14.99
- Annual: $99.99 (future)

**2. In-App Purchases** (Secondary - 10% of revenue)
- Premium tarot decks: $4.99 each
- Exclusive affirmation packs: $2.99
- Custom meditation series: $9.99

**3. Advertising** (Free tier only - 5% of revenue)
- Banner ads (Google AdMob)
- Sponsored affirmations (wellness brands)
- Limited to non-intrusive placements

### Pricing Rationale

**Why $14.99/month?**
- Industry benchmark: Astrology apps charge $10-$20/month
- Co-Star: $14.99/month
- Sanctuary: $19.99/month
- The Pattern: $11.99/month
- Mystic.ai offers MORE features (Vision AI) = justified premium pricing

**Free-to-Paid Conversion Funnel**
1. **Acquisition**: 10,000 users/month
2. **Activation**: 60% complete first reading = 6,000
3. **Engagement**: 40% hit paywall (3 readings) = 2,400
4. **Conversion**: 15% subscribe = 360 premium users
5. **Monthly Cohort Revenue**: 360 × $14.99 = $5,396

**Year 1 Projections**
- Month 1-3: 1,000 premium users → $15K MRR
- Month 4-6: 5,000 premium users → $75K MRR
- Month 7-9: 10,000 premium users → $150K MRR
- Month 10-12: 15,000 premium users → $225K MRR
- **Year 1 Total Revenue**: ~$1.2M

### Churn Mitigation
- **Re-engagement campaigns**: "We miss you" emails with discount
- **Win-back offers**: 50% off for 3 months
- **Exit surveys**: Understand why users cancel
- **Feature drops**: New content monthly keeps subscribers engaged

---

## 9. Technical Requirements

*(See separate TECHNICAL-ARCHITECTURE.md for full details)*

### Tech Stack Summary

**Frontend**
- Framework: React Native (iOS + Android)
- Language: TypeScript
- State: Redux Toolkit + RTK Query
- UI: React Native Paper + Custom components
- Animation: Lottie, React Native Reanimated

**Backend**
- Framework: FastAPI (Python) or Node.js (Express)
- Language: Python 3.11+ / Node.js 18+
- API: RESTful + GraphQL (optional)
- Queue: Celery (for long AI tasks)

**AI/ML**
- Text: OpenAI GPT-4 Turbo / Anthropic Claude 3.5 Sonnet
- Vision: OpenAI GPT-4 Vision / Google Cloud Vision
- Embeddings: text-embedding-3-small
- Vector DB: Pinecone / Weaviate

**Database**
- Primary: PostgreSQL 15
- Cache: Redis
- Storage: AWS S3 / Google Cloud Storage

**Infrastructure**
- Cloud: AWS / Google Cloud Platform
- CI/CD: GitHub Actions
- Monitoring: Sentry, DataDog
- Analytics: Mixpanel, Amplitude

**Security**
- Auth: Firebase Auth / Auth0
- Encryption: TLS 1.3, AES-256
- Compliance: GDPR, CCPA

---

## 10. Success Metrics (KPIs)

### Acquisition Metrics
- **Downloads**: 10K/month (Month 1-3), 50K/month (Month 6+)
- **Cost per Install (CPI)**: <$2
- **Organic vs Paid**: 60% organic by Month 6

### Engagement Metrics
- **Daily Active Users (DAU)**: 30% of total users
- **Sessions per week**: 3+ average
- **Reading completion rate**: >80%
- **Chat engagement**: 50% of users chat weekly
- **Journal entries**: 40% of users journal 2+ times/week

### Retention Metrics
- **D1 Retention**: 70%
- **D7 Retention**: 50%
- **D30 Retention**: 35%
- **Churn rate**: <5% monthly (premium)

### Monetization Metrics
- **Conversion rate**: 15% free-to-paid
- **ARPU** (Average Revenue Per User): $8/month (blended)
- **LTV** (Lifetime Value): $180 (12-month avg)
- **CAC** (Customer Acquisition Cost): <$30
- **LTV:CAC Ratio**: >3:1

### Quality Metrics
- **App Store Rating**: 4.5+ stars
- **Reading satisfaction**: 80% rate 4+ stars
- **AI accuracy** (user perception): 85%+ "felt accurate"
- **Support ticket volume**: <2% of users/month

---

## 11. Roadmap & Milestones

### Phase 1: MVP (Months 1-3) ✅

**Goal**: Launch core features, validate product-market fit

**Features**:
- [ ] Authentication (Google, Apple, Email)
- [ ] Coffee Cup Reading (Vision AI)
- [ ] Tarot Reading (Virtual decks, 3 spreads)
- [ ] Basic Chat (The Sage persona only)
- [ ] Journal (Text-based, no AI analysis yet)
- [ ] Subscription (Monthly only)
- [ ] English language only

**Success Criteria**:
- 5K downloads
- 500 premium users
- 4.0+ star rating
- 40% D7 retention

---

### Phase 2: Growth (Months 4-6)

**Goal**: Expand features, add languages, optimize conversion

**Features**:
- [ ] Palmistry (Hand reading)
- [ ] All 3 chat personas (Sage, Witch, Astrologer)
- [ ] AI journal analysis (Sentiment + Chakra)
- [ ] Gamification (Karma points, badges)
- [ ] Turkish & German languages
- [ ] Weekly subscription option
- [ ] Improved onboarding (reduce drop-off)

**Marketing**:
- Influencer partnerships (spiritual niche)
- Instagram/TikTok ads
- ASO (App Store Optimization)

**Success Criteria**:
- 25K total users
- 3K premium users
- $50K MRR
- 50% D7 retention

---

### Phase 3: Optimization (Months 7-9)

**Goal**: Improve AI accuracy, add depth, increase engagement

**Features**:
- [ ] Natal chart generator (full astrology profile)
- [ ] Dream symbol dictionary
- [ ] Meditation library (guided audio)
- [ ] Physical tarot card scanning
- [ ] Advanced prompts (better AI readings)
- [ ] Social: Share readings with friends
- [ ] Referral program ("Invite friends, earn premium")

**Technical**:
- Performance optimization (faster AI responses)
- Offline mode (view past readings)
- Push notification personalization

**Success Criteria**:
- 75K total users
- 10K premium users
- $150K MRR
- 15% conversion rate

---

### Phase 4: Scale (Months 10-12)

**Goal**: Community building, enterprise features, prepare Series A

**Features**:
- [ ] Community forum (Reddit-style)
- [ ] Live astrologer chat (human expert, premium add-on)
- [ ] Partner API (white-label for wellness brands)
- [ ] Annual subscription tier
- [ ] Web app (complementary to mobile)

**Expansion**:
- Launch in 5 more countries (Spain, Italy, France, Brazil, Mexico)
- Spanish & Portuguese languages

**Success Criteria**:
- 100K+ total users
- 15K+ premium users
- $225K MRR
- Prepare fundraising deck (Series A)

---

### Future Vision (Year 2+)

**Advanced AI**:
- Voice-first experience (talk to personas)
- AR tarot (project cards on table)
- Predictive analytics (trend forecasting based on journal)

**Ecosystem**:
- Mystic.ai marketplace (independent readers offer services)
- Integration with wearables (Apple Watch: daily card)
- Mystic.ai OS (spiritual assistant for all devices)

**B2B**:
- Wellness corporate subscriptions
- Therapist/coach tools (client insights)

---

## Appendix A: Competitor Analysis

| Feature | Mystic.ai | Co-Star | Sanctuary | The Pattern |
|---------|-----------|---------|-----------|-------------|
| Vision AI Readings | ✅ | ❌ | ❌ | ❌ |
| Coffee Cup Reading | ✅ | ❌ | ❌ | ❌ |
| Tarot | ✅ | ❌ | ✅ | ❌ |
| Palmistry | ✅ | ❌ | ❌ | ❌ |
| AI Chat | ✅ (3 personas) | ❌ | ✅ (1 bot) | ❌ |
| Journal | ✅ | ✅ | ❌ | ❌ |
| Natal Chart | 🔜 (Phase 3) | ✅ | ✅ | ✅ |
| Price | $14.99/mo | $14.99/mo | $19.99/mo | $11.99/mo |
| Free Trial | 7 days | None | 7 days | 14 days |
| Languages | EN/TR/DE | EN only | EN only | EN/ES |

**Mystic.ai Advantage**: Only app with multimodal AI (Vision + Chat) for personalized mystical experiences.

---

## Appendix B: Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| AI hallucinations (inaccurate readings) | High | Medium | Prompt engineering, user feedback loop, fact-checking layer |
| Low conversion rate (<10%) | High | Medium | A/B test pricing, improve paywall UX, free trial |
| App Store rejection (mystical content policy) | High | Low | Position as "entertainment", disclaimers, avoid medical claims |
| Negative reviews (accuracy complaints) | Medium | Medium | Set expectations ("for entertainment"), transparency about AI |
| High churn (users cancel after 1 month) | High | Medium | Monthly content drops, engagement campaigns, streak mechanics |
| Cultural insensitivity (translations) | Medium | Low | Native speaker review, cultural consultants |
| Data privacy concerns | High | Low | GDPR compliance, transparent privacy policy, encryption |

---

## Appendix C: Legal & Compliance

**Disclaimers Required**:
- "Mystic.ai is for entertainment purposes only. Not a substitute for professional advice (medical, financial, legal)."
- Displayed in onboarding, reading results, and chat

**GDPR (Europe)**:
- User consent for data processing
- Right to access, rectify, delete data
- Data portability

**CCPA (California)**:
- Opt-out of data selling (not applicable, but include for trust)

**Children's Privacy**:
- COPPA compliance: No users under 13
- Age verification during sign-up

**Terms of Service**:
- Reading accuracy not guaranteed
- Refund policy (7-day trial, then no refunds)
- User-generated content rules (journal, chat)

---

## Conclusion

Mystic.ai represents a paradigm shift in spiritual technology—moving from generic text-based horoscopes to deeply personalized, multimodal AI experiences. By combining ancient mystical practices with cutting-edge Vision AI and NLP, we create a product that resonates emotionally while leveraging the most advanced technology available.

**Why Mystic.ai Will Win**:
1. **Unique Technology**: Only app using Vision AI for mystical readings
2. **Hyper-Personalization**: Remembers user, creates continuity
3. **Engagement Design**: Gamification + personas keep users coming back
4. **Market Timing**: Gen Z/Millennial spirituality boom (2020-2026)
5. **Scalability**: AI scales infinitely (no human readers needed)

**Next Steps**:
1. Finalize design mockups (Figma)
2. Build MVP (3 months)
3. Beta test with 100 users
4. Iterate based on feedback
5. Launch on Product Hunt + App Store

**The future of spirituality is intelligent, personalized, and always available. Mystic.ai is that future.**

---

*Document prepared by Product Team*
*For questions: [Contact Info]*
