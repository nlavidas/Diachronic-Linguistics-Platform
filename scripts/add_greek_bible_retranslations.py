import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time
import re

class BibleRetranslationCollector:
    def __init__(self):
        # Load existing URLs
        existing_file = Path('corpus_texts/collected_urls_extended.json')
        with open(existing_file, 'r', encoding='utf-8') as f:
            self.urls_database = json.load(f)
        print(f"Loaded {len(self.urls_database)} existing URLs")
    
    def collect_greek_bible_retranslations(self):
        """Collect Greek Bible retranslations across periods - TEXTS ONLY"""
        print("=== COLLECTING GREEK BIBLE RETRANSLATIONS ===")
        
        bible_searches = [
            # Ancient Greek Bible
            'Septuagint Greek Bible',
            'LXX Greek Old Testament',
            'Greek New Testament',
            'Textus Receptus',
            
            # Byzantine period Biblical texts
            'Byzantine Greek Bible',
            'Constantinople Bible Greek',
            'Chrysostom Bible',
            
            # Modern Greek Bible translations
            'Modern Greek New Testament',
            'Contemporary Greek Bible',
            'Greek Bible 19th century',
            'Greek Bible 20th century',
            'Vamvas Bible Greek',
            'Neophytos Vamvas',
            
            # Specific Biblical books in Greek
            'Greek Psalms translation',
            'Greek Gospels translation',
            'Greek Genesis translation',
            'Greek Exodus translation'
        ]
        
        for search in bible_searches:
            print(f"Searching Biblical texts: {search}")
            self.search_bible_texts_gutenberg(search)
            self.search_bible_texts_archive(search)
            time.sleep(1)
    
    def search_bible_texts_gutenberg(self, term):
        """Search Gutenberg for Biblical texts only"""
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
                    
                    # STRICT filter for Biblical texts only
                    if self.is_biblical_text_only(title):
                        book_id = link_elem['href'].split('/')[-1]
                        
                        url_entry = {
                            'source': 'gutenberg',
                            'category': 'greek_bible',
                            'id': book_id,
                            'title': title,
                            'author': author_elem.get_text(strip=True) if author_elem else 'Biblical',
                            'search_term': term,
                            'period': self.extract_biblical_period(title),
                            'text_type': 'biblical_text',
                            'text_url': f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8',
                            'preview_info': self.create_preview_info(title, 'biblical')
                        }
                        
                        if not any(u.get('id') == book_id and u.get('source') == 'gutenberg' for u in self.urls_database):
                            self.urls_database.append(url_entry)
                            print(f"  ✓ Biblical text: {title[:40]}...")
                            
        except Exception as e:
            print(f"Error: {e}")
    
    def search_bible_texts_archive(self, term):
        """Search Archive.org for Biblical texts"""
        try:
            # Very specific search for Biblical texts
            query = f'{term} AND (bible OR testament OR psalms OR gospel) AND mediatype:texts'
            api_url = f'https://archive.org/advancedsearch.php?q={query.replace(" ", "%20")}&fl=identifier,title,creator,date,subject&rows=20&page=1&output=json'
            
            response = requests.get(api_url, timeout=15)
            data = response.json()
            
            for doc in data.get('response', {}).get('docs', []):
                title = doc.get('title', 'Unknown')
                
                if self.is_biblical_text_only(title):
                    url_entry = {
                        'source': 'archive_org',
                        'category': 'greek_bible',
                        'id': doc.get('identifier', ''),
                        'title': title,
                        'author': doc.get('creator', 'Biblical'),
                        'date': doc.get('date', 'Unknown'),
                        'search_term': term,
                        'period': self.extract_biblical_period(title),
                        'text_type': 'biblical_text',
                        'download_url': f"https://archive.org/download/{doc.get('identifier', '')}/{doc.get('identifier', '')}.txt",
                        'preview_info': self.create_preview_info(title, 'biblical')
                    }
                    
                    if not any(u.get('id') == url_entry['id'] and u.get('source') == 'archive_org' for u in self.urls_database):
                        self.urls_database.append(url_entry)
                        print(f"  ✓ Biblical text: {title[:40]}...")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Archive error: {e}")
    
    def is_biblical_text_only(self, title):
        """STRICT filter for Biblical texts only - NO commentaries"""
        title_lower = title.lower()
        
        # Must contain Biblical indicators
        biblical_indicators = [
            'bible', 'testament', 'septuagint', 'lxx', 'gospel', 'psalms',
            'genesis', 'exodus', 'matthew', 'mark', 'luke', 'john', 
            'textus receptus', 'vamvas', 'greek new testament'
        ]
        
        has_biblical = any(indicator in title_lower for indicator in biblical_indicators)
        
        # EXCLUDE commentaries/studies
        exclude_terms = [
            'commentary', 'comments', 'notes', 'study', 'analysis', 'introduction',
            'guide', 'handbook', 'history of', 'about the', 'criticism',
            'interpretation', 'dictionary', 'concordance', 'lexicon'
        ]
        
        has_exclusion = any(exclude in title_lower for exclude in exclude_terms)
        
        return has_biblical and not has_exclusion
    
    def extract_biblical_period(self, title):
        """Extract Biblical period"""
        title_lower = title.lower()
        
        if 'septuagint' in title_lower or 'lxx' in title_lower:
            return 'Ancient_Biblical'
        elif 'byzantine' in title_lower or 'constantinople' in title_lower:
            return 'Byzantine_Biblical'
        elif any(word in title_lower for word in ['modern', '19th', '20th', 'contemporary']):
            return 'Modern_Biblical'
        elif 'textus receptus' in title_lower:
            return 'Classical_Biblical'
        else:
            return 'Biblical_Unknown'
    
    def create_preview_info(self, title, text_type):
        """Create 2-line preview information"""
        if text_type == 'biblical':
            if 'septuagint' in title.lower():
                return ["Ancient Greek Old Testament (LXX)", "3rd-2nd century BCE Greek translation"]
            elif 'new testament' in title.lower():
                return ["Greek New Testament text", "Original Koine Greek Christian scriptures"]
            elif 'vamvas' in title.lower():
                return ["Modern Greek Bible translation", "19th century Greek vernacular version"]
            else:
                return ["Biblical text in Greek", "Historical Greek religious literature"]
        else:
            return ["Classical Greek text", "Ancient/Medieval Greek literature"]
    
    def create_preview_dashboard(self):
        """Create beautiful preview dashboard of all collected texts"""
        print("\n" + "="*80)
        print("📚 DIACHRONIC GREEK CORPUS - PREVIEW DASHBOARD")
        print("="*80)
        
        # Group by category and period
        categories = {}
        for url in self.urls_database:
            cat = url.get('category', 'unknown')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(url)
        
        # Display by category
        for category, urls in categories.items():
            if len(urls) > 0:
                print(f"\n📖 {category.upper().replace('_', ' ')} ({len(urls)} texts)")
                print("-" * 60)
                
                for i, url in enumerate(urls[:10]):  # Show first 10 per category
                    title = url.get('title', 'Unknown')[:50]
                    period = url.get('period', 'Unknown')
                    author = url.get('author', 'Unknown')[:20]
                    
                    print(f"{i+1:2d}. {title}...")
                    print(f"    📅 Period: {period} | 👤 Author: {author}")
                    
                    # Show preview info if available
                    preview_info = url.get('preview_info', [])
                    if preview_info:
                        print(f"    ℹ️  {preview_info[0]}")
                        print(f"    📝 {preview_info[1]}")
                    
                    print()
                
                if len(urls) > 10:
                    print(f"    ... and {len(urls) - 10} more texts")
                print()
    
    def save_final_database(self):
        """Save final database with Biblical texts"""
        urls_file = Path('corpus_texts/collected_urls_final.json')
        
        with open(urls_file, 'w', encoding='utf-8') as f:
            json.dump(self.urls_database, f, indent=2, ensure_ascii=False)
        
        # Final statistics
        total = len(self.urls_database)
        by_category = {}
        by_period = {}
        biblical_count = 0
        
        for url in self.urls_database:
            cat = url.get('category', 'unknown')
            period = url.get('period', 'Unknown')
            text_type = url.get('text_type', '')
            
            by_category[cat] = by_category.get(cat, 0) + 1
            by_period[period] = by_period.get(period, 0) + 1
            
            if 'biblical' in text_type:
                biblical_count += 1
        
        print(f"\n📊 FINAL COLLECTION STATISTICS")
        print("="*50)
        print(f"📚 Total URLs: {total}")
        print(f"⛪ Biblical texts: {biblical_count}")
        print(f"📖 Other texts: {total - biblical_count}")
        print(f"💾 Database saved: {urls_file}")
        
        return urls_file, total, biblical_count

if __name__ == "__main__":
    collector = BibleRetranslationCollector()
    collector.collect_greek_bible_retranslations()
    collector.create_preview_dashboard()
    collector.save_final_database()
