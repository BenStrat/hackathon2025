"""
Caption Extractor for TikTok and Instagram videos
"""
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
import json
import re


class CaptionExtractor:
    """Extract captions from TikTok and Instagram videos"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def extract_caption(self, platform: str, video_id: str, url: str) -> Dict[str, any]:
        """
        Extract caption from a video URL

        Args:
            platform: 'tiktok' or 'instagram'
            video_id: The video ID
            url: The full video URL

        Returns:
            Dictionary with 'caption', 'author', and other metadata
        """
        if platform == 'tiktok':
            return self._extract_tiktok_caption(url)
        elif platform == 'instagram':
            return self._extract_instagram_caption(url)
        else:
            return {
                'caption': None,
                'error': f'Unsupported platform: {platform}'
            }

    def _extract_tiktok_caption(self, url: str) -> Dict[str, any]:
        """Extract caption from TikTok video"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Try to find the video description in meta tags
            caption = None
            author = None

            # Method 1: Check meta description
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                caption = meta_desc.get('content')

            # Method 2: Check Open Graph description
            if not caption:
                og_desc = soup.find('meta', {'property': 'og:description'})
                if og_desc and og_desc.get('content'):
                    caption = og_desc.get('content')

            # Method 3: Check Twitter description
            if not caption:
                twitter_desc = soup.find('meta', {'name': 'twitter:description'})
                if twitter_desc and twitter_desc.get('content'):
                    caption = twitter_desc.get('content')

            # Try to extract from JSON-LD or script tags
            if not caption:
                scripts = soup.find_all('script', {'type': 'application/ld+json'})
                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        if isinstance(data, dict) and 'description' in data:
                            caption = data['description']
                            break
                    except:
                        continue

            # Try to find SIGI_STATE data (TikTok's data structure)
            if not caption:
                for script in soup.find_all('script'):
                    if script.string and 'SIGI_STATE' in script.string:
                        try:
                            # Extract JSON data
                            match = re.search(r'<script id="SIGI_STATE"[^>]*>(.*?)</script>', response.text, re.DOTALL)
                            if match:
                                data = json.loads(match.group(1))
                                # Navigate through the nested structure to find video description
                                if 'ItemModule' in data:
                                    for key, value in data['ItemModule'].items():
                                        if isinstance(value, dict) and 'desc' in value:
                                            caption = value['desc']
                                            if 'author' in value:
                                                author = value['author']
                                            break
                        except:
                            pass

            return {
                'caption': caption or 'Caption not found',
                'author': author,
                'platform': 'tiktok',
                'url': url
            }

        except requests.RequestException as e:
            return {
                'caption': None,
                'error': f'Failed to fetch TikTok video: {str(e)}',
                'platform': 'tiktok',
                'url': url
            }
        except Exception as e:
            return {
                'caption': None,
                'error': f'Error extracting TikTok caption: {str(e)}',
                'platform': 'tiktok',
                'url': url
            }

    def _extract_instagram_caption(self, url: str) -> Dict[str, any]:
        """Extract caption from Instagram Reel/Post"""
        try:
            # Add trailing slash if not present
            if not url.endswith('/'):
                url = url + '/'

            # Try to fetch the page
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            caption = None
            author = None

            # Method 1: Check meta description
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                content = meta_desc.get('content')
                # Instagram format is usually: "X Likes, Y Comments - @username on Instagram: "caption text""
                match = re.search(r'on Instagram:\s*["\']?([^"\']+)', content)
                if match:
                    caption = match.group(1).strip()
                else:
                    caption = content

            # Method 2: Check Open Graph description
            if not caption:
                og_desc = soup.find('meta', {'property': 'og:description'})
                if og_desc and og_desc.get('content'):
                    caption = og_desc.get('content')

            # Method 3: Check for JSON data in script tags
            if not caption:
                scripts = soup.find_all('script', {'type': 'application/ld+json'})
                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        if isinstance(data, dict):
                            if 'articleBody' in data:
                                caption = data['articleBody']
                                break
                            elif 'description' in data:
                                caption = data['description']
                                break
                    except:
                        continue

            # Try to extract from shared data
            if not caption:
                for script in soup.find_all('script'):
                    if script.string and 'window._sharedData' in script.string:
                        try:
                            match = re.search(r'window\._sharedData\s*=\s*({.+?});', script.string)
                            if match:
                                data = json.loads(match.group(1))
                                # Navigate the structure to find caption
                                if 'entry_data' in data:
                                    for page_type in ['PostPage', 'ProfilePage']:
                                        if page_type in data['entry_data']:
                                            entries = data['entry_data'][page_type]
                                            if entries and len(entries) > 0:
                                                media = entries[0].get('graphql', {}).get('shortcode_media', {})
                                                if media:
                                                    edges = media.get('edge_media_to_caption', {}).get('edges', [])
                                                    if edges and len(edges) > 0:
                                                        caption = edges[0].get('node', {}).get('text')
                                                        owner = media.get('owner', {})
                                                        if owner:
                                                            author = owner.get('username')
                                                    break
                        except:
                            pass

            return {
                'caption': caption or 'Caption not found',
                'author': author,
                'platform': 'instagram',
                'url': url
            }

        except requests.RequestException as e:
            return {
                'caption': None,
                'error': f'Failed to fetch Instagram video: {str(e)}',
                'platform': 'instagram',
                'url': url
            }
        except Exception as e:
            return {
                'caption': None,
                'error': f'Error extracting Instagram caption: {str(e)}',
                'platform': 'instagram',
                'url': url
            }
