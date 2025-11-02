#!/bin/bash
# Setup script for Social Video Parser

echo "🚀 Setting up Social Video Parser..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "⚠️  Please edit .env and add your OpenAI API key"
else
    echo "✓ .env file already exists"
fi
echo ""

echo "="
echo "✅ Setup complete!"
echo "="
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your OpenAI API key (optional, for AI-powered detection)"
echo "  2. Activate the virtual environment: source venv/bin/activate"
echo "  3. Run tests: python test_parser.py"
echo "  4. Run examples: python example.py"
echo "  5. Parse a URL: python main.py 'https://www.tiktok.com/@user/video/123'"
echo ""
