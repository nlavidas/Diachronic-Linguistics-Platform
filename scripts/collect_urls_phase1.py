import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time

class URLCollector:
    def __init__(self):
        self.urls_database = []
        
    def collect_gutenberg_urls(self):
        """Phase 1: Collect all relevant Gutenberg URLs"""
        search_terms = [
            'Homer', 'Iliad', 'Odyssey', 'Plato', 'Republic', 'Aristotle',
            'Sophocles', 'Oedipus', 'Aeschylus', 'Euripides', 'Medea',
            'Thucydides', 'Xenophon', 'Demosthenes', 'Apollonius',
            'Greek', 'Classical', 'Ancient Greece', 'Mythology'
        ]
        
        print("=== PHASE 1: COLLECTING GUTENBERG URLs ===")
        
        for term in search_terms:
            print(f"Searching: {term}")
            search_url = f'https://www.gutenberg.org/ebooks/search/?query={term.replace(" ", "%20")}'
            
            try:
                response = requests.get(search_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for result in soup.select('li.booklink'):
                    title_elem = result.select_one('span.title')
                    author_elem = result.select_one('span.author')
                    link_elem = result.select_one('a')
                    
                    if title_elem and link_elem:
                        book_id = link_elem['href'].split('/')[-1]
                        
                        url_entry = {
                            'source': 'gutenberg',
                            'id': book_id,
                            'title': title_elem.get_text(strip=True),
                            'author': author_elem.get_text(strip=True) if author_elem else 'Unknown',
                            'search_term': term,
                            'text_url': f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8',
                            'html_url': f'https://www.gutenberg.org/ebooks/{book_id}.html.images',
                            'epub_url': f'https://www.gutenberg.org/ebooks/{book_id}.epub.images'
                        }
                        
                        # Avoid duplicates
                        if not any(u['id'] == book_id and u['source'] == 'gutenberg' for u in self.urls_database):
                            self.urls_database.append(url_entry)
                            
                time.sleep(1)  # Be respectful to server
                
            except Exception as e:
                print(f"Error with {term}: {e}")
        
        print(f"Collected {len([u for u in self.urls_database if u['source'] == 'gutenberg'])} Gutenberg URLs")
    
    def collect_archive_org_urls(self):
        """Phase 1: Collect Archive.org URLs for Greek texts"""
        print("=== COLLECTING ARCHIVE.ORG URLs ===")
        
        archive_searches = [
            'Greek literature translations',
            'Ancient Greek texts English',
            'Classical literature translations',
            'Byzantine Greek texts'
        ]
        
        for search in archive_searches:
            try:
                # Archive.org API search
                api_url = f'https://archive.org/advancedsearch.php?q={search.replace(" ", "%20")}&fl=identifier,title,creator,date&rows=50&page=1&output=json'
                response = requests.get(api_url, timeout=15)
                data = response.json()
                
                for doc in data.get('response', {}).get('docs', []):
                    url_entry = {
                        'source': 'archive_org',
                        'id': doc.get('identifier', ''),
                        'title': doc.get('title', 'Unknown'),
                        'author': doc.get('creator', 'Unknown'),
                        'date': doc.get('date', 'Unknown'),
                        'search_term': search,
                        'download_url': f"https://archive.org/download/{doc.get('identifier', '')}/{doc.get('identifier', '')}.txt",
                        'page_url': f"https://archive.org/details/{doc.get('identifier', '')}"
                    }
                    
                    if not any(u['id'] == url_entry['id'] and u['source'] == 'archive_org' for u in self.urls_database):
                        self.urls_database.append(url_entry)
                
                time.sleep(2)  # Archive.org rate limiting
                
            except Exception as e:
                print(f"Error with Archive.org search '{search}': {e}")
        
        print(f"Collected {len([u for u in self.urls_database if u['source'] == 'archive_org'])} Archive.org URLs")
    
    def collect_perseus_urls(self):
        """Phase 1: Collect Perseus Digital Library URLs"""
        print("=== COLLECTING PERSEUS URLs ===")
        
        # Perseus has a more structured approach
        perseus_base = "http://www.perseus.tufts.edu/hopper/"
        
        # Common Perseus text patterns
        perseus_patterns = [
            "text?doc=Perseus:text:1999.01.0133",  # Homer Iliad Greek
            "text?doc=Perseus:text:1999.01.0134",  # Homer Iliad English
            "text?doc=Perseus:text:1999.01.0135",  # Homer Odyssey Greek
            "text?doc=Perseus:text:1999.01.0136",  # Homer Odyssey English
            "text?doc=Perseus:text:1999.01.0159",  # Plato Republic Greek
            "text?doc=Perseus:text:1999.01.0168"   # Plato Republic English
        ]
        
        for pattern in perseus_patterns:
            url_entry = {
                'source': 'perseus',
                'id': pattern.split(':')[-1],
                'title': f"Perseus Text {pattern.split(':')[-1]}",
                'author': 'Perseus Collection',
                'full_url': perseus_base + pattern,
                'type': 'greek' if 'grc' in pattern else 'english'
            }
            self.urls_database.append(url_entry)
        
        print(f"Collected {len([u for u in self.urls_database if u['source'] == 'perseus'])} Perseus URLs")
    
    def save_urls_database(self):
        """Save all collected URLs to JSON file for Phase 2"""
        urls_file = Path('corpus_texts/collected_urls.json')
        urls_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(urls_file, 'w', encoding='utf-8') as f:
            json.dump(self.urls_database, f, indent=2, ensure_ascii=False)
        
        print(f"=== URLS COLLECTION SUMMARY ===")
        print(f"Total URLs collected: {len(self.urls_database)}")
        print(f"Gutenberg: {len([u for u in self.urls_database if u['source'] == 'gutenberg'])}")
        print(f"Archive.org: {len([u for u in self.urls_database if u['source'] == 'archive_org'])}")
        print(f"Perseus: {len([u for u in self.urls_database if u['source'] == 'perseus'])}")
        print(f"URLs database saved to: {urls_file}")
        
        return urls_file

if __name__ == "__main__":
    collector = URLCollector()
    collector.collect_gutenberg_urls()
    collector.collect_archive_org_urls()
    collector.collect_perseus_urls()
    urls_file = collector.save_urls_database()
