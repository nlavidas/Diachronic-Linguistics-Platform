import logging
import sqlite3
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import trafilatura
import time
from lxml import etree

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
project_root = Path(__file__).resolve().parent.parent
DB_PATH = project_root / "corpus.db"
PERSEUS_PATH = project_root / "_archive" / "canonical-greekLit" / "data"

class DiachronicCorpusCollector:
    def __init__(self):
        self.setup_database()
        self.texts_collected = []
    
    def setup_database(self):
        """Initialize the database"""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY,
            source TEXT,
            title TEXT,
            content TEXT,
            language TEXT,
            period TEXT,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        conn.close()
    
    def collect_perseus(self):
        """Collect texts from Perseus repository"""
        logger.info("Collecting from Perseus...")
        
        if not PERSEUS_PATH.exists():
            logger.warning(f"Perseus path not found: {PERSEUS_PATH}")
            return []
        
        texts = []
        # Look for Greek XML files
        xml_files = list(PERSEUS_PATH.rglob("*grc*.xml"))
        
        for xml_file in xml_files[:10]:  # Limit to first 10 for testing
            try:
                tree = etree.parse(str(xml_file))
                ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
                
                # Extract text from TEI XML
                text_nodes = tree.xpath('//tei:text/tei:body//text()', namespaces=ns)
                text_content = " ".join(t.strip() for t in text_nodes if t.strip())
                
                if text_content and len(text_content) > 100:
                    texts.append({
                        'source': 'perseus',
                        'title': xml_file.stem,
                        'content': text_content[:5000],  # Limit size
                        'language': 'ancient_greek',
                        'period': 'classical'
                    })
                    logger.info(f"Collected Perseus text: {xml_file.stem}")
            except Exception as e:
                logger.debug(f"Error parsing {xml_file}: {e}")
        
        return texts
    
    def collect_gutenberg(self):
        """Collect texts from Project Gutenberg"""
        logger.info("Collecting from Gutenberg...")
        
        # Specific Gutenberg texts to collect
        urls = {
            "Beowulf": "https://www.gutenberg.org/files/16328/16328-h/16328-h.htm",
            "Canterbury_Tales": "https://www.gutenberg.org/files/2253/2253-h/2253-h.htm",
            "Iliad_Butler": "https://www.gutenberg.org/files/2199/2199-h/2199-h.htm",
            "Odyssey_Butler": "https://www.gutenberg.org/files/1727/1727-h/1727-h.htm"
        }
        
        texts = []
        headers = {'User-Agent': 'DiachronicLinguistics/1.0'}
        
        for title, url in urls.items():
            try:
                response = requests.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    # Extract clean text
                    clean_text = trafilatura.extract(response.text)
                    if clean_text and len(clean_text) > 100:
                        texts.append({
                            'source': 'gutenberg',
                            'title': title,
                            'content': clean_text[:5000],  # Limit size
                            'language': 'english',
                            'period': 'various'
                        })
                        logger.info(f"Collected Gutenberg text: {title}")
                time.sleep(2)  # Be polite
            except Exception as e:
                logger.warning(f"Error collecting {title}: {e}")
        
        return texts
    
    def collect_wikisource(self):
        """Collect texts from Wikisource"""
        logger.info("Collecting from Wikisource...")
        
        # Specific Wikisource pages to collect
        urls = {
            "Iliad_Ancient_Greek": "https://el.wikisource.org/wiki/Ιλιάς",
            "Odyssey_Ancient_Greek": "https://el.wikisource.org/wiki/Οδύσσεια",
            "New_Testament_Greek": "https://el.wikisource.org/wiki/Καινή_Διαθήκη"
        }
        
        texts = []
        headers = {'User-Agent': 'DiachronicLinguistics/1.0'}
        
        for title, url in urls.items():
            try:
                response = requests.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Find the main content
                    content_div = soup.find('div', {'class': 'mw-parser-output'})
                    if content_div:
                        text = content_div.get_text(strip=True)
                        if text and len(text) > 100:
                            texts.append({
                                'source': 'wikisource',
                                'title': title,
                                'content': text[:5000],  # Limit size
                                'language': 'greek',
                                'period': 'various'
                            })
                            logger.info(f"Collected Wikisource text: {title}")
                time.sleep(2)  # Be polite
            except Exception as e:
                logger.warning(f"Error collecting {title}: {e}")
        
        return texts
    
    def save_to_database(self, texts):
        """Save collected texts to database"""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        for text in texts:
            try:
                cur.execute('''INSERT OR IGNORE INTO texts 
                    (source, title, content, language, period) 
                    VALUES (?, ?, ?, ?, ?)''',
                    (text['source'], text['title'], text['content'], 
                     text['language'], text['period']))
            except Exception as e:
                logger.warning(f"Error saving text {text['title']}: {e}")
        
        conn.commit()
        conn.close()
    
    def run(self):
        """Run all collectors"""
        all_texts = []
        
        # Collect from each source
        all_texts.extend(self.collect_perseus())
        all_texts.extend(self.collect_gutenberg())
        all_texts.extend(self.collect_wikisource())
        
        # Save to database
        if all_texts:
            self.save_to_database(all_texts)
            logger.info(f"Saved {len(all_texts)} texts to database")
        else:
            logger.warning("No texts collected!")
        
        print(f"Total texts collected: {len(all_texts)}")
        return all_texts

if __name__ == "__main__":
    collector = DiachronicCorpusCollector()
    collector.run()