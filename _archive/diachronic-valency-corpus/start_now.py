#!/usr/bin/env python3
"""
START YOUR CORPUS NOW!
One command to launch everything
"""

import os
import sys
import subprocess

print("""
================================================================================
                    DIACHRONIC CORPUS AGENT - READY TO START
================================================================================

Checking your setup...
""")

# 1. Check Z: drive
if os.path.exists("Z:\\"):
    print("✅ Z: drive found")
else:
    print("❌ Z: drive not found - please connect your external drive")
    sys.exit(1)

# 2. Create directory
BASE_PATH = "Z:\\DiachronicValencyCorpus"
os.makedirs(BASE_PATH, exist_ok=True)
print(f"✅ Directory created: {BASE_PATH}")

# 3. Check Python packages
required = ['requests', 'lxml', 'beautifulsoup4', 'pandas', 'schedule']
missing = []

for package in required:
    try:
        __import__(package)
        print(f"✅ {package} installed")
    except ImportError:
        missing.append(package)
        print(f"❌ {package} missing")

if missing:
    print(f"\nInstalling missing packages...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
    print("✅ All packages installed")

# 4. Optional tools check
print("\nOptional tools (will work without these):")
optional = ['spacy', 'nltk', 'stanza', 'cltk']
for tool in optional:
    try:
        __import__(tool)
        print(f"✅ {tool} available")
    except:
        print(f"⚡ {tool} not installed (agent will work anyway)")

print("""
================================================================================
                              READY TO START!
================================================================================

Your agent will:
✅ Store everything on Z: drive
✅ Connect to your GitHub (nlavidas/diachronic-indo-european-corpus)
✅ Download REAL texts (no placeholders)
✅ Run 24/7 without stopping
✅ Have 1 hour consultation every morning at 09:00
✅ Process texts with Beck conversion
✅ Build massive corpus (10,000+ texts)

Starting in 5 seconds...
""")

import time
time.sleep(5)

# Launch the agent
print("\n🚀 LAUNCHING AGENT...\n")
os.system("python final_complete_agent.py")