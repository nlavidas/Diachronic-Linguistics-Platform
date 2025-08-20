import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time

class EnglishIntralingualHarvester:
    def __init__(self):
        self.urls = []
        self.session = requests.Session()
        self.session.headers.update({'User-Agent':'Mozilla/5.0'})

    def harvest_early_modern_to_modern(self):
        terms = ['Shakespeare Modern English', 'King James Modern English', 'Milton Modern English']
        for term in terms:
            url = f'https://www.gutenberg.org/ebooks/search/?query={term.replace(" ","%20")}'
            r = self.session.get(url,timeout=10)
            soup = BeautifulSoup(r.text,'html.parser')
            for li in soup.select('li.booklink')[:3]:
                title=li.select_one('span.title').get_text(strip=True)
                href=li.select_one('a')['href']
                bid=href.split('/')[-1]
                txt=f'https://www.gutenberg.org/ebooks/{bid}.txt.utf-8'
                self.urls.append({'url':txt,'title':title,'period':'early_modern_to_modern','language':'english','source':'gutenberg'})
            time.sleep(0.5)

    def harvest_18th_to_19th(self):
        terms = ['Pope Homer Modern English', 'Victorian translation']
        for term in terms:
            url = f'https://www.gutenberg.org/ebooks/search/?query={term.replace(" ","%20")}'
            r = self.session.get(url,timeout=10)
            soup = BeautifulSoup(r.text,'html.parser')
            for li in soup.select('li.booklink')[:2]:
                title=li.select_one('span.title').get_text(strip=True)
                href=li.select_one('a')['href']
                bid=href.split('/')[-1]
                txt=f'https://www.gutenberg.org/ebooks/{bid}.txt.utf-8'
                self.urls.append({'url':txt,'title':title,'period':'18th_to_19th','language':'english','source':'gutenberg'})
            time.sleep(0.5)

    def save(self):
        out=Path('corpus_urls/english_intralingual')
        out.mkdir(parents=True,exist_ok=True)
        f=out/'english_intralingual_urls.json'
        with open(f,'w',encoding='utf-8') as fp: json.dump(self.urls,fp,indent=2)
        print(f"📊 English intralingual URLs: {len(self.urls)} saved to {f}")

    def run(self):
        print("🇬🇧 English Intralingual Retranslations Harvesting...")
        self.harvest_early_modern_to_modern()
        self.harvest_18th_to_19th()
        self.save()

if __name__=='__main__':
    EnglishIntralingualHarvester().run()
