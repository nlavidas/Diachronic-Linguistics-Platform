import subprocess
import json
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import torch

class LinguisticAIEngine:
    def __init__(self):
        self.models = {
            'ollama_models': ['llama2', 'mistral', 'phi', 'tinyllama'],
            'huggingface_models': {
                'ner': 'dbmdz/bert-large-cased-finetuned-conll03-english',
                'pos': 'vblagoje/bert-english-uncased-finetuned-pos',
                'translation': 'Helsinki-NLP/opus-mt-en-de'
            }
        }
    
    def compare_translations(self, texts_dict):
        """Compare multiple translations of the same text"""
        # texts_dict = {'KJV': text1, 'NIV': text2, 'Vulgate': text3}
        results = {}
        for version, text in texts_dict.items():
            results[version] = {
                'tokens': text.split(),
                'length': len(text.split()),
                'unique_words': len(set(text.lower().split()))
            }
        return results
    
    def run_ollama_analysis(self, text, model='phi'):
        """Run Ollama model for linguistic analysis"""
        prompt = f"Perform linguistic analysis: {text[:500]}"
        result = subprocess.run(
            ['ollama', 'run', model, prompt],
            capture_output=True, text=True
        )
        return result.stdout
    
    def parallel_text_alignment(self, text1, text2):
        """Align parallel texts for comparison"""
        # Simple word-level alignment
        words1 = text1.split()
        words2 = text2.split()
        alignment = []
        for i, (w1, w2) in enumerate(zip(words1, words2)):
            alignment.append({
                'position': i,
                'text1': w1,
                'text2': w2,
                'match': w1.lower() == w2.lower()
            })
        return alignment