import requests
import sqlite3
import time
from datetime import datetime

class AutoTextFetcher:
    def __init__(self):
        self.texts_to_fetch = [
            ('16328', 'Beowulf', 'Unknown', 'old_english'),
            ('2383', 'Canterbury Tales', 'Chaucer', 'middle_english'),
            ('26', 'Paradise Lost', 'Milton', 'early_modern'),
            ('1524', 'Hamlet', 'Shakespeare', 'early_modern'),
            ('996', 'Don Quixote', 'Cervantes', 'early_modern')
        ]
        
    def fetch_all(self):
        for text_id, title, author, period in self.texts_to_fetch:
            print(f"Fetching {title}...")
            url = f"https://www.gutenberg.org/files/{text_id}/{text_id}-0.txt"
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    print(f"  Success: {len(r.text)} chars")
                else:
                    print(f"  Failed: {r.status_code}")
            except Exception as e:
                print(f"  Error: {e}")
            time.sleep(2)  # Be polite to Gutenberg

fetcher = AutoTextFetcher()
fetcher.fetch_all()
