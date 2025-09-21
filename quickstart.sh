#!/bin/bash

# Claude Cache - Quick Start Script

echo "Claude Cache - Quick Start"
echo "======================================"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install package
echo ""
echo "Installing Claude Cache..."
pip install -e . --quiet

# Run test
echo ""
echo "Running installation test..."
python test_installation.py

echo ""
echo "======================================"
echo "Setup complete!"
echo ""
echo "To start using Claude Cache:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Start monitoring: cache start"
echo "  3. Or process existing logs: cache process"
echo ""
echo "For help: cache --help"