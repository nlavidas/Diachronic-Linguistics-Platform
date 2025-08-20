import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time

class MultilingualRetranslationCollector:
    def __init__(self):
        self.collections = {
            'koine_to_later_greek': [],
            'ancient_to_byzantine_greek': [],
            'greek_to_latin': [],
            'greek_to_english': [],
            'greek_to_french': [],
            'greek_to_german': [],
            'greek_to_italian': [],
            'greek_to_spanish': [],
            'greek_to_slavonic': [],
            'greek_to_arabic': [],
            'greek_to_armenian': []
        }
    
    def collect_koine_to_later_greek(self):
        """Collect Koine Greek → Later Greek retranslations"""
        print("=== KOINE GREEK → LATER GREEK RETRANSLATIONS ===")
        
        koine_searches = [
            # New Testament Koine → Modern Greek
            'Koine Greek New Testament Modern Greek',
            'Greek New Testament Vamvas',
            'Byzantine Greek Bible Modern Greek',
            'Septuagint Modern Greek translation',
            
            # Early Christian texts → Later Greek
            'Chrysostom Modern Greek translation',
            'Patristic texts Modern Greek',
            'Early Christian Greek Modern Greek',
            'Byzantine chronicles Modern Greek',
            
            # Classical → Medieval Greek
            'Homer Byzantine Greek',
            'Plato Medieval Greek',
            'Ancient Greek Medieval Greek translation',
            
            # Koine → Katharevousa → Demotic
            'Katharevousa Greek translation',
            'Demotic Greek translation',
            'Puristic Greek Modern Greek'
        ]
        
        for search in koine_searches:
            print(f"Searching: {search}")
            results = self.search_specialized_collections(search, 'koine_later_greek')
            self.collections['koine_to_later_greek'].extend(results)
            time.sleep(1)
    
    def collect_greek_to_target_languages(self):
        """Collect Greek → Other Languages by historical periods"""
        print("=== GREEK → OTHER LANGUAGES BY PERIOD ===")
        
        # Define target languages and their historical periods
        language_mappings = {
            'latin': {
                'folder': 'greek_to_latin',
                'searches': [
                    'Greek Latin translation Medieval',
                    'Homer Latin Virgil',
                    'Plato Latin Augustine',
                    'Aristotle Latin Aquinas',
                    'Greek Fathers Latin translation',
                    'Septuagint Vulgate Latin'
                ]
            },
            'english': {
                'folder': 'greek_to_english',
                'searches': [
                    'Homer English 16th century',
                    'Homer English 17th century', 
                    'Homer English 18th century',
                    'Homer English 19th century',
                    'Homer English 20th century',
                    'Plato English Renaissance',
                    'Plato English Jowett',
                    'Greek tragedy English',
                    'Septuagint English translation'
                ]
            },
            'french': {
                'folder': 'greek_to_french',
                'searches': [
                    'Homère français traduction',
                    'Platon français traduction', 
                    'Sophocle français traduction',
                    'Grec ancien français',
                    'Nouveau Testament grec français'
                ]
            },
            'german': {
                'folder': 'greek_to_german',
                'searches': [
                    'Homer Deutsch Übersetzung',
                    'Platon Deutsch Übersetzung',
                    'Griechisch Deutsch Übersetzung',
                    'Neues Testament Griechisch Deutsch'
                ]
            },
            'italian': {
                'folder': 'greek_to_italian',
                'searches': [
                    'Omero italiano traduzione',
                    'Platone italiano traduzione',
                    'Greco antico italiano',
                    'Nuovo Testamento greco italiano'
                ]
            },
            'spanish': {
                'folder': 'greek_to_spanish',
                'searches': [
                    'Homero español traducción',
                    'Platón español traducción',
                    'Griego antiguo español',
                    'Nuevo Testamento griego español'
                ]
            },
            'slavonic': {
                'folder': 'greek_to_slavonic',
                'searches': [
                    'Greek Church Slavonic translation',
                    'Byzantine Greek Slavonic',
                    'Orthodox Greek Slavonic',
                    'Cyril Methodius Greek Slavonic'
                ]
            },
            'arabic': {
                'folder': 'greek_to_arabic',
                'searches': [
                    'Greek Arabic translation Bayt al-Hikma',
                    'Aristotle Arabic translation',
                    'Plato Arabic translation',
                    'Greek philosophy Arabic'
                ]
            }
        }
        
        for lang, config in language_mappings.items():
            print(f"\n--- GREEK → {lang.upper()} ---")
            for search in config['searches']:
                print(f"  Searching: {search}")
                results = self.search_specialized_collections(search, config['folder'])
                self.collections[config['folder']].extend(results)
                time.sleep(1)
    
    def search_specialized_collections(self, term, collection_type):
        """Search with specialized filtering for each collection type"""
        results = []
        
        # Search Gutenberg
        gutenberg_results = self.search_gutenberg_filtered(term, collection_type)
        results.extend(gutenberg_results)
        
        # Search Archive.org
        archive_results = self.search_archive_filtered(term, collection_type)
        results.extend(archive_results)
        
        return results
    
    def search_gutenberg_filtered(self, term, collection_type):
        """Search Gutenberg with collection-specific filters"""
        results = []
        search_url = f'https://www.gutenberg.org/ebooks/search/?query={term.replace(" ", "%20")}'
        
        try:
            response = requests.get(search_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for result in soup.select('li.booklink')[:5]:  # Limit results
                title_elem = result.select_one('span.title')
                author_elem = result.select_one('span.author')
                link_elem = result.select_one('a')
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    
                    if self.is_valid_retranslation(title, collection_type):
                        book_id = link_elem['href'].split('/')[-1]
                        
                        result_entry = {
                            'source': 'gutenberg',
                            'collection': collection_type,
                            'id': book_id,
                            'title': title,
                            'author': author_elem.get_text(strip=True) if author_elem else 'Unknown',
                            'search_term': term,
                            'period': self.extract_period_from_title(title),
                            'language_pair': self.identify_language_pair(title, collection_type),
                            'text_url': f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8',
                            'preview_info': self.create_retranslation_preview(title, collection_type)
                        }
                        
                        results.append(result_entry)
                        print(f"    ✓ Found: {title[:45]}...")
                        
        except Exception as e:
            print(f"    Error: {e}")
        
        return results
    
    def search_archive_filtered(self, term, collection_type):
        """Search Archive.org with collection-specific filters"""
        results = []
        
        try:
            # Construct query based on collection type
            if 'koine' in collection_type:
                query = f'{term} AND (greek OR koine OR byzantine) AND mediatype:texts'
            elif 'greek_to_' in collection_type:
                target_lang = collection_type.split('_')[-1]
                query = f'{term} AND (greek OR translation OR {target_lang}) AND mediatype:texts'
            else:
                query = f'{term} AND mediatype:texts'
                
            api_url = f'https://archive.org/advancedsearch.php?q={query.replace(" ", "%20")}&fl=identifier,title,creator,date,language&rows=10&page=1&output=json'
            
            response = requests.get(api_url, timeout=15)
            data = response.json()
            
            for doc in data.get('response', {}).get('docs', []):
                title = doc.get('title', 'Unknown')
                
                if self.is_valid_retranslation(title, collection_type):
                    result_entry = {
                        'source': 'archive_org',
                        'collection': collection_type,
                        'id': doc.get('identifier', ''),
                        'title': title,
                        'author': doc.get('creator', 'Unknown'),
                        'date': doc.get('date', 'Unknown'),
                        'language': doc.get('language', []),
                        'search_term': term,
                        'period': self.extract_period_from_title(title),
                        'language_pair': self.identify_language_pair(title, collection_type),
                        'download_url': f"https://archive.org/download/{doc.get('identifier', '')}/{doc.get('identifier', '')}.txt",
                        'preview_info': self.create_retranslation_preview(title, collection_type)
                    }
                    
                    results.append(result_entry)
                    print(f"    ✓ Found: {title[:45]}...")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"    Archive error: {e}")
        
        return results
    
    def is_valid_retranslation(self, title, collection_type):
        """Validate if title matches collection type criteria"""
        title_lower = title.lower()
        
        # Basic exclusions (no commentaries)
        exclusions = ['commentary', 'notes', 'study', 'analysis', 'history of']
        if any(excl in title_lower for excl in exclusions):
            return False
        
        # Collection-specific validation
        if collection_type == 'koine_later_greek':
            return any(term in title_lower for term in ['greek', 'testament', 'bible', 'byzantine', 'modern'])
        elif 'greek_to_' in collection_type:
            target_lang = collection_type.split('_')[-1]
            if target_lang == 'english':
                return 'translation' in title_lower and any(term in title_lower for term in ['homer', 'plato', 'greek'])
            elif target_lang in ['french', 'german', 'italian', 'spanish']:
                return any(term in title_lower for term in ['translation', 'traduction', 'übersetzung', 'traduzione'])
        
        return True
    
    def extract_period_from_title(self, title):
        """Extract historical period from title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['16th', 'xvii', '1500', '1600']):
            return '16th-17th_century'
        elif any(word in title_lower for word in ['18th', 'xviii', '1700']):
            return '18th_century'
        elif any(word in title_lower for word in ['19th', 'xix', '1800']):
            return '19th_century'
        elif any(word in title_lower for word in ['20th', 'xx', '1900']):
            return '20th_century'
        elif any(word in title_lower for word in ['medieval', 'byzantine']):
            return 'Medieval_Byzantine'
        elif any(word in title_lower for word in ['renaissance']):
            return 'Renaissance'
        else:
            return 'Unknown_period'
    
    def identify_language_pair(self, title, collection_type):
        """Identify source → target language pair"""
        if collection_type == 'koine_later_greek':
            return 'Koine_Greek → Modern_Greek'
        elif collection_type == 'greek_to_english':
            return 'Ancient_Greek → English'
        elif collection_type == 'greek_to_latin':
            return 'Ancient_Greek → Latin'
        elif collection_type == 'greek_to_french':
            return 'Ancient_Greek → French'
        elif collection_type == 'greek_to_german':
            return 'Ancient_Greek → German'
        else:
            return f'Greek → {collection_type.split("_")[-1].title()}'
    
    def create_retranslation_preview(self, title, collection_type):
        """Create preview info for retranslations"""
        if 'koine' in collection_type:
            return ["Koine/Byzantine Greek → Modern Greek", "Diachronic Greek language evolution"]
        elif 'english' in collection_type:
            return ["Classical Greek → English translation", "Historical English reception of Greek texts"]
        elif 'latin' in collection_type:
            return ["Greek → Medieval Latin translation", "Transmission through Latin tradition"]
        else:
            target = collection_type.split('_')[-1].title()
            return [f"Greek → {target} translation", f"Cross-cultural transmission to {target}"]
    
    def save_multilingual_collections(self):
        """Save collections in separate folders by target language"""
        base_dir = Path('corpus_texts/multilingual_retranslations')
        base_dir.mkdir(parents=True, exist_ok=True)
        
        total_texts = 0
        collection_summary = {}
        
        print(f"\n{'='*80}")
        print("🌍 MULTILINGUAL RETRANSLATION COLLECTIONS SAVED")
        print(f"{'='*80}")
        
        for collection_name, texts in self.collections.items():
            if texts:  # Only create files for non-empty collections
                # Create subfolder
                collection_dir = base_dir / collection_name
                collection_dir.mkdir(parents=True, exist_ok=True)
                
                # Save collection JSON
                collection_file = collection_dir / f'{collection_name}_urls.json'
                with open(collection_file, 'w', encoding='utf-8') as f:
                    json.dump(texts, f, indent=2, ensure_ascii=False)
                
                # Create preview file
                preview_file = collection_dir / f'{collection_name}_preview.txt'
                with open(preview_file, 'w', encoding='utf-8') as f:
                    f.write(f"📚 {collection_name.upper().replace('_', ' ')} COLLECTION\n")
                    f.write("=" * 60 + "\n\n")
                    
                    for i, text in enumerate(texts[:20], 1):  # First 20 texts
                        f.write(f"{i:2d}. {text.get('title', 'Unknown')}\n")
                        f.write(f"    👤 {text.get('author', 'Unknown')}\n")
                        f.write(f"    📅 {text.get('period', 'Unknown')}\n")
                        f.write(f"    🔄 {text.get('language_pair', 'Unknown')}\n")
                        if text.get('preview_info'):
                            f.write(f"    ℹ️  {text['preview_info'][0]}\n")
                            f.write(f"    📝 {text['preview_info'][1]}\n")
                        f.write("\n")
                    
                    if len(texts) > 20:
                        f.write(f"... and {len(texts) - 20} more texts\n")
                
                total_texts += len(texts)
                collection_summary[collection_name] = len(texts)
                
                print(f"📁 {collection_name:25s}: {len(texts):3d} texts → {collection_dir}")
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total retranslation texts: {total_texts}")
        print(f"   Collections created: {len(collection_summary)}")
        print(f"   Base directory: {base_dir}")
        
        return base_dir, total_texts, collection_summary

if __name__ == "__main__":
    collector = MultilingualRetranslationCollector()
    collector.collect_koine_to_later_greek()
    collector.collect_greek_to_target_languages()
    base_dir, total, summary = collector.save_multilingual_collections()
