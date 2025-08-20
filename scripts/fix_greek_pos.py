import sqlite3
import stanza
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_greek_pos_tags():
    """Reprocess Greek texts with proper Ancient Greek NLP"""
    
    # Download if needed
    try:
        nlp = stanza.Pipeline('grc', processors='tokenize,pos,lemma,depparse')
    except:
        stanza.download('grc')
        nlp = stanza.Pipeline('grc', processors='tokenize,pos,lemma,depparse')
    
    conn = sqlite3.connect('corpus.db')
    cur = conn.cursor()
    
    # Get a sample Greek text
    cur.execute("""
        SELECT DISTINCT text_id, filename 
        FROM texts 
        WHERE filename LIKE 'Perseus%'
        LIMIT 1
    """)
    
    text_id, filename = cur.fetchone()
    logger.info(f"Processing {filename} (ID: {text_id})")
    
    # Get the actual text
    text_path = Path('corpus_texts/perseus_greek_classics') / filename
    if text_path.exists():
        text = text_path.read_text(encoding='utf-8')[:5000]  # First 5000 chars
        
        # Process with Stanza
        doc = nlp(text)
        
        # Clear old tokens for this text
        cur.execute("DELETE FROM tokens WHERE text_id = ?", (text_id,))
        
        # Insert corrected tokens
        for sent_id, sentence in enumerate(doc.sentences):
            for token_id, word in enumerate(sentence.words):
                cur.execute("""
                    INSERT INTO tokens 
                    (text_id, sentence_id, token_id_in_sent, text, lemma, pos, dependency, head_text)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (text_id, sent_id, token_id, 
                      word.text, word.lemma, word.upos,
                      word.deprel if hasattr(word, 'deprel') else None,
                      sentence.words[word.head-1].text if word.head > 0 else None))
        
        conn.commit()
        
        # Check the corrected verbs
        cur.execute("""
            SELECT lemma, COUNT(*) as freq
            FROM tokens
            WHERE text_id = ? AND pos = 'VERB'
            GROUP BY lemma
            ORDER BY freq DESC
            LIMIT 10
        """, (text_id,))
        
        print("\n=== CORRECTED VERBS ===")
        for lemma, freq in cur.fetchall():
            print(f"{lemma:20} : {freq} occurrences")
    
    conn.close()

if __name__ == "__main__":
    fix_greek_pos_tags()
