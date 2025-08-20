import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import sqlite3
from pathlib import Path
import logging
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiachronicCorpusCollector:
    def __init__(self):
        self.db_path = Path('corpus.db')
        self.sources = {
            'perseus': {
                'url': 'https://www.perseus.tufts.edu/hopper/collection?collection=Perseus%3Acollection%3AGreco-Roman',
                'selector': '.text_container',
                'title_selector': 'h2'
            },
            'gutenberg': {
                'url': 'https://www.gutenberg.org/browse/languages/el',
                'selector': '.booklink',
                'title_selector': '.title'
            },
            'wikisource': {
                'url': 'https://el.wikisource.org/wiki/',
                'selector': '.mw-parser-output',
                'title_selector': 'h1'
            }
        }
    
    def extract_period(self, text: str) -> str:
        '''Determine historical period from text content'''
        periods = {
            'Ancient': ['ancient', 'classical', 'archaic'],
            'Hellenistic': ['hellenistic', 'alexander', 'ptolemaic'],
            'Koine': ['koine', 'septuagint', 'new testament'],
            'Byzantine': ['byzantine', 'medieval greek'],
            'Modern': ['modern', 'contemporary', '19th century', '20th century']
        }
        
        text_lower = text.lower()
        for period, keywords in periods.items():
            if any(kw in text_lower for kw in keywords):
                return period
        return 'Unknown'
    
    def extract_author(self, text: str) -> str:
        '''Extract author from text'''
        patterns = [
            r'By\s+([A-Za-z\s]+)[\.,]',
            r'Author:\s*([A-Za-z\s]+)',
            r'Written by\s+([A-Za-z\s]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return 'Unknown'
    
    def generate_title(self, body: str) -> str:
        '''Generate title from text body'''
        lines = [l.strip() for l in body.split('\n') if l.strip()]
        if lines:
            return lines[0][:100] + ('...' if len(lines[0]) > 100 else '')
        return 'Untitled'
    
    def generate_description(self, body: str) -> str:
        '''Generate description from first 500 characters'''
        return body[:500] + '...' if len(body) > 500 else body
    
    def collect_from_source(self, source_name: str) -> List[Dict]:
        '''Collect texts from a specific source'''
        source = self.sources[source_name]
        texts = []
        
        try:
            response = requests.get(source['url'], timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            elements = soup.select(source['selector'])[:10]  # Limit to 10 for testing
            
            for element in elements:
                text_body = element.get_text(separator=' ', strip=True)
                
                title_elem = element.select_one(source['title_selector'])
                title = title_elem.get_text() if title_elem else self.generate_title(text_body)
                
                text_data = {
                    'title': title,
                    'author': self.extract_author(text_body),
                    'period': self.extract_period(text_body),
                    'source_url': source['url'],
                    'full_description': self.generate_description(text_body),
                    'body': text_body,
                    'language': 'Greek',
                    'source': source_name
                }
                
                texts.append(text_data)
                logger.info(f'Collected: {title[:50]}...')
                
        except Exception as e:
            logger.error(f'Error collecting from {source_name}: {e}')
        
        return texts
    
    def save_to_database(self, texts: List[Dict]):
        '''Save collected texts to database'''
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        for text in texts:
            cur.execute('''
                INSERT INTO texts (title, author, period, source_url, full_description, body, language)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                text['title'],
                text['author'],
                text['period'],
                text['source_url'],
                text['full_description'],
                text['body'],
                text['language']
            ))
        
        conn.commit()
        conn.close()
        logger.info(f'Saved {len(texts)} texts to database')
    
    def collect_all(self):
        '''Collect from all configured sources'''
        all_texts = []
        for source_name in self.sources:
            logger.info(f'Collecting from {source_name}...')
            texts = self.collect_from_source(source_name)
            all_texts.extend(texts)
        
        self.save_to_database(all_texts)
        return all_texts

if __name__ == '__main__':
    collector = DiachronicCorpusCollector()
    results = collector.collect_all()
    print(f'Total texts collected: {len(results)}')
