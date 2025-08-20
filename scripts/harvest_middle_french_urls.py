import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time
from urllib.parse import urljoin

class MiddleFrenchURLHarvester:
    def __init__(self):
        self.urls = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0'
        })
    
    def harvest_gutenberg_middle_french(self):
        print("📚 Harvesting Gutenberg Middle French texts...")
        terms = ['Marie de France', 'Chanson de geste', 'Roman de la Rose', 'Chrétien de Troyes']
        
        for term in terms:
            search_url = f'https://www.gutenberg.org/ebooks/search/?query={term.replace(" ", "%20")}'
            try:
                resp = self.session.get(search_url, timeout=10)
                soup = BeautifulSoup(resp.text, 'html.parser')
                for item in soup.select('li.booklink')[:5]:
                    title = item.select_one('span.title').get_text(strip=True)
                    link = item.select_one('a')['href']
                    book_id = link.split('/')[-1]
                    if 'French' in title or 'français' in title:
                        url = f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8'
                        self.urls.append({'url': url, 'title': title, 'language': 'middle_french', 'source': 'gutenberg', 'term': term})
                        print(f"  ✓ {title}")
                time.sleep(0.5)
            except Exception as e:
                print(f"  ✗ {term}: {e}")
    
    def harvest_archive_middle_french(self):
        print("🏛️ Harvesting Archive.org Middle French texts...")
        queries = ['medieval french literature', 'trouvère', 'troubadour', 'francien']
        for q in queries:
            api = f'https://archive.org/advancedsearch.php?q={q.replace(" ", "%20")}+AND+mediatype:texts&fl=identifier,title&rows=5&page=1&output=json'
            try:
                r = self.session.get(api, timeout=10).json()
                for doc in r['response']['docs']:
                    idn = doc['identifier']
                    title = doc['title']
                    url = f'https://archive.org/download/{idn}/{idn}.txt'
                    self.urls.append({'url': url, 'title': title, 'language': 'middle_french', 'source': 'archive_org', 'term': q})
                    print(f"  ✓ {title}")
                time.sleep(1)
            except Exception as e:
                print(f"  ✗ {q}: {e}")
    
    def save_urls(self):
        out = Path('corpus_urls/middle_french')
        out.mkdir(parents=True, exist_ok=True)
        f = out / 'middle_french_urls.json'
        with open(f, 'w', encoding='utf-8') as fp:
            json.dump(self.urls, fp, indent=2, ensure_ascii=False)
        print(f"\n📊 MIDDLE FRENCH URLS: {len(self.urls)} saved to {f}")
    
    def run(self):
        print("🇫🇷 MIDDLE FRENCH HARVEST STARTED")
        self.harvest_gutenberg_middle_french()
        self.harvest_archive_middle_french()
        self.save_urls()

if __name__ == "__main__":
    MiddleFrenchURLHarvester().run()
