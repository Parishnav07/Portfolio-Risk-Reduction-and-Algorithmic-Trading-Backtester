#!/bin/bash

# Portfolio Risk Reduction - Setup Script

echo "=================================================="
echo "Portfolio Risk Reduction - Setup"
echo "=================================================="

# Check Python version
echo ""
echo "Checking Python version..."
python --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
echo ""
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file"
    echo "⚠ Please edit .env and add your Gemini API key"
else
    echo "✓ .env file already exists"
fi

# Create output directory
echo ""
echo "Creating output directory..."
mkdir -p output
mkdir -p sample_data

# Generate sample data
echo ""
echo "Generating sample data..."
python generate_sample_data.py

echo ""
echo "=================================================="
echo "✓ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env file and add your Gemini API key"
echo "  2. Run the web app: streamlit run app.py"
echo "  3. Or use CLI: python main.py sample_data/stock_data.csv"
echo ""
echo "For detailed instructions, see README.md"
echo "For quick start, see QUICKSTART.md"
echo ""
