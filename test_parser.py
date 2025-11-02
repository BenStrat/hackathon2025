#!/usr/bin/env python3
"""
Quick test script for the Social Video Parser
"""
from src.url_parser import SocialURLParser
from src.caption_extractor import CaptionExtractor
from src.restaurant_detector import RestaurantDetector
from src.video_parser import SocialVideoParser


def test_url_parser():
    """Test URL parsing"""
    print("Testing URL Parser...")

    parser = SocialURLParser()

    test_urls = [
        "https://www.tiktok.com/@user/video/1234567890",
        "https://vm.tiktok.com/ABC123/",
        "https://www.instagram.com/reel/ABC123/",
        "https://www.instagram.com/p/XYZ789/",
        "https://www.youtube.com/watch?v=123",  # Should fail
    ]

    for url in test_urls:
        result = parser.parse_url(url)
        platform = result.get('platform') or 'Invalid'
        print(f"  {url[:50]:50} -> {platform:10}")

    print("✓ URL Parser test completed\n")


def test_restaurant_detector():
    """Test restaurant detection"""
    print("Testing Restaurant Detector (Simple Mode)...")

    # Use simple detection (no API key needed)
    detector = RestaurantDetector(api_key="dummy")

    test_captions = [
        "Just had the best burger at Five Guys! #foodie",
        "Amazing ramen at @tanakasramen in downtown",
        "Check out this delicious pizza! 🍕",
        "Beautiful sunset today at the beach",
    ]

    for caption in test_captions:
        result = detector._simple_detection(caption)
        found = "✓" if result['restaurant_found'] else "✗"
        name = result.get('restaurant_name') or 'N/A'
        print(f"  {found} '{caption[:40]:40}' -> {name}")

    print("✓ Restaurant Detector test completed\n")


def test_integrated_parser():
    """Test the integrated parser"""
    print("Testing Integrated Video Parser...")

    parser = SocialVideoParser(use_ai=False)

    # Test URL validation
    test_urls = [
        "https://www.tiktok.com/@foodlover/video/1234567890",
        "https://www.instagram.com/reel/ABC123/",
        "https://invalid.com/video",
    ]

    for url in test_urls:
        is_supported = parser.is_supported_url(url)
        platform = parser.get_platform(url)
        status = "✓ Supported" if is_supported else "✗ Not supported"
        print(f"  {status:15} {platform or 'Unknown':10} {url[:45]}")

    print("✓ Integrated Parser test completed\n")


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("RUNNING UNIT TESTS")
    print("=" * 80 + "\n")

    try:
        test_url_parser()
        test_restaurant_detector()
        test_integrated_parser()

        print("=" * 80)
        print("✅ ALL TESTS PASSED")
        print("=" * 80 + "\n")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
