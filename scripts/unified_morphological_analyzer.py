import spacy
import stanza
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedMorphologicalAnalyzer:
    def __init__(self):
        self.models_loaded = False
        
    def load_models(self):
        if not self.models_loaded:
            try:
                logger.info('Loading spaCy model...')
                self.spacy_model = spacy.load('el_core_news_sm')
            except:
                logger.warning('spaCy Greek model not found, using English')
                self.spacy_model = spacy.load('en_core_web_sm')
            
            try:
                logger.info('Loading Stanza pipeline...')
                self.stanza_pipeline = stanza.Pipeline('el', processors='tokenize,pos,lemma')
            except:
                logger.warning('Stanza Greek model not found')
                self.stanza_pipeline = None
            
            self.models_loaded = True
    
    def analyze_text(self, text, analyzer='spacy'):
        self.load_models()
        
        if analyzer == 'spacy' and self.spacy_model:
            doc = self.spacy_model(text)
            return [{'text': token.text, 'lemma': token.lemma_, 'pos': token.pos_} for token in doc]
        elif analyzer == 'stanza' and self.stanza_pipeline:
            doc = self.stanza_pipeline(text)
            results = []
            for sentence in doc.sentences:
                for word in sentence.words:
                    results.append({'text': word.text, 'lemma': word.lemma, 'pos': word.upos})
            return results
        else:
            return []

if __name__ == '__main__':
    analyzer = UnifiedMorphologicalAnalyzer()
    test_text = 'This is a test sentence.'
    results = analyzer.analyze_text(test_text)
    print(f'Analyzed {len(results)} tokens')
    for r in results[:5]:
        print(r)
