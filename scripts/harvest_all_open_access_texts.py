import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time
from urllib.parse import urljoin

class UniversalOpenAccessHarvester:
    def __init__(self):
        self.urls = []
        self.session = requests.Session()
        self.session.headers.update({'User-Agent':'Mozilla/5.0'})
    
    def harvest_gutenberg(self, terms):
        for term in terms:
            search = term.replace(' ','%20')
            url = f'https://www.gutenberg.org/ebooks/search/?query={search}'
            r = self.session.get(url,timeout=10)
            soup = BeautifulSoup(r.text,'html.parser')
            for li in soup.select('li.booklink')[:5]:
                title = li.select_one('span.title').get_text(strip=True)
                link = li.select_one('a')['href']
                if not self.exclude(title):
                    book_id = link.split('/')[-1]
                    txt = f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8'
                    self.urls.append({'url':txt,'title':title,'source':'gutenberg','term':term})
            time.sleep(0.5)
    
    def harvest_archive(self, queries):
        for q in queries:
            api = f'https://archive.org/advancedsearch.php?q={q.replace(" ","%20")}+AND+mediatype:texts&fl=identifier,title&rows=5&output=json'
            data = self.session.get(api,timeout=10).json()
            for doc in data['response']['docs']:
                idn, title = doc['identifier'], doc['title']
                if not self.exclude(title):
                    txt = f'https://archive.org/download/{idn}/{idn}.txt'
                    self.urls.append({'url':txt,'title':title,'source':'archive_org','term':q})
            time.sleep(1)
    
    def harvest_perseus(self):
        url='http://www.perseus.tufts.edu/hopper/collection?collection=Perseus%3Acollection%3AGreco-Roman'
        r=self.session.get(url,timeout=10); soup=BeautifulSoup(r.text,'html.parser')
        for a in soup.select('a[href*="text?doc=Perseus:"]'):
            title=a.get_text(strip=True); link=urljoin('http://www.perseus.tufts.edu',a['href'])
            if not self.exclude(title):
                self.urls.append({'url':link,'title':title,'source':'perseus','term':'all_texts'})
    
    def exclude(self,title):
        t=title.lower()
        for ex in ['commentary','notes','study','analysis','guide','handbook','introduction','history of','about']:
            if ex in t: return True
        return False
    
    def save(self):
        out=Path('corpus_urls/all_texts')
        out.mkdir(parents=True,exist_ok=True)
        f=out/'all_open_access_urls.json'
        with open(f,'w',encoding='utf-8') as fp: json.dump(self.urls,fp,indent=2)
        print(f"\n📊 UNIVERSAL OPEN ACCESS URLS: {len(self.urls)} saved to {f}")
    
    def run(self):
        terms = ['Greek literature', 'Latin literature', 'English literature', 'Medieval French', 'Bible', 'Testament', 'Gospel']
        archive_q = ['greek literature','latin literature','english literature','medieval french','bible','septuagint','vulgate']
        print("🌐 UNIVERSAL HARVEST START")
        self.harvest_gutenberg(terms)
        self.harvest_archive(archive_q)
        self.harvest_perseus()
        self.save()

if __name__=='__main__':
    UniversalOpenAccessHarvester().run()
