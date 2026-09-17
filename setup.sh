#!/bin/bash

echo "========================================="
echo "Herb Identification System - Setup"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "========================================="
echo "Setup complete!"
echo "========================================="
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then open your browser to: http://localhost:8000"
echo ""
