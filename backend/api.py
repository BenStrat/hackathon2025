"""
FastAPI Backend for Social Video Parser
"""
import os
import sys
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.video_parser import SocialVideoParser

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Social Video Parser API",
    description="Parse TikTok and Instagram Reels URLs to extract captions and detect restaurants",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize parser
api_key = os.getenv('OPENAI_API_KEY')
use_ai = bool(api_key)
parser = SocialVideoParser(openai_api_key=api_key, use_ai=use_ai)


# Pydantic models
class ParseRequest(BaseModel):
    url: str


class BatchParseRequest(BaseModel):
    urls: List[str]


class ParseResponse(BaseModel):
    success: bool
    url: str
    platform: Optional[str] = None
    video_id: Optional[str] = None
    caption: Optional[str] = None
    author: Optional[str] = None
    restaurant_found: bool = False
    restaurant_name: Optional[str] = None
    confidence: float = 0.0
    reasoning: Optional[str] = None
    additional_context: Optional[str] = None
    error: Optional[str] = None


class StatusResponse(BaseModel):
    status: str
    ai_enabled: bool
    supported_platforms: List[str]


# Routes
@app.get("/", response_model=StatusResponse)
async def root():
    """Get API status"""
    return StatusResponse(
        status="online",
        ai_enabled=use_ai,
        supported_platforms=["tiktok", "instagram"]
    )


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/parse", response_model=ParseResponse)
async def parse_url(request: ParseRequest):
    """
    Parse a single video URL

    Returns caption and restaurant detection results
    """
    url = request.url.strip()

    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    # Check if URL is supported
    if not parser.is_supported_url(url):
        return ParseResponse(
            success=False,
            url=url,
            error="Unsupported URL format. Please use TikTok or Instagram Reels URLs."
        )

    try:
        # Parse the URL
        result = parser.parse_url(url)

        # Convert to response model
        return ParseResponse(
            success=result.get('success', False),
            url=url,
            platform=result.get('platform'),
            video_id=result.get('video_id'),
            caption=result.get('caption'),
            author=result.get('author'),
            restaurant_found=result.get('restaurant_found', False),
            restaurant_name=result.get('restaurant_name'),
            confidence=result.get('confidence', 0.0),
            reasoning=result.get('reasoning'),
            additional_context=result.get('additional_context'),
            error=result.get('error')
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing URL: {str(e)}")


@app.post("/parse/batch", response_model=List[ParseResponse])
async def parse_batch(request: BatchParseRequest):
    """
    Parse multiple video URLs in batch

    Returns list of results for each URL
    """
    if not request.urls:
        raise HTTPException(status_code=400, detail="At least one URL is required")

    results = []

    for url in request.urls:
        url = url.strip()
        if not url:
            continue

        try:
            if not parser.is_supported_url(url):
                results.append(ParseResponse(
                    success=False,
                    url=url,
                    error="Unsupported URL format"
                ))
                continue

            result = parser.parse_url(url)

            results.append(ParseResponse(
                success=result.get('success', False),
                url=url,
                platform=result.get('platform'),
                video_id=result.get('video_id'),
                caption=result.get('caption'),
                author=result.get('author'),
                restaurant_found=result.get('restaurant_found', False),
                restaurant_name=result.get('restaurant_name'),
                confidence=result.get('confidence', 0.0),
                reasoning=result.get('reasoning'),
                additional_context=result.get('additional_context'),
                error=result.get('error')
            ))

        except Exception as e:
            results.append(ParseResponse(
                success=False,
                url=url,
                error=f"Error: {str(e)}"
            ))

    return results


@app.get("/validate")
async def validate_url(url: str):
    """
    Validate if a URL is supported

    Query parameter: url
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required")

    is_valid = parser.is_supported_url(url)
    platform = parser.get_platform(url)

    return {
        "url": url,
        "is_valid": is_valid,
        "platform": platform
    }


if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 80)
    print("🚀 Starting Social Video Parser API")
    print("=" * 80)
    print(f"AI Mode: {'Enabled' if use_ai else 'Disabled (using simple detection)'}")
    print("API Docs: http://localhost:8000/docs")
    print("=" * 80 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
