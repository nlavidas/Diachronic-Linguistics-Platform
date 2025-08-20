#!/usr/bin/env python3
"""
Fix case extraction to get proper Greek cases (NOM, ACC, DAT, GEN)
instead of UNK
"""

import pandas as pd
from lxml import etree
import json
from collections import Counter, defaultdict

print("🔧 Fixing Greek case extraction...\n")

# Load the existing CSV
df = pd.read_csv('corpus_data/valency_patterns.csv')
print(f"Loaded {len(df)} patterns from CSV")

# Parse the XML again for proper case extraction
xml_path = "corpus_data/greek-nt.xml"
tree = etree.parse(xml_path)

# Comprehensive Greek morphology mapping
GREEK_MORPHOLOGY = {
    # Case position is character 7 (0-indexed)
    'cases': {
        'n': 'NOM',    # Nominative
        'g': 'GEN',    # Genitive  
        'd': 'DAT',    # Dative
        'a': 'ACC',    # Accusative
        'v': 'VOC',    # Vocative
        'l': 'LOC',    # Locative
        'i': 'INS',    # Instrumental
        '-': None
    },
    # Voice position is character 4
    'voices': {
        'a': 'active',
        'p': 'passive',
        'm': 'middle',
        'e': 'medio-passive',
        '-': 'active'
    }
}

def extract_proper_cases(sentence, verb):
    """Extract cases with correct morphology parsing"""
    verb_id = verb.get('id')
    arguments = []
    
    for token in sentence.xpath('.//token'):
        if token.get('head-id') == verb_id:
            rel = token.get('relation')
            
            # Core argument relations
            if rel in ['sub', 'obj', 'obl', 'xobj', 'xsub', 'arg', 'adv']:
                pos = token.get('part-of-speech', '')
                morph = token.get('morphology', '')
                
                # Check if it's a noun, pronoun, or adjective
                if pos and pos[0] in ['N', 'P', 'A', 'S']:  # S for articles
                    # PROIEL morphology: POS-person-number-tense-voice-mood-degree-case-gend-anim
                    if len(morph) >= 8:
                        case_char = morph[7]
                        case = GREEK_MORPHOLOGY['cases'].get(case_char)
                        
                        if case:
                            arguments.append({
                                'relation': rel,
                                'case': case,
                                'lemma': token.get('lemma'),
                                'pos': pos[0]
                            })
    
    return arguments

# Re-process all sentences
print("\nRe-processing sentences for proper cases...")
sentence_patterns = {}
verb_data = []

sentences = tree.xpath('//sentence')
for i, sentence in enumerate(sentences):
    if i % 1000 == 0:
        print(f"Processing sentence {i}/{len(sentences)}...")
    
    sent_id = sentence.get('id')
    
    # Find all verbs
    verbs = sentence.xpath('.//token[starts-with(@part-of-speech, "V-")]')
    
    for verb in verbs:
        lemma = verb.get('lemma')
        form = verb.get('form')
        morph = verb.get('morphology', '')
        
        # Extract voice properly
        voice = 'active'
        if len(morph) > 4:
            voice = GREEK_MORPHOLOGY['voices'].get(morph[4], 'active')
        
        # Get arguments with proper cases
        arguments = extract_proper_cases(sentence, verb)
        
        # Create case pattern
        cases = [arg['case'] for arg in arguments if arg['case']]
        
        # Order by typical Greek word order preferences
        case_order = {'NOM': 1, 'ACC': 2, 'GEN': 3, 'DAT': 4, 'VOC': 5}
        cases.sort(key=lambda x: case_order.get(x, 99))
        
        case_pattern = '-'.join(cases) if cases else 'INTR'
        
        verb_data.append({
            'sentence_id': sent_id,
            'lemma': lemma,
            'form': form,
            'voice': voice,
            'case_pattern': case_pattern,
            'argument_count': len(arguments),
            'arguments': json.dumps(arguments, ensure_ascii=False)
        })

# Create new DataFrame with proper cases
new_df = pd.DataFrame(verb_data)

# Save the corrected data
new_df.to_csv('corpus_data/valency_patterns_fixed.csv', index=False)
print(f"\n✅ Saved {len(new_df)} patterns with proper cases")

# Analyze the results
print("\n📊 CASE PATTERN DISTRIBUTION:")
case_counts = new_df['case_pattern'].value_counts()
for pattern, count in case_counts.head(20).items():
    if pattern != 'INTR':
        print(f"  {pattern}: {count} instances")

# Voice alternations with case patterns
print("\n🔄 VOICE ALTERNATIONS WITH CASES:")
voice_patterns = new_df.groupby(['lemma', 'voice', 'case_pattern']).size().reset_index(name='count')
voice_patterns = voice_patterns[voice_patterns['count'] > 5]

# Find verbs with multiple voice-case combinations
lemma_variations = voice_patterns.groupby('lemma').size()
variable_verbs = lemma_variations[lemma_variations > 1].index

print(f"\nVerbs with voice-case variations: {len(variable_verbs)}")
for verb in list(variable_verbs)[:10]:
    verb_data = voice_patterns[voice_patterns['lemma'] == verb]
    print(f"\n{verb}:")
    for _, row in verb_data.iterrows():
        print(f"  {row['voice']} + {row['case_pattern']}: {row['count']} instances")

# Find argument structure changes (NOM-ACC → NOM-DAT)
print("\n🔄 POTENTIAL ARGUMENT STRUCTURE VARIATIONS:")
lemma_patterns = new_df.groupby(['lemma', 'case_pattern']).size().reset_index(name='count')
lemma_patterns = lemma_patterns[lemma_patterns['count'] > 10]

# Find verbs with multiple patterns
pattern_variations = lemma_patterns.groupby('lemma')['case_pattern'].apply(list).reset_index()
pattern_variations['num_patterns'] = pattern_variations['case_pattern'].apply(len)
pattern_variations = pattern_variations[pattern_variations['num_patterns'] > 1]

for _, row in pattern_variations.head(10).iterrows():
    print(f"\n{row['lemma']}: {', '.join(row['case_pattern'])}")

# Summary statistics
print("\n📈 SUMMARY:")
print(f"Total verb instances: {len(new_df)}")
print(f"Unique case patterns: {new_df['case_pattern'].nunique()}")
print(f"Transitive patterns: {len(new_df[new_df['case_pattern'] != 'INTR'])}")
print(f"Most common pattern: {case_counts.index[0]} ({case_counts.iloc[0]} instances)")

# Create a report
report = f"""
# GREEK VALENCY PATTERNS - CORRECTED ANALYSIS
Generated: {pd.Timestamp.now()}

## TOP CASE PATTERNS
"""
for pattern, count in case_counts.head(30).items():
    report += f"- {pattern}: {count} instances\n"

with open('corpus_data/case_analysis_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("\n✅ Analysis complete! Check corpus_data/case_analysis_report.md")