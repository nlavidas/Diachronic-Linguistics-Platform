"""
Valency Pattern Extraction Module
Real implementation for automatic valency analysis
"""

import logging
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, Counter
import json
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValencyExtractor:
    """Extract valency patterns from parsed texts"""
    
    def __init__(self):
        self.patterns = defaultdict(list)
        self.statistics = defaultdict(Counter)
        
    def extract_from_parsed(self, parsed_data: List[Dict]) -> List[Dict]:
        """Extract valency patterns from parsed sentences"""
        logger.info("Extracting valency patterns...")
        
        all_patterns = []
        
        for sentence in parsed_data:
            sent_patterns = self._extract_from_sentence(sentence)
            all_patterns.extend(sent_patterns)
        
        logger.info(f"Extracted {len(all_patterns)} valency patterns")
        return all_patterns
    
    def _extract_from_sentence(self, sentence: Dict) -> List[Dict]:
        """Extract patterns from single sentence"""
        patterns = []
        tokens = sentence.get('tokens', [])
        
        # Build token lookup
        token_dict = {t['id']: t for t in tokens}
        
        # Find all verbs
        for token in tokens:
            if token['upos'] in ['VERB', 'AUX']:
                pattern = self._analyze_verb(token, tokens, token_dict)
                if pattern:
                    patterns.append(pattern)
        
        return patterns
    
    def _analyze_verb(self, verb: Dict, tokens: List[Dict], token_dict: Dict) -> Optional[Dict]:
        """Analyze valency pattern of a verb"""
        
        # Find dependents
        dependents = [t for t in tokens if t['head'] == verb['id']]
        
        # Classify arguments
        arguments = []
        for dep in dependents:
            if dep['deprel'] in ['nsubj', 'obj', 'iobj', 'obl', 'ccomp', 'xcomp']:
                arg = {
                    'role': dep['deprel'],
                    'form': dep['form'],
                    'lemma': dep['lemma'],
                    'upos': dep['upos'],
                    'case': self._extract_case(dep),
                    'obligatory': self._is_obligatory(dep['deprel'])
                }
                arguments.append(arg)
        
        # Determine valency type
        valency_type = self._classify_valency(arguments)
        
        # Create case frame
        case_frame = self._create_case_frame(arguments)
        
        pattern = {
            'verb_form': verb['form'],
            'verb_lemma': verb['lemma'],
            'verb_id': verb['id'],
            'arguments': arguments,
            'argument_count': len(arguments),
            'valency_type': valency_type,
            'case_frame': case_frame,
            'tense': self._extract_tense(verb),
            'voice': self._extract_voice(verb),
            'mood': self._extract_mood(verb)
        }
        
        return pattern
    
    def _classify_valency(self, arguments: List[Dict]) -> str:
        """Classify valency pattern type"""
        arg_count = len(arguments)
        
        if arg_count == 0:
            return 'AVALENT'
        elif arg_count == 1:
            if arguments[0]['role'] == 'nsubj':
                return 'MONOVALENT_INTRANSITIVE'
            else:
                return 'MONOVALENT'
        elif arg_count == 2:
            roles = set(arg['role'] for arg in arguments)
            if 'nsubj' in roles and 'obj' in roles:
                return 'BIVALENT_TRANSITIVE'
            else:
                return 'BIVALENT'
        elif arg_count == 3:
            roles = set(arg['role'] for arg in arguments)
            if 'nsubj' in roles and 'obj' in roles and 'iobj' in roles:
                return 'TRIVALENT_DITRANSITIVE'
            else:
                return 'TRIVALENT'
        else:
            return 'POLYVALENT'
    
    def _create_case_frame(self, arguments: List[Dict]) -> str:
        """Create case frame representation"""
        if not arguments:
            return '∅'
        
        frame_parts = []
        for arg in sorted(arguments, key=lambda x: x['role']):
            case = arg.get('case', 'None')
            frame_parts.append(f"{arg['role']}[{case}]")
        
        return ' + '.join(frame_parts)
    
    def _extract_case(self, token: Dict) -> Optional[str]:
        """Extract grammatical case from token"""
        feats = token.get('feats', '_')
        if feats and feats != '_':
            for feat in feats.split('|'):
                if feat.startswith('Case='):
                    return feat.split('=')[1]
        return None
    
    def _extract_tense(self, verb: Dict) -> Optional[str]:
        """Extract tense from verb"""
        feats = verb.get('feats', '_')
        if feats and feats != '_':
            for feat in feats.split('|'):
                if feat.startswith('Tense='):
                    return feat.split('=')[1]
        return None
    
    def _extract_voice(self, verb: Dict) -> Optional[str]:
        """Extract voice from verb"""
        feats = verb.get('feats', '_')
        if feats and feats != '_':
            for feat in feats.split('|'):
                if feat.startswith('Voice='):
                    return feat.split('=')[1]
        return None
    
    def _extract_mood(self, verb: Dict) -> Optional[str]:
        """Extract mood from verb"""
        feats = verb.get('feats', '_')
        if feats and feats != '_':
            for feat in feats.split('|'):
                if feat.startswith('Mood='):
                    return feat.split('=')[1]
        return None
    
    def _is_obligatory(self, deprel: str) -> bool:
        """Determine if argument is obligatory"""
        obligatory = ['nsubj', 'obj', 'ccomp', 'xcomp']
        return deprel in obligatory
    
    def analyze_patterns(self, patterns: List[Dict]) -> Dict:
        """Analyze extracted patterns for statistics"""
        logger.info("Analyzing valency patterns...")
        
        stats = {
            'total_patterns': len(patterns),
            'unique_verbs': len(set(p['verb_lemma'] for p in patterns)),
            'valency_distribution': Counter(p['valency_type'] for p in patterns),
            'case_frames': Counter(p['case_frame'] for p in patterns),
            'verb_frequencies': Counter(p['verb_lemma'] for p in patterns),
            'average_arguments': sum(p['argument_count'] for p in patterns) / len(patterns) if patterns else 0
        }
        
        # Top patterns by verb
        verb_patterns = defaultdict(list)
        for pattern in patterns:
            verb_patterns[pattern['verb_lemma']].append(pattern)
        
        stats['verb_pattern_details'] = {}
        for verb, verb_pats in verb_patterns.items():
            stats['verb_pattern_details'][verb] = {
                'frequency': len(verb_pats),
                'case_frames': list(Counter(p['case_frame'] for p in verb_pats).items()),
                'valency_types': list(Counter(p['valency_type'] for p in verb_pats).items())
            }
        
        return stats
    
    def export_patterns(self, patterns: List[Dict], output_file: Path):
        """Export patterns to JSON"""
        logger.info(f"Exporting patterns to {output_file}")
        
        output_data = {
            'extracted_date': datetime.now().isoformat(),
            'total_patterns': len(patterns),
            'patterns': patterns,
            'statistics': self.analyze_patterns(patterns)
        }
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logger.info("Export complete")
    
    def create_pattern_database(self, patterns: List[Dict]) -> Dict[str, List[Dict]]:
        """Create searchable pattern database"""
        logger.info("Creating pattern database...")
        
        database = {
            'by_verb': defaultdict(list),
            'by_valency': defaultdict(list),
            'by_case_frame': defaultdict(list)
        }
        
        for pattern in patterns:
            database['by_verb'][pattern['verb_lemma']].append(pattern)
            database['by_valency'][pattern['valency_type']].append(pattern)
            database['by_case_frame'][pattern['case_frame']].append(pattern)
        
        # Convert defaultdicts to regular dicts
        return {
            'by_verb': dict(database['by_verb']),
            'by_valency': dict(database['by_valency']),
            'by_case_frame': dict(database['by_case_frame'])
        }
    
    def generate_report(self, patterns: List[Dict], output_file: Path):
        """Generate human-readable report"""
        logger.info("Generating valency report...")
        
        stats = self.analyze_patterns(patterns)
        
        report = []
        report.append("=" * 60)
        report.append("VALENCY PATTERN ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("SUMMARY")
        report.append("-" * 60)
        report.append(f"Total patterns extracted: {stats['total_patterns']}")
        report.append(f"Unique verbs: {stats['unique_verbs']}")
        report.append(f"Average arguments per verb: {stats['average_arguments']:.2f}")
        report.append("")
        
        report.append("VALENCY TYPE DISTRIBUTION")
        report.append("-" * 60)
        for vtype, count in stats['valency_distribution'].most_common():
            percentage = (count / stats['total_patterns']) * 100
            report.append(f"{vtype:30s}: {count:5d} ({percentage:5.1f}%)")
        report.append("")
        
        report.append("TOP 20 CASE FRAMES")
        report.append("-" * 60)
        for frame, count in list(stats['case_frames'].most_common(20)):
            report.append(f"{frame:40s}: {count:5d}")
        report.append("")
        
        report.append("TOP 20 MOST FREQUENT VERBS")
        report.append("-" * 60)
        for verb, count in list(stats['verb_frequencies'].most_common(20)):
            report.append(f"{verb:30s}: {count:5d} occurrences")
        report.append("")
        
        report.append("=" * 60)
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        logger.info(f"Report saved to {output_file}")


if __name__ == "__main__":
    # Test with sample parsed data
    sample_parsed = [{
        'id': 1,
        'text': 'Sample sentence',
        'tokens': [
            {'id': 1, 'form': 'ἄειδε', 'lemma': 'ἀείδω', 'upos': 'VERB', 
             'feats': 'Tense=Pres|Voice=Act', 'head': 0, 'deprel': 'root'},
            {'id': 2, 'form': 'θεὰ', 'lemma': 'θεά', 'upos': 'NOUN',
             'feats': 'Case=Nom', 'head': 1, 'deprel': 'nsubj'},
            {'id': 3, 'form': 'μῆνιν', 'lemma': 'μῆνις', 'upos': 'NOUN',
             'feats': 'Case=Acc', 'head': 1, 'deprel': 'obj'}
        ]
    }]
    
    extractor = ValencyExtractor()
    patterns = extractor.extract_from_parsed(sample_parsed)
    
    print("\n=== Valency Extraction Test ===")
    for pattern in patterns:
        print(f"Verb: {pattern['verb_lemma']}")
        print(f"Type: {pattern['valency_type']}")
        print(f"Frame: {pattern['case_frame']}")
        print(f"Arguments: {len(pattern['arguments'])}")
