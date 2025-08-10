import logging
from pathlib import Path
import sys
import sqlite3
import json

# --- SETUP ---
# Ensure the project root is on the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = project_root / "corpus.db"
OUTPUT_FILE = project_root / "output" / "valency_patterns.jsonl"
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# --- VALENCY EXTRACTOR CLASS (from your script) ---

class ValencyExtractor:
    """
    Extracts verb argument frames from dependency-parsed sentences stored in our database.
    """
    def __init__(self, subj_rels=('nsubj',), obj_rels=('obj', 'dobj', 'iobj')):
        self.subj_rels = set(subj_rels)
        self.obj_rels = set(obj_rels)

    def extract_frames_from_sentence(self, tokens: list):
        """
        Processes a single sentence (represented as a list of token dictionaries).
        """
        id_map = {t['token_id_in_sent']: t for t in tokens}
        frames = []
        
        for token in tokens:
            if token['pos'] in ('VERB', 'AUX') or token['dependency'] == 'ROOT':
                verb = token
                verb_id = verb['token_id_in_sent']
                
                frame = {
                    'verb_lemma': verb['lemma'],
                    'verb_text': verb['text'],
                    'arguments': []
                }
                
                # Find dependents of this verb
                for dependent in tokens:
                    if dependent.get('head_text') == verb['text']: # Simple head matching for now
                        role = None
                        deprel = dependent['dependency']
                        
                        if deprel in self.subj_rels:
                            role = 'SUBJ'
                        elif deprel in self.obj_rels:
                            role = 'OBJ'
                        elif deprel.startswith('obl'):
                            role = 'OBLIQUE'
                        
                        if role:
                            frame['arguments'].append({
                                'text': dependent['text'],
                                'lemma': dependent['lemma'],
                                'pos': dependent['pos'],
                                'role': role
                            })
                
                if frame['arguments']:
                    frames.append(frame)
        return frames

# --- MAIN EXECUTION ---
def main():
    logger.info("--- Valency Extractor Initialized ---")
    if not DB_PATH.exists():
        logger.error("Database not found. Please run the preprocessor first.")
        return

    extractor = ValencyExtractor()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get all sentences from the database
    cur.execute("SELECT text_id, sentence_id FROM tokens GROUP BY text_id, sentence_id")
    sentences = cur.fetchall()
    
    logger.info(f"Found {len(sentences)} sentences to analyze in the database.")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        for i, sent in enumerate(sentences):
            if i > 500: break # Process a sample of 500 sentences for this test
            
            cur.execute("SELECT * FROM tokens WHERE text_id = ? AND sentence_id = ?", (sent['text_id'], sent['sentence_id']))
            tokens_in_sent = [dict(row) for row in cur.fetchall()]
            
            frames = extractor.extract_frames_from_sentence(tokens_in_sent)
            
            if frames:
                for frame in frames:
                    f_out.write(json.dumps(frame, ensure_ascii=False) + '\n')
    
    conn.close()
    logger.info(f"--- Valency Extraction Complete. Results saved to {OUTPUT_FILE.name} ---")

if __name__ == "__main__":
    main()