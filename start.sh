#!/bin/bash

echo "========================================"
echo "🚀 Social Video Parser - Full Stack App"
echo "========================================"
echo ""

# Check if in the right directory
if [ ! -f "backend/api.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Start backend
echo "📦 Starting Backend API (FastAPI)..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install backend dependencies
pip install -q -r requirements.txt

# Start backend in background
echo "✓ Backend starting on http://localhost:8000"
python3 api.py &
BACKEND_PID=$!

cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Start frontend
echo ""
echo "🎨 Starting Frontend (Next.js)..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies (this may take a minute)..."
    npm install
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    cp .env.local.example .env.local
fi

echo "✓ Frontend starting on http://localhost:3000"
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "========================================"
echo "✅ Application Started Successfully!"
echo "========================================"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
