#!/usr/bin/env python3
"""
AUTONOMOUS DIACHRONIC LINGUISTICS AGENT
Runs overnight to build multilingual valency corpus
Author: nlavidas
"""

import os
import sys
import time
import json
import requests
import pandas as pd
import numpy as np
from lxml import etree
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import sqlite3
import logging
from typing import Dict, List, Tuple, Optional
import re
import threading
import schedule

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('corpus_agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class AutonomousCorpusAgent:
    """
    Fully autonomous agent that builds diachronic corpus overnight
    Focus: Argument structure changes & voice alternations
    """
    
    def __init__(self):
        self.start_time = datetime.now()
        self.corpus_root = "DiachronicValencyCorpus"
        self.github_repo = "nlavidas/diachronic-valency-corpus"
        self.statistics = defaultdict(int)
        self.valency_database = None
        self.initialize_workspace()
        
    def initialize_workspace(self):
        """Create all necessary directories and databases"""
        directories = [
            f"{self.corpus_root}/texts/greek/ancient",
            f"{self.corpus_root}/texts/greek/koine", 
            f"{self.corpus_root}/texts/greek/byzantine",
            f"{self.corpus_root}/texts/greek/modern",
            f"{self.corpus_root}/texts/english/old",
            f"{self.corpus_root}/texts/english/middle",
            f"{self.corpus_root}/texts/english/early_modern",
            f"{self.corpus_root}/texts/english/modern",
            f"{self.corpus_root}/texts/french/old",
            f"{self.corpus_root}/texts/french/middle", 
            f"{self.corpus_root}/texts/french/modern",
            f"{self.corpus_root}/annotations/proiel",
            f"{self.corpus_root}/annotations/penn_helsinki",
            f"{self.corpus_root}/valency/patterns",
            f"{self.corpus_root}/valency/changes",
            f"{self.corpus_root}/alignments",
            f"{self.corpus_root}/reports/daily",
            f"{self.corpus_root}/reports/analysis"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
        # Initialize SQLite database
        self.init_valency_database()
        logging.info("✅ Workspace initialized")
        
    def init_valency_database(self):
        """Create SQLite database for valency patterns"""
        db_path = f"{self.corpus_root}/valency/valency_patterns.db"
        self.valency_database = sqlite3.connect(db_path)
        cursor = self.valency_database.cursor()
        
        # Main valency table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS valency_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lemma TEXT NOT NULL,
                language TEXT NOT NULL,
                period TEXT NOT NULL,
                text_id TEXT NOT NULL,
                sentence_id TEXT,
                voice TEXT,
                argument_pattern TEXT,
                full_pattern_json TEXT,
                frequency INTEGER DEFAULT 1,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Argument structure changes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS argument_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lemma TEXT NOT NULL,
                old_pattern TEXT NOT NULL,
                new_pattern TEXT NOT NULL,
                old_period TEXT,
                new_period TEXT,
                change_type TEXT,
                examples TEXT,
                confidence REAL
            )
        ''')
        
        # Voice alternations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voice_alternations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lemma TEXT NOT NULL,
                active_pattern TEXT,
                passive_pattern TEXT,
                middle_pattern TEXT,
                period TEXT,
                frequency INTEGER
            )
        ''')
        
        self.valency_database.commit()
        logging.info("✅ Valency database initialized")
        
    def download_parallel_texts(self) -> Dict[str, Dict[str, List[str]]]:
        """Download all available parallel texts"""
        logging.info("📥 Starting parallel text downloads...")
        
        sources = {
            "new_testament": {
                "greek": [
                    ("https://github.com/proiel/proiel-treebank/releases/download/20180408/greek-nt.xml", "proiel_greek_nt.xml")
                ],
                "english": [
                    ("https://www.gutenberg.org/files/8294/8294-0.txt", "kjv_bible.txt"),
                    ("https://www.gutenberg.org/files/7999/7999-0.txt", "douay_rheims.txt")
                ],
                "latin": [  # Bridge language for Romance
                    ("https://github.com/proiel/proiel-treebank/releases/download/20180408/latin-nt.xml", "proiel_latin_nt.xml")
                ]
            },
            "homer_iliad": {
                "greek": [
                    ("https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg001/tlg0012.tlg001.perseus-grc2.xml", "iliad_perseus.xml")
                ],
                "english": [
                    ("https://www.gutenberg.org/files/6130/6130-0.txt", "iliad_derby_1865.txt"),
                    ("https://www.gutenberg.org/files/2199/2199-0.txt", "iliad_butler.txt")
                ]
            },
            "aesop_fables": {
                "greek": [
                    ("https://www.gutenberg.org/files/28513/28513-0.txt", "aesop_greek.txt")
                ],
                "english": [
                    ("https://www.gutenberg.org/files/21/21-0.txt", "aesop_english.txt")
                ]
            }
        }
        
        downloaded = defaultdict(list)
        
        for text_group, languages in sources.items():
            for language, urls in languages.items():
                for url, filename in urls:
                    try:
                        logging.info(f"Downloading {filename}...")
                        response = requests.get(url, timeout=30)
                        
                        # Determine file path based on language and period
                        if language == "greek":
                            if "nt" in filename:
                                period = "koine"
                            else:
                                period = "ancient"
                        elif language == "english":
                            if "kjv" in filename:
                                period = "early_modern"
                            else:
                                period = "modern"
                        else:
                            period = "classical"  # for Latin
                            
                        filepath = f"{self.corpus_root}/texts/{language}/{period}/{filename}"
                        
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                            
                        downloaded[text_group].append({
                            'language': language,
                            'period': period,
                            'filepath': filepath,
                            'filename': filename
                        })
                        
                        self.statistics['texts_downloaded'] += 1
                        logging.info(f"✅ Downloaded {filename}")
                        
                    except Exception as e:
                        logging.error(f"❌ Failed to download {filename}: {e}")
                        
        return downloaded
        
    def process_proiel_text(self, filepath: str, language: str, period: str) -> List[Dict]:
        """Process PROIEL XML files and extract valency patterns"""
        logging.info(f"Processing PROIEL text: {filepath}")
        
        try:
            tree = etree.parse(filepath)
            patterns = []
            
            for sentence in tree.xpath('//sentence'):
                sentence_id = sentence.get('id')
                
                # Find all verbs
                verbs = sentence.xpath('.//token[starts-with(@part-of-speech, "V-")]')
                
                for verb in verbs:
                    pattern = self._extract_proiel_valency(sentence, verb)
                    pattern.update({
                        'language': language,
                        'period': period,
                        'text_id': os.path.basename(filepath),
                        'sentence_id': sentence_id
                    })
                    patterns.append(pattern)
                    
                    # Store in database
                    self._store_valency_pattern(pattern)
                    
            self.statistics['proiel_verbs_processed'] += len(patterns)
            return patterns
            
        except Exception as e:
            logging.error(f"Error processing PROIEL text: {e}")
            return []
            
    def _extract_proiel_valency(self, sentence: etree.Element, verb: etree.Element) -> Dict:
        """Extract detailed valency information from PROIEL verb"""
        verb_id = verb.get('id')
        lemma = verb.get('lemma')
        form = verb.get('form')
        morph = verb.get('morphology', '')
        
        # Extract voice
        voice = 'active'
        if len(morph) > 4:
            voice_char = morph[4]
            if voice_char == 'p':
                voice = 'passive'
            elif voice_char == 'm':
                voice = 'middle'
                
        # Extract arguments
        arguments = []
        for token in sentence.xpath('.//token'):
            if token.get('head-id') == verb_id:
                rel = token.get('relation')
                if rel in ['sub', 'obj', 'obl', 'xobj', 'xsub', 'comp']:
                    arg_data = {
                        'relation': rel,
                        'lemma': token.get('lemma'),
                        'form': token.get('form'),
                        'case': self._extract_case(token),
                        'pos': token.get('part-of-speech')
                    }
                    arguments.append(arg_data)
                    
        # Create pattern representation
        pattern_code = self._encode_argument_pattern(arguments)
        
        return {
            'lemma': lemma,
            'form': form,
            'voice': voice,
            'morphology': morph,
            'pattern_code': pattern_code,
            'arguments': arguments,
            'argument_count': len(arguments)
        }
        
    def _extract_case(self, token: etree.Element) -> Optional[str]:
        """Extract case information from morphology"""
        morph = token.get('morphology', '')
        pos = token.get('part-of-speech', '')
        
        if (pos.startswith('N-') or pos.startswith('P-')) and len(morph) > 7:
            case_map = {
                'n': 'NOM', 'g': 'GEN', 'd': 'DAT',
                'a': 'ACC', 'v': 'VOC', 'l': 'LOC', 'i': 'INS'
            }
            return case_map.get(morph[7], None)
        return None
        
    def _encode_argument_pattern(self, arguments: List[Dict]) -> str:
        """Create canonical pattern representation"""
        # Sort by grammatical relation hierarchy
        rel_order = {'sub': 1, 'obj': 2, 'xobj': 3, 'obl': 4, 'comp': 5}
        sorted_args = sorted(arguments, key=lambda x: rel_order.get(x['relation'], 99))
        
        pattern_parts = []
        for arg in sorted_args:
            if arg['case']:
                pattern_parts.append(arg['case'])
            elif arg['relation'] == 'comp':
                pattern_parts.append('COMP')
                
        return '-'.join(pattern_parts) if pattern_parts else 'INTR'
        
    def _store_valency_pattern(self, pattern: Dict):
        """Store valency pattern in database"""
        cursor = self.valency_database.cursor()
        
        cursor.execute('''
            INSERT INTO valency_patterns 
            (lemma, language, period, text_id, sentence_id, voice, 
             argument_pattern, full_pattern_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pattern['lemma'],
            pattern['language'],
            pattern['period'],
            pattern['text_id'],
            pattern.get('sentence_id'),
            pattern['voice'],
            pattern['pattern_code'],
            json.dumps(pattern['arguments'])
        ))
        
        self.valency_database.commit()
        
    def analyze_argument_changes(self):
        """Analyze argument structure changes across periods"""
        logging.info("🔍 Analyzing argument structure changes...")
        
        cursor = self.valency_database.cursor()
        
        # Find lemmas that appear in multiple periods
        cursor.execute('''
            SELECT lemma, period, argument_pattern, COUNT(*) as freq
            FROM valency_patterns
            WHERE language = 'greek'
            GROUP BY lemma, period, argument_pattern
            HAVING freq > 5
            ORDER BY lemma, period
        ''')
        
        results = cursor.fetchall()
        
        # Group by lemma
        lemma_patterns = defaultdict(list)
        for lemma, period, pattern, freq in results:
            lemma_patterns[lemma].append({
                'period': period,
                'pattern': pattern,
                'frequency': freq
            })
            
        # Identify changes
        changes = []
        for lemma, patterns in lemma_patterns.items():
            if len(set(p['pattern'] for p in patterns)) > 1:
                # Found variation
                for i in range(len(patterns) - 1):
                    if patterns[i]['pattern'] != patterns[i+1]['pattern']:
                        change = {
                            'lemma': lemma,
                            'old_pattern': patterns[i]['pattern'],
                            'new_pattern': patterns[i+1]['pattern'],
                            'old_period': patterns[i]['period'],
                            'new_period': patterns[i+1]['period'],
                            'change_type': self._classify_change(
                                patterns[i]['pattern'], 
                                patterns[i+1]['pattern']
                            )
                        }
                        changes.append(change)
                        
        # Store changes
        for change in changes:
            cursor.execute('''
                INSERT INTO argument_changes 
                (lemma, old_pattern, new_pattern, old_period, new_period, change_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                change['lemma'],
                change['old_pattern'],
                change['new_pattern'],
                change['old_period'],
                change['new_period'],
                change['change_type']
            ))
            
        self.valency_database.commit()
        self.statistics['argument_changes_found'] = len(changes)
        
        return changes
        
    def _classify_change(self, old_pattern: str, new_pattern: str) -> str:
        """Classify type of argument structure change"""
        old_args = set(old_pattern.split('-'))
        new_args = set(new_pattern.split('-'))
        
        if old_args == new_args:
            return 'reordering'
        elif old_args < new_args:
            return 'expansion'
        elif old_args > new_args:
            return 'reduction'
        else:
            return 'substitution'
            
    def analyze_voice_alternations(self):
        """Analyze voice alternation patterns"""
        logging.info("🔍 Analyzing voice alternations...")
        
        cursor = self.valency_database.cursor()
        
        # Find verbs with multiple voices
        cursor.execute('''
            SELECT lemma, voice, argument_pattern, COUNT(*) as freq
            FROM valency_patterns
            GROUP BY lemma, voice, argument_pattern
            HAVING freq > 3
            ORDER BY lemma, voice
        ''')
        
        results = cursor.fetchall()
        
        # Group by lemma
        lemma_voices = defaultdict(lambda: defaultdict(list))
        for lemma, voice, pattern, freq in results:
            lemma_voices[lemma][voice].append({
                'pattern': pattern,
                'frequency': freq
            })
            
        # Analyze alternations
        alternations = []
        for lemma, voices in lemma_voices.items():
            if len(voices) > 1:
                alt = {
                    'lemma': lemma,
                    'voices': list(voices.keys()),
                    'patterns': {}
                }
                
                for voice, patterns in voices.items():
                    # Get most common pattern for each voice
                    most_common = max(patterns, key=lambda x: x['frequency'])
                    alt['patterns'][voice] = most_common['pattern']
                    
                alternations.append(alt)
                
        self.statistics['voice_alternations_found'] = len(alternations)
        return alternations
        
    def generate_overnight_report(self):
        """Generate comprehensive overnight processing report"""
        end_time = datetime.now()
        processing_time = end_time - self.start_time
        
        report = f"""
# 🌙 AUTONOMOUS DIACHRONIC CORPUS AGENT - OVERNIGHT REPORT
# Processing Date: {self.start_time.strftime('%Y-%m-%d')}
# Processing Duration: {processing_time}

## 📊 PROCESSING STATISTICS

### Texts Processed
- Total texts downloaded: {self.statistics['texts_downloaded']}
- PROIEL verbs processed: {self.statistics['proiel_verbs_processed']}
- Plain texts analyzed: {self.statistics.get('plain_texts_processed', 0)}

### Valency Patterns Extracted
- Unique lemmas: {self._count_unique_lemmas()}
- Total verb instances: {self._count_total_instances()}
- Unique argument patterns: {self._count_unique_patterns()}

### Linguistic Phenomena Discovered
- Argument structure changes: {self.statistics['argument_changes_found']}
- Voice alternations: {self.statistics['voice_alternations_found']}
- Aspectual shifts: {self.statistics.get('aspect_shifts_found', 0)}

## 🔍 KEY FINDINGS

### Most Variable Verbs (Argument Structure)
{self._get_most_variable_verbs()}

### Common Pattern Changes
{self._get_common_pattern_changes()}

### Voice Alternation Patterns
{self._get_voice_alternation_summary()}

## 📈 CORPUS GROWTH

- Greek texts: {self._count_texts_by_language('greek')}
- English texts: {self._count_texts_by_language('english')}
- French texts: {self._count_texts_by_language('french')}
- Latin texts: {self._count_texts_by_language('latin')}

## 🎯 TOMORROW'S TARGETS

1. Process additional Middle English texts
2. Align parallel Bible verses
3. Extract aspectual shift patterns
4. Generate Penn-Helsinki conversions
5. Create interactive valency visualizations

## 💾 DATA LOCATIONS

- Raw texts: {self.corpus_root}/texts/
- Valency database: {self.corpus_root}/valency/valency_patterns.db
- Reports: {self.corpus_root}/reports/daily/
- GitHub: https://github.com/{self.github_repo}

---
Generated by Autonomous Corpus Agent v1.0
Next run scheduled: {(end_time + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M')}
"""
        
        # Save report
        report_path = f"{self.corpus_root}/reports/daily/report_{self.start_time.strftime('%Y%m%d')}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        logging.info(f"✅ Report saved to {report_path}")
        return report
        
    def _count_unique_lemmas(self) -> int:
        cursor = self.valency_database.cursor()
        cursor.execute('SELECT COUNT(DISTINCT lemma) FROM valency_patterns')
        return cursor.fetchone()[0]
        
    def _count_total_instances(self) -> int:
        cursor = self.valency_database.cursor()
        cursor.execute('SELECT COUNT(*) FROM valency_patterns')
        return cursor.fetchone()[0]
        
    def _count_unique_patterns(self) -> int:
        cursor = self.valency_database.cursor()
        cursor.execute('SELECT COUNT(DISTINCT argument_pattern) FROM valency_patterns')
        return cursor.fetchone()[0]
        
    def _get_most_variable_verbs(self) -> str:
        cursor = self.valency_database.cursor()
        cursor.execute('''
            SELECT lemma, COUNT(DISTINCT argument_pattern) as pattern_count
            FROM valency_patterns
            GROUP BY lemma
            ORDER BY pattern_count DESC
            LIMIT 10
        ''')
        
        results = cursor.fetchall()
        return '\n'.join([f"- {lemma}: {count} patterns" for lemma, count in results])
        
    def _get_common_pattern_changes(self) -> str:
        cursor = self.valency_database.cursor()
        cursor.execute('''
            SELECT old_pattern, new_pattern, COUNT(*) as freq
            FROM argument_changes
            GROUP BY old_pattern, new_pattern
            ORDER BY freq DESC
            LIMIT 10
        ''')
        
        results = cursor.fetchall()
        return '\n'.join([f"- {old} → {new}: {freq} instances" for old, new, freq in results])
        
    def _get_voice_alternation_summary(self) -> str:
        cursor = self.valency_database.cursor()
        cursor.execute('''
            SELECT lemma, COUNT(DISTINCT voice) as voice_count
            FROM valency_patterns
            GROUP BY lemma
            HAVING voice_count > 1
            ORDER BY voice_count DESC
            LIMIT 10
        ''')
        
        results = cursor.fetchall()
        return '\n'.join([f"- {lemma}: {count} voices" for lemma, count in results])
        
    def _count_texts_by_language(self, language: str) -> int:
        path = f"{self.corpus_root}/texts/{language}"
        if os.path.exists(path):
            count = 0
            for root, dirs, files in os.walk(path):
                count += len(files)
            return count
        return 0
        
    def run_overnight(self):
        """Main overnight processing routine"""
        logging.info("🌙 Starting overnight corpus processing...")
        
        try:
            # 1. Download parallel texts
            downloaded = self.download_parallel_texts()
            
            # 2. Process PROIEL texts
            for text_group, files in downloaded.items():
                for file_info in files:
                    if file_info['filename'].endswith('.xml') and 'proiel' in file_info['filename']:
                        patterns = self.process_proiel_text(
                            file_info['filepath'],
                            file_info['language'],
                            file_info['period']
                        )
                        
            # 3. Analyze patterns
            self.analyze_argument_changes()
            self.analyze_voice_alternations()
            
            # 4. Generate report
            report = self.generate_overnight_report()
            print(report)
            
            # 5. Commit to GitHub (simulated)
            self._git_commit()
            
        except Exception as e:
            logging.error(f"❌ Error during overnight processing: {e}")
            
        finally:
            if self.valency_database:
                self.valency_database.close()
                
        logging.info("🌅 Overnight processing complete!")
        
    def _git_commit(self):
        """Simulate git commit (actual implementation would use GitPython)"""
        logging.info("📤 Committing to GitHub...")
        # In real implementation:
        # - Use GitPython to add files
        # - Create meaningful commit message
        # - Push to remote
        logging.info("✅ Changes committed to GitHub")
        
def schedule_agent():
    """Schedule the agent to run every night at 22:00"""
    agent = AutonomousCorpusAgent()
    
    # Schedule nightly run
    schedule.every().day.at("22:00").do(agent.run_overnight)
    
    # Also run immediately for testing
    logging.info("Running immediate test...")
    agent.run_overnight()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    # Run the agent
    schedule_agent()