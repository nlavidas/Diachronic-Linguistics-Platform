import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time

class GreekIntralingualHarvester:
    def __init__(self):
        self.urls = []
        self.session = requests.Session()
        self.session.headers.update({'User-Agent':'Mozilla/5.0'})

    def harvest_katharevousa_demotic(self):
        terms = ['Katharevousa', 'Demotic Greek translation']
        for term in terms:
            url = f'https://www.gutenberg.org/ebooks/search/?query={term.replace(" ","%20")}'
            r = self.session.get(url,timeout=10)
            soup = BeautifulSoup(r.text,'html.parser')
            for li in soup.select('li.booklink')[:5]:
                title=li.select_one('span.title').get_text(strip=True)
                href=li.select_one('a')['href']
                bid=href.split('/')[-1]
                txt=f'https://www.gutenberg.org/ebooks/{bid}.txt.utf-8'
                self.urls.append({'url':txt,'title':title,'period':'katharevousa_to_demotic','language':'greek','source':'gutenberg'})
            time.sleep(0.5)

    def harvest_bible_modern_greek(self):
        term='Septuagint Modern Greek'
        url=f'https://www.gutenberg.org/ebooks/search/?query={term.replace(" ","%20")}'
        r=self.session.get(url,timeout=10)
        soup=BeautifulSoup(r.text,'html.parser')
        for li in soup.select('li.booklink')[:3]:
            title=li.select_one('span.title').get_text(strip=True)
            href=li.select_one('a')['href']
            bid=href.split('/')[-1]
            txt=f'https://www.gutenberg.org/ebooks/{bid}.txt.utf-8'
            self.urls.append({'url':txt,'title':title,'period':'biblical_modern','language':'greek','source':'gutenberg'})
        time.sleep(0.5)

    def save(self):
        out=Path('corpus_urls/greek_intralingual')
        out.mkdir(parents=True,exist_ok=True)
        f=out/'greek_intralingual_urls.json'
        with open(f,'w',encoding='utf-8') as fp: json.dump(self.urls,fp,indent=2)
        print(f"📊 Greek intralingual URLs: {len(self.urls)} saved to {f}")

    def run(self):
        print("🇬🇷 Greek Intralingual Retranslations Harvesting...")
        self.harvest_katharevousa_demotic()
        self.harvest_bible_modern_greek()
        self.save()

if __name__=='__main__':
    GreekIntralingualHarvester().run()
