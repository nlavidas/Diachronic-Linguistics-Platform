import sqlite3
import requests

# Get a text from database
conn = sqlite3.connect('texts.db')
c = conn.cursor()
c.execute("SELECT raw_text FROM texts WHERE gutenberg_id='16328' LIMIT 1")
result = c.fetchone()
conn.close()

if result:
    text_sample = result[0][:200]  # First 200 chars of Beowulf
    
    # Process through pipeline
    response = requests.post('http://localhost:5000/api/process',
                            json={'text': text_sample, 'period': 'old_english'})
    print("Processing result:", response.json())
else:
    print("No Beowulf text found in database")
