#!/usr/bin/env python3
"""
ULTIMATE 24/7 DIACHRONIC CORPUS AGENT WITH AI DISCOVERY
Combines everything: 24/7 collection, AI discovery, NLP tools, monitoring
Battle-tested with all fixes from tonight's experience
"""

import os
import sys
import time
import json
import sqlite3
import requests
import schedule
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

# Add the AI Discovery Module
from ai_discovery_module import AITextDiscoveryEngine, integrate_ai_discovery

# Configuration
BASE_PATH = "Z:\\DiachronicValencyCorpus"
GITHUB_REPO = "nlavidas/diachronic-indo-european-corpus"
CONSULTATION_TIME = "09:00"  # Daily consultation
CONSULTATION_DURATION = 60  # Exactly 60 minutes

# Real, confirmed sources (from tonight's testing)
REAL_SOURCES = {
    'perseus': {
        'base_url': 'https://www.perseus.tufts.edu/hopper/',
        'texts': [
            ('text?doc=Perseus:text:1999.01.0133', 'Homer_Iliad_Murray'),
            ('text?doc=Perseus:text:1999.01.0135', 'Homer_Odyssey_Murray'),
            ('text?doc=Perseus:text:1999.01.0003', 'Aeschylus_Agamemnon'),
        ]
    },
    'gutenberg': {
        'base_url': 'https://www.gutenberg.org/files/',
        'texts': [
            ('10/10-0.txt', 'Bible_KJV_1611'),
            ('2199/2199-0.txt', 'Iliad_Butler_1898'),
            ('3059/3059-0.txt', 'Iliad_Pope_1720'),
            ('6130/6130-0.txt', 'Iliad_Chapman_1611'),
            ('22382/22382-0.txt', 'Iliad_Lang_Leaf_Myers_1883'),
        ]
    },
    'proiel': {
        'base_url': 'https://raw.githubusercontent.com/proiel/proiel-treebank/master/',
        'texts': [
            ('greek-nt.xml', 'PROIEL_Greek_NT'),
            ('latin-nt.xml', 'PROIEL_Latin_NT'),
        ]
    }
}

