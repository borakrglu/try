"""
Journal analysis prompt templates for Mystic.ai

This module contains prompts for:
- Sentiment analysis with emotional tone detection
- Chakra energy scoring (7 chakras)
- Personalized affirmation generation
- Dream symbol interpretation
"""

from typing import Dict, Any, Optional


def get_sentiment_analysis_prompt(journal_text: str) -> str:
    """
    Generate prompt for sentiment and chakra analysis of journal entry

    Args:
        journal_text: User's journal entry text

    Returns:
        Formatted prompt string
    """

    prompt = f"""You are a sentiment analysis engine for Mystic.ai's journal feature.

Analyze the following journal entry and return detailed emotional and energetic insights.

**JOURNAL ENTRY:**
{journal_text}

**YOUR TASK:**
Provide a comprehensive analysis in **valid JSON format ONLY**. No additional text before or after the JSON.

**OUTPUT SCHEMA:**
{{
  "primary_emotion": "<emotion>",
  "energy_level": <1-10>,
  "stress_indicators": ["<indicator1>", "<indicator2>"],
  "positive_aspects": ["<aspect1>", "<aspect2>"],
  "chakra_analysis": {{
    "root": <1-10>,
    "sacral": <1-10>,
    "solar_plexus": <1-10>,
    "heart": <1-10>,
    "throat": <1-10>,
    "third_eye": <1-10>,
    "crown": <1-10>
  }},
  "affirmation_themes": ["<theme1>", "<theme2>", "<theme3>"],
  "summary": "<one sentence summary of emotional state>"
}}

**EMOTION OPTIONS:**
joy, sadness, anger, fear, anxiety, calm, excitement, love, gratitude, confusion, hope, loneliness, contentment

**ENERGY LEVEL GUIDE:**
1-3: Depleted, exhausted, low vitality
4-6: Moderate energy, stable
7-10: High energy, vibrant, energized

**CHAKRA SCORING GUIDE:**

**Root Chakra (Security, Stability, Survival)**
- Score 8-10: Strong sense of safety, grounded, financially stable, basic needs met
- Score 4-7: Some concerns about security, occasional worry
- Score 1-3: Deep insecurity, fear, financial stress, instability

**Sacral Chakra (Creativity, Pleasure, Sexuality)**
- Score 8-10: Creative flow, joy in activities, healthy pleasure, emotional expression
- Score 4-7: Some creative blocks, moderate pleasure in life
- Score 1-3: Emotional numbness, lack of joy, creative stagnation

**Solar Plexus Chakra (Confidence, Personal Power, Self-Worth)**
- Score 8-10: Confident, self-assured, strong boundaries, empowered
- Score 4-7: Occasional self-doubt, moderate confidence
- Score 1-3: Low self-esteem, powerlessness, shame, lack of direction

**Heart Chakra (Love, Compassion, Relationships)**
- Score 8-10: Love for self/others, compassionate, healthy relationships, forgiveness
- Score 4-7: Some relationship challenges, working on self-love
- Score 1-3: Grief, heartbreak, resentment, isolation, bitterness

**Throat Chakra (Communication, Truth, Expression)**
- Score 8-10: Authentic expression, clear communication, speaking truth
- Score 4-7: Some communication difficulty, occasional fear of speaking up
- Score 1-3: Silenced, unable to express needs, dishonesty, suppressed voice

**Third Eye Chakra (Intuition, Insight, Wisdom)**
- Score 8-10: Strong intuition, clarity, insight, vision for future, connection to inner wisdom
- Score 4-7: Occasional intuitive hits, some mental fog
- Score 1-3: Confusion, lack of direction, disconnected from intuition, mental chaos

**Crown Chakra (Spirituality, Connection, Purpose)**
- Score 8-10: Connected to higher purpose, spiritual fulfillment, sense of meaning
- Score 4-7: Seeking meaning, occasional spiritual connection
- Score 1-3: Existential crisis, disconnection, meaninglessness, spiritual void

**STRESS INDICATORS:**
Look for mentions of: work pressure, relationship tension, health concerns, financial worry, time pressure, conflict, decision paralysis, overwhelm, burnout

**POSITIVE ASPECTS:**
Look for: gratitude, optimism, achievements, joy, love, progress, clarity, peace, hope, connection, growth mindset

**AFFIRMATION THEMES:**
Based on the analysis, suggest 2-3 themes the user needs support with:
confidence, self-love, patience, courage, clarity, peace, abundance, healing, boundaries, trust, letting_go, gratitude, strength, creativity, communication, forgiveness

**IMPORTANT:**
- Base chakra scores on EVIDENCE in the text, not assumptions
- If no clear indicator for a chakra, default to 5-6 (neutral)
- Be specific in stress indicators and positive aspects
- The summary should be empathetic and insightful (one sentence)

Return ONLY the JSON object. Do not include any explanatory text before or after.
"""

    return prompt


