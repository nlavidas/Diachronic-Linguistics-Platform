import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time
import re
from urllib.parse import urljoin

class AncientGreekURLHarvester:
    def __init__(self):
        self.urls = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def harvest_perseus_ancient_greek(self):
        """Harvest Perseus Ancient Greek texts"""
        print("🏛️ Harvesting Perseus Ancient Greek texts...")
        
        perseus_searches = [
            'http://www.perseus.tufts.edu/hopper/collection?collection=Perseus%3Acollection%3AGreco-Roman',
            'http://www.perseus.tufts.edu/hopper/searchresults?q=*&target=grc'
        ]
        
        for search_url in perseus_searches:
            try:
                response = self.session.get(search_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.select('a[href*="text?doc=Perseus:"]'):
                    text_url = urljoin('http://www.perseus.tufts.edu', link['href'])
                    title = link.get_text(strip=True)
                    
                    if self.is_ancient_greek_text(title):
                        self.urls.append({
                            'url': text_url,
                            'title': title,
                            'language': 'ancient_greek',
                            'source': 'perseus',
                            'period': 'classical',
                            'type': 'original_text'
                        })
                        print(f"  ✓ {title[:50]}...")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"  ✗ Error with Perseus: {e}")
    
    def harvest_gutenberg_ancient_greek(self):
        """Harvest Project Gutenberg Ancient Greek texts"""
        print("📚 Harvesting Gutenberg Ancient Greek texts...")
        
        greek_searches = [
            'Homer', 'Hesiod', 'Pindar', 'Sappho', 'Plato', 'Aristotle',
            'Sophocles', 'Euripides', 'Aeschylus', 'Aristophanes',
            'Thucydides', 'Herodotus', 'Xenophon', 'Demosthenes'
        ]
        
        for author in greek_searches:
            try:
                search_url = f'https://www.gutenberg.org/ebooks/search/?query={author}+greek'
                response = self.session.get(search_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for result in soup.select('li.booklink')[:5]:  # Top 5 per author
                    title_elem = result.select_one('span.title')
                    link_elem = result.select_one('a')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        book_id = link_elem['href'].split('/')[-1]
                        
                        if self.is_ancient_greek_text(title):
                            text_url = f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8'
                            
                            self.urls.append({
                                'url': text_url,
                                'title': title,
                                'language': 'ancient_greek',
                                'source': 'gutenberg',
                                'period': 'classical',
                                'author': author,
                                'type': 'translation' if 'english' in title.lower() else 'original_text'
                            })
                            print(f"  ✓ {title[:50]}...")
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ✗ Error with {author}: {e}")
    
    def is_ancient_greek_text(self, title):
        """Filter for real Ancient Greek texts (not commentary)"""
        title_lower = title.lower()
        
        # EXCLUDE commentary/studies
        exclude_terms = [
            'commentary', 'notes', 'study', 'analysis', 'introduction',
            'guide', 'handbook', 'criticism', 'interpretation', 'about'
        ]
        
        if any(term in title_lower for term in exclude_terms):
            return False
        
        # INCLUDE indicators of real texts
        include_terms = [
            'homer', 'iliad', 'odyssey', 'plato', 'republic', 'aristotle',
            'sophocles', 'oedipus', 'euripides', 'medea', 'aeschylus',
            'complete works', 'collected works', 'text', 'translation'
        ]
        
        return any(term in title_lower for term in include_terms)
    
    def save_urls(self):
        """Save collected URLs"""
        output_dir = Path('corpus_urls/ancient_greek')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / 'ancient_greek_urls.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.urls, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 ANCIENT GREEK URL COLLECTION COMPLETE")
        print(f"   Total URLs: {len(self.urls)}")
        print(f"   Saved to: {output_file}")
        
        return output_file, len(self.urls)
    
    def run_harvest(self):
        """Run complete Ancient Greek URL harvest"""
        print("🇬🇷 ANCIENT GREEK URL HARVESTING STARTED")
        print("="*50)
        
        self.harvest_perseus_ancient_greek()
        self.harvest_gutenberg_ancient_greek()
        
        return self.save_urls()

if __name__ == "__main__":
    harvester = AncientGreekURLHarvester()
    output_file, count = harvester.run_harvest()
