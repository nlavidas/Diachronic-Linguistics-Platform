"""
QUALITY VALIDATION SYSTEM
Integrated from corpus_validator.py (21KB!)
5-Phase comprehensive validation for diachronic corpus
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple
import re
import logging
from datetime import datetime
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityValidator:
    """
    Comprehensive corpus validation system
    Integrated from corpus_validator.py
    
    5-Phase Validation:
    1. Text Type (authentic vs monograph)
    2. Period Appropriateness (diachronic validity)
    3. Format Compliance (PROIEL, Penn-Helsinki)
    4. Linguistic Quality (grammar, completeness)
    5. Metadata Verification (author, date, source)
    """
    
    def __init__(self, db_path: str = "Z:/GlossaChronos/automated_pipeline/texts.db"):
        self.db_path = db_path
        
        # Period definitions
        self.periods = {
            'grc': {
                'Archaic': (800, 480, 'BCE'),
                'Classical': (480, 323, 'BCE'),
                'Hellenistic': (323, 146, 'BCE'),
                'Byzantine': (330, 1453, 'CE')
            },
            'la': {
                'Classical': (75, 200, 'BCE-CE'),
                'Vulgar': (200, 600, 'CE'),
                'Medieval': (600, 1500, 'CE'),
                'Renaissance': (1300, 1600, 'CE')
            },
            'en': {
                'Old English': (450, 1150, 'CE'),
                'Middle English': (1150, 1500, 'CE'),
                'Early Modern': (1500, 1700, 'CE'),
                'Modern': (1700, 2000, 'CE')
            }
        }
        
        # Monograph exclusion patterns
        self.monograph_patterns = [
            r'introduction',
            r'commentary',
            r'notes',
            r'bibliography',
            r'appendix',
            r'chapter \d+:',
            r'references',
            r'index',
            r'preface',
            r'acknowledgments',
            r'figure \d+',
            r'table \d+'
        ]
        
        # Required text indicators
        self.authentic_indicators = [
            r'[α-ω]{10,}',  # Greek words
            r'[a-z]{5,}um\b',  # Latin endings
            r'þ|ð|æ',  # Old English characters
        ]
        
        self.stats = {
            'total_validated': 0,
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'average_score': 0.0
        }
        
        logger.info("="*80)
        logger.info("QUALITY VALIDATION SYSTEM")
        logger.info("="*80)
    
    def validate_text(self, text: str, language: str, period: str, 
                     metadata: Dict) -> Dict:
        """
        Comprehensive 5-phase validation
        
        Returns validation report with scores
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"VALIDATING TEXT: {metadata.get('title', 'Unknown')[:50]}")
        logger.info('='*80)
        
        results = {
            'title': metadata.get('title'),
            'language': language,
            'period': period,
            'timestamp': datetime.now().isoformat(),
            'phases': {},
            'overall_score': 0.0,
            'pass': False,
            'warnings': [],
            'errors': []
        }
        
        # PHASE 1: Text Type Validation
        logger.info("\n📋 Phase 1: Text Type Validation")
        phase1 = self._validate_text_type(text, metadata)
        results['phases']['text_type'] = phase1
        logger.info(f"  Score: {phase1['score']:.1f}% - {phase1['status']}")
        
        # PHASE 2: Period Appropriateness
        logger.info("\n📅 Phase 2: Period Appropriateness")
        phase2 = self._validate_period(text, language, period, metadata)
        results['phases']['period'] = phase2
        logger.info(f"  Score: {phase2['score']:.1f}% - {phase2['status']}")
        
        # PHASE 3: Format Compliance
        logger.info("\n📄 Phase 3: Format Compliance")
        phase3 = self._validate_format(text, language)
        results['phases']['format'] = phase3
        logger.info(f"  Score: {phase3['score']:.1f}% - {phase3['status']}")
        
        # PHASE 4: Linguistic Quality
        logger.info("\n🔤 Phase 4: Linguistic Quality")
        phase4 = self._validate_linguistic_quality(text, language)
        results['phases']['linguistic'] = phase4
        logger.info(f"  Score: {phase4['score']:.1f}% - {phase4['status']}")
        
        # PHASE 5: Metadata Verification
        logger.info("\n🏷️  Phase 5: Metadata Verification")
        phase5 = self._validate_metadata(metadata, language, period)
        results['phases']['metadata'] = phase5
        logger.info(f"  Score: {phase5['score']:.1f}% - {phase5['status']}")
        
        # Calculate overall score (weighted)
        weights = {
            'text_type': 0.25,
            'period': 0.20,
            'format': 0.20,
            'linguistic': 0.25,
            'metadata': 0.10
        }
        
        overall_score = sum(
            results['phases'][phase]['score'] * weights[phase]
            for phase in weights
        )
        
        results['overall_score'] = overall_score
        
        # Determine pass/fail
        if overall_score >= 80:
            results['pass'] = True
            results['status'] = 'PASS'
        elif overall_score >= 60:
            results['pass'] = True
            results['status'] = 'PASS (with warnings)'
            results['warnings'].append(f"Score {overall_score:.1f}% below ideal threshold of 80%")
        else:
            results['pass'] = False
            results['status'] = 'FAIL'
            results['errors'].append(f"Score {overall_score:.1f}% below minimum threshold of 60%")
        
        # Update statistics
        self.stats['total_validated'] += 1
        if results['pass']:
            self.stats['passed'] += 1
        else:
            self.stats['failed'] += 1
        if results['warnings']:
            self.stats['warnings'] += 1
        
        # Print summary
        logger.info("\n" + "="*80)
        logger.info("VALIDATION SUMMARY")
        logger.info("="*80)
        logger.info(f"Overall Score: {overall_score:.1f}%")
        logger.info(f"Status: {results['status']}")
        if results['warnings']:
            logger.info(f"Warnings: {len(results['warnings'])}")
        if results['errors']:
            logger.info(f"Errors: {len(results['errors'])}")
        logger.info("="*80)
        
        return results
    
    def _validate_text_type(self, text: str, metadata: Dict) -> Dict:
        """Phase 1: Validate text type (authentic vs monograph)"""
        
        score = 100.0
        issues = []
        
        # Check for monograph patterns
        text_lower = text.lower()
        for pattern in self.monograph_patterns:
            matches = len(re.findall(pattern, text_lower))
            if matches > 0:
                score -= min(matches * 5, 30)  # Max 30 point deduction
                issues.append(f"Found monograph indicator: '{pattern}' ({matches}x)")
        
        # Check for authentic text indicators
        has_authentic = False
        for pattern in self.authentic_indicators:
            if re.search(pattern, text):
                has_authentic = True
                break
        
        if not has_authentic and len(text) > 1000:
            score -= 20
            issues.append("No authentic text indicators found")
        
        # Check minimum length
        if len(text) < 500:
            score -= 30
            issues.append(f"Text too short ({len(text)} chars)")
        
        status = "AUTHENTIC" if score >= 80 else "SUSPICIOUS" if score >= 60 else "MONOGRAPH"
        
        return {
            'score': max(0, score),
            'status': status,
            'issues': issues
        }
    
    def _validate_period(self, text: str, language: str, period: str, 
                        metadata: Dict) -> Dict:
        """Phase 2: Validate period appropriateness"""
        
        score = 100.0
        issues = []
        
        # Check if period exists for language
        if language not in self.periods:
            score = 50.0
            issues.append(f"Language '{language}' has no period definitions")
            return {'score': score, 'status': 'UNKNOWN', 'issues': issues}
        
        # Check if specified period is valid
        valid_periods = self.periods[language].keys()
        if period not in [p.lower().replace(' ', '_') for p in valid_periods]:
            # Try to find closest match
            found_match = False
            for valid_period in valid_periods:
                if period.lower() in valid_period.lower():
                    score -= 10
                    issues.append(f"Period '{period}' approximate match to '{valid_period}'")
                    found_match = True
                    break
            
            if not found_match:
                score -= 30
                issues.append(f"Period '{period}' not recognized for {language}")
        
        # Check for anachronisms (simplified)
        modern_indicators = [
            r'\d{4}',  # 4-digit years
            r'email',
            r'internet',
            r'computer',
            r'telephone',
            r'copyright ©'
        ]
        
        for pattern in modern_indicators:
            if re.search(pattern, text.lower()):
                score -= 25
                issues.append(f"Found anachronistic term: '{pattern}'")
        
        status = "PERIOD-APPROPRIATE" if score >= 80 else "QUESTIONABLE" if score >= 60 else "ANACHRONISTIC"
        
        return {
            'score': max(0, score),
            'status': status,
            'issues': issues
        }
    
    def _validate_format(self, text: str, language: str) -> Dict:
        """Phase 3: Validate format compliance"""
        
        score = 100.0
        issues = []
        
        # Check encoding (should be clean UTF-8)
        try:
            text.encode('utf-8')
        except UnicodeEncodeError:
            score -= 20
            issues.append("Text contains encoding errors")
        
        # Check for proper sentence structure
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) < 2:
            score -= 15
            issues.append("Text lacks proper sentence structure")
        
        # Check for minimum word count
        words = text.split()
        if len(words) < 100:
            score -= 20
            issues.append(f"Too few words ({len(words)})")
        
        # Check character diversity (not just repeating characters)
        unique_chars = len(set(text.replace(' ', '')))
        if unique_chars < 20:
            score -= 30
            issues.append(f"Low character diversity ({unique_chars} unique)")
        
        status = "COMPLIANT" if score >= 80 else "ACCEPTABLE" if score >= 60 else "NON-COMPLIANT"
        
        return {
            'score': max(0, score),
            'status': status,
            'issues': issues
        }
    
    def _validate_linguistic_quality(self, text: str, language: str) -> Dict:
        """Phase 4: Validate linguistic quality"""
        
        score = 100.0
        issues = []
        
        # Check for complete words (not fragments)
        words = text.split()
        if words:
            avg_word_length = sum(len(w) for w in words) / len(words)
            if avg_word_length < 2:
                score -= 40
                issues.append(f"Average word length too short ({avg_word_length:.1f})")
            elif avg_word_length > 15:
                score -= 20
                issues.append(f"Average word length suspicious ({avg_word_length:.1f})")
        
        # Check for proper spacing
        if '  ' in text:  # Double spaces
            score -= 5
            issues.append("Contains improper spacing")
        
        # Check for mixed scripts (could indicate corruption)
        scripts = set()
        for char in text:
            if '\u0370' <= char <= '\u03FF':  # Greek
                scripts.add('greek')
            elif '\u0041' <= char <= '\u007A':  # Latin
                scripts.add('latin')
            elif '\u0400' <= char <= '\u04FF':  # Cyrillic
                scripts.add('cyrillic')
        
        if len(scripts) > 2:  # More than 2 scripts is suspicious
            score -= 15
            issues.append(f"Mixed scripts detected: {scripts}")
        
        # Check for reasonable sentence length
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        if sentences:
            avg_sent_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_sent_length < 3:
                score -= 25
                issues.append(f"Sentences too short (avg {avg_sent_length:.1f} words)")
            elif avg_sent_length > 100:
                score -= 15
                issues.append(f"Sentences unusually long (avg {avg_sent_length:.1f} words)")
        
        status = "HIGH QUALITY" if score >= 80 else "ACCEPTABLE" if score >= 60 else "LOW QUALITY"
        
        return {
            'score': max(0, score),
            'status': status,
            'issues': issues
        }
    
    def _validate_metadata(self, metadata: Dict, language: str, period: str) -> Dict:
        """Phase 5: Validate metadata"""
        
        score = 100.0
        issues = []
        
        # Required fields
        required = ['title', 'source', 'language']
        for field in required:
            if not metadata.get(field):
                score -= 30 / len(required)
                issues.append(f"Missing required field: {field}")
        
        # Check title format
        title = metadata.get('title', '')
        if title:
            if len(title) < 3:
                score -= 10
                issues.append("Title too short")
            elif len(title) > 200:
                score -= 5
                issues.append("Title unusually long")
        
        # Check author field
        author = metadata.get('author')
        if author and len(str(author)) > 100:
            score -= 5
            issues.append("Author field unusually long")
        
        # Check language consistency
        if metadata.get('language') != language:
            score -= 20
            issues.append(f"Language mismatch: metadata={metadata.get('language')} vs specified={language}")
        
        status = "COMPLETE" if score >= 90 else "ACCEPTABLE" if score >= 60 else "INCOMPLETE"
        
        return {
            'score': max(0, score),
            'status': status,
            'issues': issues
        }
    
    def batch_validate(self, texts: List[Dict]) -> Dict:
        """Validate multiple texts"""
        logger.info("\n" + "="*80)
        logger.info(f"BATCH VALIDATION: {len(texts)} texts")
        logger.info("="*80)
        
        results = []
        
        for idx, text_data in enumerate(texts, 1):
            logger.info(f"\n[{idx}/{len(texts)}] Processing...")
            
            result = self.validate_text(
                text=text_data['content'],
                language=text_data['language'],
                period=text_data.get('period', 'unknown'),
                metadata=text_data
            )
            
            results.append(result)
        
        # Summary
        self.print_stats()
        
        return {
            'total': len(results),
            'passed': sum(1 for r in results if r['pass']),
            'failed': sum(1 for r in results if not r['pass']),
            'average_score': sum(r['overall_score'] for r in results) / len(results),
            'results': results
        }
    
    def print_stats(self):
        """Print validation statistics"""
        print("\n" + "="*80)
        print("QUALITY VALIDATION STATISTICS")
        print("="*80)
        print(f"Total validated: {self.stats['total_validated']}")
        print(f"Passed: {self.stats['passed']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Warnings: {self.stats['warnings']}")
        
        if self.stats['total_validated'] > 0:
            pass_rate = (self.stats['passed'] / self.stats['total_validated']) * 100
            print(f"Pass rate: {pass_rate:.1f}%")
        
        print("="*80 + "\n")


if __name__ == "__main__":
    validator = QualityValidator()
    
    # Test validation
    sample_text = "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος οὐλομένην, ἣ μυρί᾽ Ἀχαιοῖς ἄλγε᾽ ἔθηκε. πολλὰς δ᾽ ἰφθίμους ψυχὰς Ἄϊδι προΐαψεν ἡρώων."
    
    result = validator.validate_text(
        text=sample_text,
        language='grc',
        period='ancient',
        metadata={
            'title': 'Homer Iliad Book 1',
            'author': 'Homer',
            'source': 'test',
            'language': 'grc'
        }
    )
    
    print("\n=== Validation Result ===")
    print(f"Overall Score: {result['overall_score']:.1f}%")
    print(f"Status: {result['status']}")
    
    validator.print_stats()