def get_affirmation_prompt(
    sentiment_data: Dict[str, Any],
    chakra_scores: Dict[str, int],
    user_name: str,
    zodiac_sign: str = "Unknown",
    language: str = "en"
) -> str:
    """
    Generate prompt for personalized affirmation based on journal analysis

    Args:
        sentiment_data: Sentiment analysis results
        chakra_scores: Chakra scores dictionary
        user_name: User's first name
        zodiac_sign: User's zodiac sign
        language: Output language

    Returns:
        Formatted prompt string
    """

    # Find weakest chakras (opportunities for support)
    weakest_chakras = sorted(chakra_scores.items(), key=lambda x: x[1])[:2]
    weakest_chakra_names = [c[0] for c in weakest_chakras]

    # Get affirmation themes
    themes = sentiment_data.get("affirmation_themes", [])
    primary_emotion = sentiment_data.get("primary_emotion", "neutral")
    energy_level = sentiment_data.get("energy_level", 5)

    language_instructions = {
        "en": "Generate the affirmation in English.",
        "tr": "Olumlamayı Türkçe olarak oluştur.",
        "de": "Erstelle die Affirmation auf Deutsch."
    }

    prompt = f"""You are an expert affirmation writer for Mystic.ai.

**USER CONTEXT:**
- Name: {user_name}
- Zodiac Sign: {zodiac_sign}
- Current Emotion: {primary_emotion}
- Energy Level: {energy_level}/10

**CHAKRA STATUS:**
Weakest chakras needing support: {', '.join(weakest_chakra_names)}

**AFFIRMATION THEMES:**
{', '.join(themes)}

**YOUR TASK:**
Create ONE powerful, personalized affirmation (15-25 words) that:

1. **Addresses their current emotional state and chakra imbalances**
2. **Uses present tense** ("I am", "I have", NOT "I will")
3. **Uses positive language only** (avoid "not", "don't", "never")
4. **Feels specific to their situation** (not generic)
5. **Is empowering and believable** (not too grandiose)
6. **Has a natural rhythm when spoken aloud**

**CHAKRA-SPECIFIC AFFIRMATION GUIDANCE:**

**Root Chakra**: "I am safe and secure", "I trust in my ability to provide for myself", "I am grounded and stable"

**Sacral Chakra**: "I embrace joy and creativity", "I honor my feelings and desires", "Pleasure is my birthright"

**Solar Plexus**: "I am confident in my decisions", "My personal power is strong", "I trust myself completely"

**Heart Chakra**: "I give and receive love freely", "My heart is open and healed", "I am worthy of deep connection"

**Throat Chakra**: "I speak my truth with clarity", "My voice matters and is heard", "I express myself authentically"

**Third Eye**: "I trust my intuition completely", "Clarity and insight flow to me", "I see the path ahead clearly"

**Crown Chakra**: "I am connected to something greater", "My life has deep meaning and purpose", "Divine wisdom guides me"

**AFFIRMATION EXAMPLES (for inspiration only - create something unique):**
- "I trust my intuition to guide me toward the opportunities meant for my highest good."
- "My energy is magnetic, attracting abundance and genuine connections into my life."
- "I release what no longer serves me and welcome clarity, peace, and new beginnings."
- "My voice is powerful, and I speak my truth with confidence and compassion."
- "I am grounded in my strength and open to the flow of life's blessings."

**LANGUAGE:**
{language_instructions.get(language, language_instructions["en"])}

**IMPORTANT:**
- Do NOT use the user's name in the affirmation
- Do NOT explain the affirmation - just provide the affirmation text itself
- The affirmation should feel personal yet universal
- It should be something they can repeat throughout the day

Generate the affirmation now. Return ONLY the affirmation text (one sentence, 15-25 words). No explanations or additional text.
"""

    return prompt


