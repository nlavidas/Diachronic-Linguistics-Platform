#!/usr/bin/env python3
"""
Immediate collection agent - starts working right away
"""

import os
import sys
import time
import json
import sqlite3
import requests
import logging
from datetime import datetime
import threading

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class ImmediateAgent:
    def __init__(self):
        self.init_database()
        
    def init_database(self):
        self.db = sqlite3.connect('immediate_agent.db', check_same_thread=False)
        cursor = self.db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY,
                work TEXT,
                translator TEXT,
                year INTEGER,
                url TEXT,
                size INTEGER,
                collected DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.db.commit()
        
    def collect_now(self):
        """Collect texts immediately"""
        logging.info("📚 Starting immediate collection...")
        
        texts_to_collect = [
            {
                'work': 'Bible',
                'translator': 'KJV',
                'year': 1611,
                'url': 'https://www.gutenberg.org/files/10/10-0.txt'
            },
            {
                'work': 'Iliad',
                'translator': 'Butler',
                'year': 1898,
                'url': 'https://www.gutenberg.org/cache/epub/2199/pg2199.txt'
            },
            {
                'work': 'Iliad', 
                'translator': 'Chapman',
                'year': 1611,
                'url': 'https://www.gutenberg.org/files/48895/48895-0.txt'
            },
            {
                'work': 'Iliad',
                'translator': 'Pope', 
                'year': 1720,
                'url': 'https://www.gutenberg.org/files/6130/6130-0.txt'
            },
            {
                'work': 'Metamorphoses',
                'translator': 'More',
                'year': 1922,
                'url': 'https://www.gutenberg.org/files/26073/26073-0.txt'
            }
        ]
        
        collected = 0
        
        for text in texts_to_collect:
            logging.info(f"Downloading: {text['work']} - {text['translator']} ({text['year']})")
            
            try:
                response = requests.get(
                    text['url'], 
                    timeout=60,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                
                if response.status_code == 200:
                    # Save file
                    filename = f"{text['work']}_{text['translator']}_{text['year']}.txt"
                    filepath = os.path.join('texts/collected', filename)
                    
                    os.makedirs('texts/collected', exist_ok=True)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                        
                    # Log to database
                    cursor = self.db.cursor()
                    cursor.execute('''
                        INSERT INTO texts (work, translator, year, url, size)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (text['work'], text['translator'], text['year'], 
                         text['url'], len(response.text)))
                    self.db.commit()
                    
                    collected += 1
                    logging.info(f"✅ Success! Size: {len(response.text):,} characters")
                    
                else:
                    logging.error(f"❌ Failed: HTTP {response.status_code}")
                    
            except Exception as e:
                logging.error(f"❌ Error: {e}")
                
            # Brief pause between downloads
            time.sleep(2)
            
        logging.info(f"\n📊 Collection complete! Downloaded {collected} texts")
        
        # Show what we collected
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM texts')
        
        print("\n📚 COLLECTED TEXTS:")
        print("-" * 60)
        for row in cursor.fetchall():
            print(f"{row[1]} - {row[2]} ({row[3]}): {row[5]:,} characters")
            
    def run(self):
        """Run the agent"""
        # Collect immediately
        self.collect_now()
        
        # Then continue with regular schedule
        while True:
            time.sleep(3600)  # Wait 1 hour
            logging.info("⏰ Checking for new texts...")
            # Could add more collection here
            

if __name__ == "__main__":
    print("🚀 Immediate Collection Agent")
    print("📚 Starting downloads now...\n")
    
    agent = ImmediateAgent()
    agent.run()