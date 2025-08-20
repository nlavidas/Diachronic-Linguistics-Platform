#!/usr/bin/env python3
"""
Debug PROIEL XML format to understand why we're not getting cases
"""

from lxml import etree
import pandas as pd

print("🔍 DEBUGGING PROIEL XML FORMAT\n")

# Parse XML
xml_path = "corpus_data/greek-nt.xml"
tree = etree.parse(xml_path)

# Get first few sentences for detailed inspection
sentences = tree.xpath('//sentence')[:5]

for i, sentence in enumerate(sentences):
    print(f"\n{'='*60}")
    print(f"SENTENCE {i+1} (id: {sentence.get('id')})")
    print('='*60)
    
    # Get all tokens
    tokens = sentence.xpath('.//token')
    
    # First, show all tokens in order
    print("\nALL TOKENS:")
    for token in tokens:
        form = token.get('form', '')
        lemma = token.get('lemma', '')
        pos = token.get('part-of-speech', '')
        relation = token.get('relation', '')
        head_id = token.get('head-id', '')
        morph = token.get('morphology', '')
        
        print(f"\nToken: {form} ({lemma})")
        print(f"  POS: {pos}")
        print(f"  Morphology: {morph} (length: {len(morph)})")
        print(f"  Relation: {relation}")
        print(f"  Head: {head_id}")
        
        # Break down morphology if it exists
        if morph and len(morph) >= 8:
            print(f"  Morphology breakdown:")
            print(f"    [0] POS: {morph[0] if len(morph) > 0 else '-'}")
            print(f"    [1] Person: {morph[1] if len(morph) > 1 else '-'}")
            print(f"    [2] Number: {morph[2] if len(morph) > 2 else '-'}")
            print(f"    [3] Tense: {morph[3] if len(morph) > 3 else '-'}")
            print(f"    [4] Voice: {morph[4] if len(morph) > 4 else '-'}")
            print(f"    [5] Mood: {morph[5] if len(morph) > 5 else '-'}")
            print(f"    [6] Degree: {morph[6] if len(morph) > 6 else '-'}")
            print(f"    [7] Case: {morph[7] if len(morph) > 7 else '-'}")
            print(f"    [8] Gender: {morph[8] if len(morph) > 8 else '-'}")
    
    # Find verbs and their arguments
    verbs = sentence.xpath('.//token[starts-with(@part-of-speech, "V-")]')
    
    for verb in verbs:
        verb_id = verb.get('id')
        verb_form = verb.get('form')
        print(f"\n🔵 VERB: {verb_form} (id: {verb_id})")
        
        # Find all dependents
        dependents = sentence.xpath(f'.//token[@head-id="{verb_id}"]')
        print(f"  Has {len(dependents)} dependents:")
        
        for dep in dependents:
            dep_form = dep.get('form')
            dep_rel = dep.get('relation')
            dep_pos = dep.get('part-of-speech', '')
            dep_morph = dep.get('morphology', '')
            
            print(f"    - {dep_form}: relation={dep_rel}, POS={dep_pos}")
            if dep_morph and len(dep_morph) > 7:
                print(f"      Case character at [7]: '{dep_morph[7]}'")

# Now let's check the overall statistics
print("\n" + "="*60)
print("OVERALL STATISTICS")
print("="*60)

# Check all relations
all_relations = tree.xpath('//token/@relation')
relation_counts = pd.Series(all_relations).value_counts()
print("\nAll relation types:")
for rel, count in relation_counts.head(20).items():
    print(f"  {rel}: {count}")

# Check POS tags for nouns/pronouns
noun_tokens = tree.xpath('//token[starts-with(@part-of-speech, "N-") or starts-with(@part-of-speech, "P")]')
print(f"\nFound {len(noun_tokens)} noun/pronoun tokens")

# Sample some nouns with morphology
print("\nSample noun morphologies:")
for token in noun_tokens[:10]:
    form = token.get('form')
    morph = token.get('morphology', '')
    pos = token.get('part-of-speech')
    if morph and len(morph) > 7:
        case_char = morph[7]
        print(f"  {form}: morph={morph}, case_char='{case_char}', POS={pos}")

# Check how many tokens have morphology
tokens_with_morph = tree.xpath('//token[@morphology]')
print(f"\nTokens with morphology: {len(tokens_with_morph)}")

# Check specific attributes
print("\nChecking token attributes:")
sample_token = tree.xpath('//token')[0]
attrs = sample_token.attrib
print(f"Available attributes: {list(attrs.keys())}")