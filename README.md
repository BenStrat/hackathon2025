# Social Video URL Parser

A Python tool to parse TikTok and Instagram Reels URLs, extract captions, and detect restaurant mentions using AI.

## Features

- Parse TikTok and Instagram Reels URLs
- Extract video captions/descriptions
- AI-powered restaurant detection and suggestion
- Support for multiple video URLs

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

3. Run the parser:
```bash
python main.py
```

## Usage

```python
from video_parser import SocialVideoParser

parser = SocialVideoParser()

# Parse a TikTok URL
result = parser.parse_url("https://www.tiktok.com/@username/video/1234567890")
print(f"Caption: {result['caption']}")
print(f"Restaurant: {result['restaurant']}")

# Parse an Instagram Reel
result = parser.parse_url("https://www.instagram.com/reel/ABC123/")
print(f"Caption: {result['caption']}")
print(f"Restaurant: {result['restaurant']}")
```

## Requirements

- Python 3.8+
- OpenAI API key (for restaurant detection)

## License

MIT
