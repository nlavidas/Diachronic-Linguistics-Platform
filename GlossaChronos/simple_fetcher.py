import requests
import sqlite3
from datetime import datetime

def fetch_gutenberg(text_id):
    url = f"https://www.gutenberg.org/files/{text_id}/{text_id}-0.txt"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Fetched text {text_id}: {len(response.text)} characters")
        return response.text
    return None

# Test with Canterbury Tales
text = fetch_gutenberg("2383")
print("First 200 chars:", text[:200] if text else "Failed")
