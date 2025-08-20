import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time
from urllib.parse import urljoin

class LatinURLHarvester:
    def __init__(self):
        self.urls = []
        self.session = requests.Session()
        self.session.headers.update({'User-Agent':'Mozilla/5.0'})
    
    def harvest_gutenberg_latin(self):
        print("📚 Harvesting Gutenberg Latin texts...")
        authors = ['Virgil', 'Ovid', 'Cicero', 'Caesar', 'Tacitus']
        for author in authors:
            search_url = f'https://www.gutenberg.org/ebooks/search/?query={author.replace(" ","%20")}'
            resp = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(resp.text,'html.parser')
            for item in soup.select('li.booklink')[:5]:
                title = item.select_one('span.title').get_text(strip=True)
                link = item.select_one('a')['href']
                if 'Latin' in title or author in title:
                    book_id = link.split('/')[-1]
                    url = f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8'
                    self.urls.append({'url':url,'title':title,'language':'latin','source':'gutenberg','author':author})
                    print(f"  ✓ {title}")
            time.sleep(0.5)
    
    def harvest_perseus_latin(self):
        print("🏛️ Harvesting Perseus Latin texts...")
        url = 'http://www.perseus.tufts.edu/hopper/searchresults?q=*&target=lat'
        resp = self.session.get(url, timeout=10)
        soup = BeautifulSoup(resp.text,'html.parser')
        for link in soup.select('a[href*="text?doc=Perseus:"]'):
            title = link.get_text(strip=True)
            if 'Latin' in title or any(w in title for w in ['Virgil','Ovid','Cicero','Caesar']):
                full = urljoin('http://www.perseus.tufts.edu', link['href'])
                self.urls.append({'url':full,'title':title,'language':'latin','source':'perseus'})
                print(f"  ✓ {title}")
        time.sleep(1)
    
    def save(self):
        out=Path('corpus_urls/latin')
        out.mkdir(parents=True,exist_ok=True)
        f=out/'latin_urls.json'
        with open(f,'w',encoding='utf-8') as fp: json.dump(self.urls,fp,indent=2)
        print(f"\n📊 LATIN URLS: {len(self.urls)} saved to {f}")
    
    def run(self):
        print("🇱🇻 LATIN HARVEST STARTED")
        self.harvest_gutenberg_latin()
        self.harvest_perseus_latin()
        self.save()

if __name__=='__main__':
    LatinURLHarvester().run()
