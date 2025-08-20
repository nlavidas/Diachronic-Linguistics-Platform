import requests
from bs4 import BeautifulSoup
from pathlib import Path
import sqlite3
import datetime

def collect_homer_translations():
    """Collect different Homer translations from Gutenberg"""
    print("=== COLLECTING HOMER TRANSLATIONS ===")
    
    # Search for Homer Iliad
    search_url = 'https://www.gutenberg.org/ebooks/search/?query=Homer%20Iliad'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    translations_found = []
    for result in soup.select('li.booklink')[:3]:  # First 3 results
        title_elem = result.select_one('span.title')
        link_elem = result.select_one('a')
        
        if title_elem and link_elem:
            book_id = link_elem['href'].split('/')[-1]
            title = title_elem.get_text(strip=True)
            
            print(f"Found: {title} (ID: {book_id})")
            
            # Download the text
            download_url = f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8'
            try:
                text_response = requests.get(download_url, timeout=30)
                if text_response.status_code == 200:
                    # Save to file
                    filename = f'Homer_Iliad_translation_{book_id}.txt'
                    filepath = Path('corpus_texts/gutenberg_translations') 
                    filepath.mkdir(parents=True, exist_ok=True)
                    full_path = filepath / filename
                    full_path.write_text(text_response.text, encoding='utf-8')
                    
                    # Add to database
                    conn = sqlite3.connect('corpus.db')
                    cursor = conn.cursor()
                    now = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
                    rel_path = f'gutenberg_translations/{filename}'
                    cursor.execute(
                        "INSERT INTO texts (filename, language, processed_at) VALUES (?, ?, ?)",
                        (rel_path, 'english', now)
                    )
                    conn.commit()
                    conn.close()
                    
                    translations_found.append({
                        'title': title,
                        'id': book_id,
                        'file': rel_path,
                        'words': len(text_response.text.split())
                    })
                    print(f"Downloaded: {filename} ({len(text_response.text.split()):,} words)")
                    
            except Exception as e:
                print(f"Failed to download {book_id}: {e}")
    
    print(f"\n=== COLLECTION COMPLETE ===")
    print(f"Downloaded {len(translations_found)} Homer translations")
    return translations_found

if __name__ == "__main__":
    results = collect_homer_translations()
    for result in results:
        print(f"- {result['title']}: {result['words']:,} words")
