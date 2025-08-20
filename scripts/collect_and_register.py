import requests
from bs4 import BeautifulSoup
from pathlib import Path
import sqlite3
from datetime import datetime
import re

# Directories
greek_dir = Path('corpus_texts/perseus_greek')
eng_dir = Path('corpus_texts/perseus_translations/english')
greek_dir.mkdir(parents=True, exist_ok=True)
eng_dir.mkdir(parents=True, exist_ok=True)

# Database path
db_path = 'corpus.db'

def save_text(filename, content):
    path = Path(filename)
    path.write_text(content, encoding='utf-8')
    return str(path)

def insert_metadata(filename, language, title, author, period, subject):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now = datetime.now().isoformat(sep=' ', timespec='seconds')
    cursor.execute(
        "INSERT INTO texts (filename, language, processed_at, title, author, period, subject) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (filename, language, now, title, author, period, subject)
    )
    conn.commit()
    conn.close()

def fetch_greek_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.get_text()
    return text

def fetch_english_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.get_text()
    return text

def generate_title(body_text):
    lines = body_text.splitlines()
    for line in lines:
        line = line.strip()
        if line:
            return line[:100]
    return "Untitled"

# Main process
if __name__ == '__main__':
    # Example input: Use your source URLs
    greek_url = input("Enter Greek text URL: ")
    english_url = input("Enter English translation URL: ")
    subject = input("Enter subject/topic: ")

    # Fetch texts
    greek_text = fetch_greek_text(greek_url)
    english_text = fetch_english_text(english_url)

    # Generate filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    greek_filename = f'perseus_greek/collection_{timestamp}.txt'
    english_filename = f'perseus_translations/english/collection_{timestamp}.txt'

    # Save texts
    save_text(greek_filename, greek_text)
    save_text(english_filename, english_text)

    # Generate metadata
    title = generate_title(greek_text)
    # For author and period, consider manual input or automated metadata extraction
    author = 'Various'  # Or parse from source
    period = 'Known Period'  # Or parse from source

    # Record into database
    insert_metadata(greek_filename, 'greek', title, author, period, subject)
    insert_metadata(english_filename, 'english', title, author, period, subject)

    print(f"Saved texts and metadata for {title}")