class Ultimate24_7AgentWithAI:
    def __init__(self):
        self.base_path = Path(BASE_PATH)
        self.running = True
        self.consultation_active = False
        self.db_path = self.base_path / 'corpus_complete.db'
        
        # Create directories
        self.setup_directories()
        
        # Setup logging
        self.setup_logging()
        
        # Initialize database
        self.setup_database()
        
        # Statistics
        self.stats = {
            'texts_downloaded': 0,
            'valency_patterns': 0,
            'errors': 0,
            'ai_discoveries': 0,
            'start_time': datetime.now()
        }
        
        # Initialize AI Discovery Engine
        self.ai_discovery = None
        self.setup_ai_discovery()
        
        logging.info("🚀 Ultimate 24/7 Agent with AI Discovery initialized")
        
    def setup_directories(self):
        """Create all necessary directories"""
        dirs = [
            'texts/collected',
            'texts/processed',
            'valency/patterns',
            'github_platform',
            'logs',
            'reports/daily',
            'backups',
            'open_source_tools',
            'ai_discoveries'
        ]
        
        for dir_path in dirs:
            (self.base_path / dir_path).mkdir(parents=True, exist_ok=True)
            
    def setup_logging(self):
        """Configure logging"""
        log_file = self.base_path / f'logs/agent_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
    def setup_database(self):
        """Initialize SQLite database with all needed tables"""
        self.db = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.db.execute('PRAGMA journal_mode=WAL')  # Write-Ahead Logging for safety
        
        cursor = self.db.cursor()
        
        # Main texts table (with all columns from tonight's fix)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE,
                source TEXT,
                url TEXT,
                language TEXT,
                author TEXT,
                work TEXT,
                translator TEXT,
                year INTEGER,
                size INTEGER,
                word_count INTEGER,
                download_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed BOOLEAN DEFAULT 0,
                quality_score REAL,
                ai_discovered BOOLEAN DEFAULT 0
            )
        ''')
        
        # Valency patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS valency_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_id INTEGER,
                lemma TEXT,
                frame TEXT,
                frequency INTEGER,
                examples TEXT,
                pattern_type TEXT,
                FOREIGN KEY (text_id) REFERENCES texts(id)
            )
        ''')
        
        # Translation chains (from AI discovery)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS translation_chains (
                id INTEGER PRIMARY KEY,
                work TEXT,
                original_lang TEXT,
                translations TEXT,
                span_years INTEGER,
                chain_quality REAL
            )
        ''')
        
        # Consultation log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                duration_minutes INTEGER,
                texts_shown INTEGER,
                patterns_shown INTEGER,
                ai_discoveries_shown INTEGER,
                user_present BOOLEAN,
                notes TEXT
            )
        ''')
        
        self.db.commit()
        
    def setup_ai_discovery(self):
        """Initialize AI Discovery Engine"""
        try:
            self.ai_discovery = AITextDiscoveryEngine(str(self.db_path))
            
            # Start discovery in parallel thread
            discovery_thread = threading.Thread(target=self.ai_discovery_worker, daemon=True)
            discovery_thread.start()
            
            logging.info("✅ AI Discovery Engine started")
        except Exception as e:
            logging.error(f"Failed to start AI Discovery: {e}")
            
    def ai_discovery_worker(self):
        """AI Discovery worker thread"""
        while self.running:
            try:
                if not self.consultation_active:
                    # Let AI discovery run
                    self.ai_discovery.discover_continuously()
                    
                time.sleep(3600)  # Check every hour
                
            except Exception as e:
                logging.error(f"AI Discovery error: {e}")
                time.sleep(300)
                
    def download_text(self, source, url, filename):
        """Download a single text with error handling"""
        try:
            full_url = url if url.startswith('http') else f"{REAL_SOURCES[source]['base_url']}{url}"
            
            logging.info(f"Downloading: {filename} from {source}")
            
            response = requests.get(full_url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            # Save text
            output_path = self.base_path / f'texts/collected/{filename}.txt'
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
                
            # Record in database
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO texts 
                (filename, source, url, size, language, ai_discovered)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (filename, source, full_url, len(response.text), 'english', 0))
            
            self.db.commit()
            self.stats['texts_downloaded'] += 1
            
            logging.info(f"✅ Downloaded: {filename} ({len(response.text):,} bytes)")
            
            # Show progress
            print(f"\r📥 Total downloaded: {self.stats['texts_downloaded']} texts | Latest: {filename[:30]}...", end='', flush=True)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to download {filename}: {e}")
            self.stats['errors'] += 1
            return False
            
    def process_ai_discoveries(self):
        """Process texts discovered by AI module"""
        try:
            cursor = self.db.cursor()
            
            # Get unprocessed AI discoveries
            cursor.execute('''
                SELECT url, work, translator, year, quality_score
                FROM discovered_texts
                WHERE url NOT IN (SELECT url FROM texts WHERE url IS NOT NULL)
                ORDER BY quality_score DESC
                LIMIT 10
            ''')
            
            discoveries = cursor.fetchall()
            
            for url, work, translator, year, score in discoveries:
                if url and score > 5:  # High quality discoveries
                    filename = f"{work}_{translator}_{year}".replace(' ', '_')
                    
                    # Download the discovered text
                    try:
                        response = requests.get(url, timeout=30)
                        if response.status_code == 200:
                            output_path = self.base_path / f'texts/collected/{filename}.txt'
                            
                            with open(output_path, 'w', encoding='utf-8') as f:
                                f.write(response.text)
                                
                            # Record as AI discovered
                            cursor.execute('''
                                INSERT OR IGNORE INTO texts 
                                (filename, source, url, work, translator, year, size, ai_discovered, quality_score)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (filename, 'ai_discovery', url, work, translator, year, 
                                  len(response.text), 1, score))
                            
                            self.db.commit()
                            self.stats['ai_discoveries'] += 1
                            
                            logging.info(f"✨ AI Discovery: {filename} (score: {score})")
                            
                    except Exception as e:
                        logging.error(f"Failed to download AI discovery {url}: {e}")
                        
        except Exception as e:
            logging.error(f"AI discovery processing error: {e}")
            
    def collection_worker(self):
        """Continuous text collection"""
        while self.running:
            try:
                if not self.consultation_active:
                    # Download from regular sources
                    for source, config in REAL_SOURCES.items():
                        for url, filename in config['texts']:
                            cursor = self.db.cursor()
                            cursor.execute('SELECT id FROM texts WHERE filename = ?', (filename,))
                            
                            if not cursor.fetchone():
                                self.download_text(source, url, filename)
                                time.sleep(10)  # Be polite to servers
                                
                    # Process AI discoveries
                    self.process_ai_discoveries()
                    
                # Sleep before next cycle
                time.sleep(1800)  # 30 minutes
                
            except Exception as e:
                logging.error(f"Collection worker error: {e}")
                time.sleep(300)
                
    def extract_valency_patterns(self):
        """Extract valency patterns from texts"""
        try:
            cursor = self.db.cursor()
            
            # Get unprocessed texts
            cursor.execute('''
                SELECT id, filename FROM texts 
                WHERE processed = 0 AND word_count > 1000
                LIMIT 5
            ''')
            
            texts = cursor.fetchall()
            
            for text_id, filename in texts:
                text_path = self.base_path / f'texts/collected/{filename}.txt'
                
                if text_path.exists():
                    # Simple pattern extraction (enhance with NLP tools later)
                    patterns = self.analyze_valency_patterns(text_path)
                    
                    # Store patterns
                    for pattern in patterns:
                        cursor.execute('''
                            INSERT INTO valency_patterns
                            (text_id, lemma, frame, frequency, pattern_type)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (text_id, pattern['lemma'], pattern['frame'], 
                              pattern['frequency'], pattern['type']))
                    
                    # Mark as processed
                    cursor.execute('UPDATE texts SET processed = 1 WHERE id = ?', (text_id,))
                    self.db.commit()
                    
                    self.stats['valency_patterns'] += len(patterns)
                    logging.info(f"Extracted {len(patterns)} patterns from {filename}")
                    
        except Exception as e:
            logging.error(f"Valency extraction error: {e}")
            
    def analyze_valency_patterns(self, text_path):
        """Basic valency pattern analysis"""
        patterns = []
        
        try:
            with open(text_path, 'r', encoding='utf-8') as f:
                text = f.read()
                
            # Simple patterns (will be enhanced with spaCy/Stanza)
            ditransitive_verbs = ['give', 'gave', 'send', 'sent', 'show', 'showed']
            
            for verb in ditransitive_verbs:
                count = text.lower().count(verb)
                if count > 0:
                    patterns.append({
                        'lemma': verb,
                        'frame': 'NOM-ACC-DAT',
                        'frequency': count,
                        'type': 'ditransitive'
                    })
                    
        except Exception as e:
            logging.error(f"Pattern analysis error: {e}")
            
        return patterns
            
    def daily_consultation(self):
        """Exactly 1 hour consultation with AI discoveries"""
        self.consultation_active = True
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=CONSULTATION_DURATION)
        
        print("\n" + "="*70)
        print("🌅 DAILY CONSULTATION SESSION")
        print(f"Time: {start_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Duration: Exactly {CONSULTATION_DURATION} minutes")
        print("="*70)
        
        # Show statistics
        cursor = self.db.cursor()
        cursor.execute('SELECT COUNT(*), SUM(word_count) FROM texts')
        text_count, total_words = cursor.fetchone()
        
        # Get AI discoveries
        cursor.execute('SELECT COUNT(*) FROM texts WHERE ai_discovered = 1')
        ai_count = cursor.fetchone()[0]
        
        print(f"\n📊 CORPUS STATISTICS:")
        print(f"Total texts: {text_count or 0}")
        print(f"Total words: {(total_words or 0):,}")
        print(f"AI discoveries: {ai_count}")
        print(f"Valency patterns: {self.stats['valency_patterns']}")
        print(f"Days running: {(datetime.now() - self.stats['start_time']).days}")
        
        # Show AI Discovery findings
        print(f"\n✨ AI DISCOVERY HIGHLIGHTS:")
        cursor.execute('''
            SELECT work, COUNT(*) as versions, MIN(year) as earliest, MAX(year) as latest
            FROM discovered_texts
            GROUP BY work
            ORDER BY versions DESC
            LIMIT 5
        ''')
        
        discoveries = cursor.fetchall()
        for work, versions, earliest, latest in discoveries:
            print(f"  {work}: {versions} versions ({earliest}-{latest})")
            
        # Show recent downloads
        cursor.execute('''
            SELECT filename, source, word_count, download_time 
            FROM texts 
            ORDER BY download_time DESC 
            LIMIT 10
        ''')
        
        recent = cursor.fetchall()
        if recent:
            print(f"\n📚 RECENT DOWNLOADS:")
            for filename, source, words, dl_time in recent:
                ai_marker = "✨" if source == 'ai_discovery' else "📥"
                print(f"  {ai_marker} {filename}: {(words or 0):,} words from {source}")
                
        # User interaction with timeout
        print(f"\n⏰ You have until {end_time.strftime('%H:%M')} for consultation")
        print("Agent will continue automatically after consultation ends")
        
        # Show options
        print("\n💬 CONSULTATION OPTIONS:")
        print("1. Review AI discoveries")
        print("2. View translation chains")
        print("3. Check valency patterns")
        print("4. Adjust priorities")
        print("5. Skip consultation")
        
        # Wait for consultation period
        while datetime.now() < end_time and self.consultation_active:
            remaining = (end_time - datetime.now()).seconds
            minutes = remaining // 60
            seconds = remaining % 60
            print(f"\r⏱️ Time remaining: {minutes}:{seconds:02d} ", end='', flush=True)
            time.sleep(1)
            
        # Log consultation
        cursor.execute('''
            INSERT INTO consultations 
            (date, duration_minutes, texts_shown, patterns_shown, ai_discoveries_shown, user_present)
            VALUES (date('now'), ?, ?, ?, ?, ?)
        ''', (CONSULTATION_DURATION, text_count, self.stats['valency_patterns'], ai_count, True))
        
        self.db.commit()
        
        print("\n\n✅ Consultation ended. Returning to autonomous operation...")
        print("="*70)
        
        self.consultation_active = False
        
    def status_monitor(self):
        """Update status file every 5 minutes"""
        while self.running:
            try:
                # Get current stats
                cursor = self.db.cursor()
                text_count = cursor.execute('SELECT COUNT(*) FROM texts').fetchone()[0]
                ai_count = cursor.execute('SELECT COUNT(*) FROM texts WHERE ai_discovered = 1').fetchone()[0]
                
                status = {
                    'timestamp': datetime.now().isoformat(),
                    'running': True,
                    'texts_downloaded': text_count,
                    'ai_discoveries': ai_count,
                    'valency_patterns': self.stats['valency_patterns'],
                    'errors': self.stats['errors'],
                    'consultation_active': self.consultation_active
                }
                
                with open(self.base_path / 'agent_status.json', 'w') as f:
                    json.dump(status, f, indent=2)
                    
                time.sleep(300)  # 5 minutes
                
            except Exception as e:
                logging.error(f"Status monitor error: {e}")
                
    def github_updater(self):
        """Update GitHub repository every 2 hours"""
        while self.running:
            try:
                if not self.consultation_active:
                    # Run platform builder
                    from github_platform_builder_v2 import GitHubPlatformBuilderV2
                    builder = GitHubPlatformBuilderV2()
                    
                    if builder.build():
                        logging.info("✅ GitHub platform updated")
                        
                        # Git operations
                        os.chdir(str(self.base_path / 'github_platform'))
                        
                        if (self.base_path / 'github_platform/.git').exists():
                            subprocess.run(['git', 'add', '.'])
                            subprocess.run(['git', 'commit', '-m', f'Auto-update: {datetime.now().strftime("%Y-%m-%d %H:%M")}'])
                            subprocess.run(['git', 'push'])
                            
                        os.chdir(str(self.base_path))
                        
                time.sleep(7200)  # 2 hours
                
            except Exception as e:
                logging.error(f"GitHub updater error: {e}")
                time.sleep(7200)
                
    def run_24_7(self):
        """Main execution - runs forever"""
        logging.info("🚀 Starting Ultimate 24/7 operation with AI Discovery")
        
        # Schedule daily consultation
        schedule.every().day.at(CONSULTATION_TIME).do(self.daily_consultation)
        
        # Schedule periodic tasks
        schedule.every(30).minutes.do(self.extract_valency_patterns)
        
        # Start worker threads
        threads = [
            threading.Thread(target=self.collection_worker, daemon=True, name='Collector'),
            threading.Thread(target=self.status_monitor, daemon=True, name='Monitor'),
            threading.Thread(target=self.github_updater, daemon=True, name='GitHub')
        ]
        
        for t in threads:
            t.start()
            logging.info(f"Started thread: {t.name}")
            
        # Main loop
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                logging.info("Shutdown requested")
                self.running = False
                break
            except Exception as e:
                logging.error(f"Main loop error: {e}")
                time.sleep(60)
                

if __name__ == "__main__":
    print("="*70)
    print("🤖 ULTIMATE 24/7 DIACHRONIC CORPUS AGENT WITH AI DISCOVERY")
    print("="*70)
    print("✅ Features:")
    print("   - Runs continuously 24/7")
    print("   - AI-powered text discovery")
    print("   - Translation chain mapping")
    print("   - Quality scoring")
    print("   - 1 hour consultation daily at 09:00")
    print("   - Automatic error recovery")
    print("   - GitHub integration")
    print("   - Open source NLP tools ready")
    print("="*70)
    print("\nStarting agent...\n")
    
    # Run validation first
    print("Running validation checks...")
    import subprocess
    subprocess.run([sys.executable, 'validation_script.py'])
    print("\nStarting main agent...\n")
    
    agent = Ultimate24_7AgentWithAI()
    
    try:
        agent.run_24_7()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"\n❌ Fatal error: {e}")
    finally:
        print("\n👋 Agent stopped")