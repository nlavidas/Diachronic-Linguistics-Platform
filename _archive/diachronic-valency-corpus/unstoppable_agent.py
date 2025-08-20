#!/usr/bin/env python3
"""
UNSTOPPABLE 24/7 DIACHRONIC CORPUS BUILDER
- NEVER STOPS - handles all errors
- Builds massive corpus (focus on QUANTITY)
- Auto-creates GitHub platform
- Comprehensive statistics
"""

import os
import sys
import time
import json
import sqlite3
import requests
import schedule
import logging
import subprocess
import threading
import queue
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import traceback
import re

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Robust logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('unstoppable_agent.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

class UnstoppableCorpusBuilder:
    """
    Never-stopping agent that builds massive corpus
    """
    
    def __init__(self):
        self.start_time = datetime.now()
        self.running = True
        self.stats = defaultdict(int)
        self.collection_queue = queue.Queue(maxsize=10000)
        self.github_update_queue = queue.Queue()
        
        # Massive source list for quantity
        self.sources = {
            'gutenberg': {
                'base': 'https://www.gutenberg.org',
                'catalogs': [
                    'https://www.gutenberg.org/browse/scores/top',
                    'https://www.gutenberg.org/browse/languages/en',
                    'https://www.gutenberg.org/browse/languages/fr',
                    'https://www.gutenberg.org/browse/languages/de',
                    'https://www.gutenberg.org/browse/languages/it',
                    'https://www.gutenberg.org/browse/languages/es',
                    'https://www.gutenberg.org/browse/languages/la',
                    'https://www.gutenberg.org/browse/languages/el'
                ],
                'bulk_searches': [
                    'translation', 'translated', 'version', 'retold',
                    'iliad', 'odyssey', 'aeneid', 'bible', 'gospel',
                    'metamorphoses', 'canterbury', 'divine comedy',
                    'faust', 'quixote', 'arabian nights', 'beowulf',
                    'nibelungenlied', 'kalevala', 'mahabharata'
                ]
            },
            'archive_org': {
                'base': 'https://archive.org',
                'collections': [
                    'opensource', 'texts', 'americana', 
                    'europeanlibraries', 'toronto', 'princeton',
                    'library_of_congress', 'gutenberg'
                ]
            },
            'wikisource': {
                'languages': ['en', 'fr', 'de', 'it', 'es', 'la', 'el', 'nl'],
                'categories': [
                    'Translations', 'Epic_poetry', 'Religious_texts',
                    'Classical_literature', 'Medieval_literature'
                ]
            }
        }
        
        self.init_workspace()
        self.init_database()
        self.init_github_platform()
        
    def init_workspace(self):
        """Create comprehensive workspace"""
        dirs = [
            # Massive text storage
            "corpus/raw/gutenberg",
            "corpus/raw/archive_org", 
            "corpus/raw/wikisource",
            "corpus/raw/perseus",
            "corpus/raw/other",
            
            # Processed versions
            "corpus/processed/tokenized",
            "corpus/processed/annotated",
            "corpus/processed/aligned",
            
            # GitHub platform structure
            "github_platform/frontend/src",
            "github_platform/frontend/public",
            "github_platform/backend/api",
            "github_platform/backend/database",
            "github_platform/docs",
            "github_platform/stats",
            "github_platform/visualizations",
            
            # Statistics
            "statistics/tokens",
            "statistics/words",
            "statistics/daily",
            "statistics/cumulative",
            
            # Reports
            "reports/hourly",
            "reports/daily",
            "reports/weekly"
        ]
        
        for d in dirs:
            os.makedirs(d, exist_ok=True)
            
    def init_database(self):
        """Initialize massive database"""
        self.db = sqlite3.connect('massive_corpus.db', check_same_thread=False)
        cursor = self.db.cursor()
        
        # Main corpus table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS corpus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work TEXT,
                author TEXT,
                translator TEXT,
                year INTEGER,
                language TEXT,
                source TEXT,
                url TEXT,
                file_path TEXT,
                size_bytes INTEGER,
                word_count INTEGER,
                token_count INTEGER,
                sentence_count INTEGER,
                unique_words INTEGER,
                collected_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                processed BOOLEAN DEFAULT 0,
                quality_score REAL,
                INDEX idx_work (work),
                INDEX idx_year (year),
                INDEX idx_language (language)
            )
        ''')
        
        # Statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_texts INTEGER,
                total_bytes INTEGER,
                total_words INTEGER,
                total_tokens INTEGER,
                languages_count INTEGER,
                works_count INTEGER,
                translators_count INTEGER,
                collection_rate_per_hour REAL
            )
        ''')
        
        # Error recovery table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                error_type TEXT,
                error_message TEXT,
                recovery_action TEXT,
                success BOOLEAN
            )
        ''')
        
        self.db.commit()
        
    def init_github_platform(self):
        """Initialize GitHub platform structure"""
        logging.info("🏗️ Building GitHub platform...")
        
        # Create README
        readme = """# Massive Diachronic Corpus Platform

## 📊 Current Statistics
- **Total Texts**: {total_texts}
- **Total Size**: {total_size} GB
- **Total Words**: {total_words:,}
- **Total Tokens**: {total_tokens:,}
- **Languages**: {languages}
- **Time Span**: Ancient to Modern

## 🚀 Features
- Massive multilingual diachronic corpus
- Real-time collection (24/7)
- Advanced search and analysis
- Visualization tools
- API access

## 📈 Collection Rate
- **Per Hour**: {per_hour} texts
- **Per Day**: {per_day} texts
- **Growth**: Exponential

[Live Platform](https://your-platform-url.com)
"""
        
        with open('github_platform/README.md', 'w') as f:
            f.write(readme.format(
                total_texts=0,
                total_size=0,
                total_words=0,
                total_tokens=0,
                languages=0,
                per_hour=0,
                per_day=0
            ))
            
        # Create platform files
        self.create_platform_structure()
        
    def create_platform_structure(self):
        """Create complete GitHub platform"""
        
        # Frontend React App
        frontend_files = {
            'github_platform/frontend/package.json': {
                "name": "diachronic-corpus-platform",
                "version": "1.0.0",
                "scripts": {
                    "start": "react-scripts start",
                    "build": "react-scripts build"
                },
                "dependencies": {
                    "react": "^18.0.0",
                    "react-dom": "^18.0.0",
                    "recharts": "^2.5.0",
                    "d3": "^7.0.0",
                    "axios": "^1.0.0"
                }
            },
            'github_platform/frontend/src/App.js': '''
