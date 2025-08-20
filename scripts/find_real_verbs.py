import sqlite3
from collections import defaultdict

def get_real_greek_verbs():
    """Get actual Greek verbs using linguistic rules"""
    
    conn = sqlite3.connect('corpus.db')
    cur = conn.cursor()
    
    # Real Greek verb endings
    verb_endings = [
        'ω', 'ῶ', 'ομαι', 'οῦμαι',  # Present
        'ον', 'ομην', 'ούμην',       # Imperfect  
        'σω', 'σομαι',                # Future
        'σα', 'σάμην',                # Aorist
        'κα', 'μαι',                  # Perfect
        'κειν', 'κέναι',              # Perfect
        'ειν', 'εῖν', 'ᾶν',          # Infinitives
        'ων', 'ῶν', 'ούς',           # Participles
    ]
    
    # Get words that might be verbs based on endings
    cur.execute("""
        SELECT DISTINCT lemma, COUNT(*) as freq
        FROM tokens
        WHERE length(lemma) > 2
        GROUP BY lemma
        HAVING freq > 10
        ORDER BY freq DESC
    """)
    
    potential_verbs = []
    for lemma, freq in cur.fetchall():
        for ending in verb_endings:
            if lemma.endswith(ending):
                potential_verbs.append((lemma, freq))
                break
    
    print("=== LIKELY ANCIENT GREEK VERBS ===\n")
    for verb, freq in potential_verbs[:30]:
        print(f"{verb:20} : {freq:,} occurrences")
    
    conn.close()
    return potential_verbs

get_real_greek_verbs()
