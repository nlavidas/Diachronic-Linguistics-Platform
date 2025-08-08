import os
import json
import re
from collections import Counter

def process_text(filepath):
    """Process a collected text"""
    print(f"\nProcessing: {os.path.basename(filepath)}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Remove Gutenberg headers
    text = re.sub(r'\*\*\* START.*?\*\*\*', '', text, flags=re.DOTALL)
    text = re.sub(r'\*\*\* END.*?\*\*\*', '', text, flags=re.DOTALL)
    
    # Basic statistics
    sentences = re.split(r'[.!?]+', text)
    words = text.split()
    
    stats = {
        'characters': len(text),
        'words': len(words),
        'sentences': len([s for s in sentences if len(s.strip()) > 10]),
        'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
        'unique_words': len(set(w.lower() for w in words))
    }
    
    # Sample text
    sample = ' '.join(sentences[:5])
    
    return stats, sample

# Process all collected texts
collected_dir = r"Z:\DiachronicValencyCorpus\texts\collected"
results = {}

for filename in os.listdir(collected_dir):
    if filename.endswith('.txt'):
        filepath = os.path.join(collected_dir, filename)
        stats, sample = process_text(filepath)
        results[filename] = {
            'stats': stats,
            'sample': sample[:500] + '...'
        }
        
        print(f"  Words: {stats['words']:,}")
        print(f"  Sentences: {stats['sentences']:,}")
        print(f"  Avg sentence length: {stats['avg_sentence_length']:.1f} words")

# Save results
with open('texts/processed/processing_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n✅ Processing complete!")