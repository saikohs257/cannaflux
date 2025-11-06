#!/bin/bash

# CryptoLLM Setup Script

echo "================================================"
echo "CryptoLLM Setup"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
echo "This may take several minutes..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ".env file created. You can customize it as needed."
fi

# Create examples directory if it doesn't exist
mkdir -p examples

echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "To get started:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the interactive chat:"
echo "     python crypto_llm.py"
echo ""
echo "  3. Or launch the web interface:"
echo "     python web_interface.py"
echo ""
echo "  4. Or try an example:"
echo "     python examples/simple_question.py"
echo ""
echo "See README.md for more information."
echo "================================================"
