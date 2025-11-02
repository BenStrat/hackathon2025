# Social Video URL Parser

A full-stack web application to parse TikTok and Instagram Reels URLs, extract captions, and detect restaurant mentions using AI.

## Features

- 🎬 Parse TikTok and Instagram Reels URLs
- 📝 Extract video captions/descriptions
- 🤖 AI-powered restaurant detection and suggestion
- 🔍 Support for batch processing multiple URLs
- 🌐 **Modern Web UI built with Next.js + shadcn/ui**
- 🚀 **FastAPI REST API backend**
- 💻 Command-line interface (CLI)

## Quick Start - Web Application (Recommended)

The easiest way to use this tool is through the modern web interface:

```bash
# Launch both backend and frontend with one command
chmod +x start.sh
./start.sh
```

Then open your browser to: **http://localhost:3000**

The startup script will:
- Start the FastAPI backend on port 8000
- Start the Next.js frontend on port 3000
- Install all dependencies automatically

### Manual Start

**Backend (Terminal 1):**
```bash
cd backend
pip install -r requirements.txt
python3 api.py
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm install
npm run dev
```

### Web UI Features

- ✨ **Modern, responsive design** - Built with Next.js and shadcn/ui components
- 📹 **Single URL parsing** - Beautiful interface to analyze one video at a time
- 📋 **Batch processing** - Process multiple URLs simultaneously
- 🎯 **Real-time results** - Instant feedback with detailed analysis
- 📊 **Comprehensive data** - View captions, confidence scores, and AI reasoning
- 🎨 **Beautiful UI** - Tailwind CSS with dark mode support
- 🔌 **REST API** - FastAPI backend with interactive docs at `/docs`

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

**Option A: Web Application (Recommended)**
```bash
./start.sh
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**Option B: Gradio Interface (Simple)**
```bash
python app.py
# Opens at http://localhost:7860
```

**Option C: Command Line**
```bash
python main.py 'https://www.tiktok.com/@user/video/123'
```

## Usage

### Web Application (Recommended)

Start the full-stack application:
```bash
./start.sh
```

Then navigate to `http://localhost:3000` in your browser and:
1. Paste a TikTok or Instagram Reels URL
2. Click "Parse"
3. View comprehensive results including captions and restaurant detection

**API Documentation**: Visit `http://localhost:8000/docs` for interactive API documentation

### Gradio Interface (Alternative)

Quick web interface without Node.js:
```bash
python app.py
# Opens at http://localhost:7860
```

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

### For Web Application
- Python 3.8+
- Node.js 18+
- Dependencies in `backend/requirements.txt` and `frontend/package.json`
- OpenAI API key (optional, for AI-powered detection)

### For CLI/Gradio Only
- Python 3.8+
- Dependencies in `requirements.txt`
- OpenAI API key (optional)

## Project Structure

```
hackathon2025/
├── frontend/                 # 🌐 Next.js Web Application
│   ├── app/                 # Next.js app directory
│   │   ├── page.tsx        # Main UI page
│   │   ├── layout.tsx      # App layout
│   │   └── globals.css     # Global styles
│   ├── components/ui/       # shadcn/ui components
│   ├── lib/                # Utility functions
│   └── package.json        # Node.js dependencies
├── backend/                 # 🚀 FastAPI REST API
│   ├── api.py              # FastAPI application
│   └── requirements.txt    # Backend dependencies
├── src/                     # 📦 Core Python Modules
│   ├── url_parser.py       # URL parsing & validation
│   ├── caption_extractor.py # Caption extraction
│   ├── restaurant_detector.py # Restaurant detection
│   └── video_parser.py     # Main integrated parser
├── app.py                   # 🎨 Gradio web interface (alternative)
├── main.py                  # 💻 CLI tool
├── example.py               # 📚 Usage examples
├── test_parser.py          # ✅ Unit tests
├── start.sh                # 🚀 Startup script
├── requirements.txt        # Python dependencies (CLI/Gradio)
├── WEBUI_README.md         # Web UI documentation
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
