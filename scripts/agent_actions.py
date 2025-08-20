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
            
        elif command == "PROCESS":
            if data == "ENGLISH_CORPUS":
                process_english_corpus()
            else:
                logger.info(f"Processing corpus: {data}")
                
        elif command == "EXTRACT_VALENCY":
            extract_valency_patterns()
            
        elif command == "DISCOVER":
            logger.info(f"Discovery mission for: {data}")
            # Simple discovery - just log for now
            
        elif command == "HARVEST_URL":
            logger.info(f"Harvesting URL: {data}")
            # Simple harvest - just log for now
            
        else:
            logger.warning(f"Unknown command: {command}")
            
    except Exception as e:
        logger.error(f"Mission action failed: {e}")
        raise

def process_english_corpus():
    """Process English texts in the corpus"""
    logger.info("Processing English corpus...")
    
    corpus_dir = project_root / "corpus_texts/gutenberg_english"
    if not corpus_dir.exists():
        logger.warning(f"Corpus directory not found: {corpus_dir}")
        return
        
    text_files = list(corpus_dir.glob("*.txt"))
    logger.info(f"Found {len(text_files)} English texts to process")
    
    # For now, just count them
    logger.info("English corpus processing complete")

def extract_valency_patterns():
    """Extract valency patterns from database"""
    logger.info("Extracting valency patterns...")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Count verbs in database
    cur.execute("SELECT COUNT(DISTINCT lemma) FROM tokens WHERE pos = 'VERB'")
    verb_count = cur.fetchone()[0]
    
    logger.info(f"Found {verb_count} unique verbs in database")
    
    # Simple valency extraction
    cur.execute("""
        SELECT lemma, COUNT(*) as freq 
        FROM tokens 
        WHERE pos = 'VERB' 
        GROUP BY lemma 
        ORDER BY freq DESC 
        LIMIT 10
    """)
    
    top_verbs = cur.fetchall()
    for verb, freq in top_verbs:
        logger.info(f"Verb '{verb}': {freq} occurrences")
    
    conn.close()
    logger.info("Valency extraction complete")

if __name__ == "__main__":
    setup_database()
    logger.info("Agent actions module ready")
