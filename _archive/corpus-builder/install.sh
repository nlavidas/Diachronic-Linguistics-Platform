#!/bin/bash

echo "[INFO] Installing AI-Powered Corpus System..."

# Update and Upgrade System
sudo apt update && sudo apt upgrade -y

# Install Required Packages
sudo apt install -y wget curl git unzip python3 python3-pip python3-venv

# Create a Virtual Environment
python3 -m venv ai-corpus-env
source ai-corpus-env/bin/activate

# Install AI-Powered Corpus Dependencies
pip install flask requests numpy pandas torch transformers

# Clone the Corpus Processing Repository (Optional Step - If Hosted)
git clone https://github.com/nlavidas/corpus-builder.git

echo "[INFO] Installation Complete! Run 'python3 main.py' to start the system."
