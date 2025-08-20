#!/usr/bin/env python3
"""
Process the successfully downloaded files with the working extractor
"""

import os
import sys
import shutil
from lxml import etree

# First, let's copy the Greek NT to where the valency extractor expects it
print("Setting up files for processing...")

# Source and destination
source = "Z:\\DiachronicValencyCorpus\\texts\\greek\\koine\\proiel_greek_nt.xml"
dest_dir = "Z:\\DiachronicValencyCorpus\\corpus_data"
dest_file = os.path.join(dest_dir, "greek-nt.xml")

# Create corpus_data directory if needed
os.makedirs(dest_dir, exist_ok=True)

# Copy the file
if os.path.exists(source):
    shutil.copy2(source, dest_file)
    print(f"Copied Greek NT to {dest_file}")
    
    # Now run the valency extractor
    print("\nRunning valency extractor...")
    os.system("python valency_extractor_fixed.py")
else:
    print(f"Source file not found: {source}")

# Also process other Greek texts
iliad_source = "Z:\\DiachronicValencyCorpus\\texts\\greek\\ancient\\iliad_perseus.xml"
if os.path.exists(iliad_source):
    print(f"\nFound Iliad at: {iliad_source}")
    # We can process this too later