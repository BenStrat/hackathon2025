"""
URL Parser for TikTok and Instagram Reels
"""
import re
from typing import Dict, Optional
from urllib.parse import urlparse


class SocialURLParser:
    """Parse and validate social media video URLs"""

    TIKTOK_PATTERNS = [
        r'https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/(\d+)',
        r'https?://(?:vm|vt)\.tiktok\.com/([\w]+)',
        r'https?://(?:www\.)?tiktok\.com/t/([\w]+)',
    ]

    INSTAGRAM_PATTERNS = [
        r'https?://(?:www\.)?instagram\.com/reel/([\w-]+)',
        r'https?://(?:www\.)?instagram\.com/p/([\w-]+)',
        r'https?://(?:www\.)?instagram\.com/tv/([\w-]+)',
    ]

    def __init__(self):
        self.tiktok_regex = [re.compile(pattern) for pattern in self.TIKTOK_PATTERNS]
        self.instagram_regex = [re.compile(pattern) for pattern in self.INSTAGRAM_PATTERNS]

    def parse_url(self, url: str) -> Dict[str, Optional[str]]:
        """
        Parse a social media URL and return platform and video ID

        Args:
            url: The URL to parse

        Returns:
            Dictionary with 'platform', 'video_id', and 'url' keys
        """
        url = url.strip()

        # Check TikTok patterns
        for regex in self.tiktok_regex:
            match = regex.search(url)
            if match:
                return {
                    'platform': 'tiktok',
                    'video_id': match.group(1),
                    'url': url
                }

        # Check Instagram patterns
        for regex in self.instagram_regex:
            match = regex.search(url)
            if match:
                return {
                    'platform': 'instagram',
                    'video_id': match.group(1),
                    'url': url
                }

        return {
            'platform': None,
            'video_id': None,
            'url': url,
            'error': 'Unsupported or invalid URL format'
        }

    def is_valid_url(self, url: str) -> bool:
        """Check if URL is a valid TikTok or Instagram URL"""
        result = self.parse_url(url)
        return result['platform'] is not None

    def get_platform(self, url: str) -> Optional[str]:
        """Get the platform name from URL"""
        result = self.parse_url(url)
        return result.get('platform')
