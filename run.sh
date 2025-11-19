#!/bin/bash
# Quick start script for Linux/Mac

echo "Starting Smart Water Saver Agent..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please create a .env file with your API keys."
    echo "See .env.example for reference."
    echo ""
    exit 1
fi

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting FastAPI server..."
echo "Access the API at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""

python main.py

