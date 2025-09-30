import requests
import sqlite3
from datetime import datetime
import json

class TextCollector:
    def __init__(self):
        self.db_path = 'Z:\\GlossaChronos\\texts.db'
        self.init_db()
        
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS texts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      gutenberg_id TEXT UNIQUE,
                      title TEXT,
                      author TEXT,
                      period TEXT,
                      language TEXT,
                      raw_text TEXT,
                      char_count INTEGER,
                      fetched_date TEXT)''')
        conn.commit()
        conn.close()
        
    def fetch_and_store(self, text_id, title, author, period):
        url = f"https://www.gutenberg.org/files/{text_id}/{text_id}-0.txt"
        response = requests.get(url)
        if response.status_code == 200:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO texts 
                         VALUES (NULL,?,?,?,?,?,?,?,?)''',
                      (text_id, title, author, period, 'english',
                       response.text, len(response.text),
                       datetime.now().isoformat()))
            conn.commit()
            conn.close()
            print(f"Stored: {title} ({len(response.text)} chars)")
            return True
        return False
        
# Fetch key historical texts
collector = TextCollector()
texts = [
    ("2383", "Canterbury Tales", "Chaucer", "middle_english"),
    ("16328", "Beowulf", "Unknown", "old_english"),
    ("26", "Paradise Lost", "Milton", "early_modern")
]

for text_id, title, author, period in texts:
    collector.fetch_and_store(text_id, title, author, period)
