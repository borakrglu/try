"""
OpenAI Vision Service - Image analysis for readings
"""

import base64
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class VisionService:
    """Service for analyzing images with OpenAI GPT-4 Vision"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def detect_coffee_symbols(
        self,
        image_url: str,
        image_type: str = "cup"
    ) -> List[Dict[str, Any]]:
        """
        Detect symbols in a coffee cup image

        Args:
            image_url: URL or base64 of the coffee cup image
            image_type: Type of image (cup, saucer, side)

        Returns:
            List of detected symbols with their properties
        """
        prompt = self._get_coffee_detection_prompt(image_type)

        try:
            logger.info(f"Analyzing coffee cup image ({image_type})")

            response = await self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url, "detail": "high"}
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.3,  # Lower temp for more consistent detection
            )

            # Parse the response (expecting JSON-like format)
            content = response.choices[0].message.content
            logger.info(f"Vision API response: {content[:200]}...")

            # Try to extract symbols from response
            symbols = self._parse_symbols_from_response(content)

            logger.info(f"Detected {len(symbols)} symbols in {image_type}")
            return symbols

        except Exception as e:
            logger.error(f"Vision API error: {str(e)}")
            # Return empty list on error, don't fail the reading
            return []

    async def detect_palm_lines(
        self,
        image_url: str,
        hand_type: str = "right"
    ) -> Dict[str, Any]:
        """
        Detect palm lines in a hand image

        Args:
            image_url: URL or base64 of the palm image
            hand_type: Type of hand (left, right)

        Returns:
            Dictionary with detected palm line information
        """
        prompt = self._get_palm_detection_prompt(hand_type)

        try:
            logger.info(f"Analyzing palm image ({hand_type} hand)")

            response = await self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url, "detail": "high"}
                            }
                        ]
                    }
                ],
                max_tokens=600,
                temperature=0.3,
            )

            content = response.choices[0].message.content
            logger.info(f"Palm detection response received")

            # Parse palm line data
            palm_data = self._parse_palm_data_from_response(content)

            return palm_data

        except Exception as e:
            logger.error(f"Palm detection error: {str(e)}")
            return {}

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

Return your response in this JSON-like format:
[
  {{"symbol": "bird", "position": "top-right", "clarity": 8, "description": "Bird with wings spread, facing upward", "size": "medium"}},
  {{"symbol": "road", "position": "center-left", "clarity": 6, "description": "Winding path ascending", "size": "large"}}
]

Be thorough but only include symbols you can clearly see. If you see very few or no clear symbols, return an empty array."""

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
        """Parse symbols from Vision API response"""
        import json
        import re

        try:
            # Try to find JSON array in the response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                symbols_json = json_match.group(0)
                symbols = json.loads(symbols_json)
                return symbols
            else:
                # If no JSON found, return empty list
                logger.warning("No JSON found in Vision API response")
                return []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse symbols JSON: {e}")
            return []

    def _parse_palm_data_from_response(self, content: str) -> Dict[str, Any]:
        """Parse palm data from Vision API response"""
        import json
        import re

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

    async def enhance_image_for_reading(
        self,
        image_url: str,
        enhancement_type: str = "coffee"
    ) -> Optional[str]:
        """
        Optional: Enhance image quality/contrast for better symbol detection
        This could use additional image processing libraries like OpenCV

        Args:
            image_url: Original image URL
            enhancement_type: Type of enhancement (coffee, palm)

        Returns:
            Enhanced image URL or None
        """
        # TODO: Implement image enhancement if needed
        # Could use OpenCV for contrast enhancement, edge detection, etc.
        return None
