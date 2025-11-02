#!/usr/bin/env python3
"""
Social Video URL Parser - Main Entry Point

Parse TikTok and Instagram Reels URLs, extract captions, and detect restaurants
"""
import os
import sys
from dotenv import load_dotenv
from src.video_parser import SocialVideoParser


def print_result(result: dict):
    """Pretty print the parsing result"""
    print("\n" + "=" * 80)
    print("VIDEO ANALYSIS RESULT")
    print("=" * 80)

    if not result.get('success'):
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        return

    print(f"✓ URL: {result['url']}")
    print(f"✓ Platform: {result['platform'].upper()}")
    print(f"✓ Video ID: {result['video_id']}")

    if result.get('author'):
        print(f"✓ Author: @{result['author']}")

    print(f"\n📝 Caption:")
    caption = result.get('caption', 'N/A')
    if caption and len(caption) > 200:
        print(f"   {caption[:200]}...")
    else:
        print(f"   {caption}")

    print(f"\n🍽️  Restaurant Detection:")
    if result.get('restaurant_found'):
        print(f"   ✓ Restaurant Found: YES")
        print(f"   ✓ Name: {result.get('restaurant_name', 'Unknown')}")
        print(f"   ✓ Confidence: {result.get('confidence', 0) * 100:.1f}%")
        print(f"   ✓ Reasoning: {result.get('reasoning', 'N/A')}")
        if result.get('additional_context'):
            print(f"   ✓ Context: {result['additional_context']}")
    else:
        print(f"   ✗ Restaurant Found: NO")
        print(f"   ✓ Reasoning: {result.get('reasoning', 'N/A')}")

    if result.get('caption_error'):
        print(f"\n⚠️  Caption Extraction Warning: {result['caption_error']}")

    print("=" * 80 + "\n")


def main():
    """Main function"""
    # Load environment variables
    load_dotenv()

    # Check if OpenAI API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    use_ai = bool(api_key)

    if not api_key:
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables.")
        print("   Using simple pattern matching for restaurant detection.")
        print("   For better results, add your OpenAI API key to .env file.\n")

    # Initialize parser
    print("🚀 Initializing Social Video Parser...")
    parser = SocialVideoParser(openai_api_key=api_key, use_ai=use_ai)
    print(f"   Mode: {'AI-powered' if use_ai else 'Simple pattern matching'}\n")

    # Example URLs (you can replace these with actual URLs)
    example_urls = [
        # TikTok examples
        "https://www.tiktok.com/@username/video/1234567890123456789",
        "https://vm.tiktok.com/ZMhs4LD3A/",

        # Instagram examples
        "https://www.instagram.com/reel/ABC123DEF456/",
        "https://www.instagram.com/p/XYZ789/",
    ]

    # Check if URLs provided as command line arguments
    if len(sys.argv) > 1:
        urls_to_parse = sys.argv[1:]
    else:
        print("📌 Usage: python main.py <url1> <url2> ...")
        print("📌 Or: Run without arguments to see example usage\n")
        print("Example URLs (for demonstration):")
        for url in example_urls:
            print(f"   - {url}")
        print("\n💡 To parse real videos, run:")
        print("   python main.py 'https://www.tiktok.com/@user/video/123'")
        print("   python main.py 'https://www.instagram.com/reel/ABC123/'\n")
        return

    # Parse each URL
    for url in urls_to_parse:
        try:
            print(f"🔍 Parsing: {url}")

            # Check if URL is supported
            if not parser.is_supported_url(url):
                print(f"❌ Unsupported URL format: {url}\n")
                continue

            # Parse the URL
            result = parser.parse_url(url)

            # Print the result
            print_result(result)

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error parsing {url}: {str(e)}\n")


if __name__ == "__main__":
    main()
