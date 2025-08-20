#!/usr/bin/env python3
"""
KICKSTART DOWNLOADS
Forces immediate download of new texts
Run this when agent seems stuck
"""

import os
import sys
import time
import requests
import sqlite3
from datetime import datetime
from pathlib import Path

BASE_PATH = "Z:\\DiachronicValencyCorpus"

# Additional sources to download immediately
IMMEDIATE_DOWNLOADS = [
    # More Gutenberg texts
    ('https://www.gutenberg.org/files/1727/1727-0.txt', 'Odyssey_Butcher_Lang_1879'),
    ('https://www.gutenberg.org/files/3160/3160-0.txt', 'Odyssey_Lawrence_1932'),
    ('https://www.gutenberg.org/files/1728/1728-0.txt', 'Odyssey_Pope_1899'),
    ('https://www.gutenberg.org/files/228/228-0.txt', 'Aesop_Fables_Townsend'),
    ('https://www.gutenberg.org/files/2456/2456-0.txt', 'Eclogues_Virgil'),
    ('https://www.gutenberg.org/files/22/22-0.txt', 'Beowulf_Gummere'),
    ('https://www.gutenberg.org/files/16328/16328-0.txt', 'Beowulf_Hall'),
    ('https://www.gutenberg.org/files/4783/4783-0.txt', 'Heimskringla_Norse'),
    ('https://www.gutenberg.org/files/17008/17008-0.txt', 'Nibelungenlied'),
    ('https://www.gutenberg.org/files/2500/2500-0.txt', 'Siddhartha_Hesse'),
]

def download_now(url, filename):
    """Download a single text immediately"""
    try:
        print(f"📥 Downloading: {filename}...", end='', flush=True)
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save text
        output_path = Path(BASE_PATH) / f'texts/collected/{filename}.txt'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        # Record in database
        db_path = Path(BASE_PATH) / 'corpus_complete.db'
        if db_path.exists():
            db = sqlite3.connect(str(db_path))
            cursor = db.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO texts 
                (filename, source, url, size, download_time)
                VALUES (?, ?, ?, ?, datetime('now'))
            ''', (filename, 'gutenberg', url, len(response.text)))
            db.commit()
            db.close()
            
        print(f" ✅ Done! ({len(response.text):,} bytes)")
        return True
        
    except Exception as e:
        print(f" ❌ Failed: {e}")
        return False

def main():
    print("="*60)
    print("🚀 KICKSTART DOWNLOADS - Force New Collection")
    print("="*60)
    print(f"Time: {datetime.now()}")
    print(f"Target: {BASE_PATH}")
    print("-"*60)
    
    # Check current status
    text_dir = Path(BASE_PATH) / "texts/collected"
    if text_dir.exists():
        current_texts = list(text_dir.glob('*.txt'))
        print(f"Current texts: {len(current_texts)}")
    else:
        print("Creating text directory...")
        text_dir.mkdir(parents=True, exist_ok=True)
        
    print("\n🔥 Starting immediate downloads...\n")
    
    success = 0
    for url, filename in IMMEDIATE_DOWNLOADS:
        # Check if already downloaded
        if (text_dir / f"{filename}.txt").exists():
            print(f"⏭️  Skipping {filename} (already exists)")
            continue
            
        if download_now(url, filename):
            success += 1
            time.sleep(2)  # Be polite
            
    print("\n" + "="*60)
    print(f"✅ Downloaded {success} new texts!")
    print(f"Total texts now: {len(list(text_dir.glob('*.txt')))}")
    print("="*60)
    
    # Create a timestamp file to show we ran
    timestamp_file = Path(BASE_PATH) / f"kickstart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(timestamp_file, 'w') as f:
        f.write(f"Kickstart ran at {datetime.now()}\n")
        f.write(f"Downloaded {success} texts\n")
        
    print(f"\nLog saved to: {timestamp_file}")
    

if __name__ == "__main__":
    main()