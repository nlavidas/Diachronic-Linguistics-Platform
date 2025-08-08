#!/usr/bin/env python3
"""
SIMPLIFIED 24/7 AUTONOMOUS DIACHRONIC AGENT
Windows-compatible with lightweight dependencies
"""

import os
import sys
import time
import json
import sqlite3
import requests
import schedule
import logging
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import queue

# Windows-friendly imports only
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('agent_simple.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

class SimpleDiachronicAgent:
    """
    Simplified 24/7 Agent that works on Windows
    without complex ML dependencies
    """
    
    def __init__(self):
        self.start_time = datetime.now()
        self.consultation_queue = queue.Queue()
        self.daily_findings = []
        self.issues_to_discuss = []
        
        # Historical texts to collect
        self.target_texts = {
            'homer_iliad': {
                'translations': [
                    {'name': 'Chapman', 'year': 1611, 'url': 'https://www.gutenberg.org/ebooks/48895'},
                    {'name': 'Pope', 'year': 1720, 'url': 'https://www.gutenberg.org/ebooks/6130'},
                    {'name': 'Derby', 'year': 1865, 'url': 'https://www.gutenberg.org/ebooks/16452'},
                    {'name': 'Butler', 'year': 1898, 'url': 'https://www.gutenberg.org/ebooks/2199'},
                    {'name': 'Lang', 'year': 1883, 'url': 'https://www.gutenberg.org/ebooks/3059'}
                ]
            },
            'bible': {
                'translations': [
                    {'name': 'KJV', 'year': 1611, 'url': 'https://www.gutenberg.org/ebooks/10'},
                    {'name': 'Douay-Rheims', 'year': 1582, 'url': 'https://www.gutenberg.org/ebooks/1581'},
                    {'name': 'Young Literal', 'year': 1862, 'url': 'https://www.gutenberg.org/ebooks/1907'},
                    {'name': 'American Standard', 'year': 1901, 'url': 'https://www.gutenberg.org/ebooks/13841'}
                ]
            },
            'metamorphoses': {
                'translations': [
                    {'name': 'Golding', 'year': 1567, 'url': 'https://www.gutenberg.org/ebooks/1496'},
                    {'name': 'More', 'year': 1922, 'url': 'https://www.gutenberg.org/ebooks/26073'}
                ]
            }
        }
        
        # Simple text analysis tools
        self.analysis_tools = {
            'sentence_splitter': self.split_sentences,
            'word_counter': self.count_words,
            'pattern_finder': self.find_patterns,
            'aligner': self.simple_align
        }
        
        self.init_workspace()
        self.init_database()
        
    def init_workspace(self):
        """Create workspace directories"""
        dirs = [
            "texts/collected",
            "texts/processed", 
            "texts/aligned",
            "reports/daily",
            "reports/consultation",
            "analysis/patterns",
            "analysis/changes"
        ]
        
        for d in dirs:
            os.makedirs(d, exist_ok=True)
            
    def init_database(self):
        """Initialize SQLite database"""
        self.db = sqlite3.connect('agent_simple.db', check_same_thread=False)
        cursor = self.db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collected_texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work TEXT,
                translator TEXT,
                year INTEGER,
                language TEXT,
                url TEXT,
                file_path TEXT,
                collected_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                processed BOOLEAN DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                activity TEXT,
                details TEXT,
                success BOOLEAN
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                topics_discussed TEXT,
                user_feedback TEXT,
                decisions TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS text_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work TEXT,
                translator TEXT,
                pattern_type TEXT,
                pattern TEXT,
                frequency INTEGER,
                examples TEXT
            )
        ''')
        
        self.db.commit()
        
    def run_24_7(self):
        """Main execution loop"""
        logging.info("🚀 Starting Simplified 24/7 Agent")
        
        # Schedule tasks
        schedule.every().day.at("10:00").do(self.daily_consultation)
        schedule.every(2).hours.do(self.collect_texts)
        schedule.every(3).hours.do(self.process_texts)
        schedule.every(4).hours.do(self.analyze_patterns)
        schedule.every(6).hours.do(self.align_translations)
        schedule.every().day.at("02:00").do(self.night_processing)
        schedule.every().day.at("06:00").do(self.generate_report)
        
        # Start background processing
        bg_thread = threading.Thread(target=self.background_tasks)
        bg_thread.daemon = True
        bg_thread.start()
        
        # Main loop
        while True:
            schedule.run_pending()
            time.sleep(60)
            
    def background_tasks(self):
        """Background processing"""
        while True:
            try:
                # Process queue
                if not self.consultation_queue.empty():
                    task = self.consultation_queue.get()
                    self.process_task(task)
                    
                time.sleep(300)  # Every 5 minutes
                
            except Exception as e:
                logging.error(f"Background error: {e}")
                
    def collect_texts(self):
        """Collect texts from open sources"""
        logging.info("📚 Collecting texts...")
        
        collected = 0
        
        for work, data in self.target_texts.items():
            for translation in data['translations']:
                if not self.text_exists(work, translation['name']):
                    success = self.download_text(work, translation)
                    if success:
                        collected += 1
                        
        self.log_activity('collect_texts', f'Collected {collected} new texts', collected > 0)
        
        if collected > 0:
            self.issues_to_discuss.append({
                'topic': 'New Texts Collected',
                'details': f'Found {collected} new translations',
                'priority': 1
            })
            
    def download_text(self, work, translation):
        """Download a text from Gutenberg"""
        try:
            # Get text URL
            text_url = translation['url'].replace('ebooks', 'files') + '/1/1-0.txt'
            
            response = requests.get(text_url, timeout=30)
            if response.status_code == 200:
                # Save text
                filename = f"{work}_{translation['name']}_{translation['year']}.txt"
                filepath = os.path.join('texts/collected', filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                    
                # Log to database
                cursor = self.db.cursor()
                cursor.execute('''
                    INSERT INTO collected_texts 
                    (work, translator, year, language, url, file_path)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (work, translation['name'], translation['year'], 
                     'english', translation['url'], filepath))
                self.db.commit()
                
                logging.info(f"✅ Downloaded: {filename}")
                return True
                
        except Exception as e:
            logging.error(f"Download error: {e}")
            return False
            
    def text_exists(self, work, translator):
        """Check if text already collected"""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM collected_texts
            WHERE work = ? AND translator = ?
        ''', (work, translator))
        return cursor.fetchone()[0] > 0
        
    def process_texts(self):
        """Process collected texts"""
        logging.info("🔧 Processing texts...")
        
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT id, file_path, work, translator 
            FROM collected_texts 
            WHERE processed = 0
        ''')
        
        for text_id, filepath, work, translator in cursor.fetchall():
            if os.path.exists(filepath):
                self.process_single_text(text_id, filepath, work, translator)
                
    def process_single_text(self, text_id, filepath, work, translator):
        """Process a single text"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Clean Gutenberg headers/footers
            content = self.clean_gutenberg_text(content)
            
            # Split into sentences
            sentences = self.split_sentences(content)
            
            # Basic analysis
            stats = {
                'sentences': len(sentences),
                'words': self.count_words(content),
                'avg_sentence_length': len(content.split()) / len(sentences) if sentences else 0
            }
            
            # Save processed version
            processed_path = filepath.replace('collected', 'processed')
            processed_data = {
                'work': work,
                'translator': translator,
                'sentences': sentences,
                'stats': stats
            }
            
            with open(processed_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)
                
            # Update database
            cursor = self.db.cursor()
            cursor.execute('UPDATE collected_texts SET processed = 1 WHERE id = ?', (text_id,))
            self.db.commit()
            
            logging.info(f"✅ Processed: {work} - {translator}")
            
        except Exception as e:
            logging.error(f"Processing error: {e}")
            
    def clean_gutenberg_text(self, text):
        """Remove Gutenberg headers and footers"""
        lines = text.split('\n')
        
        # Find start
        start_idx = 0
        for i, line in enumerate(lines):
            if '*** START' in line or '***START' in line:
                start_idx = i + 1
                break
                
        # Find end
        end_idx = len(lines)
        for i in range(len(lines)-1, -1, -1):
            if '*** END' in lines[i] or '***END' in lines[i]:
                end_idx = i
                break
                
        return '\n'.join(lines[start_idx:end_idx])
        
    def split_sentences(self, text):
        """Simple sentence splitter"""
        import re
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
        
    def count_words(self, text):
        """Count words in text"""
        return len(text.split())
        
    def find_patterns(self, text):
        """Find linguistic patterns"""
        patterns = {
            'questions': len([s for s in text.split('.') if '?' in s]),
            'exclamations': len([s for s in text.split('.') if '!' in s]),
            'passive_voice': text.count('was ') + text.count('were ') + text.count('been ')
        }
        return patterns
        
    def analyze_patterns(self):
        """Analyze patterns across translations"""
        logging.info("🔍 Analyzing patterns...")
        
        # Get processed texts by work
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT work, COUNT(*) as versions
            FROM collected_texts
            WHERE processed = 1
            GROUP BY work
            HAVING versions > 1
        ''')
        
        for work, versions in cursor.fetchall():
            self.analyze_work_patterns(work)
            
    def analyze_work_patterns(self, work):
        """Analyze patterns for a specific work"""
        # Load all translations
        translations = []
        
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT translator, year, file_path
            FROM collected_texts
            WHERE work = ? AND processed = 1
            ORDER BY year
        ''', (work,))
        
        for translator, year, filepath in cursor.fetchall():
            processed_path = filepath.replace('collected', 'processed')
            if os.path.exists(processed_path):
                with open(processed_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    translations.append({
                        'translator': translator,
                        'year': year,
                        'data': data
                    })
                    
        # Compare patterns
        if len(translations) > 1:
            changes = self.compare_translations(translations)
            if changes:
                self.issues_to_discuss.append({
                    'topic': f'Pattern Changes in {work}',
                    'details': changes,
                    'priority': 2
                })
                
    def compare_translations(self, translations):
        """Compare patterns across translations"""
        changes = []
        
        # Compare sentence lengths over time
        for i in range(len(translations)-1):
            t1 = translations[i]
            t2 = translations[i+1]
            
            avg_len1 = t1['data']['stats']['avg_sentence_length']
            avg_len2 = t2['data']['stats']['avg_sentence_length']
            
            if abs(avg_len1 - avg_len2) > 5:
                changes.append(f"Sentence length change: {t1['translator']} ({avg_len1:.1f}) → {t2['translator']} ({avg_len2:.1f})")
                
        return changes
        
    def simple_align(self, text1, text2):
        """Simple text alignment"""
        sentences1 = self.split_sentences(text1)
        sentences2 = self.split_sentences(text2)
        
        # Very simple alignment by position
        alignments = []
        for i in range(min(len(sentences1), len(sentences2))):
            alignments.append((sentences1[i], sentences2[i]))
            
        return alignments
        
    def align_translations(self):
        """Align parallel translations"""
        logging.info("🔗 Aligning translations...")
        
        # Implementation for alignment
        
    def night_processing(self):
        """Heavy processing at night"""
        logging.info("🌙 Night processing...")
        
        # Download larger texts
        # Process intensive tasks
        
    def generate_report(self):
        """Generate daily report"""
        logging.info("📄 Generating daily report...")
        
        report = f"""
