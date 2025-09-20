 
import requests
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class DiverseTextProcessor:
    def __init__(self):
        self.processed_count = 0
        self.all_urls = self.get_all_urls()
        
    def get_all_urls(self):
        """Returns 100+ diverse text URLs"""
        urls = []
        
        # Iliad - all 24 books
        for i in range(1, 25):
            urls.append(f'https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg001/tlg0012.tlg001.perseus-grc{i}.xml')
        
        # Odyssey - all 24 books  
        for i in range(1, 25):
            urls.append(f'https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc{i}.xml')
            
        # Biblical texts
        for book in ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1Corinthians', '2Corinthians']:
            urls.append(f'https://raw.githubusercontent.com/morphgnt/sblgnt/master/{book}.txt')
            
        return urls
    
    def process_next_batch(self):
        # Get next 3 URLs in rotation
        start_idx = (self.processed_count * 3) % len(self.all_urls)
        batch = self.all_urls[start_idx:start_idx+3]
        
        for url in batch:
            try:
                response = requests.get(url, timeout=30)
                logging.info(f'Downloaded {url.split("/")[-1]}: {len(response.text)} chars')
            except Exception as e:
                logging.error(f'Failed {url}: {e}')
                
        self.processed_count += 1
        
    def run_forever(self):
        while True:
            logging.info(f'=== Cycle {self.processed_count} ===')
            self.process_next_batch()
            logging.info('Sleeping 3600 seconds')
            time.sleep(3600)

if __name__ == '__main__':
    processor = DiverseTextProcessor()
    processor.run_forever()