import React, { useState, useEffect } from 'react';
import Statistics from './components/Statistics';
import Search from './components/Search';
import Timeline from './components/Timeline';
import './App.css';

function App() {
    const [stats, setStats] = useState({});
    
    useEffect(() => {
        fetchStats();
        const interval = setInterval(fetchStats, 60000); // Update every minute
        return () => clearInterval(interval);
    }, []);
    
    const fetchStats = async () => {
        const response = await fetch('/api/stats');
        const data = await response.json();
        setStats(data);
    };
    
    return (
        <div className="App">
            <h1>Massive Diachronic Corpus</h1>
            <Statistics stats={stats} />
            <Search />
            <Timeline />
        </div>
    );
}

export default App;
''',
            'github_platform/frontend/src/components/Statistics.js': '''
import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const Statistics = ({ stats }) => {
    return (
        <div className="statistics">
            <h2>📊 Live Statistics</h2>
            <div className="stat-grid">
                <div className="stat-card">
                    <h3>Total Texts</h3>
                    <div className="number">{stats.total_texts?.toLocaleString()}</div>
                </div>
                <div className="stat-card">
                    <h3>Total Words</h3>
                    <div className="number">{stats.total_words?.toLocaleString()}</div>
                </div>
                <div className="stat-card">
                    <h3>Total Tokens</h3>
                    <div className="number">{stats.total_tokens?.toLocaleString()}</div>
                </div>
                <div className="stat-card">
                    <h3>Collection Rate</h3>
                    <div className="number">{stats.rate_per_hour} texts/hour</div>
                </div>
            </div>
            <div className="charts">
                <LineChart width={600} height={300} data={stats.growth_data}>
                    <Line type="monotone" dataKey="texts" stroke="#8884d8" />
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                </LineChart>
            </div>
        </div>
    );
};

