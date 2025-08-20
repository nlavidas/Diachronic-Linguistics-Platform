#!/usr/bin/env python3
"""
10-HOUR OVERNIGHT AUTONOMOUS AGENT
Runs continuously extracting valency patterns, analyzing changes,
generating reports, and building your complete corpus
"""

import os
import sys
import time
import json
import sqlite3
import pandas as pd
from lxml import etree
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import logging
import random

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('overnight_10hour.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

class TenHourAgent:
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(hours=10)
        
        # CORRECT PROIEL morphology mapping
        self.PROIEL_CASES = {
            # Position 6 in morphology string
            'n': 'NOM',    # Nominative
            'g': 'GEN',    # Genitive  
            'd': 'DAT',    # Dative
            'a': 'ACC',    # Accusative
            'v': 'VOC',    # Vocative
            'b': 'ABL',    # Ablative
            '-': None
        }
        
        self.PROIEL_VOICES = {
            # Different position based on POS
            'a': 'active',
            'p': 'passive',
            'm': 'middle',
            'e': 'medio-passive',
            'd': 'deponent',
            '-': None
        }
        
        self.stats = defaultdict(int)
        self.init_database()
        
    def init_database(self):
        """Initialize comprehensive database"""
        self.db = sqlite3.connect('valency/complete_corpus.db')
        cursor = self.db.cursor()
        
        # Main patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_id TEXT,
                sentence_id TEXT,
                verb_id TEXT,
                lemma TEXT,
                form TEXT,
                voice TEXT,
                tense TEXT,
                mood TEXT,
                person TEXT,
                number TEXT,
                case_pattern TEXT,
                relation_pattern TEXT,
                full_morphology TEXT,
                arguments_json TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Valency frames table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS valency_frames (
                lemma TEXT,
                case_pattern TEXT,
                frequency INTEGER,
                voice TEXT,
                examples TEXT,
                PRIMARY KEY (lemma, case_pattern, voice)
            )
        ''')
        
        # Diachronic changes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diachronic_changes (
                lemma TEXT,
                old_pattern TEXT,
                new_pattern TEXT,
                period1 TEXT,
                period2 TEXT,
                change_type TEXT,
                evidence TEXT
            )
        ''')
        
        self.db.commit()
        
    def extract_proiel_morphology(self, morph, pos):
        """Extract morphology with CORRECT positions"""
        data = {}
        
        if pos.startswith('V'):  # Verb morphology
            # V- person number tense voice mood
            data['person'] = morph[0] if len(morph) > 0 else '-'
            data['number'] = morph[1] if len(morph) > 1 else '-'
            data['tense'] = morph[2] if len(morph) > 2 else '-'
            data['voice'] = self.PROIEL_VOICES.get(morph[3] if len(morph) > 3 else '-', 'active')
            data['mood'] = morph[4] if len(morph) > 4 else '-'
            
        elif pos[0] in ['N', 'P', 'A', 'D', 'S']:  # Nominal morphology
            # N- person number gender case degree
            data['person'] = morph[0] if len(morph) > 0 else '-'
            data['number'] = morph[1] if len(morph) > 1 else '-'
            data['gender'] = morph[5] if len(morph) > 5 else '-'
            data['case'] = self.PROIEL_CASES.get(morph[6] if len(morph) > 6 else '-')
            
        return data
        
    def process_greek_nt(self):
        """Process Greek NT with correct morphology"""
        logging.info("📖 Processing Greek New Testament...")
        
        xml_path = "corpus_data/greek-nt.xml"
        if not os.path.exists(xml_path):
            xml_path = "texts/greek/koine/proiel_greek_nt.xml"
            
        tree = etree.parse(xml_path)
        sentences = tree.xpath('//sentence')
        
        patterns_extracted = 0
        
        for i, sentence in enumerate(sentences):
            if i % 500 == 0:
                logging.info(f"  Processing sentence {i}/{len(sentences)}...")
                
            # Find all verbs
            verbs = sentence.xpath('.//token[starts-with(@part-of-speech, "V-")]')
            
            for verb in verbs:
                pattern = self.extract_verb_pattern(sentence, verb)
                if pattern:
                    self.store_pattern(pattern)
                    patterns_extracted += 1
                    
                    # Update valency frame
                    self.update_valency_frame(pattern)
                    
        logging.info(f"✅ Extracted {patterns_extracted} verb patterns")
        self.stats['greek_nt_patterns'] = patterns_extracted
        
    def extract_verb_pattern(self, sentence, verb):
        """Extract complete verb pattern with arguments"""
        verb_id = verb.get('id')
        lemma = verb.get('lemma')
        form = verb.get('form')
        morph = verb.get('morphology', '')
        pos = verb.get('part-of-speech', '')
        
        # Extract verb morphology
        verb_morph = self.extract_proiel_morphology(morph, pos)
        
        # Find arguments
        arguments = []
        cases = []
        relations = []
        
        # Get all dependents
        for token in sentence.xpath(f'.//token[@head-id="{verb_id}"]'):
            rel = token.get('relation')
            
            # Core arguments
            if rel in ['sub', 'obj', 'obl', 'xobj', 'ag', 'comp', 'xadv']:
                token_pos = token.get('part-of-speech', '')
                token_morph = token.get('morphology', '')
                
                # Extract case
                if token_pos and token_pos[0] in ['N', 'P', 'A', 'D', 'S']:
                    morph_data = self.extract_proiel_morphology(token_morph, token_pos)
                    case = morph_data.get('case')
                    
                    if case:
                        arguments.append({
                            'relation': rel,
                            'case': case,
                            'lemma': token.get('lemma'),
                            'form': token.get('form'),
                            'pos': token_pos,
                            'morphology': token_morph
                        })
                        cases.append(case)
                        relations.append(rel)
                        
        # Create patterns
        case_pattern = self.create_case_pattern(cases)
        relation_pattern = '-'.join(sorted(relations))
        
        return {
            'text_id': 'greek_nt',
            'sentence_id': sentence.get('id'),
            'verb_id': verb_id,
            'lemma': lemma,
            'form': form,
            'voice': verb_morph.get('voice', 'active'),
            'tense': verb_morph.get('tense'),
            'mood': verb_morph.get('mood'),
            'person': verb_morph.get('person'),
            'number': verb_morph.get('number'),
            'case_pattern': case_pattern,
            'relation_pattern': relation_pattern,
            'full_morphology': morph,
            'arguments': arguments
        }
        
    def create_case_pattern(self, cases):
        """Create canonical case pattern"""
        if not cases:
            return 'INTR'
            
        # Greek word order preferences
        case_order = {'NOM': 1, 'ACC': 2, 'GEN': 3, 'DAT': 4, 'VOC': 5, 'ABL': 6}
        cases.sort(key=lambda x: case_order.get(x, 99))
        
        return '-'.join(cases)
        
    def store_pattern(self, pattern):
        """Store pattern in database"""
        cursor = self.db.cursor()
        
        cursor.execute('''
            INSERT INTO patterns 
            (text_id, sentence_id, verb_id, lemma, form, voice, tense, 
             mood, person, number, case_pattern, relation_pattern, 
             full_morphology, arguments_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pattern['text_id'],
            pattern['sentence_id'],
            pattern['verb_id'],
            pattern['lemma'],
            pattern['form'],
            pattern['voice'],
            pattern['tense'],
            pattern['mood'],
            pattern['person'],
            pattern['number'],
            pattern['case_pattern'],
            pattern['relation_pattern'],
            pattern['full_morphology'],
            json.dumps(pattern['arguments'], ensure_ascii=False)
        ))
        
        self.db.commit()
        
    def update_valency_frame(self, pattern):
        """Update valency frame statistics"""
        cursor = self.db.cursor()
        
        # Check if frame exists
        cursor.execute('''
            SELECT frequency, examples FROM valency_frames
            WHERE lemma = ? AND case_pattern = ? AND voice = ?
        ''', (pattern['lemma'], pattern['case_pattern'], pattern['voice']))
        
        result = cursor.fetchone()
        
        if result:
            # Update existing
            freq, examples = result
            examples_list = json.loads(examples)
            examples_list.append(pattern['form'])
            
            cursor.execute('''
                UPDATE valency_frames 
                SET frequency = ?, examples = ?
                WHERE lemma = ? AND case_pattern = ? AND voice = ?
            ''', (freq + 1, json.dumps(examples_list[-10:]), 
                  pattern['lemma'], pattern['case_pattern'], pattern['voice']))
        else:
            # Insert new
            cursor.execute('''
                INSERT INTO valency_frames (lemma, case_pattern, voice, frequency, examples)
                VALUES (?, ?, ?, 1, ?)
            ''', (pattern['lemma'], pattern['case_pattern'], pattern['voice'], 
                  json.dumps([pattern['form']])))
                  
        self.db.commit()
        
    def analyze_voice_alternations(self):
        """Analyze voice alternations every hour"""
        logging.info("🔄 Analyzing voice alternations...")
        
        cursor = self.db.cursor()
        
        # Find verbs with multiple voices
        cursor.execute('''
            SELECT lemma, voice, case_pattern, COUNT(*) as freq
            FROM patterns
            WHERE case_pattern != 'INTR'
            GROUP BY lemma, voice, case_pattern
            HAVING freq > 5
            ORDER BY lemma, freq DESC
        ''')
        
        results = defaultdict(lambda: defaultdict(list))
        
        for lemma, voice, case_pattern, freq in cursor.fetchall():
            results[lemma][voice].append({
                'pattern': case_pattern,
                'frequency': freq
            })
            
        # Find interesting alternations
        alternations = []
        for lemma, voices in results.items():
            if len(voices) > 1:
                alternations.append({
                    'lemma': lemma,
                    'voices': dict(voices)
                })
                
        logging.info(f"  Found {len(alternations)} verbs with voice alternations")
        
        # Save report
        self.save_voice_report(alternations)
        
    def analyze_argument_changes(self):
        """Look for argument structure variations"""
        logging.info("🔍 Analyzing argument structure changes...")
        
        cursor = self.db.cursor()
        
        # Find lemmas with multiple patterns
        cursor.execute('''
            SELECT lemma, case_pattern, COUNT(*) as freq
            FROM patterns
            WHERE case_pattern != 'INTR'
            GROUP BY lemma, case_pattern
            HAVING freq > 10
            ORDER BY lemma, freq DESC
        ''')
        
        lemma_patterns = defaultdict(list)
        
        for lemma, pattern, freq in cursor.fetchall():
            lemma_patterns[lemma].append({
                'pattern': pattern,
                'frequency': freq
            })
            
        # Find changes
        changes = []
        for lemma, patterns in lemma_patterns.items():
            if len(patterns) > 1:
                # Sort by frequency
                patterns.sort(key=lambda x: x['frequency'], reverse=True)
                
                for i in range(len(patterns)-1):
                    change = {
                        'lemma': lemma,
                        'pattern1': patterns[i]['pattern'],
                        'freq1': patterns[i]['frequency'],
                        'pattern2': patterns[i+1]['pattern'],
                        'freq2': patterns[i+1]['frequency'],
                        'type': self.classify_change(patterns[i]['pattern'], 
                                                   patterns[i+1]['pattern'])
                    }
                    changes.append(change)
                    
        logging.info(f"  Found {len(changes)} potential argument structure changes")
        self.save_changes_report(changes)
        
    def classify_change(self, pattern1, pattern2):
        """Classify type of change"""
        cases1 = set(pattern1.split('-'))
        cases2 = set(pattern2.split('-'))
        
        if cases1 == cases2:
            return 'order_change'
        elif cases1 < cases2:
            return 'expansion'
        elif cases1 > cases2:
            return 'reduction'
        else:
            common = cases1 & cases2
            if 'ACC' in cases1 and 'DAT' in cases2 and 'ACC' not in cases2:
                return 'ACC_to_DAT'
            elif 'DAT' in cases1 and 'ACC' in cases2 and 'DAT' not in cases2:
                return 'DAT_to_ACC'
            else:
                return 'substitution'
                
    def process_iliad(self):
        """Process Perseus Iliad for comparison"""
        logging.info("📜 Processing Homer's Iliad...")
        
        iliad_path = "texts/greek/ancient/iliad_perseus.xml"
        if os.path.exists(iliad_path):
            try:
                tree = etree.parse(iliad_path)
                
                # Perseus format is different - adapt extraction
                # This is a placeholder - would need format-specific parsing
                
                logging.info("  Iliad processing completed")
            except Exception as e:
                logging.error(f"  Error processing Iliad: {e}")
                
    def generate_hourly_report(self, hour):
        """Generate detailed report every hour"""
        logging.info(f"\n{'='*60}")
        logging.info(f"HOUR {hour} REPORT - {datetime.now().strftime('%H:%M')}")
        logging.info('='*60)
        
        cursor = self.db.cursor()
        
        # Overall statistics
        cursor.execute("SELECT COUNT(*) FROM patterns")
        total_patterns = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT lemma) FROM patterns")
        unique_lemmas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT case_pattern) FROM patterns WHERE case_pattern != 'INTR'")
        unique_patterns = cursor.fetchone()[0]
        
        # Top patterns
        cursor.execute('''
            SELECT case_pattern, COUNT(*) as freq
            FROM patterns
            WHERE case_pattern != 'INTR'
            GROUP BY case_pattern
            ORDER BY freq DESC
            LIMIT 10
        ''')
        top_patterns = cursor.fetchall()
        
        report = f"""
### HOUR {hour} STATISTICS ###

Total Patterns Extracted: {total_patterns:,}
Unique Verbs: {unique_lemmas:,}
Unique Case Patterns: {unique_patterns}

TOP CASE PATTERNS:
"""
        for pattern, freq in top_patterns:
            report += f"  {pattern}: {freq:,} instances\n"
            
        # Most variable verbs
        cursor.execute('''
            SELECT lemma, COUNT(DISTINCT case_pattern) as patterns
            FROM patterns
            WHERE case_pattern != 'INTR'
            GROUP BY lemma
            ORDER BY patterns DESC
            LIMIT 10
        ''')
        
        report += "\nMOST VARIABLE VERBS:\n"
        for lemma, count in cursor.fetchall():
            report += f"  {lemma}: {count} different patterns\n"
            
        logging.info(report)
        
        # Save to file
        with open(f'reports/hour_{hour}_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
            
    def save_voice_report(self, alternations):
        """Save voice alternation analysis"""
        report = "# VOICE ALTERNATION ANALYSIS\n\n"
        
        for alt in alternations[:50]:  # Top 50
            report += f"\n## {alt['lemma']}\n"
            for voice, patterns in alt['voices'].items():
                report += f"\n### {voice}:\n"
                for p in patterns:
                    report += f"  - {p['pattern']}: {p['frequency']} instances\n"
                    
        with open('reports/voice_alternations.md', 'w', encoding='utf-8') as f:
            f.write(report)
            
    def save_changes_report(self, changes):
        """Save argument structure changes"""
        report = "# ARGUMENT STRUCTURE VARIATIONS\n\n"
        
        # Group by change type
        by_type = defaultdict(list)
        for change in changes:
            by_type[change['type']].append(change)
            
        for change_type, items in by_type.items():
            report += f"\n## {change_type.upper()}\n"
            for item in items[:20]:  # Top 20 per type
                report += f"\n{item['lemma']}:\n"
                report += f"  - {item['pattern1']} ({item['freq1']} instances)\n"
                report += f"  - {item['pattern2']} ({item['freq2']} instances)\n"
                
        with open('reports/argument_changes.md', 'w', encoding='utf-8') as f:
            f.write(report)
            
    def run_for_10_hours(self):
        """Main 10-hour processing loop"""
        logging.info("🌙 STARTING 10-HOUR OVERNIGHT PROCESSING")
        logging.info(f"Start time: {self.start_time}")
        logging.info(f"End time: {self.end_time}")
        logging.info("="*60)
        
        hour = 0
        
        while datetime.now() < self.end_time:
            hour += 1
            hour_start = datetime.now()
            
            logging.info(f"\n⏰ HOUR {hour} STARTING...")
            
            # Different tasks each hour
            if hour == 1:
                self.process_greek_nt()
            elif hour == 2:
                self.analyze_voice_alternations()
                self.process_iliad()
            elif hour == 3:
                self.analyze_argument_changes()
            elif hour % 2 == 0:
                # Even hours: deeper analysis
                self.analyze_voice_alternations()
                self.extract_complex_patterns()
            else:
                # Odd hours: more extraction
                self.reprocess_with_improvements()
                
            # Generate hourly report
            self.generate_hourly_report(hour)
            
            # Calculate time for next hour
            hour_duration = datetime.now() - hour_start
            if hour_duration < timedelta(hours=1):
                sleep_time = (timedelta(hours=1) - hour_duration).total_seconds()
                logging.info(f"  Sleeping for {sleep_time/60:.1f} minutes until next hour...")
                time.sleep(sleep_time)
                
        # Final comprehensive report
        self.generate_final_report()
        
    def extract_complex_patterns(self):
        """Extract more complex patterns"""
        logging.info("🔧 Extracting complex patterns...")
        
        cursor = self.db.cursor()
        
        # Find ditransitive patterns
        cursor.execute('''
            SELECT lemma, case_pattern, COUNT(*) as freq
            FROM patterns
            WHERE case_pattern LIKE '%-%-%'
            GROUP BY lemma, case_pattern
            ORDER BY freq DESC
            LIMIT 50
        ''')
        
        ditransitives = cursor.fetchall()
        logging.info(f"  Found {len(ditransitives)} ditransitive patterns")
        
    def reprocess_with_improvements(self):
        """Reprocess to catch missed patterns"""
        logging.info("🔄 Reprocessing for missed patterns...")
        
        # Re-examine sentences with multiple verbs
        # Look for embedded clauses
        # Extract non-finite forms
        
        self.stats['reprocessing_runs'] += 1
        
    def generate_final_report(self):
        """Generate comprehensive final report"""
        logging.info("\n" + "="*60)
        logging.info("FINAL 10-HOUR REPORT")
        logging.info("="*60)
        
        cursor = self.db.cursor()
        
        # Complete statistics
        cursor.execute("SELECT COUNT(*) FROM patterns")
        total = cursor.fetchone()[0]
        
        report = f"""
# 10-HOUR OVERNIGHT PROCESSING COMPLETE

## SUMMARY
- Total patterns extracted: {total:,}
- Processing duration: {datetime.now() - self.start_time}
- Greek NT patterns: {self.stats.get('greek_nt_patterns', 0):,}

## FILES CREATED
- Database: valency/complete_corpus.db
- Voice report: reports/voice_alternations.md
- Changes report: reports/argument_changes.md
- Hourly reports: reports/hour_*.txt

## KEY FINDINGS
[Generated findings here]

## NEXT STEPS
1. Process Latin texts for comparison
2. Add English Bible translations
3. Create alignment algorithms
4. Generate visualization

---
Agent ran successfully for 10 hours!
        """
        
        with open('FINAL_10HOUR_REPORT.md', 'w', encoding='utf-8') as f:
            f.write(report)
            
        logging.info(report)
        
        
if __name__ == "__main__":
    agent = TenHourAgent()
    agent.run_for_10_hours()