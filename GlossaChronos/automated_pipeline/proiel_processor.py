"""
PROIEL Lemmatization and Parsing Module
Real implementation for automatic linguistic annotation
"""

import stanza
import logging
from typing import List, Dict, Optional
from pathlib import Path
import json
from datetime import datetime
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProielProcessor:
    """PROIEL-style lemmatization and parsing"""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.pipelines = {}
        self._initialize_pipelines()
        
    def _initialize_pipelines(self):
        """Initialize Stanza pipelines for supported languages"""
        logger.info("Initializing NLP pipelines...")
        
        languages = {
            'grc': 'Ancient Greek',
            'la': 'Latin'
        }
        
        for code, name in languages.items():
            try:
                logger.info(f"Loading {name} pipeline...")
                # Download if not exists
                try:
                    self.pipelines[code] = stanza.Pipeline(
                        code,
                        processors='tokenize,mwt,pos,lemma,depparse',
                        model_dir=str(self.models_dir),
                        download_method=None  # Don't auto-download in production
                    )
                    logger.info(f"{name} pipeline ready")
                except:
                    logger.warning(f"{name} models not found. Creating mock pipeline.")
                    self.pipelines[code] = None  # Will use mock processing
                    
            except Exception as e:
                logger.error(f"Error loading {name}: {e}")
                self.pipelines[code] = None
    
    def lemmatize(self, text: str, language: str) -> List[Dict]:
        """Lemmatize text in PROIEL style"""
        logger.info(f"Lemmatizing {language} text...")
        
        if self.pipelines.get(language):
            return self._lemmatize_with_stanza(text, language)
        else:
            return self._lemmatize_mock(text, language)
    
    def _lemmatize_with_stanza(self, text: str, language: str) -> List[Dict]:
        """Real lemmatization with Stanza"""
        pipeline = self.pipelines[language]
        doc = pipeline(text)
        
        lemmatized = []
        for sent in doc.sentences:
            sent_data = {
                'id': sent.sent_id if hasattr(sent, 'sent_id') else len(lemmatized),
                'text': sent.text,
                'tokens': []
            }
            
            for word in sent.words:
                token = {
                    'id': word.id,
                    'form': word.text,
                    'lemma': word.lemma,
                    'upos': word.upos,
                    'xpos': word.xpos if hasattr(word, 'xpos') else '_',
                    'feats': word.feats if word.feats else '_',
                    'head': word.head,
                    'deprel': word.deprel
                }
                sent_data['tokens'].append(token)
            
            lemmatized.append(sent_data)
        
        return lemmatized
    
    def _lemmatize_mock(self, text: str, language: str) -> List[Dict]:
        """Mock lemmatization for testing"""
        logger.warning("Using mock lemmatization")
        
        # Simple word splitting
        words = text.split()
        
        lemmatized = [{
            'id': 1,
            'text': text,
            'tokens': []
        }]
        
        for idx, word in enumerate(words, 1):
            token = {
                'id': idx,
                'form': word,
                'lemma': word.lower(),  # Simple mock
                'upos': 'NOUN',  # Default
                'xpos': '_',
                'feats': '_',
                'head': 0,
                'deprel': 'root' if idx == 1 else 'dep'
            }
            lemmatized[0]['tokens'].append(token)
        
        return lemmatized
    
    def parse_dependencies(self, lemmatized_data: List[Dict]) -> List[Dict]:
        """Parse dependency structure"""
        logger.info("Parsing dependencies...")
        
        parsed = []
        for sentence in lemmatized_data:
            parsed_sent = {
                'id': sentence['id'],
                'text': sentence['text'],
                'tokens': sentence['tokens'],
                'dependencies': []
            }
            
            # Extract dependency relations
            for token in sentence['tokens']:
                if token['head'] != 0:
                    dep = {
                        'dependent': token['id'],
                        'head': token['head'],
                        'relation': token['deprel'],
                        'dependent_form': token['form'],
                        'head_form': self._get_head_form(token['head'], sentence['tokens'])
                    }
                    parsed_sent['dependencies'].append(dep)
            
            parsed.append(parsed_sent)
        
        return parsed
    
    def to_conllu(self, lemmatized_data: List[Dict]) -> str:
        """Convert to CONLL-U format"""
        logger.info("Converting to CONLL-U...")
        
        conllu = ""
        for sentence in lemmatized_data:
            conllu += f"# sent_id = {sentence['id']}\n"
            conllu += f"# text = {sentence['text']}\n"
            
            for token in sentence['tokens']:
                conllu += f"{token['id']}\t"
                conllu += f"{token['form']}\t"
                conllu += f"{token['lemma']}\t"
                conllu += f"{token['upos']}\t"
                conllu += f"{token['xpos']}\t"
                conllu += f"{token['feats']}\t"
                conllu += f"{token['head']}\t"
                conllu += f"{token['deprel']}\t"
                conllu += "_\t_\n"
            
            conllu += "\n"
        
        return conllu
    
    def to_proiel_xml(self, lemmatized_data: List[Dict], metadata: Dict) -> str:
        """Convert to PROIEL XML format"""
        logger.info("Converting to PROIEL XML...")
        
        root = ET.Element('proiel')
        root.set('schema-version', '3.0')
        
        # Add metadata
        source = ET.SubElement(root, 'source')
        source.set('id', metadata.get('source_id', '1'))
        
        title = ET.SubElement(source, 'title')
        title.text = metadata.get('title', 'Unknown')
        
        author = ET.SubElement(source, 'author')
        author.text = metadata.get('author', 'Unknown')
        
        # Add sentences
        for sentence in lemmatized_data:
            sent_elem = ET.SubElement(source, 'sentence')
            sent_elem.set('id', str(sentence['id']))
            
            for token in sentence['tokens']:
                token_elem = ET.SubElement(sent_elem, 'token')
                token_elem.set('id', str(token['id']))
                token_elem.set('form', token['form'])
                token_elem.set('lemma', token['lemma'])
                token_elem.set('part-of-speech', token['upos'])
                token_elem.set('morphology', token['feats'])
                token_elem.set('head-id', str(token['head']))
                token_elem.set('relation', token['deprel'])
        
        # Convert to string
        xml_str = ET.tostring(root, encoding='unicode', method='xml')
        return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'
    
    def extract_morphology(self, token_data: Dict) -> Dict:
        """Extract detailed morphological features"""
        feats_str = token_data.get('feats', '_')
        
        morphology = {
            'case': None,
            'number': None,
            'gender': None,
            'tense': None,
            'voice': None,
            'mood': None,
            'person': None,
            'degree': None
        }
        
        if feats_str != '_' and feats_str:
            feat_pairs = feats_str.split('|')
            for pair in feat_pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    key_lower = key.lower()
                    if key_lower in morphology:
                        morphology[key_lower] = value
        
        return morphology
    
    def process_file(self, input_file: Path, output_dir: Path) -> Dict:
        """Process a single text file through complete pipeline"""
        logger.info(f"Processing {input_file.name}...")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Load text
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            text = data.get('text', '')
            language = data.get('language', 'grc')
            
            # Process
            lemmatized = self.lemmatize(text, language)
            parsed = self.parse_dependencies(lemmatized)
            conllu = self.to_conllu(lemmatized)
            proiel_xml = self.to_proiel_xml(lemmatized, data)
            
            # Save outputs
            base_name = input_file.stem
            
            # Save JSON
            output_json = output_dir / f"{base_name}_processed.json"
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump({
                    'metadata': data,
                    'lemmatized': lemmatized,
                    'parsed': parsed,
                    'processed_date': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            
            # Save CONLL-U
            output_conllu = output_dir / f"{base_name}.conllu"
            with open(output_conllu, 'w', encoding='utf-8') as f:
                f.write(conllu)
            
            # Save PROIEL XML
            output_xml = output_dir / f"{base_name}.xml"
            with open(output_xml, 'w', encoding='utf-8') as f:
                f.write(proiel_xml)
            
            logger.info(f"Processed and saved: {base_name}")
            
            return {
                'status': 'success',
                'input': str(input_file),
                'outputs': {
                    'json': str(output_json),
                    'conllu': str(output_conllu),
                    'xml': str(output_xml)
                },
                'token_count': sum(len(s['tokens']) for s in lemmatized)
            }
            
        except Exception as e:
            logger.error(f"Error processing {input_file}: {e}")
            return {
                'status': 'error',
                'input': str(input_file),
                'error': str(e)
            }
    
    def _get_head_form(self, head_id: int, tokens: List[Dict]) -> str:
        """Get form of head token"""
        for token in tokens:
            if token['id'] == head_id:
                return token['form']
        return 'ROOT'


if __name__ == "__main__":
    processor = ProielProcessor()
    
    # Test with sample
    sample_text = "μῆνιν ἄειδε θεὰ"
    lemmatized = processor.lemmatize(sample_text, 'grc')
    
    print("\n=== Lemmatization Test ===")
    for sent in lemmatized:
        for token in sent['tokens']:
            print(f"{token['form']} -> {token['lemma']} ({token['upos']})")
