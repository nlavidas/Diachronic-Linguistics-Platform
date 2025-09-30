import sqlite3
import requests
import json

conn = sqlite3.connect('Z:\\GlossaChronos\\texts.db')
c = conn.cursor()
c.execute("SELECT raw_text FROM texts WHERE gutenberg_id='2383'")
text = c.fetchone()[0][:1000]  # First 1000 chars
conn.close()

# Send to bridge for processing
response = requests.post('http://localhost:5000/api/process',
                         json={'text': text, 'period': 'middle_english'})
print("Processing result:", response.json())
