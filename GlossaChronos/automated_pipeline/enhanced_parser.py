"""
ENHANCED UNIVERSAL DEPENDENCIES PARSER
Integrated from enhanced_universal_parser.py (10.8KB) + glossachronos_parser.py (7.8KB)
Advanced UD parsing with historical syntax support
"""

import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedParser:
    """
    Advanced Universal Dependencies parser
    Combines enhanced_universal_parser.py + glossachronos_parser.py
    Enhanced with Greek script detection from artifacts
    """
    
    def __init__(self):
        # Ancient Greek high-frequency verbs (from artifacts)
        self.ancient_greek_verbs = {
            'εἰμί', 'ἔχω', 'λέγω', 'ποιέω', 'γίγνομαι',
            'δίδωμι', 'τίθημι', 'ἵστημι', 'φημί', 'οἶδα'
        }
        
        # UD POS tags (Universal Dependencies)
        self.ud_pos_tags = [
            'ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN',
            'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 
            'VERB', 'X'
        ]
        
        # UD dependency relations
        self.ud_deprels = [
            'acl', 'advcl', 'advmod', 'amod', 'appos', 'aux', 'case',
            'cc', 'ccomp', 'clf', 'compound', 'conj', 'cop', 'csubj',
            'dep', 'det', 'discourse', 'dislocated', 'expl', 'fixed',
            'flat', 'goeswith', 'iobj', 'list', 'mark', 'nmod', 'nsubj',
            'nummod', 'obj', 'obl', 'orphan', 'parataxis', 'punct',
            'reparandum', 'root', 'vocative', 'xcomp'
        ]
        
        # Historical syntax patterns (for diachronic texts)
        self.historical_patterns = {
            'verb_final': r'\b\w+\s+\w+\s+(sum|est|sunt)',  # Latin V-final
            'old_english_order': r'þ[aæ]\s+\w+\s+\w+',
            'greek_postpositive': r'\w+\s+(δέ|γάρ|μέν)',
        }
        
        # Parsing rules
        self.parsing_rules = {
            'subject_verb_agreement': True,
            'object_case_marking': True,
            'modifier_agreement': True
        }
        
        logger.info("="*80)
        logger.info("ENHANCED UD PARSER")
        logger.info("="*80)
        logger.info(f"POS tags: {len(self.ud_pos_tags)}")
        logger.info(f"Dependency relations: {len(self.ud_deprels)}")
        logger.info(f"Ancient Greek verbs loaded: {len(self.ancient_greek_verbs)}")
    
    def parse_sentence(self, sentence: str, language: str = 'grc',
                      period: str = 'ancient') -> Dict:
        """
        Parse sentence with enhanced UD analysis
        
        Returns:
            {
                'tokens': [...],
                'dependencies': [...],
                'syntax_notes': [...],
                'conllu': '...'
            }
        """
        logger.info(f"\n[PARSING] {sentence[:50]}...")
        
        # Tokenize
        tokens = self._tokenize(sentence)
        
        # POS tagging (simplified - would use real NLP model)
        pos_tagged = self._pos_tag(tokens, language)
        
        # Dependency parsing
        dependencies = self._parse_dependencies(pos_tagged, language, period)
        
        # Historical syntax analysis
        syntax_notes = self._analyze_historical_syntax(sentence, language, period)
        
        # Generate CONLL-U
        conllu = self._to_conllu(pos_tagged, dependencies)
        
        result = {
            'tokens': pos_tagged,
            'dependencies': dependencies,
            'syntax_notes': syntax_notes,
            'conllu': conllu,
            'language': language,
            'period': period
        }
        
        logger.info(f"  ✓ Parsed: {len(tokens)} tokens, {len(dependencies)} dependencies")
        
        return result
    
    def _tokenize(self, sentence: str) -> List[str]:
        """Tokenize sentence"""
        # Simple word tokenization
        tokens = re.findall(r'\b\w+\b|[.,;!?]', sentence)
        return tokens
    
    def _pos_tag(self, tokens: List[str], language: str) -> List[Dict]:
        """
        POS tag tokens (simplified)
        Real implementation would use Stanza or similar
        """
        tagged = []
        
        for idx, token in enumerate(tokens, 1):
            # Heuristic tagging (simplified)
            if token in '.,;!?':
                pos = 'PUNCT'
            elif token.istitle() and idx == 1:
                pos = 'PROPN'
            elif any(c.isupper() for c in token):
                pos = 'PROPN'
            elif token.endswith(('ing', 'ed', 'es', 's')):
                pos = 'VERB'
            elif token.endswith(('ly', 'mente')):
                pos = 'ADV'
            elif token in ('the', 'a', 'an', 'ὁ', 'ἡ', 'τό'):
                pos = 'DET'
            elif token in ('and', 'or', 'but', 'καί', 'ἤ'):
                pos = 'CCONJ'
            elif token in ('in', 'on', 'at', 'ἐν', 'ἐπί'):
                pos = 'ADP'
            else:
                # Default to NOUN (would be smarter in real implementation)
                pos = 'NOUN'
            
            tagged.append({
                'id': idx,
                'form': token,
                'lemma': token.lower(),
                'upos': pos,
                'xpos': '_',
                'feats': '_',
                'head': 0,  # Will be set in dependency parsing
                'deprel': '_'
            })
        
        return tagged
    
    def _parse_dependencies(self, tokens: List[Dict], language: str, 
                          period: str) -> List[Dict]:
        """
        Parse dependency structure (simplified)
        Real implementation would use neural parser
        """
        dependencies = []
        
        # Find verb (root)
        verb_idx = None
        for token in tokens:
            if token['upos'] == 'VERB':
                verb_idx = token['id']
                token['head'] = 0
                token['deprel'] = 'root'
                break
        
        if not verb_idx:
            # No verb, use first noun as root
            for token in tokens:
                if token['upos'] in ['NOUN', 'PROPN']:
                    verb_idx = token['id']
                    token['head'] = 0
                    token['deprel'] = 'root'
                    break
        
        # Simple heuristic dependencies
        for token in tokens:
            if token['head'] == 0 and token['deprel'] == 'root':
                continue
            
            if token['upos'] == 'NOUN' and verb_idx:
                # Attach nouns to verb
                token['head'] = verb_idx
                token['deprel'] = 'nsubj' if token['id'] < verb_idx else 'obj'
            elif token['upos'] == 'ADJ':
                # Attach adjectives to nearest noun
                nearest_noun = self._find_nearest_noun(token['id'], tokens)
                if nearest_noun:
                    token['head'] = nearest_noun
                    token['deprel'] = 'amod'
            elif token['upos'] == 'ADP':
                # Attach prepositions to following noun
                next_noun = self._find_next_noun(token['id'], tokens)
                if next_noun:
                    token['head'] = next_noun
                    token['deprel'] = 'case'
            elif token['upos'] == 'DET':
                # Attach determiners to following noun
                next_noun = self._find_next_noun(token['id'], tokens)
                if next_noun:
                    token['head'] = next_noun
                    token['deprel'] = 'det'
            elif token['upos'] == 'PUNCT':
                # Attach punctuation to root
                token['head'] = verb_idx or 1
                token['deprel'] = 'punct'
            else:
                # Default attachment to root
                token['head'] = verb_idx or 1
                token['deprel'] = 'dep'
            
            dependencies.append({
                'dependent': token['id'],
                'head': token['head'],
                'deprel': token['deprel'],
                'dependent_form': token['form']
            })
        
        return dependencies
    
    def _find_nearest_noun(self, token_id: int, tokens: List[Dict]) -> Optional[int]:
        """Find nearest noun token"""
        for token in tokens:
            if token['upos'] in ['NOUN', 'PROPN']:
                if abs(token['id'] - token_id) <= 3:
                    return token['id']
        return None
    
    def _find_next_noun(self, token_id: int, tokens: List[Dict]) -> Optional[int]:
        """Find next noun after token"""
        for token in tokens:
            if token['id'] > token_id and token['upos'] in ['NOUN', 'PROPN']:
                return token['id']
        return None
    
    def _analyze_historical_syntax(self, sentence: str, language: str, 
                                  period: str) -> List[str]:
        """Analyze historical syntax patterns"""
        notes = []
        
        # Check for historical patterns
        for pattern_name, pattern in self.historical_patterns.items():
            if re.search(pattern, sentence):
                notes.append(f"Historical pattern detected: {pattern_name}")
        
        # Period-specific observations
        if language == 'grc' and period == 'ancient':
            if 'μέν' in sentence and 'δέ' in sentence:
                notes.append("Men...de construction (contrast)")
        
        elif language == 'la' and period == 'classical':
            if sentence.strip().endswith(('est', 'sunt', 'sum')):
                notes.append("Verb-final word order (typical Latin)")
        
        elif language == 'en' and period == 'old':
            if 'þ' in sentence or 'ð' in sentence:
                notes.append("Old English characters present")
        
        return notes
    
    def _to_conllu(self, tokens: List[Dict], dependencies: List[Dict]) -> str:
        """Convert to CONLL-U format"""
        conllu_lines = []
        
        conllu_lines.append("# sent_id = 1")
        conllu_lines.append(f"# text = {' '.join(t['form'] for t in tokens)}")
        
        for token in tokens:
            line = '\t'.join([
                str(token['id']),
                token['form'],
                token['lemma'],
                token['upos'],
                token['xpos'],
                token['feats'],
                str(token['head']),
                token['deprel'],
                '_',  # deps
                '_'   # misc
            ])
            conllu_lines.append(line)
        
        conllu_lines.append('')  # Empty line at end
        
        return '\n'.join(conllu_lines)
    
    def parse_text(self, text: str, language: str = 'grc', 
                  period: str = 'ancient') -> List[Dict]:
        """Parse entire text (multiple sentences)"""
        logger.info(f"\n[TEXT PARSING] Parsing {language}/{period} text...")
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        
        results = []
        
        for idx, sentence in enumerate(sentences, 1):
            logger.info(f"  Sentence {idx}/{len(sentences)}")
            result = self.parse_sentence(sentence, language, period)
            results.append(result)
        
        logger.info(f"✓ Parsed {len(results)} sentences")
        
        return results
    
    def detect_greek_script(self, text: str) -> str:
        """
        Detect Greek script type (from artifacts)
        Returns: 'polytonic', 'monotonic', 'not_greek', or 'unknown'
        """
        if not text:
            return 'unknown'
        
        # Count polytonic characters (Greek extended range)
        polytonic_chars = sum(1 for c in text if '\u1F00' <= c <= '\u1FFF')
        
        # Count all Greek characters
        total_greek = sum(1 for c in text if 
                         '\u0370' <= c <= '\u03FF' or  # Greek and Coptic
                         '\u1F00' <= c <= '\u1FFF')      # Greek Extended
        
        if total_greek == 0:
            return 'not_greek'
        
        # Calculate polytonic ratio
        polytonic_ratio = polytonic_chars / total_greek
        
        # Threshold: > 10% polytonic chars = polytonic Greek
        return 'polytonic' if polytonic_ratio > 0.1 else 'monotonic'
    
    def calculate_greek_percentage(self, text: str) -> float:
        """
        Calculate percentage of Greek characters in text (from artifacts)
        """
        if not text:
            return 0.0
        
        total_chars = len(text)
        greek_chars = sum(1 for c in text if 
                         '\u0370' <= c <= '\u03FF' or 
                         '\u1F00' <= c <= '\u1FFF')
        
        return (greek_chars / total_chars) * 100.0


if __name__ == "__main__":
    parser = EnhancedParser()
    
    # Test with Ancient Greek
    sample_grc = "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος"
    result = parser.parse_sentence(sample_grc, 'grc', 'ancient')
    
    print("\n=== Parse Result ===")
    print(f"Tokens: {len(result['tokens'])}")
    print(f"Dependencies: {len(result['dependencies'])}")
    print(f"Syntax notes: {result['syntax_notes']}")
    print("\nCONLL-U:")
    print(result['conllu'])
