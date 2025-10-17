#!/bin/bash

# Synthetic Data Generator - Installation and Run Script

echo "🎲 Synthetic Data Generator - Installation Script"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check the requirements.txt file."
    exit 1
fi

# Run tests
echo ""
echo "🧪 Running tests..."
python3 test_app.py

if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "⚠️  Some tests failed, but the app might still work."
fi

# Start the application
echo ""
echo "🚀 Starting Synthetic Data Generator..."
echo "The application will be available at: http://localhost:7860"
echo "Press Ctrl+C to stop the application."
echo ""

python3 app.py
