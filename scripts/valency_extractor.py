#!/usr/bin/env python3
import spacy
import json
from pathlib import Path

class ValencyExtractor:
    def __init__(self):
        print("[INFO] --- Valency Extractor Initialized ---")
        self.nlp = spacy.load("en_core_web_sm")
    
    def extract_valency_patterns(self, text):
        doc = self.nlp(text)
        patterns = []
        
        for sent in doc.sents:
            for token in sent:
                if token.pos_ == "VERB":
                    # Extract subject, object, indirect object
                    subj = [child for child in token.children if "subj" in child.dep_]
                    obj = [child for child in token.children if "obj" in child.dep_]
                    
                    pattern = {
                        "verb": token.lemma_,
                        "text": token.text,
                        "valency": len(subj) + len(obj),
                        "subjects": [s.text for s in subj],
                        "objects": [o.text for o in obj],
                        "sentence": sent.text
                    }
                    patterns.append(pattern)
        
        return patterns
    
    def process_corpus_file(self, filepath):
        text = Path(filepath).read_text(encoding='utf-8')
        return self.extract_valency_patterns(text)

if __name__ == "__main__":
    extractor = ValencyExtractor()
    # Add processing logic here