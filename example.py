#!/usr/bin/env python3
"""
Example usage of the Social Video Parser library
"""
import os
from dotenv import load_dotenv
from src.video_parser import SocialVideoParser


def example_basic_usage():
    """Basic usage example"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 80 + "\n")

    # Load environment variables
    load_dotenv()

    # Initialize parser
    parser = SocialVideoParser()

    # Example TikTok URL
    tiktok_url = "https://www.tiktok.com/@gordonramsayofficial/video/7234567890123456789"

    # Parse the URL
    result = parser.parse_url(tiktok_url)

    # Access the results
    print(f"Platform: {result['platform']}")
    print(f"Caption: {result['caption']}")
    print(f"Restaurant found: {result['restaurant_found']}")
    if result['restaurant_found']:
        print(f"Restaurant name: {result['restaurant_name']}")
        print(f"Confidence: {result['confidence'] * 100:.1f}%")

    print("\n")


def example_without_ai():
    """Example using simple pattern matching instead of AI"""
    print("=" * 80)
    print("EXAMPLE 2: Using Simple Pattern Matching (No OpenAI API Key Required)")
    print("=" * 80 + "\n")

    # Initialize parser without AI
    parser = SocialVideoParser(use_ai=False)

    # Example Instagram URL
    instagram_url = "https://www.instagram.com/reel/ABC123DEF456/"

    # Parse the URL
    result = parser.parse_url(instagram_url)

    print(f"Platform: {result['platform']}")
    print(f"Restaurant found: {result['restaurant_found']}")
    print(f"Reasoning: {result['reasoning']}")

    print("\n")


def example_check_url():
    """Example of checking if a URL is supported"""
    print("=" * 80)
    print("EXAMPLE 3: Checking URL Support")
    print("=" * 80 + "\n")

    parser = SocialVideoParser(use_ai=False)

    urls = [
        "https://www.tiktok.com/@user/video/123",
        "https://www.instagram.com/reel/ABC/",
        "https://www.youtube.com/watch?v=123",  # Not supported
        "https://example.com/video",  # Not supported
    ]

    for url in urls:
        is_supported = parser.is_supported_url(url)
        platform = parser.get_platform(url)
        print(f"URL: {url}")
        print(f"  Supported: {is_supported}")
        print(f"  Platform: {platform or 'Unknown'}")
        print()


def example_batch_processing():
    """Example of processing multiple URLs"""
    print("=" * 80)
    print("EXAMPLE 4: Batch Processing Multiple URLs")
    print("=" * 80 + "\n")

    load_dotenv()
    parser = SocialVideoParser()

    urls = [
        "https://www.tiktok.com/@foodie/video/1234567890",
        "https://www.instagram.com/reel/XYZ123/",
        "https://vm.tiktok.com/ABC123/",
    ]

    results = []
    for url in urls:
        if parser.is_supported_url(url):
            result = parser.parse_url(url)
            results.append(result)

    # Summary
    print(f"Processed {len(results)} videos")
    restaurants_found = sum(1 for r in results if r.get('restaurant_found'))
    print(f"Restaurants detected: {restaurants_found}/{len(results)}")

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['platform'].upper()} - {result['url']}")
        if result['restaurant_found']:
            print(f"   Restaurant: {result['restaurant_name']}")

    print("\n")


if __name__ == "__main__":
    print("\n🎯 Social Video Parser - Examples\n")

    try:
        example_basic_usage()
        example_without_ai()
        example_check_url()
        example_batch_processing()

        print("=" * 80)
        print("✅ All examples completed!")
        print("=" * 80)
        print("\nTo run the main parser with actual URLs:")
        print("  python main.py 'https://www.tiktok.com/@user/video/123'")
        print("\n")

    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}\n")
