import requests, time, json
from pathlib import Path

def download_text(url):
    r = requests.get(url, timeout=30)
    r.encoding = 'utf-8'
    return r.text

def main():
    with open('corpus_urls/middle_french/middle_french_urls.json','r',encoding='utf-8') as f:
        urls = json.load(f)
    out = Path('corpus_texts/middle_french_texts')
    out.mkdir(parents=True, exist_ok=True)
    for e in urls:
        # sanitize title for filename
        title = ''.join(c for c in e['title'] if c.isalnum() or c in ' _-')[:100]
        fname = out / f"{title}.txt"
        try:
            print(f"Downloading: {e['title']}")
            txt = download_text(e['url'])
            fname.write_text(txt, encoding='utf-8')
            time.sleep(1)
        except Exception as ex:
            print(f"Error: {ex}")

if __name__=='__main__':
    main()
