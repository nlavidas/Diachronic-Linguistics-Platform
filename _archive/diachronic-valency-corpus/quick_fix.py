#!/usr/bin/env python3
"""
Quick fix script - fixes the syntax error and runs the agent
"""

import os
import subprocess
import sys

# Fix the syntax error in complete_agent.py
print("🔧 Fixing syntax error in complete_agent.py...")

try:
    with open('complete_agent.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all emoji characters that might cause issues
    replacements = {
        '⚠️': 'WARNING:',
        '❌': 'ERROR:',
        '✅': 'OK:',
        '🔄': 'RESTART:'
    }
    
    for emoji, text in replacements.items():
        content = content.replace(emoji, text)
    
    # Save fixed version
    with open('complete_agent_fixed.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed! Saved as complete_agent_fixed.py")
    
except Exception as e:
    print(f"Error fixing file: {e}")
    print("Please manually fix the syntax error on line 50")
    sys.exit(1)

# Install basic requirements
print("\n📦 Installing basic requirements...")
requirements = ['requests', 'beautifulsoup4', 'lxml', 'pandas', 'schedule']

for req in requirements:
    try:
        __import__(req.replace('-', '_'))
        print(f"✅ {req} already installed")
    except ImportError:
        print(f"Installing {req}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', req])

# Install ML tools
print("\n🤖 Installing ML tools (this may take a few minutes)...")
ml_tools = ['spacy', 'transformers', 'nltk']

for tool in ml_tools:
    try:
        print(f"\nInstalling {tool}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', tool])
        print(f"✅ {tool} installed")
    except:
        print(f"⚠️  {tool} installation failed - agent will work without it")

# Install spaCy model
try:
    print("\n📦 Installing spaCy English model...")
    subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
    print("✅ spaCy model installed")
except:
    print("⚠️  spaCy model installation failed")

# Download NLTK data
try:
    print("\n📦 Downloading NLTK data...")
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
    print("✅ NLTK data downloaded")
except:
    print("⚠️  NLTK data download failed")

print("\n" + "="*70)
print("✅ SETUP COMPLETE!")
print("="*70)

# Run the fixed agent
print("\n🚀 Starting the Diachronic Corpus Agent...")
print("="*70)

try:
    subprocess.run([sys.executable, 'complete_agent_fixed.py'])
except KeyboardInterrupt:
    print("\n\nAgent stopped by user")
except Exception as e:
    print(f"\nError running agent: {e}")
    print("Try running manually: python complete_agent_fixed.py")