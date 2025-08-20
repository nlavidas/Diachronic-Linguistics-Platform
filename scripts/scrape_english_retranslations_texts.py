# scripts/scrape_english_retranslations_texts.py

import re
import requests
from pathlib import Path
import json
import time

def download_text(url):
    r = requests.get(url, timeout=30)
    r.encoding = 'utf-8'
    text = r.text
    if 'Project Gutenberg' in url:
        start = text.find('\n\n') + 2
        end = text.rfind('***')
        text = text[start:end].strip()
    return text

def sanitize_filename(name):
    # Remove or replace characters invalid in file names
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name.strip()[:100]  # limit to 100 chars

def main():
    url_file = 'corpus_urls/english/english_retranslations_urls.json'
    with open(url_file, 'r', encoding='utf-8') as f:
        urls = json.load(f)

    outdir = Path('corpus_texts/english_retranslations')
    outdir.mkdir(parents=True, exist_ok=True)

    for entry in urls:
        url = entry['url']
        raw_title = entry.get('title', 'untitled')
        title = sanitize_filename(raw_title)
        fname = outdir / f"{title}.txt"
        try:
            print(f"Downloading: {raw_title}")
            txt = download_text(url)
            with open(fname, 'w', encoding='utf-8') as fw:
                fw.write(txt)
            time.sleep(1)
        except Exception as e:
            print(f"Error downloading {raw_title}: {e}")

if __name__ == '__main__':
    main()
