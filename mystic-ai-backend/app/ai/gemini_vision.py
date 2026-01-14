"""
Gemini Vision Service - Image analysis for readings (FREE!)
Replacement for OpenAI GPT-4 Vision
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import logging
import json
import re
from PIL import Image
import io
import base64
import httpx

from app.config import settings

logger = logging.getLogger(__name__)


class GeminiVisionService:
    """Service for analyzing images with Google Gemini Vision (FREE!)"""

    def __init__(self):
        """Initialize Gemini Vision service"""
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Gemini 1.5 Flash has vision capabilities and is FREE!
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def detect_coffee_symbols(
        self,
        image_url: str,
        image_type: str = "cup"
    ) -> List[Dict[str, Any]]:
        """
        Detect symbols in a coffee cup image using Gemini Vision

        Args:
            image_url: URL or base64 of the coffee cup image
            image_type: Type of image (cup, saucer, side)

        Returns:
            List of detected symbols with their properties
        """
        prompt = self._get_coffee_detection_prompt(image_type)

        try:
            logger.info(f"Analyzing coffee cup image ({image_type}) with Gemini Vision")

            # Load image
            image = await self._load_image(image_url)

            # Generate content with image
            response = await self._generate_vision_async(
                prompt=prompt,
                image=image,
                temperature=0.3  # Lower temp for more consistent detection
            )

            content = response.text
            logger.info(f"Gemini Vision response: {content[:200]}...")

            # Try to extract symbols from response
            symbols = self._parse_symbols_from_response(content)

            logger.info(f"Detected {len(symbols)} symbols in {image_type}")
            return symbols

        except Exception as e:
            logger.error(f"Gemini Vision error: {str(e)}")
            # Return empty list on error, don't fail the reading
            return []

    async def detect_palm_lines(
        self,
        image_url: str,
        hand_type: str = "right"
    ) -> Dict[str, Any]:
        """
        Detect palm lines in a hand image using Gemini Vision

        Args:
            image_url: URL or base64 of the palm image
            hand_type: Type of hand (left, right)

        Returns:
            Dictionary with detected palm line information
        """
        prompt = self._get_palm_detection_prompt(hand_type)

        try:
            logger.info(f"Analyzing palm image ({hand_type} hand) with Gemini Vision")

            # Load image
            image = await self._load_image(image_url)

            # Generate content with image
            response = await self._generate_vision_async(
                prompt=prompt,
                image=image,
                temperature=0.3
            )

            content = response.text
            logger.info(f"Palm detection response received")

            # Parse palm line data
            palm_data = self._parse_palm_data_from_response(content)

            return palm_data

        except Exception as e:
            logger.error(f"Palm detection error: {str(e)}")
            return {}

    async def _load_image(self, image_url: str) -> Image.Image:
        """
        Load image from URL or base64 string

        Args:
            image_url: URL or base64 string

        Returns:
            PIL Image object
        """
        try:
            if image_url.startswith('data:image'):
                # Extract base64 data
                base64_data = image_url.split(',')[1]
                image_bytes = base64.b64decode(base64_data)
                image = Image.open(io.BytesIO(image_bytes))
            elif image_url.startswith('http'):
                # Download from URL
                async with httpx.AsyncClient() as client:
                    response = await client.get(image_url)
                    response.raise_for_status()
                    image = Image.open(io.BytesIO(response.content))
            else:
                # Assume it's a local file path
                image = Image.open(image_url)

            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')

            return image

        except Exception as e:
            logger.error(f"Failed to load image: {str(e)}")
            raise

    async def _generate_vision_async(
        self,
        prompt: str,
        image: Image.Image,
        temperature: float = 0.7
    ) -> Any:
        """
        Generate content with image using Gemini Vision

        Args:
            prompt: Text prompt
            image: PIL Image object
            temperature: Sampling temperature

        Returns:
            Gemini response object
        """
        import asyncio

        generation_config = {
            'temperature': temperature,
            'max_output_tokens': 2048,
            'top_p': 0.95,
            'top_k': 40
        }

        # Run in executor since Gemini SDK is sync
        loop = asyncio.get_event_loop()

        response = await loop.run_in_executor(
            None,
            lambda: self.model.generate_content(
                [prompt, image],
                generation_config=generation_config
            )
        )

        return response

    def _get_coffee_detection_prompt(self, image_type: str) -> str:
        """Get prompt for coffee symbol detection"""
        return f"""You are an expert in Turkish coffee cup reading (Tasseography).

Analyze this coffee cup image ({image_type}) and identify all visible shapes and symbols.

Look for common symbols:
- Animals: bird, fish, snake, cat, dog, horse, butterfly, spider
- Objects: heart, key, tree, mountain, road, stairs, ring, anchor, bridge, house
- Nature: cloud, sun, moon, star, flower, water, lightning, wave
- Abstract: lines, circles, triangles, spirals, arrows, crosses

