import requests
from pathlib import Path

# Download the Seaton 1915 translation
url = 'https://www.gutenberg.org/ebooks/830.txt.utf-8'
response = requests.get(url)

if response.status_code == 200:
    # Create directory
    translation_dir = Path('corpus_texts/perseus_translations/english')
    translation_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file
    output_file = translation_dir / 'Argonautica_Seaton1915_complete.txt'
    output_file.write_text(response.text, encoding='utf-8')
    
    # Get file stats
    text_length = len(response.text)
    word_count = len(response.text.split())
    
    print('=== SEATON TRANSLATION DOWNLOADED ===')
    print(f'File saved: {output_file}')
    print(f'Text length: {text_length:,} characters')
    print(f'Word count: {word_count:,} words')
    print(f'Translator: R.C. Seaton (1915)')
    
else:
    print(f'Download failed: {response.status_code}')
