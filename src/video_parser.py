"""
Main Video Parser - combines URL parsing, caption extraction, and restaurant detection
"""
from typing import Dict, Optional
from .url_parser import SocialURLParser
from .caption_extractor import CaptionExtractor
from .restaurant_detector import RestaurantDetector


class SocialVideoParser:
    """
    Complete parser for social media video URLs
    Parses URLs, extracts captions, and detects restaurant mentions
    """

    def __init__(self, openai_api_key: Optional[str] = None, use_ai: bool = True):
        """
        Initialize the video parser

        Args:
            openai_api_key: OpenAI API key for restaurant detection
            use_ai: Whether to use AI for restaurant detection (True) or simple pattern matching (False)
        """
        self.url_parser = SocialURLParser()
        self.caption_extractor = CaptionExtractor()
        self.use_ai = use_ai

        if use_ai:
            try:
                self.restaurant_detector = RestaurantDetector(api_key=openai_api_key)
            except ValueError as e:
                print(f"Warning: {e}. Falling back to simple detection.")
                self.use_ai = False
                self.restaurant_detector = None
        else:
            self.restaurant_detector = RestaurantDetector(api_key="dummy") if openai_api_key else None

    def parse_url(self, url: str) -> Dict[str, any]:
        """
        Parse a social media video URL and extract all information

        Args:
            url: The video URL to parse

        Returns:
            Dictionary containing:
            - url: Original URL
            - platform: 'tiktok' or 'instagram'
            - video_id: The video ID
            - caption: The video caption/description
            - author: The video author (if available)
            - restaurant_found: Whether a restaurant was detected
            - restaurant_name: Name of the restaurant (if found)
            - confidence: Confidence level of restaurant detection
            - reasoning: Explanation of restaurant detection
        """
        # Step 1: Parse the URL
        parsed = self.url_parser.parse_url(url)

        if not parsed.get('platform'):
            return {
                'url': url,
                'error': parsed.get('error', 'Invalid URL'),
                'success': False
            }

        # Step 2: Extract caption
        caption_data = self.caption_extractor.extract_caption(
            platform=parsed['platform'],
            video_id=parsed['video_id'],
            url=url
        )

        # Step 3: Detect restaurant
        restaurant_data = {}
        if self.restaurant_detector:
            caption_text = caption_data.get('caption')
            restaurant_data = self.restaurant_detector.detect_restaurant(
                caption_text,
                use_simple_detection=not self.use_ai
            )
        else:
            # Fallback to simple detection without OpenAI
            caption_text = caption_data.get('caption', '')
            detector = RestaurantDetector(api_key="dummy")
            restaurant_data = detector._simple_detection(caption_text)

        # Combine all results
        result = {
            'url': url,
            'platform': parsed['platform'],
            'video_id': parsed['video_id'],
            'caption': caption_data.get('caption'),
            'author': caption_data.get('author'),
            'restaurant_found': restaurant_data.get('restaurant_found', False),
            'restaurant_name': restaurant_data.get('restaurant_name'),
            'confidence': restaurant_data.get('confidence', 0),
            'reasoning': restaurant_data.get('reasoning', ''),
            'success': True
        }

        # Add additional context if available
        if 'additional_context' in restaurant_data:
            result['additional_context'] = restaurant_data['additional_context']

        if 'error' in caption_data:
            result['caption_error'] = caption_data['error']

        return result

    def is_supported_url(self, url: str) -> bool:
        """Check if the URL is supported"""
        return self.url_parser.is_valid_url(url)

    def get_platform(self, url: str) -> Optional[str]:
        """Get the platform from URL"""
        return self.url_parser.get_platform(url)
