#!/usr/bin/env python3
"""
Social Video Parser - Web GUI using Gradio

A web-based interface for parsing TikTok and Instagram Reels URLs,
extracting captions, and detecting restaurant mentions.
"""
import os
import gradio as gr
from dotenv import load_dotenv
from src.video_parser import SocialVideoParser

# Load environment variables
load_dotenv()

# Initialize parser
api_key = os.getenv('OPENAI_API_KEY')
use_ai = bool(api_key)

if not api_key:
    print("⚠️  Warning: OPENAI_API_KEY not found. Using simple pattern matching.")

parser = SocialVideoParser(openai_api_key=api_key, use_ai=use_ai)


def parse_video_url(url):
    """
    Parse a video URL and return formatted results

    Args:
        url: The video URL to parse

    Returns:
        Tuple of (platform, caption, author, restaurant_status, restaurant_name,
                 confidence, reasoning, additional_info, error_message)
    """
    if not url or not url.strip():
        return (
            "", "", "", "", "", "", "",
            "⚠️ Please enter a valid URL", ""
        )

    url = url.strip()

    # Check if URL is supported
    if not parser.is_supported_url(url):
        return (
            "", "", "", "", "", "", "",
            f"❌ Unsupported URL format. Please use TikTok or Instagram Reels URLs.", ""
        )

    try:
        # Parse the URL
        result = parser.parse_url(url)

        if not result.get('success'):
            error_msg = result.get('error', 'Unknown error occurred')
            return (
                "", "", "", "", "", "", "",
                f"❌ Error: {error_msg}", ""
            )

        # Extract results
        platform = result.get('platform', 'Unknown').upper()
        caption = result.get('caption', 'Caption not found')
        author = result.get('author', 'Unknown')

        # Restaurant detection results
        restaurant_found = result.get('restaurant_found', False)
        restaurant_name = result.get('restaurant_name', 'N/A')
        confidence = result.get('confidence', 0)
        reasoning = result.get('reasoning', 'N/A')

        # Format restaurant status
        if restaurant_found:
            restaurant_status = f"✅ YES (Confidence: {confidence * 100:.1f}%)"
        else:
            restaurant_status = "❌ NO"

        # Additional info
        additional_context = result.get('additional_context', '')
        caption_error = result.get('caption_error', '')

        additional_info = ""
        if additional_context:
            additional_info += f"Context: {additional_context}\n"
        if caption_error:
            additional_info += f"⚠️ Caption extraction warning: {caption_error}"

        success_msg = "✅ Parsing completed successfully!"

        return (
            platform,
            caption,
            author if author != 'Unknown' else 'N/A',
            restaurant_status,
            restaurant_name,
            f"{confidence * 100:.1f}%",
            reasoning,
            success_msg,
            additional_info.strip()
        )

    except Exception as e:
        return (
            "", "", "", "", "", "", "",
            f"❌ Error: {str(e)}", ""
        )


def parse_batch_urls(urls_text):
    """
    Parse multiple URLs (one per line)

    Args:
        urls_text: Text with URLs separated by newlines

    Returns:
        Formatted results table
    """
    if not urls_text or not urls_text.strip():
        return "⚠️ Please enter at least one URL"

    urls = [url.strip() for url in urls_text.strip().split('\n') if url.strip()]

    if not urls:
        return "⚠️ No valid URLs found"

    results = []
    results.append("=" * 100)
    results.append(f"BATCH PROCESSING RESULTS ({len(urls)} URLs)")
    results.append("=" * 100)
    results.append("")

    for i, url in enumerate(urls, 1):
        results.append(f"{i}. Processing: {url}")
        results.append("-" * 100)

        if not parser.is_supported_url(url):
            results.append("   ❌ Unsupported URL format")
            results.append("")
            continue

        try:
            result = parser.parse_url(url)

            if not result.get('success'):
                results.append(f"   ❌ Error: {result.get('error', 'Unknown error')}")
                results.append("")
                continue

            # Display results
            results.append(f"   Platform: {result['platform'].upper()}")
            results.append(f"   Author: {result.get('author', 'N/A')}")

            caption = result.get('caption', 'N/A')
            if len(caption) > 150:
                results.append(f"   Caption: {caption[:150]}...")
            else:
                results.append(f"   Caption: {caption}")

            restaurant_found = result.get('restaurant_found', False)
            if restaurant_found:
                results.append(f"   🍽️  Restaurant: ✅ {result.get('restaurant_name', 'Unknown')}")
                results.append(f"   Confidence: {result.get('confidence', 0) * 100:.1f}%")
                results.append(f"   Reasoning: {result.get('reasoning', 'N/A')}")
            else:
                results.append(f"   🍽️  Restaurant: ❌ Not found")
                results.append(f"   Reasoning: {result.get('reasoning', 'N/A')}")

            results.append("")

        except Exception as e:
            results.append(f"   ❌ Error: {str(e)}")
            results.append("")

    results.append("=" * 100)
    results.append("✅ Batch processing completed!")
    results.append("=" * 100)

    return "\n".join(results)


