import requests
from bs4 import BeautifulSoup
import json
import re

class HistoricalTextFetcher:
    def __init__(self):
        self.sources = {
            'gutenberg': 'https://www.gutenberg.org',
            'perseus': 'http://www.perseus.tufts.edu',
            'ccel': 'https://www.ccel.org',
            'sacred_texts': 'https://www.sacred-texts.com'
        }
    
    def fetch_gutenberg_text(self, text_id):
        """Fetch from Project Gutenberg"""
        url = f"https://www.gutenberg.org/files/{text_id}/{text_id}-0.txt"
        response = requests.get(url)
        return response.text if response.status_code == 200 else None
    
    def search_historical_texts(self, period, language='english'):
        """Search for texts by period"""
        periods = {
            'old_english': ['Beowulf', 'Anglo-Saxon Chronicle', 'Dream of the Rood'],
            'middle_english': ['Canterbury Tales', 'Piers Plowman', 'Sir Gawain'],
            'early_modern': ['Shakespeare', 'Marlowe', 'King James Bible'],
            'classical': ['Homer', 'Virgil', 'Ovid']
        }
        return periods.get(period, [])
    
    def process_for_corpus(self, text, metadata):
        """Prepare text for linguistic analysis"""
        return {
            'original': text,
            'normalized': self.normalize_historical_spelling(text),
            'metadata': metadata,
            'word_count': len(text.split()),
            'estimated_date': metadata.get('year', 'unknown')
        }
    
    def normalize_historical_spelling(self, text):
        """Normalize historical variations"""
        replacements = {
            'þ': 'th', 'ð': 'th', 'æ': 'ae',
            'ȝ': 'y', 'ƿ': 'w', 'ſ': 's'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text