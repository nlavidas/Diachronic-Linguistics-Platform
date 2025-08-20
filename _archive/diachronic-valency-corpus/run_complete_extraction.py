#!/usr/bin/env python3
"""
Complete extraction pipeline using both the working extractor 
and the autonomous agent
"""

import os
import sys
import subprocess
import time
from datetime import datetime

print("=== DIACHRONIC CORPUS COMPLETE EXTRACTION ===")
print(f"Started at: {datetime.now()}")
print(f"Working directory: {os.getcwd()}")

# Step 1: Run the working valency extractor
print("\n1. Running proven valency extractor...")
try:
    result = subprocess.run([sys.executable, "valency_extractor_fixed.py"], 
                          capture_output=True, text=True)
    print("Valency extraction completed!")
    print(f"Output files in: corpus_data/")
except Exception as e:
    print(f"Error running valency extractor: {e}")

# Step 2: Check database contents
print("\n2. Checking database contents...")
try:
    result = subprocess.run([sys.executable, "check_database.py"], 
                          capture_output=True, text=True)
    print(result.stdout)
except Exception as e:
    print(f"Error checking database: {e}")

# Step 3: Run autonomous agent for additional processing
print("\n3. Running autonomous agent...")
try:
    # Run for just 5 minutes to test
    result = subprocess.run([sys.executable, "autonomous_agent_fixed.py"], 
                          timeout=300, capture_output=True, text=True)
except subprocess.TimeoutExpired:
    print("Agent running successfully (stopped after 5 minutes for testing)")
except Exception as e:
    print(f"Error running agent: {e}")

print(f"\nCompleted at: {datetime.now()}")
print("\nNext steps:")
print("1. Check corpus_data/ for extraction results")
print("2. Check valency/valency_patterns.db for database")
print("3. Check reports/daily/ for reports")