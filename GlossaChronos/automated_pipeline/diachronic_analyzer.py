"""
DIACHRONIC SEMANTIC ANALYZER
Integrated from temporal_semantic_analyzer.py (10.9KB)
Track lexical semantic change across time periods
Detect meaning shifts, VAD changes, diachronic patterns
Chronoberg-inspired methodology
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime
import json
from collections import defaultdict, Counter
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiachronicAnalyzer:
    """
    Analyze semantic shifts across diachronic corpus
    Track meaning changes over time periods
    """
    
    def __init__(self, db_path: str = "Z:/GlossaChronos/automated_pipeline/texts.db"):
        self.db_path = db_path
        
        # Known semantic shifts (from historical linguistics research)
        self.known_shifts = {
            'gay': {
                'period1': {'meaning': 'happy, carefree', 'period': 'medieval', 'year': 1300},
                'period2': {'meaning': 'homosexual', 'period': 'modern', 'year': 1900},
                'shift_type': 'narrowing',
                'shift_date': 1900
            },
            'awful': {
                'period1': {'meaning': 'full of awe, impressive', 'period': 'early_modern', 'year': 1600},
                'period2': {'meaning': 'terrible, very bad', 'period': 'modern', 'year': 1800},
                'shift_type': 'pejoration',
                'shift_date': 1800
            },
            'nice': {
                'period1': {'meaning': 'foolish, ignorant', 'period': 'medieval', 'year': 1300},
                'period2': {'meaning': 'pleasant, agreeable', 'period': 'modern', 'year': 1700},
                'shift_type': 'amelioration',
                'shift_date': 1700
            },
            'silly': {
                'period1': {'meaning': 'blessed, innocent', 'period': 'old', 'year': 1000},
                'period2': {'meaning': 'foolish', 'period': 'modern', 'year': 1600},
                'shift_type': 'pejoration',
                'shift_date': 1600
            }
        }
        
        # Period mappings
        self.period_years = {
            'ancient': (-800, 600),
            'classical': (-100, 200),
            'medieval': (500, 1500),
            'old': (450, 1150),
            'middle': (1150, 1500),
            'early_modern': (1500, 1700),
            'modern': (1700, 2024)
        }
        
        # Shift types
        self.shift_types = [
            'narrowing',      # Meaning becomes more specific
            'broadening',     # Meaning becomes more general
            'amelioration',   # Meaning improves (positive)
            'pejoration',     # Meaning worsens (negative)
            'metaphor',       # Metaphorical extension
            'metonymy'        # Associated meaning transfer
        ]
        
        self.stats = {
            'texts_analyzed': 0,
            'shifts_detected': 0,
            'by_type': Counter(),
            'by_period': defaultdict(list)
        }
        
        self._init_database()
        
        logger.info("="*80)
        logger.info("DIACHRONIC SEMANTIC ANALYZER")
        logger.info("="*80)
    
    def _init_database(self):
        """Initialize database for semantic shifts"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS semantic_shifts (
                id INTEGER PRIMARY KEY,
                word TEXT,
                language TEXT,
                period1 TEXT,
                period2 TEXT,
                meaning1 TEXT,
                meaning2 TEXT,
                shift_type TEXT,
                shift_date INTEGER,
                confidence REAL,
                examples TEXT,
                detected_at TEXT
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS word_usage (
                id INTEGER PRIMARY KEY,
                word TEXT,
                language TEXT,
                period TEXT,
                context TEXT,
                frequency INTEGER,
                text_id INTEGER,
                FOREIGN KEY (text_id) REFERENCES collected_texts(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def analyze_text_for_shifts(self, text: str, language: str, 
                                period: str, text_id: Optional[int] = None) -> List[Dict]:
        """
        Analyze text for semantic shifts
        Compare word usage against known patterns
        """
        logger.info(f"\n[DIACHRONIC] Analyzing {language}/{period} text for semantic shifts...")
        
        detected_shifts = []
        
        # Tokenize (simple word split)
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = Counter(words)
        
        # Check for known shifts
        for word, shift_info in self.known_shifts.items():
            if word in word_freq:
                # Check if this period matches a shift period
                period_year = self._get_period_midpoint(period)
                shift_year = shift_info['shift_date']
                
                # Determine which meaning applies
                if period_year < shift_year:
                    current_meaning = shift_info['period1']['meaning']
                    context = "pre-shift"
                else:
                    current_meaning = shift_info['period2']['meaning']
                    context = "post-shift"
                
                # Extract examples
                examples = self._extract_word_contexts(word, text)
                
                shift_data = {
                    'word': word,
                    'language': language,
                    'period': period,
                    'frequency': word_freq[word],
                    'expected_meaning': current_meaning,
                    'shift_type': shift_info['shift_type'],
                    'shift_date': shift_year,
                    'context': context,
                    'examples': examples[:3],  # Top 3 examples
                    'confidence': self._calculate_confidence(word_freq[word], len(examples))
                }
                
                detected_shifts.append(shift_data)
                
                # Save to database
                self._save_shift(shift_data, text_id)
                
                logger.info(f"  ✓ Detected shift: '{word}' ({shift_info['shift_type']})")
        
        # Save word usage
        for word, freq in word_freq.most_common(50):  # Top 50 words
            if len(word) > 3:  # Ignore very short words
                self._save_word_usage(word, language, period, text, freq, text_id)
        
        self.stats['texts_analyzed'] += 1
        self.stats['shifts_detected'] += len(detected_shifts)
        
        return detected_shifts
    
    def compare_periods(self, word: str, language: str, 
                       period1: str, period2: str) -> Dict:
        """
        Compare word usage across two time periods
        Detect if meaning has shifted
        """
        logger.info(f"\n[COMPARISON] Comparing '{word}' between {period1} and {period2}...")
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # Get usage in period 1
        usage1 = cur.execute('''
            SELECT context, frequency
            FROM word_usage
            WHERE word = ? AND language = ? AND period = ?
            ORDER BY frequency DESC
            LIMIT 10
        ''', (word, language, period1)).fetchall()
        
        # Get usage in period 2
        usage2 = cur.execute('''
            SELECT context, frequency
            FROM word_usage
            WHERE word = ? AND language = ? AND period = ?
            ORDER BY frequency DESC
            LIMIT 10
        ''', (word, language, period2)).fetchall()
        
        conn.close()
        
        # Analyze differences
        total_freq1 = sum(f for _, f in usage1)
        total_freq2 = sum(f for _, f in usage2)
        
        # Calculate frequency change
        freq_change = ((total_freq2 - total_freq1) / total_freq1 * 100) if total_freq1 > 0 else 0
        
        # Detect shift type (simplified)
        shift_type = 'stable'
        if abs(freq_change) > 50:
            shift_type = 'frequency_shift'
        
        result = {
            'word': word,
            'language': language,
            'period1': period1,
            'period2': period2,
            'frequency1': total_freq1,
            'frequency2': total_freq2,
            'frequency_change': freq_change,
            'shift_type': shift_type,
            'examples1': [ctx[:100] for ctx, _ in usage1[:3]],
            'examples2': [ctx[:100] for ctx, _ in usage2[:3]]
        }
        
        logger.info(f"  Frequency change: {freq_change:+.1f}%")
        logger.info(f"  Shift type: {shift_type}")
        
        return result
    
    def detect_novel_shifts(self, language: str, min_frequency: int = 5) -> List[Dict]:
        """
        Detect potential new semantic shifts not in known list
        Uses frequency and context analysis
        """
        logger.info(f"\n[NOVEL SHIFTS] Detecting new shifts for {language}...")
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # Get words appearing in multiple periods
        multi_period_words = cur.execute('''
            SELECT word, COUNT(DISTINCT period) as period_count
            FROM word_usage
            WHERE language = ? AND frequency >= ?
            GROUP BY word
            HAVING period_count >= 2
        ''', (language, min_frequency)).fetchall()
        
        conn.close()
        
        potential_shifts = []
        
        for word, period_count in multi_period_words[:20]:  # Analyze top 20
            # Get all periods for this word
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            periods = cur.execute('''
                SELECT DISTINCT period, SUM(frequency) as total_freq
                FROM word_usage
                WHERE word = ? AND language = ?
                GROUP BY period
                ORDER BY period
            ''', (word, language)).fetchall()
            
            conn.close()
            
            if len(periods) >= 2:
                # Compare first and last period
                period1, freq1 = periods[0]
                period2, freq2 = periods[-1]
                
                freq_ratio = freq2 / freq1 if freq1 > 0 else 1.0
                
                # Significant change detected
                if freq_ratio > 2.0 or freq_ratio < 0.5:
                    potential_shifts.append({
                        'word': word,
                        'language': language,
                        'periods': [p for p, _ in periods],
                        'frequency_ratio': freq_ratio,
                        'confidence': min(freq_ratio / 5.0, 1.0),
                        'type': 'frequency_shift'
                    })
                    
                    logger.info(f"  ✓ Potential shift: '{word}' (ratio: {freq_ratio:.2f})")
        
        logger.info(f"  Found {len(potential_shifts)} potential novel shifts")
        
        return potential_shifts
    
    def generate_shift_report(self, language: str) -> str:
        """Generate comprehensive shift analysis report"""
        logger.info(f"\n[REPORT] Generating shift report for {language}...")
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # Get all shifts
        shifts = cur.execute('''
            SELECT word, period1, period2, shift_type, confidence
            FROM semantic_shifts
            WHERE language = ?
            ORDER BY confidence DESC
        ''', (language,)).fetchall()
        
        conn.close()
        
        report = []
        report.append("="*80)
        report.append(f"DIACHRONIC SEMANTIC SHIFT REPORT: {language.upper()}")
        report.append("="*80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total shifts detected: {len(shifts)}")
        report.append("")
        
        # Group by shift type
        by_type = defaultdict(list)
        for word, p1, p2, stype, conf in shifts:
            by_type[stype].append((word, p1, p2, conf))
        
        for shift_type in self.shift_types:
            if shift_type in by_type:
                report.append(f"\n{shift_type.upper()}")
                report.append("-"*80)
                for word, p1, p2, conf in by_type[shift_type][:10]:
                    report.append(f"  {word:20s} {p1:15s} → {p2:15s} (confidence: {conf:.2f})")
        
        report.append("\n" + "="*80)
        
        return '\n'.join(report)
    
    def _get_period_midpoint(self, period: str) -> int:
        """Get midpoint year for period"""
        if period in self.period_years:
            start, end = self.period_years[period]
            return (start + end) // 2
        return 1500  # Default
    
    def _extract_word_contexts(self, word: str, text: str, 
                              context_window: int = 50) -> List[str]:
        """Extract contexts where word appears"""
        contexts = []
        text_lower = text.lower()
        word_lower = word.lower()
        
        start = 0
        while True:
            pos = text_lower.find(word_lower, start)
            if pos == -1:
                break
            
            # Extract context window
            ctx_start = max(0, pos - context_window)
            ctx_end = min(len(text), pos + len(word) + context_window)
            context = text[ctx_start:ctx_end]
            
            contexts.append(context)
            start = pos + len(word)
        
        return contexts
    
    def _calculate_confidence(self, frequency: int, example_count: int) -> float:
        """Calculate confidence score for shift detection"""
        # More frequent = higher confidence
        freq_score = min(frequency / 10.0, 1.0)
        # More examples = higher confidence
        example_score = min(example_count / 5.0, 1.0)
        return (freq_score + example_score) / 2.0
    
    def _save_shift(self, shift_data: Dict, text_id: Optional[int]):
        """Save detected shift to database"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute('''
            INSERT INTO semantic_shifts
            (word, language, period1, period2, meaning1, meaning2, 
             shift_type, shift_date, confidence, examples, detected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            shift_data['word'],
            shift_data['language'],
            shift_data['period'],
            'compared_period',
            shift_data['expected_meaning'],
            '',
            shift_data['shift_type'],
            shift_data['shift_date'],
            shift_data['confidence'],
            json.dumps(shift_data['examples']),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def _save_word_usage(self, word: str, language: str, period: str,
                        context: str, frequency: int, text_id: Optional[int]):
        """Save word usage data"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # Get sample context
        sample_context = context[:200] if context else ''
        
        cur.execute('''
            INSERT INTO word_usage
            (word, language, period, context, frequency, text_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (word, language, period, sample_context, frequency, text_id))
        
        conn.commit()
        conn.close()
    
    def print_stats(self):
        """Print analysis statistics"""
        print("\n" + "="*80)
        print("DIACHRONIC ANALYSIS STATISTICS")
        print("="*80)
        print(f"Texts analyzed: {self.stats['texts_analyzed']}")
        print(f"Shifts detected: {self.stats['shifts_detected']}")
        
        if self.stats['by_type']:
            print("\nBy shift type:")
            for stype, count in self.stats['by_type'].most_common():
                print(f"  {stype}: {count}")
        
        print("="*80 + "\n")


if __name__ == "__main__":
    analyzer = DiachronicAnalyzer()
    
    # Test with sample text
    sample = """The gay company was full of silly people having an awful time. 
    They were nice to each other despite their foolish behavior."""
    
    shifts = analyzer.analyze_text_for_shifts(
        text=sample,
        language='en',
        period='early_modern'
    )
    
    print("\n=== Detected Shifts ===")
    for shift in shifts:
        print(f"Word: {shift['word']}")
        print(f"Type: {shift['shift_type']}")
        print(f"Meaning: {shift['expected_meaning']}")
        print(f"Confidence: {shift['confidence']:.2f}")
        print()
    
    analyzer.print_stats()
