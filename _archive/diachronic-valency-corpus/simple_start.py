#!/usr/bin/env python3
"""
SIMPLE CORPUS COLLECTOR
Minimal version that just works
"""

import os
import time
import requests
import sqlite3
from datetime import datetime

print("SIMPLE DIACHRONIC CORPUS COLLECTOR")
print("==================================")
print(f"Starting at: {datetime.now()}")
print(f"Working directory: {os.getcwd()}")

# Create directories
os.makedirs("corpus/collected", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# Create database
db = sqlite3.connect('simple_corpus.db')
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS texts (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        url TEXT,
        size INTEGER,
        downloaded DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
db.commit()

# Download some texts
texts_to_download = [
    ("https://www.gutenberg.org/files/10/10-0.txt", "Bible_KJV.txt"),
    ("https://www.gutenberg.org/files/2199/2199-0.txt", "Iliad_Butler.txt"),
    ("https://www.gutenberg.org/files/48895/48895-0.txt", "Iliad_Chapman.txt"),
]

for url, filename in texts_to_download:
    filepath = os.path.join("corpus/collected", filename)
    
    if os.path.exists(filepath):
        print(f"Already have: {filename}")
        continue
        
    print(f"Downloading: {filename}...")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            cursor.execute('INSERT INTO texts (filename, url, size) VALUES (?, ?, ?)',
                         (filename, url, len(response.text)))
            db.commit()
            
            print(f"  Success! {len(response.text):,} bytes")
    except Exception as e:
        print(f"  Error: {e}")

# Show what we have
print("\nCurrent corpus:")
cursor.execute('SELECT filename, size FROM texts')
for filename, size in cursor.fetchall():
    print(f"  {filename}: {size:,} bytes")

db.close()
print("\nDone! Check corpus/collected/ folder")