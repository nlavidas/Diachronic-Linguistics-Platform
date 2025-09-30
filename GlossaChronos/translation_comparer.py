import difflib
from collections import Counter
import nltk

class TranslationComparer:
    """Compare multiple translations of the same text"""
    
    def __init__(self):
        self.translations = {}
    
    def add_translation(self, name, text, metadata=None):
        """Add a translation version"""
        self.translations[name] = {
            'text': text,
            'metadata': metadata or {},
            'tokens': nltk.word_tokenize(text),
            'sentences': nltk.sent_tokenize(text)
        }
    
    def compare_vocabulary(self):
        """Compare vocabulary across translations"""
        vocab_stats = {}
        for name, trans in self.translations.items():
            words = [w.lower() for w in trans['tokens'] if w.isalpha()]
            vocab_stats[name] = {
                'unique_words': len(set(words)),
                'total_words': len(words),
                'avg_word_length': sum(len(w) for w in words) / len(words),
                'top_words': Counter(words).most_common(10)
            }
        return vocab_stats
    
    def find_differences(self, version1, version2):
        """Find specific differences between two versions"""
        text1 = self.translations[version1]['text']
        text2 = self.translations[version2]['text']
        
        differ = difflib.unified_diff(
            text1.split(), 
            text2.split(),
            lineterm='',
            fromfile=version1,
            tofile=version2
        )
        return list(differ)
    
    def semantic_similarity(self, version1, version2):
        """Calculate semantic similarity between translations"""
        # Simple Jaccard similarity
        words1 = set(self.translations[version1]['tokens'])
        words2 = set(self.translations[version2]['tokens'])
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0