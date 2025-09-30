import requests
from bs4 import BeautifulSoup
import time
import json
import sqlite3
from pathlib import Path

class AutomaticTextCollector:
    def __init__(self):
        self.db_path = 'Z:\\GlossaChronos\\texts.db'
        self.init_db()
        
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS texts
                     (id INTEGER PRIMARY KEY, 
                      source TEXT, 
                      title TEXT, 
                      author TEXT,
                      period TEXT,
                      language TEXT,
                      raw_text TEXT,
                      processed TEXT,
                      url TEXT,
                      fetched_date TEXT)''')
        conn.commit()
        conn.close()
    
    def fetch_gutenberg_catalog(self):
        """Get list of historical texts from Gutenberg"""
        # Real Gutenberg catalog API
        catalog_url = "https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2"
        # For now, use known IDs
        historical_texts = {
            '16328': 'Beowulf',
            '2383': 'Canterbury Tales', 
            '1250': 'Le Morte Darthur',
            '5': 'The Prince (Machiavelli)',
            '996': 'Don Quixote'
        }
        return historical_texts
    
    def fetch_text(self, gutenberg_id):
        """Fetch actual text from Gutenberg"""
        url = f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-0.txt"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    
    def run_24_7_collector(self):
        """Run continuously, fetching texts"""
        while True:
            texts = self.fetch_gutenberg_catalog()
            for text_id, title in texts.items():
                if not self.text_exists(text_id):
                    print(f"Fetching {title}...")
                    content = self.fetch_text(text_id)
                    if content:
                        self.save_text(text_id, title, content)
                time.sleep(60)  # Wait between fetches