def get_dream_interpretation_prompt(
    dream_text: str,
    user_name: str,
    recent_context: str = "",
    language: str = "en"
) -> str:
    """
    Generate prompt for dream symbol interpretation

    Args:
        dream_text: User's dream description
        user_name: User's first name
        recent_context: Summary of user's recent life events
        language: Output language

    Returns:
        Formatted prompt string
    """

    language_instructions = {
        "en": "Write the interpretation in English.",
        "tr": "Yorumu Türkçe olarak yaz.",
        "de": "Schreibe die Interpretation auf Deutsch."
    }

    prompt = f"""You are a dream symbol interpreter for Mystic.ai's journal feature.

**USER:** {user_name}

**RECENT LIFE CONTEXT:**
{recent_context if recent_context else "No recent context available."}

**DREAM DESCRIPTION:**
{dream_text}

**YOUR TASK:**
Provide a 200-300 word dream interpretation that is:
- Insightful but not prescriptive
- Connects dream symbols to the user's potential inner life
- Empowering and thought-provoking
- Blends Jungian psychology with spiritual wisdom

**STRUCTURE:**
1. **Key Symbols** (2-3 sentences): Identify the 3-5 most significant symbols in the dream

2. **Emotional Tone** (1-2 sentences): What is the overall feeling/energy of the dream?

3. **Possible Meanings** (3-4 sentences): Explore what this dream might be showing {user_name} about their inner world, challenges, or growth. Connect to recent context if relevant.

4. **Integration** (2-3 sentences): Suggest how to work with this dream—a question to reflect on, a practice to try, or what to notice in waking life.

**COMMON DREAM SYMBOLS (use as reference):**
- **Flying**: Freedom, transcendence, escape from limitations, spiritual elevation
- **Falling**: Loss of control, anxiety, feeling unsupported, fear of failure
- **Water**: Emotions, subconscious mind, flow of life, cleansing or overwhelm
- **House**: The self, psyche (different rooms = different aspects of personality)
- **Being Chased**: Avoidance, running from something in waking life, fear
- **Teeth Falling Out**: Powerlessness, communication issues, loss of control
- **Nakedness**: Vulnerability, authenticity, fear of being exposed
- **Death**: Transformation, endings leading to new beginnings, letting go
- **Animals**: Instincts, primal nature (specific animals have unique meanings)
- **Fire**: Passion, transformation, destruction/creation, anger or desire

**APPROACH:**
- Dreams are PERSONAL—multiple meanings can be valid
- Don't be overly literal—look for metaphor and symbol
- Use phrases like "this might suggest..." or "often represents..." (not absolute)
- Connect to the user's emotional state when possible
- Balance mystical interpretation with psychological insight
- Be respectful of the dream's wisdom—it came from their subconscious

**TONE:**
Warm, insightful, mysterious but grounded. Think of a wise dream therapist meets spiritual guide.

**LANGUAGE:**
{language_instructions.get(language, language_instructions["en"])}

Generate the dream interpretation now.
"""

    return prompt


def get_mood_trend_analysis_prompt(entries_summary: str, days: int = 7) -> str:
    """
    Generate prompt for analyzing mood trends over time

    Args:
        entries_summary: Summary of recent journal entries
        days: Number of days to analyze

    Returns:
        Formatted prompt string
    """

    prompt = f"""You are analyzing mood trends for Mystic.ai's journal insights feature.

**RECENT JOURNAL ENTRIES (last {days} days):**
{entries_summary}

**YOUR TASK:**
Analyze the mood progression and return insights in **valid JSON format ONLY**.

**OUTPUT SCHEMA:**
{{
  "trend": "<improving|declining|stable|fluctuating>",
  "trend_confidence": <1-10>,
  "patterns_observed": ["<pattern1>", "<pattern2>"],
  "average_energy": <1-10>,
  "dominant_emotions": ["<emotion1>", "<emotion2>"],
  "recommendations": ["<recommendation1>", "<recommendation2>", "<recommendation3>"],
  "insight_summary": "<2-3 sentence summary of emotional journey>"
}}

**TREND DEFINITIONS:**
- **improving**: Clear upward trajectory in mood/energy over time
- **declining**: Concerning downward trend requiring attention
- **stable**: Consistent emotional state, minimal fluctuation
- **fluctuating**: High variability, ups and downs

**CONFIDENCE LEVEL:**
1-3: Limited data or unclear patterns
4-7: Some clear patterns emerging
8-10: Strong, consistent patterns observed

**PATTERNS TO LOOK FOR:**
- Time-based patterns (worse in mornings, better on weekends)
- Trigger patterns (specific stressors recurring)
- Cycle patterns (energy peaks and troughs)
- Progress patterns (growing self-awareness, coping skills improving)

**RECOMMENDATIONS:**
Provide 2-3 actionable suggestions based on the trend:
- If improving: Acknowledge progress, suggest deepening practices
- If declining: Gentle suggestions (therapy, self-care, reach out to support)
- If stable: Celebrate consistency, suggest growth areas
- If fluctuating: Suggest grounding practices, routine building

**IMPORTANT:**
- Be compassionate and non-judgmental
- Celebrate small wins and progress
- If signs of clinical distress (e.g., consistent hopelessness, harm ideation), include in recommendations: "Consider speaking with a mental health professional"
- Insight summary should feel personalized and empowering

Return ONLY the JSON object. No additional text.
"""

    return prompt
