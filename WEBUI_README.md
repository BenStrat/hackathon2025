# Social Video Parser - Web UI

A modern, full-stack web application for parsing TikTok and Instagram Reels URLs with AI-powered restaurant detection.

## Architecture

### Backend (FastAPI)
- **Location**: `/backend`
- **Port**: 8000
- **Framework**: FastAPI (Python)
- **Features**:
  - RESTful API for video parsing
  - Single URL and batch processing endpoints
  - AI-powered restaurant detection
  - Automatic CORS configuration
  - Interactive API docs at `/docs`

### Frontend (Next.js + shadcn/ui)
- **Location**: `/frontend`
- **Port**: 3000
- **Framework**: Next.js 14 with React 18
- **UI Library**: shadcn/ui components
- **Styling**: Tailwind CSS
- **Features**:
  - Modern, responsive design
  - Single URL parsing interface
  - Batch processing with multiple URLs
  - Real-time results display
  - Beautiful card-based layouts
  - Dark mode support

## Quick Start

### Option 1: Automated Script (Recommended)

```bash
chmod +x start.sh
./start.sh
```

This will:
1. Set up and start the backend API on port 8000
2. Install dependencies and start the frontend on port 3000
3. Both servers run concurrently

**Access the app**: http://localhost:3000

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Environment Variables

**Backend** (optional):
Create `/backend/.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

**Frontend**:
Create `/frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Endpoints

### GET `/`
Get API status and configuration

### POST `/parse`
Parse a single video URL
```json
{
  "url": "https://www.tiktok.com/@user/video/123"
}
```

### POST `/parse/batch`
Parse multiple URLs
```json
{
  "urls": [
    "https://www.tiktok.com/@user/video/123",
    "https://www.instagram.com/reel/ABC/"
  ]
}
```

### GET `/validate?url={url}`
Validate if a URL is supported

## Features

### Single URL Parsing
1. Paste a TikTok or Instagram Reels URL
2. Click "Parse"
3. View results:
   - Platform and author
   - Full video caption
   - Restaurant detection status
   - Restaurant name (if found)
   - Confidence score
   - AI reasoning

### Batch Processing
1. Enter multiple URLs (one per line)
2. Click "Parse All URLs"
3. View summarized results for all videos

### UI Components (shadcn/ui)

The frontend uses these shadcn/ui components:
- `Button` - Primary action buttons
- `Input` - URL input fields
- `Textarea` - Multi-line batch URL input
- `Card` - Content containers
- `Label` - Form labels
- `Tabs` - Navigation between sections

## Project Structure

```
hackathon2025/
├── backend/
│   ├── api.py                 # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── __init__.py
├── frontend/
│   ├── app/
│   │   ├── layout.tsx        # Root layout
│   │   ├── page.tsx          # Main page
│   │   └── globals.css       # Global styles
│   ├── components/
│   │   └── ui/               # shadcn/ui components
│   ├── lib/
│   │   └── utils.ts          # Utility functions
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── next.config.js
├── src/                       # Shared Python modules
│   ├── url_parser.py
│   ├── caption_extractor.py
│   ├── restaurant_detector.py
│   └── video_parser.py
└── start.sh                   # Startup script
```

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Visit API docs: http://localhost:8000/docs

### Frontend Development
```bash
cd frontend
npm run dev
```

Visit app: http://localhost:3000

## Building for Production

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
npm start
```

## Troubleshooting

### Backend won't start
- Check if Python 3.8+ is installed
- Ensure all dependencies are installed: `pip install -r backend/requirements.txt`
- Check if port 8000 is available

### Frontend won't start
- Check if Node.js 18+ is installed
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available

### CORS errors
- Make sure backend is running before starting frontend
- Check that `NEXT_PUBLIC_API_URL` is set correctly in `.env.local`
- Verify CORS middleware in `backend/api.py` includes your frontend URL

### API connection failed
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify `.env.local` has the correct API URL

## Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **BeautifulSoup4** - Web scraping
- **OpenAI** - AI-powered analysis

### Frontend
- **Next.js 14** - React framework
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **shadcn/ui** - Component library
- **Radix UI** - Accessible primitives
- **Lucide React** - Icon library

## License

MIT
