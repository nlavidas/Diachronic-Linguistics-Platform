import sqlite3
import datetime

conn = sqlite3.connect('corpus.db')
cursor = conn.cursor()
now = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')

cursor.execute(
    "INSERT INTO texts (filename, language, processed_at) VALUES (?, ?, ?)",
    ('perseus_translations/english/Argonautica_Seaton1915_complete.txt', 'english', now)
)

conn.commit()
print(f"Added Seaton 1915 translation to database (ID: {cursor.lastrowid})")
conn.close()
