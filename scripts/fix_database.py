import sqlite3
from pathlib import Path

# Delete old database if exists
db_path = Path('corpus.db')
if db_path.exists():
   db_path.unlink()
   print('Old database deleted')

# Create new database with correct schema
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS texts (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   title TEXT,
   author TEXT,
   period TEXT,
   source_url TEXT,
   full_description TEXT,
   summary TEXT,
   body TEXT,
   language TEXT,
   collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS metadata (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   text_id INTEGER,
   key TEXT,
   value TEXT,
   FOREIGN KEY(text_id) REFERENCES texts(id)
)''')

conn.commit()
conn.close()
print('Database created successfully with correct schema')
