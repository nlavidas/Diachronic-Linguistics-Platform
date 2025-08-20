import logging
import sqlite3
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import spacy
import os

logger = logging.getLogger(__name__)
project_root = Path(__file__).resolve().parent.parent
DB_PATH = project_root / "corpus.db"

def setup_database():
    """Create database tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY,
            filename TEXT UNIQUE,
            language TEXT,
            source TEXT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY,
            text_id INTEGER,
            sentence_id INTEGER,
            token_id_in_sent INTEGER,
            text TEXT,
            lemma TEXT,
            pos TEXT,
            dependency TEXT,
            head_text TEXT,
            FOREIGN KEY(text_id) REFERENCES texts(id)
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS valency_patterns (
            id INTEGER PRIMARY KEY,
            verb_lemma TEXT,
            pattern TEXT,
            frequency INTEGER DEFAULT 1,
            text_id INTEGER,
            FOREIGN KEY(text_id) REFERENCES texts(id)
        )
    """)
    
    conn.commit()
    conn.close()
    logger.info("Database setup complete")

def process_mission_action(mission_string):
    """Process a mission string and execute appropriate action"""
    try:
        if ':' in mission_string:
            command, data = mission_string.split(':', 1)
        else:
            command = mission_string
            data = None
        
        logger.info(f"Executing: {command} with data: {data}")
        
        if command == "TEST":
            logger.info(f"Test mission executed successfully: {data}")
            return True
            
        elif command == "HARVEST":
            if data == "PERSEUS_GREEK":
                harvest_perseus_greek()
            elif data == "GUTENBERG_ENGLISH":
                harvest_gutenberg_english()
            else:
                harvest_url(data)
                
        elif command == "PROCESS":
            if data == "GREEK_CORPUS":
                process_corpus("corpus_texts/perseus_greek_classics", "greek")
            elif data == "ENGLISH_CORPUS":
                process_corpus("corpus_texts/gutenberg_english", "english")
            else:
                process_corpus(data, "english")
                
        elif command == "DISCOVER":
            discover_texts(data)
            
        elif command == "EXTRACT_VALENCY":
            extract_valency_patterns()
            
        else:
            logger.warning(f"Unknown command: {command}")
            
    except Exception as e:
        logger.error(f"Mission action failed: {e}")
        raise

def harvest_perseus_greek():
    """Harvest Greek texts from Perseus"""
    logger.info("Starting Perseus Greek harvest...")
    
    # Check if Perseus archive exists
    perseus_path = project_root / "_archive/canonical-greekLit/data"
    if not perseus_path.exists():
        logger.warning("Perseus archive not found. Please clone the repository first.")
        return
    
    output_dir = project_root / "corpus_texts/perseus_greek_classics"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process XML files
    from lxml import etree
    xml_files = list(perseus_path.rglob("*.xml"))
    
    for xml_file in xml_files[:10]:  # Process first 10 for testing
        try:
            tree = etree.parse(str(xml_file))
            ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
            text_nodes = tree.xpath('//tei:text/tei:body//text()', namespaces=ns)
            text = " ".join(text_nodes)
            
            if text.strip():
                output_file = output_dir / f"Perseus_{xml_file.stem}.txt"
                output_file.write_text(text, encoding='utf-8')
                logger.info(f"Harvested: {xml_file.stem}")
                
        except Exception as e:
            logger.error(f"Failed to process {xml_file}: {e}")
    
    logger.info("Perseus harvest complete")

def harvest_gutenberg_english():
    """Harvest English texts from Project Gutenberg"""
    logger.info("Starting Gutenberg English harvest...")
    
    output_dir = project_root / "corpus_texts/gutenberg_english"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample Gutenberg URLs
    urls = {
        "Beowulf": "https://www.gutenberg.org/files/16328/16328-h/16328-h.htm",
        "Canterbury_Tales": "https://www.gutenberg.org/files/2383/2383-h/2383-h.htm",
        "Paradise_Lost": "https://www.gutenberg.org/files/20/20-h/20-h.htm"
    }
    
    for name, url in urls.items():
        try:
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            
            output_file = output_dir / f"Gutenberg_{name}.txt"
            output_file.write_text(text, encoding='utf-8')
            logger.info(f"Harvested: {name}")
            
        except Exception as e:
            logger.error(f"Failed to harvest {name}: {e}")
    
    logger.info("Gutenberg harvest complete")

