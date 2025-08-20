#!/usr/bin/env python3
import spacy
import json
import sys

def extract_entities(file_path):
    try:
        nlp = spacy.load('en_core_web_sm')
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        doc = nlp(text)
        entities = {
            "people": list(set([ent.text for ent in doc.ents if ent.label_ == 'PERSON'])),
            "dates": list(set([ent.text for ent in doc.ents if ent.label_ == 'DATE'])),
            "locations": list(set([ent.text for ent in doc.ents if ent.label_ == 'GPE']))
        }
        print(json.dumps(entities, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        extract_entities(sys.argv[1])
    else:
        print(json.dumps({"error": "No input file specified."}))