# Daily Agent Report
Date: {datetime.now().strftime('%Y-%m-%d')}

## Collected Texts
"""
        
        cursor = self.db.cursor()
        
        # Today's collections
        cursor.execute('''
            SELECT work, translator, year
            FROM collected_texts
            WHERE date(collected_date) = date('now')
        ''')
        
        for work, translator, year in cursor.fetchall():
            report += f"- {work}: {translator} ({year})\n"
            
        # Save report
        report_path = f"reports/daily/report_{datetime.now().strftime('%Y%m%d')}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
    def daily_consultation(self):
        """30-minute consultation with user"""
        print("\n" + "="*60)
        print("🗣️ DAILY CONSULTATION - 30 MINUTES")
        print(f"Time: {datetime.now().strftime('%H:%M')}")
        print("="*60)
        
        print("\n📊 TODAY'S SUMMARY:")
        
        # Show activities
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT activity, details
            FROM daily_activities
            WHERE date(timestamp) = date('now')
            ORDER BY timestamp DESC
            LIMIT 5
        ''')
        
        for activity, details in cursor.fetchall():
            print(f"• {activity}: {details}")
            
        # Issues to discuss
        print("\n❓ DISCUSSION TOPICS:")
        for i, issue in enumerate(self.issues_to_discuss[:3]):
            print(f"\n{i+1}. {issue['topic']}")
            print(f"   Details: {issue['details']}")
            
            response = input("   Your thoughts (or press Enter to skip): ")
            if response:
                self.record_feedback(issue['topic'], response)
                
        # Get priorities
        print("\n🎯 WHAT SHOULD I FOCUS ON TODAY?")
        focus = input("Enter priorities (or press Enter for autonomous): ")
        
        if focus:
            self.set_priorities(focus)
            
        print("\n✅ Consultation complete! Returning to autonomous mode.")
        print("="*60)
        
        # Clear discussed issues
        self.issues_to_discuss = []
        
    def record_feedback(self, topic, feedback):
        """Record user feedback"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO consultations (date, topics_discussed, user_feedback)
            VALUES (date('now'), ?, ?)
        ''', (topic, feedback))
        self.db.commit()
        
    def set_priorities(self, priorities):
        """Set user priorities"""
        for priority in priorities.split(','):
            self.consultation_queue.put({
                'type': 'user_priority',
                'task': priority.strip(),
                'time': datetime.now()
            })
            
    def log_activity(self, activity, details, success):
        """Log activities"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO daily_activities (activity, details, success)
            VALUES (?, ?, ?)
        ''', (activity, details, success))
        self.db.commit()
        
    def process_task(self, task):
        """Process a queued task"""
        logging.info(f"Processing task: {task['task']}")
        # Implementation


if __name__ == "__main__":
    print("🚀 Starting Simplified Diachronic Agent")
    print("✅ No complex dependencies required")
    print("📅 Daily consultation at 10:00 AM")
    print("\nPress Ctrl+C to stop\n")
    
    agent = SimpleDiachronicAgent()
    
    try:
        agent.run_24_7()
    except KeyboardInterrupt:
        print("\n👋 Agent stopped")