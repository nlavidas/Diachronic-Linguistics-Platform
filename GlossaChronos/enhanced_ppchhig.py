import os
import re
import nltk
from nltk.tree import Tree

class EnhancedPPCHiGParser:
    def __init__(self):
        self.psd_path = 'Z:\\GlossaChronos\\PPCHiG\\PSD'
        
    def parse_tree_structure(self, filepath):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract first complete tree
        match = re.search(r'\((.*?)\n\n', content, re.DOTALL)
        if match:
            tree_str = match.group(0)
            # Extract Greek words
            greek_words = re.findall(r'[\u0370-\u03FF\u1F00-\u1FFF]+', tree_str)
            # Extract POS tags
            pos_tags = re.findall(r'\(([A-Z]+)\s', tree_str)
            return {
                'greek_text': ' '.join(greek_words[:20]),  # First 20 words
                'pos_tags': pos_tags[:20],
                'tree_sample': tree_str[:500]
            }
        return None
        
# Test with Mark gospel
parser = EnhancedPPCHiGParser()
result = parser.parse_tree_structure('Z:\\GlossaChronos\\PPCHiG\\PSD\\Mark.psd')
if result:
    print(f"Greek text: {result['greek_text']}")
    print(f"POS tags: {result['pos_tags'][:10]}")
