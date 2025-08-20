import requests
from pathlib import Path
import json
import time

def download_text(url, dest):
    r = requests.get(url, timeout=30)
    r.encoding = 'utf-8'
    text = r.text
    # Basic cleanup: remove Gutenberg headers/footers
    if 'Project Gutenberg' in url:
        start = text.find('\n\n') + 2
        end = text.rfind('***')
        text = text[start:end].strip()
    return text

def main():
    with open('corpus_urls/ancient_greek/ancient_greek_urls.json','r',encoding='utf-8') as f:
        urls = json.load(f)
    
    outdir = Path('corpus_texts/ancient_greek_texts')
    outdir.mkdir(parents=True, exist_ok=True)
    
    for entry in urls:
        url = entry['url']
        title = entry['title'].replace('/', '_')[:50]
        fname = outdir / f"{title}.txt"
        try:
            print(f"Downloading: {title}")
            txt = download_text(url, fname)
            with open(fname, 'w', encoding='utf-8') as fw:
                fw.write(txt)
            time.sleep(1)
        except Exception as e:
            print(f"  Error downloading {title}: {e}")

if __name__ == '__main__':
    main()
