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
        return f"""You are a palmistry expert. Analyze this {hand_type} hand image.

Identify the major palm lines:
1. Life Line: Curves around the thumb base
2. Heart Line: Runs horizontally across the top of the palm
3. Head Line: Runs horizontally across the middle of the palm
4. Fate Line: Runs vertically up the palm (if present)

For each line, describe:
- length: short, medium, long
- depth: faint, medium, deep
- quality: broken, chained, clear, forked
- special_features: any breaks, islands, or branches

Also identify:
- hand_shape: square, rectangular (determines element)
- finger_length: short, medium, long (relative to palm)

Return your response in this JSON format:
{{
  "life_line": {{"length": "long", "depth": "deep", "quality": "clear", "special_features": []}},
  "heart_line": {{"length": "long", "depth": "medium", "quality": "clear", "special_features": ["curves_upward"]}},
  "head_line": {{"length": "medium", "depth": "deep", "quality": "clear", "special_features": []}},
  "fate_line": {{"present": true, "length": "long", "depth": "faint", "quality": "broken"}},
  "hand_shape": "square",
  "finger_length": "medium"
}}"""

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
