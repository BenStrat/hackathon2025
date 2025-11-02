# Social Video URL Parser

A Python tool to parse TikTok and Instagram Reels URLs, extract captions, and detect restaurant mentions using AI.

## Features

- 🎬 Parse TikTok and Instagram Reels URLs
- 📝 Extract video captions/descriptions
- 🤖 AI-powered restaurant detection and suggestion
- 🔍 Support for batch processing multiple URLs
- 🌐 **Web-based GUI for easy interaction**
- 💻 Command-line interface (CLI)

## Quick Start - Web GUI

The easiest way to use this tool is through the web interface:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Add your OpenAI API key for better results
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here

# 3. Launch the web interface
python app.py
```

Then open your browser to: **http://localhost:7860**

### Web GUI Features

- ✨ **User-friendly interface** - No coding required
- 📹 **Single URL parsing** - Paste and analyze one video at a time
- 📋 **Batch processing** - Parse multiple URLs at once
- 🎯 **Real-time results** - See captions and restaurant detection instantly
- 📊 **Detailed analysis** - View confidence scores and reasoning

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys (optional, but recommended):
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

3. Choose how to run:

**Option A: Web GUI (Recommended)**
```bash
python app.py
# Opens at http://localhost:7860
```

**Option B: Command Line**
```bash
python main.py 'https://www.tiktok.com/@user/video/123'
```

## Usage

### Web Interface (Easiest)

```bash
python app.py
```

Then navigate to `http://localhost:7860` in your browser and:
1. Paste a TikTok or Instagram Reels URL
2. Click "Parse Video"
3. View the caption and restaurant detection results

### Command Line Interface

```bash
# Single URL
python main.py 'https://www.tiktok.com/@username/video/1234567890'

# Multiple URLs
python main.py 'https://www.tiktok.com/@user/video/123' 'https://www.instagram.com/reel/ABC/'
```

### Python Library

```python
from src.video_parser import SocialVideoParser

parser = SocialVideoParser()

# Parse a TikTok URL
result = parser.parse_url("https://www.tiktok.com/@username/video/1234567890")
print(f"Caption: {result['caption']}")
print(f"Restaurant Found: {result['restaurant_found']}")
print(f"Restaurant Name: {result['restaurant_name']}")

# Parse an Instagram Reel
result = parser.parse_url("https://www.instagram.com/reel/ABC123/")
print(f"Caption: {result['caption']}")
print(f"Confidence: {result['confidence'] * 100}%")
```

## Supported URL Formats

### TikTok
- Standard: `https://www.tiktok.com/@username/video/1234567890`
- Short link: `https://vm.tiktok.com/ABC123/`
- Mobile: `https://www.tiktok.com/t/ABC123/`

### Instagram
- Reels: `https://www.instagram.com/reel/ABC123/`
- Posts: `https://www.instagram.com/p/XYZ789/`
- IGTV: `https://www.instagram.com/tv/ABC123/`

## AI vs Simple Mode

### AI Mode (Recommended)
- Requires OpenAI API key in `.env` file
- Uses GPT-3.5-turbo for intelligent analysis
- Better accuracy for restaurant detection
- Provides detailed context and reasoning

### Simple Mode (Fallback)
- No API key required
- Uses pattern matching and keywords
- Good for obvious restaurant mentions
- Faster but less accurate

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
- OpenAI API key (optional, for AI-powered detection)

## Project Structure

```
hackathon2025/
├── app.py                    # 🌐 Web GUI (Gradio)
├── main.py                   # 💻 CLI tool
├── example.py                # 📚 Usage examples
├── test_parser.py           # ✅ Unit tests
├── src/
│   ├── url_parser.py        # URL parsing & validation
│   ├── caption_extractor.py # Caption extraction
│   ├── restaurant_detector.py # Restaurant detection
│   └── video_parser.py      # Main integrated parser
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

## Examples

See `example.py` for comprehensive usage examples:
```bash
python example.py
```

## Testing

Run the test suite:
```bash
python test_parser.py
```

## License

MIT