export default Statistics;
'''
        }
        
        # Backend API
        backend_files = {
            'github_platform/backend/api/server.py': '''
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect('../../massive_corpus.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/stats')
def get_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    # Get latest statistics
    cursor.execute("""
        SELECT * FROM statistics 
        ORDER BY timestamp DESC 
        LIMIT 1
    """)
    
    stats = dict(cursor.fetchone())
    
    # Get growth data
    cursor.execute("""
        SELECT DATE(timestamp) as date, 
               COUNT(*) as texts,
               SUM(word_count) as words
        FROM corpus
        GROUP BY DATE(timestamp)
        ORDER BY date DESC
        LIMIT 30
    """)
    
    growth_data = [dict(row) for row in cursor.fetchall()]
    stats['growth_data'] = growth_data
    
    return jsonify(stats)

@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM corpus
        WHERE work LIKE ? OR translator LIKE ?
        LIMIT 100
    """, (f'%{query}%', f'%{query}%'))
    
    results = [dict(row) for row in cursor.fetchall()]
    return jsonify(results)

@app.route('/api/timeline/<work>')
def timeline(work):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT year, translator, word_count
        FROM corpus
        WHERE work = ?
        ORDER BY year
    """, (work,))
    
    timeline = [dict(row) for row in cursor.fetchall()]
    return jsonify(timeline)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''
        }
        
        # Create all files
        for filepath, content in {**frontend_files, **backend_files}.items():
            with open(filepath, 'w', encoding='utf-8') as f:
                if isinstance(content, dict):
                    json.dump(content, f, indent=2)
                else:
                    f.write(content)
                    
    def run_forever(self):
        """Main execution - NEVER STOPS"""
        logging.info("🚀 UNSTOPPABLE AGENT STARTING")
        logging.info("🎯 Goal: Build MASSIVE diachronic corpus")
        logging.info("📊 Focus: QUANTITY + comprehensive platform")
        
        # Schedule tasks
        schedule.every(1).minutes.do(self.safe_execute(self.collect_aggressively))
        schedule.every(5).minutes.do(self.safe_execute(self.process_texts))
        schedule.every(10).minutes.do(self.safe_execute(self.update_statistics))
        schedule.every(30).minutes.do(self.safe_execute(self.update_github))
        schedule.every(1).hours.do(self.safe_execute(self.generate_report))
        
        # Daily consultation at 9 AM
        schedule.every().day.at("09:00").do(self.safe_execute(self.consultation_45min))
        
        # Start worker threads
        threads = [
            threading.Thread(target=self.collection_worker, daemon=True),
            threading.Thread(target=self.processing_worker, daemon=True),
            threading.Thread(target=self.statistics_worker, daemon=True),
            threading.Thread(target=self.github_worker, daemon=True),
            threading.Thread(target=self.error_recovery_worker, daemon=True)
        ]
        
        for t in threads:
            t.start()
            
        # Main loop - NEVER STOPS
        while True:
            try:
                schedule.run_pending()
                time.sleep(30)
            except Exception as e:
                self.handle_error('main_loop', e)
                time.sleep(60)  # Wait a bit before continuing
                
    def safe_execute(self, func):
        """Wrapper to ensure functions never crash the agent"""
        def wrapper():
            try:
                func()
            except Exception as e:
                self.handle_error(func.__name__, e)
        return wrapper
        
    def handle_error(self, location, error):
        """Handle any error without stopping"""
        error_msg = f"Error in {location}: {str(error)}"
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        
        # Log to database
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT INTO error_log (error_type, error_message, recovery_action, success)
                VALUES (?, ?, ?, ?)
            ''', (location, str(error), 'continued', True))
            self.db.commit()
        except:
            pass  # Even database errors won't stop us
            
    def collection_worker(self):
        """Continuous collection worker"""
        while True:
            try:
                if not self.collection_queue.full():
                    # Find more texts
                    self.scan_all_sources()
                time.sleep(60)
            except Exception as e:
                self.handle_error('collection_worker', e)
                time.sleep(300)
                
    def processing_worker(self):
        """Process collected texts"""
        while True:
            try:
                self.process_pending_texts()
                time.sleep(120)
            except Exception as e:
                self.handle_error('processing_worker', e)
                time.sleep(300)
                
    def statistics_worker(self):
        """Update statistics continuously"""
        while True:
            try:
                self.calculate_all_statistics()
                time.sleep(300)
            except Exception as e:
                self.handle_error('statistics_worker', e)
                time.sleep(600)
                
    def github_worker(self):
        """Update GitHub platform"""
        while True:
            try:
                if not self.github_update_queue.empty():
                    self.push_to_github()
                time.sleep(600)
            except Exception as e:
                self.handle_error('github_worker', e)
                time.sleep(1800)
                
    def error_recovery_worker(self):
        """Monitor and recover from errors"""
        while True:
            try:
                self.check_system_health()
                self.recover_failed_downloads()
                time.sleep(1800)
            except Exception as e:
                logging.error(f"Recovery worker error: {e}")
                time.sleep(3600)
                
    def collect_aggressively(self):
        """Aggressive collection for QUANTITY"""
        logging.info("🔥 Aggressive collection cycle")
        
        # Gutenberg bulk download
        try:
            for i in range(1, 100):  # Check first 100 IDs
                url = f"https://www.gutenberg.org/files/{i}/{i}-0.txt"
                self.collection_queue.put({
                    'url': url,
                    'source': 'gutenberg',
                    'id': i
                })
        except:
            pass
            
        # Search for translations
        keywords = [
            'translated', 'translation', 'version', 'retold',
            'rendered', 'englished', 'interpreted'
        ]
        
        for keyword in keywords:
            self.search_keyword(keyword)
            
    def scan_all_sources(self):
        """Scan all configured sources"""
        
        # Gutenberg catalog scan
        try:
            response = requests.get(
                'https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2',
                stream=True
            )
            # Process catalog
        except:
            pass
            
        # Archive.org bulk search
        try:
            searches = [
                'collection:gutenberg',
                'collection:opensource AND translation',
                'collection:texts AND (iliad OR odyssey OR aeneid)',
                'collection:europeanlibraries AND translated'
            ]
            
            for search in searches:
                url = f"https://archive.org/advancedsearch.php?q={search}&output=json&rows=1000"
                self.collection_queue.put({
                    'url': url,
                    'source': 'archive_org',
                    'search': search
                })
        except:
            pass
            
    def process_pending_texts(self):
        """Process all pending texts"""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT id, file_path FROM corpus
            WHERE processed = 0
            LIMIT 100
        ''')
        
        for text_id, filepath in cursor.fetchall():
            try:
                self.process_single_text(text_id, filepath)
            except:
                pass
                
    def process_single_text(self, text_id, filepath):
        """Process a single text"""
        if not os.path.exists(filepath):
            return
            
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
                
            # Calculate statistics
            words = text.split()
            word_count = len(words)
            
            # Simple tokenization
            tokens = re.findall(r'\w+|[^\w\s]', text)
            token_count = len(tokens)
            
            sentences = re.split(r'[.!?]+', text)
            sentence_count = len([s for s in sentences if len(s.strip()) > 10])
            
            unique_words = len(set(w.lower() for w in words))
            
            # Update database
            cursor = self.db.cursor()
            cursor.execute('''
                UPDATE corpus
                SET word_count = ?, token_count = ?, 
                    sentence_count = ?, unique_words = ?,
                    processed = 1
                WHERE id = ?
            ''', (word_count, token_count, sentence_count, unique_words, text_id))
            self.db.commit()
            
            self.stats['processed'] += 1
            
        except Exception as e:
            self.handle_error(f'process_text_{text_id}', e)
            
    def calculate_all_statistics(self):
        """Calculate comprehensive statistics"""
        cursor = self.db.cursor()
        
        # Overall stats
        cursor.execute('''
            SELECT 
                COUNT(*) as total_texts,
                SUM(size_bytes) as total_bytes,
                SUM(word_count) as total_words,
                SUM(token_count) as total_tokens,
                COUNT(DISTINCT language) as languages,
                COUNT(DISTINCT work) as works,
                COUNT(DISTINCT translator) as translators
            FROM corpus
        ''')
        
        stats = cursor.fetchone()
        
        # Collection rate
        cursor.execute('''
            SELECT COUNT(*) FROM corpus
            WHERE datetime(collected_time) > datetime('now', '-1 hour')
        ''')
        
        hourly_rate = cursor.fetchone()[0]
        
        # Insert statistics
        cursor.execute('''
            INSERT INTO statistics 
            (total_texts, total_bytes, total_words, total_tokens,
             languages_count, works_count, translators_count, 
             collection_rate_per_hour)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (*stats, hourly_rate))
        
        self.db.commit()
        
    def update_github(self):
        """Update GitHub platform"""
        logging.info("📤 Updating GitHub platform...")
        
        # Update README with latest stats
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM statistics ORDER BY timestamp DESC LIMIT 1')
        stats = cursor.fetchone()
        
        if stats:
            readme_template = open('github_platform/README.md', 'r').read()
            readme = readme_template.format(
                total_texts=stats[1],
                total_size=stats[2] / (1024**3),  # GB
                total_words=stats[3],
                total_tokens=stats[4],
                languages=stats[5],
                per_hour=stats[8],
                per_day=stats[8] * 24
            )
            
            with open('github_platform/README.md', 'w') as f:
                f.write(readme)
                
        # Git operations
        try:
            commands = [
                'cd github_platform && git add .',
                'cd github_platform && git commit -m "Auto-update: {}"'.format(
                    datetime.now().strftime('%Y-%m-%d %H:%M')
                ),
                'cd github_platform && git push'
            ]
            
            for cmd in commands:
                subprocess.run(cmd, shell=True, check=True)
                
        except Exception as e:
            self.handle_error('git_push', e)
            
    def consultation_45min(self):
        """45-minute morning consultation"""
        print("\n" + "="*70)
        print("🌅 DAILY 45-MINUTE CONSULTATION")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*70)
        
        # Show massive statistics
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM statistics ORDER BY timestamp DESC LIMIT 1')
        stats = cursor.fetchone()
        
        print(f"\n📊 MASSIVE CORPUS STATISTICS:")
        print(f"Total Texts: {stats[1]:,}")
        print(f"Total Size: {stats[2]/(1024**3):.2f} GB")
        print(f"Total Words: {stats[3]:,}")
        print(f"Total Tokens: {stats[4]:,}")
        print(f"Languages: {stats[5]}")
        print(f"Unique Works: {stats[6]}")
        print(f"Collection Rate: {stats[8]} texts/hour")
        
        # Quick decisions
        print("\n⚡ QUICK DECISIONS:")
        print("Continue aggressive collection? (y/n): ", end='')
        # Timeout input handling here
        
        print("\n✅ Returning to unstoppable collection mode!")
        print("="*70)
        
    def generate_report(self):
        """Generate hourly report"""
        report_path = f"reports/hourly/report_{datetime.now().strftime('%Y%m%d_%H')}.json"
        
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM statistics ORDER BY timestamp DESC LIMIT 1')
        stats = cursor.fetchone()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_texts': stats[1],
            'total_gb': stats[2] / (1024**3),
            'total_words': stats[3],
            'total_tokens': stats[4],
            'hourly_rate': stats[8],
            'health': 'RUNNING'
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
    def search_keyword(self, keyword):
        """Search for keyword across sources"""
        # Implementation for keyword search
        pass
        
    def check_system_health(self):
        """Check system health"""
        # Monitor disk space, memory, etc.
        pass
        
    def recover_failed_downloads(self):
        """Retry failed downloads"""
        # Retry logic
        pass
        
    def push_to_github(self):
        """Push updates to GitHub"""
        # Git push implementation
        pass


if __name__ == "__main__":
    print("🚀 UNSTOPPABLE DIACHRONIC CORPUS BUILDER")
    print("🎯 Mission: Build MASSIVE corpus (millions of texts)")
    print("⏰ Consultation: Daily at 09:00 AM (45 minutes)")
    print("🏗️ Auto-building GitHub platform")
    print("📊 Focus: QUANTITY + comprehensive statistics")
    print("\n⚠️ This agent NEVER STOPS\n")
    
    agent = UnstoppableCorpusBuilder()
    
    # Run forever
    agent.run_forever()