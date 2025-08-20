import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time
import re

class ExtendedURLCollector:
    def __init__(self):
        # Load existing URLs
        existing_file = Path('corpus_texts/collected_urls.json')
        if existing_file.exists():
            with open(existing_file, 'r', encoding='utf-8') as f:
                self.urls_database = json.load(f)
            print(f"Loaded {len(self.urls_database)} existing URLs")
        else:
            self.urls_database = []
    
    def collect_later_greek_periods(self):
        """Collect Byzantine, Medieval, and Modern Greek texts"""
        print("=== COLLECTING LATER GREEK PERIODS ===")
        
        later_greek_terms = [
            # Byzantine Period (330-1453 CE)
            'Byzantine Greek literature',
            'Byzantine texts',
            'Maximos Planudes',
            'Theodore Laskaris',
            'Anna Komnenos',
            'Prokopios',
            'John Chrysostom',
            'Byzantine chronicles',
            
            # Medieval Greek (1453-1669)
            'Medieval Greek',
            'Cretan Renaissance',
            'Erotokritos',
            'Vitsentzos Kornaros',
            
            # Modern Greek (1669-present)
            'Modern Greek literature',
            'Dionysios Solomos',
            'Andreas Kalvos',
            'Kostis Palamas',
            'Nikos Kazantzakis',
            'Greek folk tales',
            'Neo-Greek texts',
            'Contemporary Greek literature'
        ]
        
        for term in later_greek_terms:
            print(f"Searching later Greek: {term}")
            self.search_gutenberg_specific(term, 'later_greek')
            self.search_archive_org_specific(term, 'later_greek')
            time.sleep(1)
    
    def collect_retranslations_diachronic(self):
        """Collect retranslations of same texts across periods"""
        print("=== COLLECTING DIACHRONIC RETRANSLATIONS ===")
        
        retranslation_searches = [
            # Same text, different periods
            'Homer English translation 16th century',
            'Homer English translation 17th century', 
            'Homer English translation 18th century',
            'Homer English translation 19th century',
            'Homer English translation 20th century',
            
            'Plato English translation Pope',
            'Plato English translation Jowett',
            'Plato English translation modern',
            
            'Aristotle English translation medieval',
            'Aristotle English translation renaissance',
            'Aristotle English translation contemporary',
            
            # Greek to later Greek retranslations
            'Homer Modern Greek translation',
            'Plato Byzantine Greek',
            'Ancient Greek Modern Greek translation'
        ]
        
        for search in retranslation_searches:
            print(f"Searching retranslations: {search}")
            self.search_gutenberg_specific(search, 'retranslation')
            self.search_archive_org_specific(search, 'retranslation')
            time.sleep(1)
    
    def search_gutenberg_specific(self, term, category):
        """Search Gutenberg with text-only filtering"""
        search_url = f'https://www.gutenberg.org/ebooks/search/?query={term.replace(" ", "%20")}'
        
        try:
            response = requests.get(search_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for result in soup.select('li.booklink'):
                title_elem = result.select_one('span.title')
                author_elem = result.select_one('span.author')
                link_elem = result.select_one('a')
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    
                    # Filter OUT commentary/studies/monographs
                    if self.is_primary_text(title):
                        book_id = link_elem['href'].split('/')[-1]
                        
                        url_entry = {
                            'source': 'gutenberg',
                            'category': category,
                            'id': book_id,
                            'title': title,
                            'author': author_elem.get_text(strip=True) if author_elem else 'Unknown',
                            'search_term': term,
                            'period': self.extract_period(title),
                            'text_url': f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8',
                            'html_url': f'https://www.gutenberg.org/ebooks/{book_id}.html.images'
                        }
                        
                        # Avoid duplicates
                        if not any(u.get('id') == book_id and u.get('source') == 'gutenberg' for u in self.urls_database):
                            self.urls_database.append(url_entry)
                            print(f"  Added: {title[:50]}...")
                            
        except Exception as e:
            print(f"Error searching Gutenberg for '{term}': {e}")
    
    def search_archive_org_specific(self, term, category):
        """Search Archive.org with text filtering"""
        try:
            # More specific Archive.org search for texts only
            query = f'{term} AND mediatype:texts'
            api_url = f'https://archive.org/advancedsearch.php?q={query.replace(" ", "%20")}&fl=identifier,title,creator,date,subject&rows=30&page=1&output=json'
            
            response = requests.get(api_url, timeout=15)
            data = response.json()
            
            for doc in data.get('response', {}).get('docs', []):
                title = doc.get('title', 'Unknown')
                
                if self.is_primary_text(title):
                    url_entry = {
                        'source': 'archive_org',
                        'category': category,
                        'id': doc.get('identifier', ''),
                        'title': title,
                        'author': doc.get('creator', 'Unknown'),
                        'date': doc.get('date', 'Unknown'),
                        'subject': doc.get('subject', []),
                        'search_term': term,
                        'period': self.extract_period(title),
                        'download_url': f"https://archive.org/download/{doc.get('identifier', '')}/{doc.get('identifier', '')}.txt",
                        'page_url': f"https://archive.org/details/{doc.get('identifier', '')}"
                    }
                    
                    if not any(u.get('id') == url_entry['id'] and u.get('source') == 'archive_org' for u in self.urls_database):
                        self.urls_database.append(url_entry)
                        print(f"  Added: {title[:50]}...")
            
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"Error with Archive.org search '{term}': {e}")
    
    def is_primary_text(self, title):
        """Filter to keep only primary texts, exclude commentary/studies"""
        title_lower = title.lower()
        
        # EXCLUDE these types
        exclude_terms = [
            'commentary', 'comments', 'notes on', 'analysis', 'study of',
            'introduction to', 'guide to', 'handbook', 'companion to',
            'essays on', 'lectures on', 'criticism', 'interpretation',
            'history of', 'life of', 'biography', 'about', 'on the',
            'translation of', 'versions of', 'bibliography', 'index',
            'concordance', 'dictionary', 'lexicon', 'grammar'
        ]
        
        # INCLUDE these indicators of primary texts
        include_indicators = [
            'complete works', 'collected works', 'text', 'original',
            'translation', 'version', 'rendered', 'done into english'
        ]
        
        # Exclude if contains exclusion terms
        for exclude in exclude_terms:
            if exclude in title_lower:
                return False
        
        # Must be reasonable length (not just a fragment title)
        if len(title.split()) < 2:
            return False
            
        return True
    
    def extract_period(self, title):
        """Extract time period from title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['byzantine', 'constantinople']):
            return 'Byzantine'
        elif any(word in title_lower for word in ['medieval', 'middle']):
            return 'Medieval'
        elif any(word in title_lower for word in ['modern', 'contemporary', '19th', '20th', '21st']):
            return 'Modern'
        elif any(word in title_lower for word in ['classical', 'ancient']):
            return 'Classical'
        elif any(word in title_lower for word in ['hellenistic', 'koine']):
            return 'Hellenistic'
        else:
            return 'Unknown'
    
    def save_extended_database(self):
        """Save extended URLs database"""
        urls_file = Path('corpus_texts/collected_urls_extended.json')
        
        with open(urls_file, 'w', encoding='utf-8') as f:
            json.dump(self.urls_database, f, indent=2, ensure_ascii=False)
        
        # Summary by category and period
        categories = {}
        periods = {}
        
        for url in self.urls_database:
            cat = url.get('category', 'unknown')
            period = url.get('period', 'Unknown')
            
            categories[cat] = categories.get(cat, 0) + 1
            periods[period] = periods.get(period, 0) + 1
        
        print(f"\n=== EXTENDED COLLECTION SUMMARY ===")
        print(f"Total URLs: {len(self.urls_database)}")
        print(f"By source: Gutenberg: {len([u for u in self.urls_database if u.get('source') == 'gutenberg'])}")
        print(f"By source: Archive.org: {len([u for u in self.urls_database if u.get('source') == 'archive_org'])}")
        print(f"\nBy category:")
        for cat, count in categories.items():
            print(f"  {cat}: {count}")
        print(f"\nBy period:")
        for period, count in periods.items():
            print(f"  {period}: {count}")
        print(f"\nExtended database saved to: {urls_file}")
        
        return urls_file

if __name__ == "__main__":
    collector = ExtendedURLCollector()
    collector.collect_later_greek_periods()
    collector.collect_retranslations_diachronic()
    collector.save_extended_database()
