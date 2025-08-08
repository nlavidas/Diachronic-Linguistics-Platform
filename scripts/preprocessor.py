import logging
from pathlib import Path
import sqlite3
import time

# --- SETUP ---
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

project_root = Path(__file__).resolve().parent.parent

# --- DATABASE SETUP ---
db_path = project_root / "corpus.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS texts (
    id INTEGER PRIMARY KEY,
    filename TEXT UNIQUE,
    language TEXT,
    processed_at TEXT
)''')
cur.execute('''
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
    morphology TEXT,
    FOREIGN KEY(text_id) REFERENCES texts(id)
)''')
conn.commit()
logger.info(f"Database ready at {db_path}")

# --- MODEL LOADING ---
logger.info("Loading AI models...")
try:
    import spacy
    nlp_en = spacy.load("en_core_web_sm")
    nlp_el = spacy.load("el_core_news_sm")
    
    # --- THIS IS THE FIX ---
    # Increase the maximum text length limit for both models
    nlp_en.max_length = 6000000 
    nlp_el.max_length = 6000000 
    # ----------------------

    logger.info("Models loaded.")
except ImportError:
    logger.error("spaCy is not installed. Please run: python -m pip install spacy")
    exit()
except OSError:
    logger.error("SpaCy models not found. Please run: python -m spacy download en_core_web_sm el_core_news_sm")
    exit()


# --- BATCH PROCESSING ---
text_folder = project_root / "texts" / "perseus_greek_classics"
logger.info(f"--- Starting Batch Analysis of folder: {text_folder} ---")

for text_file in text_folder.glob('*.txt'):
    try:
        cur.execute("SELECT id FROM texts WHERE filename = ?", (text_file.name,))
        if cur.fetchone():
            logger.info(f"Skipping already processed file: {text_file.name}")
            continue

        logger.info(f"--- Analyzing file: {text_file.name} ---")
        
        if any(name in text_file.name.lower() for name in ['homer', 'plato', 'plutarch', 'sophocles', 'herodotus', 'perseus_tlg']):
            nlp = nlp_el
            lang = 'greek'
        else:
            nlp = nlp_en
            lang = 'english'
        logger.info(f"Detected language: {lang}")
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO texts (filename, language, processed_at) VALUES (?, ?, ?)", (text_file.name, lang, timestamp))
        text_id = cur.lastrowid
        conn.commit()

        text_content = text_file.read_text(encoding="utf-8")
        doc = nlp(text_content)

        token_batch = []
        for sent_idx, sent in enumerate(doc.sents):
            for token_idx, token in enumerate(sent):
                morph_info = "|".join(f"{key}={val}" for key, val in token.morph.to_dict().items()) if token.morph else "_"
                token_data = (
                    text_id, sent_idx, token_idx, token.text, token.lemma_, 
                    token.pos_, token.dep_, token.head.text, morph_info
                )
                token_batch.append(token_data)

                if len(token_batch) >= 10000:
                    cur.executemany('''INSERT INTO tokens (text_id, sentence_id, token_id_in_sent, text, lemma, pos, dependency, head_text, morphology)
                                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', token_batch)
                    conn.commit()
                    logger.info(f"Saved {len(token_batch)} tokens to database for {text_file.name}...")
                    token_batch = []
        
        if token_batch:
            cur.executemany('''INSERT INTO tokens (text_id, sentence_id, token_id_in_sent, text, lemma, pos, dependency, head_text, morphology)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', token_batch)
            conn.commit()
            logger.info(f"Saved final {len(token_batch)} tokens to database for {text_file.name}.")

        logger.info(f"--- Finished processing {text_file.name} ---")

    except Exception as e:
        logger.error(f"Could not process file {text_file.name}. Error: {e}")

conn.close()
logger.info("--- Batch Analysis Complete ---")