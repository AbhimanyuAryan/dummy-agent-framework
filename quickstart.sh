#!/bin/bash
# Quick start script for Gemini Agent on Unix/Linux/Mac

echo "============================================"
echo "Gemini Agent Framework - Quick Start"
echo "============================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo

# Check for .env file
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and add your API key"
    echo
    exit 1
fi

# Run test
echo "Running installation test..."
echo
python test_setup.py

echo
echo "============================================"
echo "Setup complete!"
echo "============================================"
echo
echo "To use the agent:"
echo "  1. python -m gemini_agent.cli"
echo "  2. python examples/simple_example.py"
echo
