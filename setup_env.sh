#!/bin/bash

# Create virtual environment
python3 -m venv venv
# Activate virtual environment
source venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Virtual environment setup and activated."