For each symbol you detect, provide:
1. symbol: Name of the symbol
2. position: Location in the cup (top-left, top-center, top-right, center-left, center, center-right, bottom-left, bottom-center, bottom-right)
3. clarity: How clear the symbol is (1-10 scale, where 10 is very clear)
4. description: Brief description of the symbol's appearance
5. size: relative size (small, medium, large)

Return your response in this JSON format:
[
  {{"symbol": "bird", "position": "top-right", "clarity": 8, "description": "Bird with wings spread, facing upward", "size": "medium"}},
  {{"symbol": "road", "position": "center-left", "clarity": 6, "description": "Winding path ascending", "size": "large"}}
]

Be thorough but only include symbols you can clearly see. If you see very few or no clear symbols, return an empty array []."""

    def _get_palm_detection_prompt(self, hand_type: str) -> str:
        """Get prompt for palm line detection"""
        return f"""You are a palmistry expert. Analyze this {hand_type} hand image comprehensively.

**MAJOR PALM LINES:**
1. **Life Line**: Curves around thumb base (vitality, life energy)
2. **Heart Line**: Horizontal across top palm (emotions, relationships)
3. **Head Line**: Horizontal across middle palm (intellect, thinking)
4. **Fate Line**: Vertical up palm center (career, life path) - may be absent

For each line detected, describe:
- length: short, medium, long
- depth: faint, medium, deep
- quality: clear, broken, chained, forked, islanded
- characteristics: List notable features (e.g., "deep and clear", "curves upward", "breaks near center")

**HAND SHAPE TYPE:**
Determine the hand element type:
- **Earth Hand**: Square palm + short fingers (practical, grounded)
- **Air Hand**: Square palm + long fingers (intellectual, communicative)
- **Fire Hand**: Rectangular palm + short fingers (energetic, passionate)
- **Water Hand**: Rectangular palm + long fingers (emotional, intuitive)

**FINGER ANALYSIS:**
Relative lengths compared to each other:
- Index finger (Jupiter): leadership, ambition
- Middle finger (Saturn): responsibility, balance
- Ring finger (Apollo): creativity, expression
- Pinky finger (Mercury): communication, intelligence

Describe as: "Index slightly longer than ring" or "All fingers balanced"

**PALM MOUNTS:** (if visible as elevated areas)
Note prominence of these areas:
- Venus (base of thumb): love, passion
- Jupiter (below index): ambition, confidence
- Saturn (below middle): wisdom, discipline
- Apollo (below ring): creativity, success
- Mercury (below pinky): communication
- Upper Mars (below Mercury): mental resilience
- Lower Mars (above Venus): physical courage
- Moon (opposite thumb): imagination, intuition

Return comprehensive JSON:
{{
  "hand_shape": "Earth Hand",
  "palm_type": "square",
  "finger_length_overall": "short relative to palm",
  "lines": [
    {{
      "name": "Heart Line",
      "present": true,
      "characteristics": ["long", "deep", "curves upward toward index", "clear and unbroken"]
    }},
    {{
      "name": "Head Line",
      "present": true,
      "characteristics": ["medium length", "straight", "deep", "separate start from life line"]
    }},
    {{
      "name": "Life Line",
      "present": true,
      "characteristics": ["long and sweeping", "deep", "clear", "wide curve"]
    }},
    {{
      "name": "Fate Line",
      "present": false,
      "characteristics": []
    }}
  ],
  "fingers": {{
    "index": {{"relative_length": "Average"}},
    "middle": {{"relative_length": "Longest"}},
    "ring": {{"relative_length": "Slightly shorter than index"}},
    "pinky": {{"relative_length": "Short"}}
  }},
  "mounts": {{
    "Venus": "Prominent",
    "Jupiter": "Average",
    "Saturn": "Flat",
    "Apollo": "Slightly prominent",
    "Mercury": "Average",
    "Moon": "Well-developed"
  }},
  "overall_impression": "Strong, practical hand with good vitality and emotional depth"
}}

Analyze the image carefully and provide as much detail as visible."""

    def _parse_symbols_from_response(self, content: str) -> List[Dict[str, Any]]:
        """Parse symbols from Gemini Vision response"""
        try:
            # Try to find JSON array in the response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                symbols_json = json_match.group(0)
                symbols = json.loads(symbols_json)
                return symbols
            else:
                # If no JSON found, return empty list
                logger.warning("No JSON found in Gemini Vision response")
                return []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse symbols JSON: {e}")
            return []

    def _parse_palm_data_from_response(self, content: str) -> Dict[str, Any]:
        """Parse palm data from Gemini Vision response"""
        try:
            # Try to find JSON object in the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                palm_json = json_match.group(0)
                palm_data = json.loads(palm_json)
                return palm_data
            else:
                logger.warning("No JSON found in palm detection response")
                return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse palm JSON: {e}")
            return {}