def harvest_url(url):
    """Harvest text from a specific URL"""
    logger.info(f"Harvesting URL: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        
        output_dir = project_root / "corpus_texts/web_discoveries"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"Web_{hash(url)}.txt"
        output_file = output_dir / filename
        output_file.write_text(text, encoding='utf-8')
        
        logger.info(f"Harvested URL to {filename}")
        
    except Exception as e:
        logger.error(f"Failed to harvest URL {url}: {e}")
        raise

def process_corpus(folder_path, language="english"):
    """Process texts in a corpus folder"""
    logger.info(f"Processing {language} corpus in {folder_path}")
    
    target_folder = project_root / folder_path
    if not target_folder.exists():
        logger.error(f"Folder not found: {target_folder}")
        return
    
    # Load appropriate spaCy model
    try:
        if language == "greek":
            nlp = spacy.load("el_core_news_sm")
        else:
            nlp = spacy.load("en_core_web_sm")
    except:
        logger.error(f"spaCy model for {language} not found. Please install it.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    text_files = list(target_folder.glob("*.txt"))
    for text_file in text_files[:5]:  # Process first 5 for testing
        try:
            # Check if already processed
            cur.execute("SELECT id FROM texts WHERE filename = ?", (text_file.name,))
            if cur.fetchone():
                logger.info(f"Already processed: {text_file.name}")
                continue
            
            # Read and process text
            text = text_file.read_text(encoding='utf-8')
            doc = nlp(text[:100000])  # Process first 100k chars
            
            # Insert text record
            cur.execute(
                "INSERT INTO texts (filename, language, source) VALUES (?, ?, ?)",
                (text_file.name, language, folder_path)
            )
            text_id = cur.lastrowid
            
            # Insert tokens
            for sent_id, sent in enumerate(doc.sents):
                for token_id, token in enumerate(sent):
                    cur.execute("""
                        INSERT INTO tokens 
                        (text_id, sentence_id, token_id_in_sent, text, lemma, pos, dependency, head_text)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (text_id, sent_id, token_id, token.text, token.lemma_, 
                         token.pos_, token.dep_, token.head.text if token.head != token else None))
            
            conn.commit()
            logger.info(f"Processed: {text_file.name}")
            
        except Exception as e:
            logger.error(f"Failed to process {text_file.name}: {e}")
    
    conn.close()
    logger.info(f"Corpus processing complete for {folder_path}")

def discover_texts(topic):
    """Discover texts related to a topic"""
    logger.info(f"Discovering texts for topic: {topic}")
    
    try:
        from googlesearch import search
        
        results = []
        for url in search(f"{topic} text corpus filetype:txt OR filetype:pdf", num=10, stop=10):
            results.append(url)
            logger.info(f"Found: {url}")
        
        # Save discovered URLs
        output_file = project_root / "discovered_urls.txt"
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n# Topic: {topic} - {datetime.now().isoformat()}\n")
            for url in results:
                f.write(f"{url}\n")
        
        logger.info(f"Discovered {len(results)} URLs for {topic}")
        
    except Exception as e:
        logger.error(f"Discovery failed for {topic}: {e}")

def extract_valency_patterns():
    """Extract valency patterns from processed texts"""
    logger.info("Extracting valency patterns...")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Get all verbs
    cur.execute("""
        SELECT DISTINCT lemma, pos, text_id 
        FROM tokens 
        WHERE pos IN ('VERB', 'AUX')
    """)
    
    verbs = cur.fetchall()
    patterns_found = 0
    
    for verb_lemma, pos, text_id in verbs:
        # Find arguments for this verb
        cur.execute("""
            SELECT dependency, COUNT(*) 
            FROM tokens 
            WHERE head_text = ? AND text_id = ?
            GROUP BY dependency
        """, (verb_lemma, text_id))
        
        dependencies = cur.fetchall()
        if dependencies:
            pattern = "+".join([f"{dep}:{count}" for dep, count in dependencies])
            
            # Store pattern
            cur.execute("""
                INSERT OR REPLACE INTO valency_patterns (verb_lemma, pattern, frequency, text_id)
                VALUES (?, ?, ?, ?)
            """, (verb_lemma, pattern, 1, text_id))
            
            patterns_found += 1
    
    conn.commit()
    conn.close()
    
    logger.info(f"Extracted {patterns_found} valency patterns")

if __name__ == "__main__":
    setup_database()
    logger.info("Agent actions module ready")
def harvest_greek_periods():
    """Execute Greek periods harvesting"""
    from scripts.greek_periods_harvester import harvest_greek_periods, find_retranslations
    
    logger.info("Starting Greek historical periods harvest...")
    harvest_greek_periods()
    retranslations = find_retranslations()
    logger.info(f"Greek periods harvest complete. Found {len(retranslations)} retranslation sources")
    
# Add this case to process_mission_action function:
elif command == "HARVEST" and data == "GREEK_PERIODS":
    harvest_greek_periods()
