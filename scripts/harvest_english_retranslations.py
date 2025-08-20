import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time
from urllib.parse import urljoin

class EnglishRetranslationsHarvester:
    def __init__(self):
        self.urls = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def harvest_english_periods(self):
        """Harvest English texts across different historical periods"""
        print("🇬🇧 Harvesting Multi-Period English Retranslations...")
        
        # English retranslations by period
        english_searches = {
            'old_english': ['Beowulf', 'Anglo-Saxon'],
            'middle_english': ['Chaucer', 'Canterbury Tales', 'Piers Plowman'],
            'early_modern': ['Shakespeare', 'King James Bible', 'Milton'],
            '18th_century': ['Pope Homer', 'Dryden', '18th century translation'],
            '19th_century': ['Victorian translation', 'Tennyson', 'Browning'],
            '20th_century': ['Modern English translation', 'Contemporary']
        }
        
        for period, authors in english_searches.items():
            print(f"  📖 Searching {period.replace('_', ' ').title()}...")
            
            for author in authors:
                try:
                    search_url = f'https://www.gutenberg.org/ebooks/search/?query={author.replace(" ", "%20")}'
                    response = self.session.get(search_url, timeout=10)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    for result in soup.select('li.booklink')[:3]:  # Top 3 per search
                        title_elem = result.select_one('span.title')
                        link_elem = result.select_one('a')
                        
                        if title_elem and link_elem:
                            title = title_elem.get_text(strip=True)
                            book_id = link_elem['href'].split('/')[-1]
                            
                            if self.is_english_retranslation(title):
                                text_url = f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8'
                                
                                self.urls.append({
                                    'url': text_url,
                                    'title': title,
                                    'language': 'english',
                                    'source': 'gutenberg',
                                    'period': period,
                                    'search_term': author,
                                    'type': self.classify_text_type(title)
                                })
                                print(f"    ✓ {title[:45]}...")
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"    ✗ Error with {author}: {e}")
    
    def harvest_bible_retranslations(self):
        """Harvest English Bible retranslations across periods"""
        print("  ✝️ Harvesting English Bible Retranslations...")
        
        bible_searches = [
            'King James Bible', 'Authorized Version', 'Douay Bible',
            'American Standard Version', 'Revised Version',
            'English Bible translation', 'New Testament English'
        ]
        
        for search in bible_searches:
            try:
                search_url = f'https://www.gutenberg.org/ebooks/search/?query={search.replace(" ", "%20")}'
                response = self.session.get(search_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for result in soup.select('li.booklink')[:2]:
                    title_elem = result.select_one('span.title')
                    link_elem = result.select_one('a')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        book_id = link_elem['href'].split('/')[-1]
                        
                        if self.is_biblical_text(title):
                            text_url = f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8'
                            
                            self.urls.append({
                                'url': text_url,
                                'title': title,
                                'language': 'english',
                                'source': 'gutenberg',
                                'period': 'biblical_retranslation',
                                'search_term': search,
                                'type': 'biblical_retranslation'
                            })
                            print(f"    ✓ {title[:45]}...")
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"    ✗ Error with {search}: {e}")
    
    def is_english_retranslation(self, title):
        """Filter for English retranslations and original works"""
        title_lower = title.lower()
        
        # EXCLUDE commentary
        exclude_terms = ['commentary', 'notes', 'study', 'analysis', 'biography']
        if any(term in title_lower for term in exclude_terms):
            return False
        
        # INCLUDE retranslations and major works
        include_terms = [
            'translation', 'version', 'rendered', 'complete works',
            'beowulf', 'chaucer', 'shakespeare', 'milton', 'pope',
            'canterbury tales', 'paradise lost', 'hamlet'
        ]
        
        return any(term in title_lower for term in include_terms)
    
    def is_biblical_text(self, title):
        """Filter for biblical texts"""
        title_lower = title.lower()
        
        biblical_terms = ['bible', 'testament', 'gospel', 'psalms', 'scripture']
        exclude_terms = ['commentary', 'notes', 'study', 'history']
        
        has_biblical = any(term in title_lower for term in biblical_terms)
        has_exclusion = any(term in title_lower for term in exclude_terms)
        
        return has_biblical and not has_exclusion
    
    def classify_text_type(self, title):
        """Classify the type of English text"""
        title_lower = title.lower()
        
        if 'translation' in title_lower:
            return 'retranslation'
        elif any(term in title_lower for term in ['complete works', 'collected']):
            return 'complete_works'
        else:
            return 'original_work'
    
    def save_urls(self):
        """Save collected URLs"""
        output_dir = Path('corpus_urls/english')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / 'english_retranslations_urls.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.urls, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 ENGLISH RETRANSLATIONS COLLECTION COMPLETE")
        print(f"   Total URLs: {len(self.urls)}")
        print(f"   Saved to: {output_file}")
        
        return output_file, len(self.urls)
    
    def run_harvest(self):
        """Run complete English retranslations harvest"""
        print("🇬🇧 ENGLISH RETRANSLATIONS HARVESTING STARTED")
        print("="*50)
        
        self.harvest_english_periods()
        self.harvest_bible_retranslations()
        
        return self.save_urls()

if __name__ == "__main__":
    harvester = EnglishRetranslationsHarvester()
    output_file, count = harvester.run_harvest()