# Create Gradio interface
with gr.Blocks(title="Social Video Parser", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🎬 Social Video Parser
        ### Parse TikTok & Instagram Reels URLs • Extract Captions • Detect Restaurants

        Parse video URLs from TikTok and Instagram Reels to extract captions and detect restaurant mentions using AI.
        """
    )

    # Display current mode
    mode_text = "🤖 AI-Powered Mode (OpenAI GPT)" if use_ai else "🔍 Simple Pattern Matching Mode"
    if not use_ai:
        mode_text += " - Add OPENAI_API_KEY to .env for better results"

    gr.Markdown(f"**Current Mode:** {mode_text}")

    with gr.Tabs():
        # Single URL Tab
        with gr.Tab("📹 Single URL"):
            gr.Markdown("### Parse a single video URL")

            with gr.Row():
                url_input = gr.Textbox(
                    label="Video URL",
                    placeholder="https://www.tiktok.com/@user/video/123 or https://www.instagram.com/reel/ABC/",
                    lines=1
                )

            parse_btn = gr.Button("🔍 Parse Video", variant="primary", size="lg")

            with gr.Row():
                with gr.Column():
                    platform_output = gr.Textbox(label="Platform", interactive=False)
                    author_output = gr.Textbox(label="Author", interactive=False)
                    caption_output = gr.Textbox(label="Caption", lines=5, interactive=False)

                with gr.Column():
                    restaurant_status_output = gr.Textbox(label="Restaurant Found?", interactive=False)
                    restaurant_name_output = gr.Textbox(label="Restaurant Name", interactive=False)
                    confidence_output = gr.Textbox(label="Confidence", interactive=False)
                    reasoning_output = gr.Textbox(label="Reasoning", lines=3, interactive=False)

            status_output = gr.Textbox(label="Status", interactive=False)
            additional_output = gr.Textbox(label="Additional Information", lines=2, interactive=False, visible=True)

            # Examples
            gr.Examples(
                examples=[
                    ["https://www.tiktok.com/@gordonramsayofficial/video/7234567890123456789"],
                    ["https://www.instagram.com/reel/ABC123DEF456/"],
                    ["https://vm.tiktok.com/ZMhs4LD3A/"],
                ],
                inputs=url_input,
                label="Example URLs (click to try)"
            )

            parse_btn.click(
                fn=parse_video_url,
                inputs=[url_input],
                outputs=[
                    platform_output,
                    caption_output,
                    author_output,
                    restaurant_status_output,
                    restaurant_name_output,
                    confidence_output,
                    reasoning_output,
                    status_output,
                    additional_output
                ]
            )

        # Batch Processing Tab
        with gr.Tab("📋 Batch Processing"):
            gr.Markdown("### Parse multiple video URLs at once")
            gr.Markdown("Enter one URL per line")

            batch_input = gr.Textbox(
                label="Video URLs (one per line)",
                placeholder="https://www.tiktok.com/@user/video/123\nhttps://www.instagram.com/reel/ABC/\nhttps://www.tiktok.com/@user2/video/456",
                lines=8
            )

            batch_btn = gr.Button("🔍 Parse All URLs", variant="primary", size="lg")

            batch_output = gr.Textbox(
                label="Results",
                lines=20,
                interactive=False,
                show_copy_button=True
            )

            batch_btn.click(
                fn=parse_batch_urls,
                inputs=[batch_input],
                outputs=[batch_output]
            )

        # About Tab
        with gr.Tab("ℹ️ About"):
            gr.Markdown(
                """
                ## About This Tool

                This tool parses social media video URLs from TikTok and Instagram Reels to:
                - Extract video captions and descriptions
                - Detect restaurant mentions using AI
                - Provide confidence scores and reasoning

                ### Supported Platforms
                - **TikTok**: Standard URLs, short links (vm.tiktok.com), and mobile links
                - **Instagram**: Reels, posts, and IGTV videos

                ### Detection Modes

                **AI-Powered Mode** (Recommended)
                - Uses OpenAI GPT for intelligent restaurant detection
                - Provides higher accuracy and detailed context
                - Requires OPENAI_API_KEY in environment variables

                **Simple Pattern Matching Mode**
                - Uses regex patterns and keywords
                - Works without API key
                - Good for obvious restaurant mentions

                ### How to Use

                1. **Single URL**: Paste a TikTok or Instagram Reels URL and click "Parse Video"
                2. **Batch Processing**: Enter multiple URLs (one per line) and click "Parse All URLs"
                3. View results including caption, restaurant detection, and confidence scores

                ### Setup for AI Mode

                ```bash
                # Create .env file
                cp .env.example .env

                # Edit .env and add your OpenAI API key
                OPENAI_API_KEY=your_key_here

                # Restart the app
                python app.py
                ```

                ### Technical Details

                - **Web Scraping**: Extracts captions from video pages
                - **AI Analysis**: Uses GPT-3.5-turbo for restaurant detection
                - **Fallback**: Automatic fallback to pattern matching if AI fails
                - **Error Handling**: Comprehensive error handling and reporting

                ---

                Built with Python, Gradio, OpenAI API, and BeautifulSoup
                """
            )

    gr.Markdown(
        """
        ---
        💡 **Tip**: For best results, use AI mode by adding your OpenAI API key to the `.env` file
        """
    )


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🚀 Starting Social Video Parser Web Interface")
    print("=" * 80)
    print(f"Mode: {mode_text}")
    print("=" * 80 + "\n")

    # Launch the app
    demo.launch(
        server_name="0.0.0.0",  # Listen on all interfaces
        server_port=7860,       # Default Gradio port
        share=False,            # Set to True to create a public link
        show_error=True
    )
