import sqlite3
import datetime

conn = sqlite3.connect('corpus.db')
cursor = conn.cursor()
now = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
entries = [
    ('perseus_greek/Argonautica_book1_greek.txt', 'greek', now),
    ('perseus_translations/english/Argonautica_book1_english.txt', 'english', now)
]
cursor.executemany(
    "INSERT INTO texts (filename, language, processed_at) VALUES (?, ?, ?)",
    entries
)
conn.commit()
print(f"Inserted {cursor.rowcount} new records into texts")
conn.close()
