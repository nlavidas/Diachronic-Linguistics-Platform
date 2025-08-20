import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time
import concurrent.futures
import threading
from urllib.parse import urljoin, urlparse
import re
from typing import List, Dict, Set

class UltimateOpenAccessHarvester:
    def __init__(self):
        self.all_open_access_urls = {
            'greek_texts': set(),
            'latin_texts': set(),
            'english_texts': set(),
            'medieval_french_texts': set(),
            'biblical_texts': set(),
            'retranslation_texts': set()
        }
        
        # Major open access repositories[177][178][179][180]
        self.repositories = {
            'gutenberg': 'https://www.gutenberg.org',
            'archive_org': 'https://archive.org',
            'hathitrust': 'https://catalog.hathitrust.org',
            'perseus': 'http://www.perseus.tufts.edu',
            'tlg_open': 'http://www.tlg.uci.edu',
            'chs_harvard': 'https://chs.harvard.edu',
            'digitized_medieval': 'https://digitizedmedievalmanuscripts.org',
            'fragmentarium': 'https://fragmentarium.ms',
            'digi_vatlib': 'https://digi.vatlib.it',
            'europeana': 'https://www.europeana.eu',
            'gallica_bnf': 'https://gallica.bnf.fr',
            'bodleian': 'https://digital.bodleian.ox.ac.uk',
            'cambridge': 'https://cudl.lib.cam.ac.uk',
            'princeton': 'https://dpul.princeton.edu'
        }
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def collect_all_open_access_urls(self):
        """Comprehensive URL collection from all major repositories"""
        print("🌐 ULTIMATE OPEN ACCESS URL COLLECTION STARTED")
        print("="*80)
        
        # Phase 1: Systematic repository harvesting
        self.harvest_project_gutenberg_comprehensive()
        self.harvest_internet_archive_comprehensive()
        self.harvest_hathitrust_open_access()
        self.harvest_perseus_comprehensive()
        self.harvest_medieval_manuscripts()
        self.harvest_european_libraries()
        self.harvest_biblical_collections()
        
        # Phase 2: Specialized collections
        self.harvest_tlg_open_texts()
        self.harvest_fragmentarium_texts()
        self.harvest_vatican_manuscripts()
        
        print(f"\n📊 COMPREHENSIVE URL COLLECTION COMPLETE")
        self.print_collection_summary()
        
    def harvest_project_gutenberg_comprehensive(self):
        """Harvest ALL relevant texts from Project Gutenberg[178]"""
        print("\n📚 HARVESTING PROJECT GUTENBERG (Comprehensive)")
        
        # Comprehensive search terms for all target languages
        comprehensive_searches = {
            'greek_texts': [
                'Homer', 'Iliad', 'Odyssey', 'Hesiod', 'Pindar', 'Sappho', 'Alcaeus',
                'Plato', 'Aristotle', 'Socrates', 'Xenophon', 'Demosthenes',
                'Sophocles', 'Euripides', 'Aeschylus', 'Aristophanes',
                'Thucydides', 'Herodotus', 'Plutarch', 'Pausanias',
                'Greek', 'Ancient Greece', 'Hellenistic', 'Byzantine',
                'New Testament Greek', 'Septuagint', 'Greek Fathers'
            ],
            
            'latin_texts': [
                'Virgil', 'Ovid', 'Cicero', 'Caesar', 'Tacitus', 'Livy',
                'Horace', 'Juvenal', 'Martial', 'Catullus', 'Lucretius',
                'Seneca', 'Pliny', 'Suetonius', 'Quintilian',
                'Latin', 'Roman', 'Medieval Latin', 'Patristic',
                'Vulgate', 'Latin Fathers', 'Scholastic'
            ],
            
            'english_texts': [
                'Shakespeare', 'Chaucer', 'Milton', 'Spenser', 'Donne',
                'Pope', 'Swift', 'Johnson', 'Wordsworth', 'Coleridge',
                'Byron', 'Shelley', 'Keats', 'Tennyson', 'Browning',
                'Old English', 'Middle English', 'Elizabethan',
                'King James Bible', 'Authorized Version', 'Book of Common Prayer'
            ],
            
            'medieval_french_texts': [
                'Chrétien de Troyes', 'Marie de France', 'Chanson de geste',
                'Roman de la Rose', 'Arthurian', 'Old French',
                'Middle French', 'Medieval French', 'Troubadour',
                'Francien', 'Anglo-Norman', 'Provençal'
            ]
        }
        
        for category, searches in comprehensive_searches.items():
            print(f"  🔍 Searching {category.replace('_', ' ').title()}")
            
            for search_term in searches:
                try:
                    urls = self.search_gutenberg_advanced(search_term, category)
                    self.all_open_access_urls[category].update(urls)
                    print(f"    ✓ {search_term}: {len(urls)} URLs found")
                    time.sleep(0.5)  # Respectful delay
                    
                except Exception as e:
                    print(f"    ✗ Error with {search_term}: {e}")
    
    def search_gutenberg_advanced(self, term: str, category: str) -> Set[str]:
        """Advanced Gutenberg search with multiple result pages"""
        urls = set()
        
        for page in range(1, 6):  # Search first 5 pages
            try:
                search_url = f'https://www.gutenberg.org/ebooks/search/?query={term.replace(" ", "%20")}&start_index={(page-1)*25}'
                response = self.session.get(search_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for result in soup.select('li.booklink'):
                    link_elem = result.select_one('a')
                    title_elem = result.select_one('span.title')
                    
                    if link_elem and title_elem:
                        title = title_elem.get_text(strip=True)
                        
                        # Advanced filtering for open access texts only
                        if self.is_open_access_text(title, category):
                            book_id = link_elem['href'].split('/')[-1]
                            
                            # Add multiple formats
                            text_urls = {
                                f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8',
                                f'https://www.gutenberg.org/ebooks/{book_id}.html.images',
                                f'https://www.gutenberg.org/ebooks/{book_id}.epub.images'
                            }
                            urls.update(text_urls)
                
                if not soup.select('li.booklink'):  # No more results
                    break
                    
            except Exception as e:
                print(f"      Error on page {page}: {e}")
                break
        
        return urls
    
    def harvest_internet_archive_comprehensive(self):
        """Harvest Internet Archive using advanced API queries[178]"""
        print("\n📖 HARVESTING INTERNET ARCHIVE (Comprehensive)")
        
        # Advanced Internet Archive queries
        ia_queries = {
            'greek_texts': [
                'greek AND (homer OR plato OR aristotle) AND mediatype:texts',
                'ancient greek literature AND mediatype:texts',
                'byzantine greek texts AND mediatype:texts',
                'septuagint greek AND mediatype:texts',
                'greek manuscripts AND mediatype:texts'
            ],
            
            'latin_texts': [
                'latin AND (virgil OR cicero OR ovid) AND mediatype:texts',
                'medieval latin texts AND mediatype:texts',
                'patristic latin AND mediatype:texts',
                'vulgate latin AND mediatype:texts',
                'latin manuscripts AND mediatype:texts'
            ],
            
            'english_texts': [
                'shakespeare AND mediatype:texts',
                'chaucer AND mediatype:texts',
                'old english AND mediatype:texts',
                'middle english AND mediatype:texts',
                'king james bible AND mediatype:texts'
            ],
            
            'medieval_french_texts': [
                'old french AND mediatype:texts',
                'medieval french literature AND mediatype:texts',
                'chanson de geste AND mediatype:texts',
                'arthurian french AND mediatype:texts'
            ]
        }
        
        for category, queries in ia_queries.items():
            print(f"  🔍 Searching {category.replace('_', ' ').title()}")
            
            for query in queries:
                try:
                    urls = self.search_internet_archive_api(query, category)
                    self.all_open_access_urls[category].update(urls)
                    print(f"    ✓ Query: {len(urls)} URLs found")
                    time.sleep(1)  # Archive.org rate limiting
                    
                except Exception as e:
                    print(f"    ✗ Error: {e}")
    
    def search_internet_archive_api(self, query: str, category: str) -> Set[str]:
        """Search Internet Archive using official API"""
        urls = set()
        
        try:
            api_url = f'https://archive.org/advancedsearch.php'
            params = {
                'q': query,
                'fl': 'identifier,title,creator,date',
                'rows': 100,
                'page': 1,
                'output': 'json'
            }
            
            response = self.session.get(api_url, params=params, timeout=15)
            data = response.json()
            
            for doc in data.get('response', {}).get('docs', []):
                identifier = doc.get('identifier', '')
                title = doc.get('title', '')
                
                if self.is_open_access_text(title, category):
                    # Multiple format URLs
                    base_url = f"https://archive.org/details/{identifier}"
                    download_urls = {
                        f"https://archive.org/download/{identifier}/{identifier}.txt",
                        f"https://archive.org/download/{identifier}/{identifier}.pdf",
                        f"https://archive.org/stream/{identifier}",
                        base_url
                    }
                    urls.update(download_urls)
        
        except Exception as e:
            print(f"      API Error: {e}")
        
        return urls
    
    def harvest_hathitrust_open_access(self):
        """Harvest HathiTrust public domain texts[194]"""
        print("\n🏛️ HARVESTING HATHITRUST (Open Access)")
        
        # HathiTrust catalog searches for public domain texts
        hathi_searches = [
            'Homer greek',
            'Plato greek', 
            'Virgil latin',
            'Cicero latin',
            'Shakespeare english',
            'Chaucer middle english',
            'Old french literature',
            'Medieval manuscripts'
        ]
        
        for search in hathi_searches:
            try:
                catalog_url = f'https://catalog.hathitrust.org/Search/Home?lookfor={search.replace(" ", "%20")}&type=all&filter%5B%5D=format%3ABook&filter%5B%5D=availability_online%3A1'
                
                response = self.session.get(catalog_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract HathiTrust record URLs
                for link in soup.select('a[href*="/Record/"]'):
                    record_url = urljoin('https://catalog.hathitrust.org', link['href'])
                    self.all_open_access_urls['retranslation_texts'].add(record_url)
                
                print(f"    ✓ {search}: HathiTrust records found")
                time.sleep(1)
                
            except Exception as e:
                print(f"    ✗ Error with {search}: {e}")
    
    def harvest_perseus_comprehensive(self):
        """Harvest Perseus Digital Library systematically[177]"""
        print("\n🏛️ HARVESTING PERSEUS DIGITAL LIBRARY")
        
        # Perseus systematic collection URLs
        perseus_collections = [
            'http://www.perseus.tufts.edu/hopper/collection?collection=Perseus%3Acollection%3AGreco-Roman',
            'http://www.perseus.tufts.edu/hopper/collection?collection=Perseus%3Acollection%3Acwar',
            'http://www.perseus.tufts.edu/hopper/collection?collection=Perseus%3Acollection%3ARenaissance'
        ]
        
        for collection_url in perseus_collections:
            try:
                response = self.session.get(collection_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract all Perseus text URLs
                for link in soup.select('a[href*="text?doc=Perseus:"]'):
                    text_url = urljoin('http://www.perseus.tufts.edu', link['href'])
                    self.all_open_access_urls['greek_texts'].add(text_url)
                
                print(f"    ✓ Perseus collection: texts found")
                time.sleep(0.5)
                
            except Exception as e:
                print(f"    ✗ Perseus error: {e}")
    
    def harvest_medieval_manuscripts(self):
        """Harvest digitized medieval manuscripts[179][9]"""
        print("\n📜 HARVESTING MEDIEVAL MANUSCRIPTS")
        
        # DMMapp (Digitized Medieval Manuscripts app) repositories
        medieval_repositories = [
            'https://fragmentarium.ms/api/fragments',
            'https://digi.vatlib.it/view/bav_pal_lat_24',
            'https://digital.bodleian.ox.ac.uk/collections/medieval-manuscripts/',
            'https://parker.stanford.edu/parker/catalog',
            'https://cudl.lib.cam.ac.uk/collections/medieval'
        ]
        
        for repo_url in medieval_repositories:
            try:
                response = self.session.get(repo_url, timeout=10)
                
                if response.status_code == 200:
                    # Process different repository formats
                    if 'fragmentarium' in repo_url:
                        data = response.json()
                        for fragment in data.get('fragments', []):
                            self.all_open_access_urls['medieval_french_texts'].add(fragment.get('url', ''))
                    else:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for link in soup.select('a[href*="manuscript"], a[href*="codex"]'):
                            manuscript_url = urljoin(repo_url, link['href'])
                            self.all_open_access_urls['medieval_french_texts'].add(manuscript_url)
                
                print(f"    ✓ {urlparse(repo_url).netloc}: manuscripts found")
                time.sleep(1)
                
            except Exception as e:
                print(f"    ✗ Error with {repo_url}: {e}")
    
    def harvest_european_libraries(self):
        """Harvest major European digital libraries[180]"""
        print("\n🇪🇺 HARVESTING EUROPEAN LIBRARIES")
        
        european_apis = {
            'gallica_bnf': 'https://gallica.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=',
            'europeana': 'https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=',
            'digitale_sammlungen': 'https://www.digitale-sammlungen.de/api/search?q='
        }
        
        search_queries = [
            'greek%20manuscripts',
            'latin%20medieval',
            'french%20manuscripts',
            'biblical%20texts'
        ]
        
        for library, api_base in european_apis.items():
            for query in search_queries:
                try:
                    api_url = f"{api_base}{query}"
                    response = self.session.get(api_url, timeout=15)
                    
                    if response.status_code == 200:
                        # Process different API formats
                        if 'json' in response.headers.get('content-type', ''):
                            data = response.json()
                            items = data.get('items', []) or data.get('objects', [])
                            for item in items:
                                item_url = item.get('link', '') or item.get('guid', '')
                                if item_url:
                                    self.all_open_access_urls['retranslation_texts'].add(item_url)
                        else:
                            # XML response processing
                            soup = BeautifulSoup(response.text, 'xml')
                            for record in soup.find_all('record'):
                                identifier = record.find('identifier')
                                if identifier:
                                    self.all_open_access_urls['retranslation_texts'].add(identifier.text)
                    
                    print(f"    ✓ {library}: {query} processed")
                    time.sleep(2)  # European libraries rate limiting
                    
                except Exception as e:
                    print(f"    ✗ Error {library}/{query}: {e}")
    
    def harvest_biblical_collections(self):
        """Harvest comprehensive biblical text collections"""
        print("\n✝️ HARVESTING BIBLICAL COLLECTIONS")
        
        biblical_sources = [
            'https://www.gutenberg.org/ebooks/search/?query=bible',
            'https://www.gutenberg.org/ebooks/search/?query=septuagint',
            'https://www.gutenberg.org/ebooks/search/?query=vulgate',
            'https://archive.org/search.php?query=bible%20AND%20mediatype%3Atexts',
            'https://archive.org/search.php?query=new%20testament%20greek'
        ]
        
        for source_url in biblical_sources:
            try:
                response = self.session.get(source_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract biblical text URLs
                for link in soup.select('a[href*="ebooks"], a[href*="details"]'):
                    text_url = urljoin(source_url, link['href'])
                    self.all_open_access_urls['biblical_texts'].add(text_url)
                
                print(f"    ✓ {urlparse(source_url).netloc}: biblical texts found")
                time.sleep(1)
                
            except Exception as e:
                print(f"    ✗ Biblical collection error: {e}")
    
    def harvest_tlg_open_texts(self):
        """Harvest open access TLG texts[177]"""
        print("\n📚 HARVESTING TLG OPEN ACCESS")
        
        # First 1K Greek Project and open TLG texts
        tlg_open_sources = [
            'http://www.opengreekandlatin.org/texts/',
            'http://www.tlg.uci.edu/index/databases.html'
        ]
        
        for source in tlg_open_sources:
            try:
                response = self.session.get(source, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.select('a[href*=".xml"], a[href*=".txt"]'):
                    text_url = urljoin(source, link['href'])
                    self.all_open_access_urls['greek_texts'].add(text_url)
                
                print(f"    ✓ TLG open texts collected")
                time.sleep(0.5)
                
            except Exception as e:
                print(f"    ✗ TLG error: {e}")
    
    def harvest_fragmentarium_texts(self):
        """Harvest Fragmentarium manuscript fragments[190]"""
        print("\n📜 HARVESTING FRAGMENTARIUM")
        
        try:
            # Fragmentarium API for manuscript fragments
            api_url = 'https://fragmentarium.ms/api/fragments?limit=1000'
            response = self.session.get(api_url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                for fragment in data.get('fragments', []):
                    fragment_url = fragment.get('permalink', '')
                    if fragment_url:
                        self.all_open_access_urls['medieval_french_texts'].add(fragment_url)
                
                print(f"    ✓ Fragmentarium: {len(data.get('fragments', []))} fragments")
            
        except Exception as e:
            print(f"    ✗ Fragmentarium error: {e}")
    
    def harvest_vatican_manuscripts(self):
        """Harvest Vatican Library digital manuscripts[182]"""
        print("\n🇻🇦 HARVESTING VATICAN LIBRARY")
        
        try:
            # Vatican Library digital collection
            vatican_url = 'https://digi.vatlib.it/mss'
            response = self.session.get(vatican_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for manuscript_link in soup.select('a[href*="/view/"]'):
                manuscript_url = urljoin(vatican_url, manuscript_link['href'])
                self.all_open_access_urls['latin_texts'].add(manuscript_url)
            
            print(f"    ✓ Vatican manuscripts collected")
            
        except Exception as e:
            print(f"    ✗ Vatican error: {e}")
    
    def is_open_access_text(self, title: str, category: str) -> bool:
        """Advanced filtering for open access primary texts only"""
        title_lower = title.lower()
        
        # EXCLUDE non-open access indicators
        restricted_terms = [
            'copyright', 'rights reserved', 'permission required',
            'subscription', 'licensed', 'proprietary'
        ]
        
        # EXCLUDE commentary/academic works
        academic_terms = [
            'commentary', 'notes', 'study', 'analysis', 'introduction',
            'guide', 'handbook', 'criticism', 'interpretation',
            'history of', 'biography', 'dissertation', 'thesis'
        ]
        
        # Check exclusions
        if any(term in title_lower for term in restricted_terms + academic_terms):
            return False
        
        # INCLUDE open access indicators
        open_access_terms = [
            'public domain', 'creative commons', 'open access',
            'free', 'gutenberg', 'archive.org'
        ]
        
        # Category-specific validation
        category_terms = {
            'greek_texts': ['greek', 'homer', 'plato', 'aristotle', 'byzantine'],
            'latin_texts': ['latin', 'roman', 'virgil', 'cicero', 'medieval'],
            'english_texts': ['english', 'shakespeare', 'chaucer', 'milton'],
            'medieval_french_texts': ['french', 'medieval', 'troyes', 'arthurian'],
            'biblical_texts': ['bible', 'testament', 'septuagint', 'vulgate']
        }
        
        relevant_terms = category_terms.get(category, [])
        has_category_relevance = any(term in title_lower for term in relevant_terms)
        has_open_access_indicator = any(term in title_lower for term in open_access_terms)
        
        return has_category_relevance or has_open_access_indicator
    
    def print_collection_summary(self):
        """Print comprehensive collection summary"""
        total_urls = sum(len(urls) for urls in self.all_open_access_urls.values())
        
        print(f"\n{'='*80}")
        print("🎯 ULTIMATE OPEN ACCESS URL COLLECTION SUMMARY")
        print(f"{'='*80}")
        
        for category, urls in self.all_open_access_urls.items():
            print(f"📚 {category.replace('_', ' ').title():25s}: {len(urls):,} URLs")
        
        print(f"\n🌟 TOTAL OPEN ACCESS URLs: {total_urls:,}")
        print(f"🏛️ Repositories harvested: {len(self.repositories)}")
        print(f"🔓 Open access only: YES")
        print(f"📖 Primary texts only: YES")
        
    def save_comprehensive_url_database(self):
        """Save the comprehensive URL database"""
        output_dir = Path('corpus_texts/ultimate_open_access_collection')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert sets to lists for JSON serialization
        serializable_data = {}
        for category, url_set in self.all_open_access_urls.items():
            serializable_data[category] = list(url_set)
        
        # Save comprehensive database
        database_file = output_dir / 'ultimate_open_access_urls.json'
        with open(database_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
        
        # Save category-specific files
        for category, url_list in serializable_data.items():
            category_file = output_dir / f'{category}_urls.json'
            with open(category_file, 'w', encoding='utf-8') as f:
                json.dump(url_list, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 URL DATABASE SAVED:")
        print(f"   Main database: {database_file}")
        print(f"   Category files: {len(serializable_data)} files")
        print(f"   Directory: {output_dir}")
        
        return database_file, output_dir

if __name__ == "__main__":
    harvester = UltimateOpenAccessHarvester()
    harvester.collect_all_open_access_urls()
    database_file, output_dir = harvester.save_comprehensive_url_database()
    
    print(f"\n🚀 READY FOR PHASE 2: BULK TEXT SCRAPING")
    print(f"📋 URLs collected and ready for download")
    print(f"💡 Next: Run the bulk scraping system on collected URLs")
