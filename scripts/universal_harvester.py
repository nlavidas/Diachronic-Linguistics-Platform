#!/usr/bin/env python3
"""
Universal Open-Access Text Harvester
Harvests from multiple sources with intelligent filtering
"""

import requests
import json
import time
import re
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib
from typing import List, Dict
from urllib.parse import urljoin, quote

class UniversalHarvester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Academic Research Bot)'
        })
        self.config = self.load_config()
        self.all_urls = []
        self.seen_hashes = set()
        
    def load_config(self):
        config_path = Path('scripts/corpus_config.json')
        if config_path.exists():
            return json.load(open(config_path, 'r', encoding='utf-8'))
        return {}
    
    def harvest_gutenberg_advanced(self):
        """Enhanced Gutenberg harvesting with better search"""
        print("Harvesting from Project Gutenberg...")
        base_url = "https://www.gutenberg.org"
        
        # Search for specific languages and exclude dictionaries
        searches = [
            ("language:Greek", "greek"),
            ("language:Latin", "latin"),
            ("language:French", "french"),
            ("subject:Bible", "biblical"),
            ("subject:Classical", "classical"),
            ("subject:Epic", "epic")
        ]
        
        for search_term, category in searches:
            try:
                # Use advanced search API
                api_url = f"{base_url}/ebooks/search/?query={quote(search_term)}&submit_search=Go"
                response = self.session.get(api_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for item in soup.select('.booklink'):
                    title_elem = item.select_one('.title')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # Filter out unwanted types
                    if any(exclude in title for exclude in ['Dictionary', 'Grammar', 'Commentary', 'Glossary']):
                        continue
                    
                    link = item.select_one('a')
                    if link:
                        book_id = link['href'].split('/')[-1]
                        
                        # Get multiple formats
                        formats = [
                            f"{base_url}/ebooks/{book_id}.txt.utf-8",
                            f"{base_url}/files/{book_id}/{book_id}-0.txt",
                            f"{base_url}/cache/epub/{book_id}/pg{book_id}.txt"
                        ]
                        
                        for format_url in formats:
                            url_data = {
                                'url': format_url,
                                'title': title,
                                'category': category,
                                'source': 'gutenberg',
                                'book_id': book_id,
                                'retrieval_date': datetime.now().isoformat()
                            }
                            
                            url_hash = hashlib.sha256(format_url.encode()).hexdigest()[:16]
                            if url_hash not in self.seen_hashes:
                                self.all_urls.append(url_data)
                                self.seen_hashes.add(url_hash)
                                break
                
                time.sleep(1)
                
            except Exception as e:
                print(f"  Error: {e}")
    
    def harvest_wikisource(self):
        """Harvest from Wikisource"""
        print("Harvesting from Wikisource...")
        
        wikisource_urls = {
            'greek': 'https://el.wikisource.org/wiki/',
            'latin': 'https://la.wikisource.org/wiki/',
            'french': 'https://fr.wikisource.org/wiki/',
            'english': 'https://en.wikisource.org/wiki/'
        }
        
        # Target specific texts
        targets = {
            'greek': ['Ιλιάς', 'Οδύσσεια', 'Πολιτεία'],
            'latin': ['Aeneis', 'De_Bello_Gallico', 'Metamorphoses'],
            'french': ['Chanson_de_Roland', 'Roman_de_la_Rose'],
            'english': ['Beowulf', 'Canterbury_Tales', 'Paradise_Lost']
        }
        
        for lang, base_url in wikisource_urls.items():
            for work in targets.get(lang, []):
                try:
                    url = f"{base_url}{work}"
                    url_data = {
                        'url': url,
                        'title': work.replace('_', ' '),
                        'language': lang,
                        'source': 'wikisource',
                        'retrieval_date': datetime.now().isoformat()
                    }
                    
                    url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
                    if url_hash not in self.seen_hashes:
                        self.all_urls.append(url_data)
                        self.seen_hashes.add(url_hash)
                        
                except Exception as e:
                    print(f"  Error harvesting {work}: {e}")
    
    def harvest_sacred_texts(self):
        """Harvest from Sacred Texts Archive"""
        print("Harvesting from Sacred Texts...")
        
        collections = {
            'classical': 'https://www.sacred-texts.com/cla/index.htm',
            'biblical': 'https://www.sacred-texts.com/bib/index.htm',
            'christian': 'https://www.sacred-texts.com/chr/index.htm'
        }
        
        for category, index_url in collections.items():
            try:
                response = self.session.get(index_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.endswith('.htm') and not href.startswith('http'):
                        title = link.get_text(strip=True)
                        
                        if any(exclude in title for exclude in ['Index', 'Contents', 'Bibliography']):
                            continue
                        
                        full_url = urljoin(index_url, href)
                        url_data = {
                            'url': full_url,
                            'title': title,
                            'category': category,
                            'source': 'sacred_texts',
                            'retrieval_date': datetime.now().isoformat()
                        }
                        
                        url_hash = hashlib.sha256(full_url.encode()).hexdigest()[:16]
                        if url_hash not in self.seen_hashes:
                            self.all_urls.append(url_data)
                            self.seen_hashes.add(url_hash)
                
                time.sleep(1)
                
            except Exception as e:
                print(f"  Error harvesting {category}: {e}")
    
    def harvest_all(self):
        """Run all harvesters"""
        print("Starting Universal Harvesting...")
        
        self.harvest_gutenberg_advanced()
        self.harvest_wikisource()
        self.harvest_sacred_texts()
        
        # Save results
        output_dir = Path('corpus_urls/universal')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f'universal_urls_{datetime.now().strftime("%Y%m%d")}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.all_urls, f, indent=2, ensure_ascii=False)
        
        print(f"\\nHarvested {len(self.all_urls)} URLs")
        print(f"Saved to {output_file}")
        
        # Save summary
        self.save_summary()
    
    def save_summary(self):
        """Generate harvest summary"""
        summary = {
            'harvest_date': datetime.now().isoformat(),
            'total_urls': len(self.all_urls),
            'by_source': {},
            'by_category': {}
        }
        
        for url in self.all_urls:
            source = url.get('source', 'unknown')
            category = url.get('category', 'uncategorized')
            
            summary['by_source'][source] = summary['by_source'].get(source, 0) + 1
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
        
        summary_file = Path('corpus_urls/universal/harvest_summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print("\\nSummary:")
        for source, count in summary['by_source'].items():
            print(f"  {source}: {count}")

if __name__ == '__main__':
    harvester = UniversalHarvester()
    harvester.harvest_all()