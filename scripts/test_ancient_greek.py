from cltk import NLP
from cltk.languages.example_texts import get_example_text
import sqlite3
from pathlib import Path

def process_ancient_greek_properly():
    # Initialize Ancient Greek NLP
    cltk_nlp = NLP(language="grc")  # grc = Ancient Greek
    
    # Test with a sample
    sample = "Μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος"  # First line of Iliad
    doc = cltk_nlp.analyze(text=sample)
    
    print("Sample analysis:")
    for token in doc.tokens[:10]:
        print(f"  {token.string:15} POS: {token.upos:10} Lemma: {token.lemma}")
    
    return doc

# Test it
doc = process_ancient_greek_properly()
print("\nCLTK is working for Ancient Greek!")
