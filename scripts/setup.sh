#!/bin/bash

echo "Setting up AI Film Studio..."

mkdir -p data/{raw,processed,model_cache}
mkdir -p logs
mkdir -p models

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete! Activate with: source venv/bin/activate"
