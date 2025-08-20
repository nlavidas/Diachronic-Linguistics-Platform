#!/usr/bin/env python3
"""
harvest_greek_period_urls.py
Comprehensive harvester for Greek texts across all historical periods
"""

import requests
import json
import time
import re
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import hashlib

class GreekPeriodHarvester:
    """Harvests Greek texts from multiple sources across all periods"""
    
    # Expanded period queries for comprehensive coverage
    PERIOD_QUERIES = {
        'ancient': [
            'Homer Greek text', 'Iliad Greek', 'Odyssey Greek',
            'Plato Greek text', 'Republic Greek', 'Symposium Greek',
            'Aristotle Greek', 'Sophocles Greek', 'Euripides Greek',
            'Aeschylus Greek', 'Herodotus Greek', 'Thucydides Greek',
            'Xenophon Greek', 'Aristophanes Greek', 'Pindar Greek',
            'Hesiod Greek', 'Sappho Greek', 'Plutarch Greek'
        ],
        'medieval': [
            'Byzantine Greek text', 'Procopius Greek', 'Michael Psellos',
            'George Akropolites', 'Byzantine chronicle', 'Byzantine hymn',
            'Constantine Porphyrogennetos', 'Anna Komnene', 'Niketas Choniates',
            'John Kantakouzenos', 'Byzantine poetry', 'Digenes Akritas'
        ],
        'early_modern': [
            'Katharevousa Greek literature', 'Korais text', 'Rigas Feraios',
            'Greek Enlightenment', 'Papadiamantis', 'Vizyenos',
            '19th century Greek', 'Greek War Independence texts',
            'Solomos poetry', 'Kalvos poetry'
        ],
        'modern': [
            'Cavafy Demotic Greek', 'Seferis poem', 'Elytis poetry',
            'Kazantzakis novel', 'Modern Greek literature', 'Ritsos poetry',
            'Kariotakis poetry', 'Sikelianos', 'Palamas poetry',
            'Contemporary Greek fiction'
        ]
    }
    
    # Multiple source platforms
    SOURCES = {
        'gutenberg': 'https://www.gutenberg.org',
        'perseus': 'http://www.perseus.tufts.edu',
        'archive': 'https://archive.org'
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.all_urls = []
        self.seen_hashes = set()
        
    def harvest_gutenberg(self, period: str, queries: List[str]) -> List[Dict]:
        """Harvest from Project Gutenberg"""
        urls = []
        
        for query in queries:
            try:
                search_url = f'{self.SOURCES["gutenberg"]}/ebooks/search/?query={query.replace(" ", "%20")}'
                response = self.session.get(search_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for li in soup.select('li.booklink')[:10]:  # Get more results
                    title_elem = li.select_one('span.title')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    link = li.select_one('a')
                    
                    if link and 'href' in link.attrs:
                        book_id = link['href'].split('/')[-1]
                        
                        # Create multiple format URLs
                        text_url = f'{self.SOURCES["gutenberg"]}/ebooks/{book_id}.txt.utf-8'
                        
                        url_data = {
                            'url': text_url,
                            'title': title,
                            'language': 'greek',
                            'period': period,
                            'source': 'gutenberg',
                            'book_id': book_id,
                            'retrieval_date': datetime.now().isoformat(),
                            'query_used': query
                        }
                        
                        # Check for duplicates using hash
                        url_hash = hashlib.sha256(text_url.encode()).hexdigest()[:16]
                        if url_hash not in self.seen_hashes:
                            urls.append(url_data)
                            self.seen_hashes.add(url_hash)
                
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                print(f"Error harvesting Gutenberg for '{query}': {e}")
                continue
                
        return urls
    
    def harvest_perseus(self, period: str, queries: List[str]) -> List[Dict]:
        """Harvest from Perseus Digital Library"""
        urls = []
        
        # Perseus-specific search patterns
        perseus_collections = {
            'ancient': 'Greek/collection:Greco-Roman',
            'medieval': 'Greek/collection:Byzantine',
            'early_modern': 'Greek/collection:Modern',
            'modern': 'Greek/collection:Contemporary'
        }
        
        collection = perseus_collections.get(period, 'Greek')
        
        try:
            catalog_url = f'{self.SOURCES["perseus"]}/hopper/collection?collection={collection}'
            response = self.session.get(catalog_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.select('a[href*="text?doc="]')[:20]:
                title = link.get_text(strip=True)
                if title:
                    doc_id = link['href'].split('doc=')[-1]
                    text_url = f'{self.SOURCES["perseus"]}/hopper/text?doc={doc_id}'
                    
                    url_data = {
                        'url': text_url,
                        'title': title,
                        'language': 'greek',
                        'period': period,
                        'source': 'perseus',
                        'doc_id': doc_id,
                        'retrieval_date': datetime.now().isoformat()
                    }
                    
                    url_hash = hashlib.sha256(text_url.encode()).hexdigest()[:16]
                    if url_hash not in self.seen_hashes:
                        urls.append(url_data)
                        self.seen_hashes.add(url_hash)
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error harvesting Perseus for {period}: {e}")
            
        return urls
    
    def harvest_archive_org(self, period: str, queries: List[str]) -> List[Dict]:
        """Harvest from Internet Archive"""
        urls = []
        
        for query in queries:
            try:
                # Use Archive.org search API
                search_url = f'{self.SOURCES["archive"]}/advancedsearch.php'
                params = {
                    'q': f'{query} AND language:Greek',
                    'fl': 'identifier,title,creator,date',
                    'rows': 10,
                    'output': 'json'
                }
                
                response = self.session.get(search_url, params=params, timeout=10)
                data = response.json()
                
                if 'response' in data and 'docs' in data['response']:
                    for doc in data['response']['docs']:
                        identifier = doc.get('identifier', '')
                        title = doc.get('title', 'Untitled')
                        
                        if identifier:
                            text_url = f'{self.SOURCES["archive"]}/stream/{identifier}/{identifier}_djvu.txt'
                            
                            url_data = {
                                'url': text_url,
                                'title': title,
                                'language': 'greek',
                                'period': period,
                                'source': 'archive.org',
                                'identifier': identifier,
                                'retrieval_date': datetime.now().isoformat(),
                                'query_used': query
                            }
                            
                            url_hash = hashlib.sha256(text_url.encode()).hexdigest()[:16]
                            if url_hash not in self.seen_hashes:
                                urls.append(url_data)
                                self.seen_hashes.add(url_hash)
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error harvesting Archive.org for '{query}': {e}")
                continue
                
        return urls
    
    def harvest_all_periods(self):
        """Main harvesting function for all periods and sources"""
        print("Starting comprehensive Greek text harvesting...")
        
        for period, queries in self.PERIOD_QUERIES.items():
            print(f"\nHarvesting {period} Greek texts...")
            
            # Harvest from all sources
            gutenberg_urls = self.harvest_gutenberg(period, queries)
            print(f"  - Found {len(gutenberg_urls)} from Gutenberg")
            self.all_urls.extend(gutenberg_urls)
            
            perseus_urls = self.harvest_perseus(period, queries)
            print(f"  - Found {len(perseus_urls)} from Perseus")
            self.all_urls.extend(perseus_urls)
            
            archive_urls = self.harvest_archive_org(period, queries)
            print(f"  - Found {len(archive_urls)} from Archive.org")
            self.all_urls.extend(archive_urls)
        
        # Save results
        self.save_results()
        
    def save_results(self):
        """Save harvested URLs to JSON files"""
        # Create output directory
        output_dir = Path('corpus_urls/greek')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save all URLs together
        all_urls_file = output_dir / 'greek_all_periods_urls.json'
        with open(all_urls_file, 'w', encoding='utf-8') as f:
            json.dump(self.all_urls, f, indent=2, ensure_ascii=False)
        print(f"\nSaved {len(self.all_urls)} total URLs to {all_urls_file}")
        
        # Also save by period for easier processing
        for period in self.PERIOD_QUERIES.keys():
            period_urls = [u for u in self.all_urls if u['period'] == period]
            if period_urls:
                period_file = output_dir / f'greek_{period}_urls.json'
                with open(period_file, 'w', encoding='utf-8') as f:
                    json.dump(period_urls, f, indent=2, ensure_ascii=False)
                print(f"Saved {len(period_urls)} {period} URLs to {period_file}")
        
        # Save metadata summary
        self.save_metadata_summary()
    
    def save_metadata_summary(self):
        """Generate and save metadata summary"""
        summary = {
            'harvest_date': datetime.now().isoformat(),
            'total_urls': len(self.all_urls),
            'by_period': {},
            'by_source': {},
            'unique_titles': len(set(u['title'] for u in self.all_urls))
        }
        
        for period in self.PERIOD_QUERIES.keys():
            summary['by_period'][period] = len([u for u in self.all_urls if u['period'] == period])
        
        for source in ['gutenberg', 'perseus', 'archive.org']:
            summary['by_source'][source] = len([u for u in self.all_urls if u['source'] == source])
        
        summary_file = Path('corpus_urls/greek/harvest_summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nHarvest Summary:")
        print(f"  Total URLs: {summary['total_urls']}")
        print(f"  Unique titles: {summary['unique_titles']}")
        print("\n  By Period:")
        for period, count in summary['by_period'].items():
            print(f"    - {period}: {count}")
        print("\n  By Source:")
        for source, count in summary['by_source'].items():
            print(f"    - {source}: {count}")

def main():
    """Main execution function"""
    harvester = GreekPeriodHarvester()
    harvester.harvest_all_periods()

if __name__ == '__main__':
    main()