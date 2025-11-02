"""
Restaurant Detector using AI to analyze video captions
"""
import os
import re
from typing import Dict, List, Optional
from openai import OpenAI


class RestaurantDetector:
    """Detect and suggest restaurants from video captions using AI"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the restaurant detector

        Args:
            api_key: OpenAI API key. If not provided, will try to get from environment
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)

    def detect_restaurant(self, caption: str, use_simple_detection: bool = False) -> Dict[str, any]:
        """
        Detect restaurant mentions in a caption

        Args:
            caption: The video caption text
            use_simple_detection: If True, use simple pattern matching instead of AI

        Returns:
            Dictionary with restaurant information
        """
        if not caption or caption == 'Caption not found':
            return {
                'restaurant_found': False,
                'restaurant_name': None,
                'confidence': 0,
                'reasoning': 'No caption available to analyze'
            }

        if use_simple_detection:
            return self._simple_detection(caption)
        else:
            return self._ai_detection(caption)

    def _simple_detection(self, caption: str) -> Dict[str, any]:
        """
        Simple pattern-based restaurant detection
        Looks for common patterns and keywords
        """
        caption_lower = caption.lower()

        # Common restaurant indicators
        restaurant_keywords = [
            'restaurant', 'cafe', 'diner', 'bistro', 'eatery',
            'grill', 'kitchen', 'bar', 'pizzeria', 'bakery',
            'steakhouse', 'sushi', 'ramen', 'burger', 'taco'
        ]

        # Check for hashtags with restaurant names
        hashtags = re.findall(r'#(\w+)', caption)

        # Check for @mentions
        mentions = re.findall(r'@(\w+)', caption)

        # Check for restaurant keywords
        found_keywords = [kw for kw in restaurant_keywords if kw in caption_lower]

        # Try to extract potential restaurant names
        potential_names = []

        # Pattern: "at [Restaurant Name]"
        at_pattern = re.findall(r'at\s+([A-Z][a-zA-Z\s&\']+?)(?:\.|,|!|\s+#|\s+@|$)', caption)
        potential_names.extend(at_pattern)

        # Pattern: "[Restaurant Name] is"
        is_pattern = re.findall(r'([A-Z][a-zA-Z\s&\']+?)\s+is\s+(?:amazing|great|delicious|the best)', caption)
        potential_names.extend(is_pattern)

        # Check mentions that might be restaurant names
        potential_names.extend([m for m in mentions if len(m) > 3])

        if potential_names or found_keywords:
            # Pick the most likely restaurant name
            restaurant_name = potential_names[0] if potential_names else None

            return {
                'restaurant_found': True,
                'restaurant_name': restaurant_name,
                'confidence': 0.6 if restaurant_name else 0.4,
                'keywords_found': found_keywords,
                'mentions': mentions,
                'hashtags': hashtags,
                'reasoning': f'Found restaurant indicators: {", ".join(found_keywords[:3])}'
            }

        return {
            'restaurant_found': False,
            'restaurant_name': None,
            'confidence': 0,
            'reasoning': 'No clear restaurant indicators found'
        }

    def _ai_detection(self, caption: str) -> Dict[str, any]:
        """
        AI-powered restaurant detection using OpenAI
        """
        try:
            prompt = f"""Analyze the following social media video caption and determine if it mentions or is about a restaurant.

Caption: "{caption}"

Please provide:
1. Whether a restaurant is mentioned (yes/no)
2. The name of the restaurant if found (or "Unknown" if yes but name not clear)
3. Your confidence level (0-100)
4. Brief reasoning for your conclusion
5. Any additional context (cuisine type, location hints, etc.)

Format your response as JSON with keys: restaurant_found (boolean), restaurant_name (string or null), confidence (number 0-100), reasoning (string), additional_context (string)."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes social media captions to identify restaurant mentions. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )

            result_text = response.choices[0].message.content.strip()

            # Try to parse JSON response
            import json
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', result_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(1))
                else:
                    # Fallback to simple detection
                    return self._simple_detection(caption)

            # Normalize the result
            return {
                'restaurant_found': bool(result.get('restaurant_found', False)),
                'restaurant_name': result.get('restaurant_name'),
                'confidence': result.get('confidence', 0) / 100.0,  # Convert to 0-1 scale
                'reasoning': result.get('reasoning', 'AI analysis completed'),
                'additional_context': result.get('additional_context', ''),
                'method': 'ai'
            }

        except Exception as e:
            # Fallback to simple detection if AI fails
            print(f"AI detection failed: {str(e)}. Falling back to simple detection.")
            result = self._simple_detection(caption)
            result['method'] = 'simple (ai_failed)'
            result['ai_error'] = str(e)
            return result

    def batch_detect(self, captions: List[str]) -> List[Dict[str, any]]:
        """
        Detect restaurants in multiple captions

        Args:
            captions: List of caption texts

        Returns:
            List of detection results
        """
        return [self.detect_restaurant(caption) for caption in captions]
