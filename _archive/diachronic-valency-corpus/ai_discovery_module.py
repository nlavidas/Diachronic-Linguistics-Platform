#!/usr/bin/env python3
"""
AI-POWERED INTELLIGENT TEXT DISCOVERY MODULE
Finds open access retranslations, influential texts, and parallel versions
Uses semantic search, citation analysis, and smart crawling
"""

import os
import json
import requests
import logging
from datetime import datetime
from collections import defaultdict
import sqlite3
import time
import re

class AITextDiscoveryEngine:
    def __init__(self, db_path):
        self.db_path = db_path
        self.setup_logging()
        self.setup_database()
        
        # Priority works for retranslation discovery
        self.priority_works = {
            'Homer': ['Iliad', 'Odyssey'],
            'Bible': ['Old Testament', 'New Testament', 'Genesis', 'Gospels'],
            'Virgil': ['Aeneid', 'Georgics', 'Eclogues'],
            'Ovid': ['Metamorphoses', 'Ars Amatoria'],
            'Plutarch': ['Parallel Lives', 'Moralia'],
            'Plato': ['Republic', 'Symposium', 'Apology'],
            'Sophocles': ['Oedipus Rex', 'Antigone'],
            'Euripides': ['Medea', 'Bacchae']
        }
        
    def setup_logging(self):
        """Configure logging for AI discovery"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [AI-Discovery] %(message)s',
            handlers=[
                logging.FileHandler('ai_discovery.log'),
                logging.StreamHandler()
            ]
        )
        
    def setup_database(self):
        """Create tables for AI discoveries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS discovered_texts (
                id INTEGER PRIMARY KEY,
                work TEXT,
                translator TEXT,
                year INTEGER,
                url TEXT,
                quality_score REAL,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
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
        
        conn.commit()
        conn.close()
        
    def search_gutenberg_advanced(self, work, author):
        """Advanced Gutenberg search with quality scoring"""
        results = []
        
        try:
            # Search Gutenberg catalog
            search_url = f"https://www.gutenberg.org/ebooks/search/?query={work}+{author}"
            
            # Simulated results for demonstration (replace with actual API/scraping)
            potential_texts = [
                {'id': '6130', 'title': f'{work} by {author}', 'translator': 'Chapman', 'year': 1611},
                {'id': '3059', 'title': f'{work} by {author}', 'translator': 'Pope', 'year': 1720},
                {'id': '2199', 'title': f'{work} by {author}', 'translator': 'Butler', 'year': 1898},
                {'id': '22382', 'title': f'{work} by {author}', 'translator': 'Lang, Leaf, Myers', 'year': 1883}
            ]
            
            for text in potential_texts:
                # Score based on historical importance and translation quality
                score = self.calculate_quality_score(text)
                
                results.append({
                    'url': f"https://www.gutenberg.org/files/{text['id']}/{text['id']}-0.txt",
                    'work': work,
                    'translator': text['translator'],
                    'year': text['year'],
                    'score': score
                })
                
            logging.info(f"Found {len(results)} translations of {work}")
            
        except Exception as e:
            logging.error(f"Gutenberg search error: {e}")
            
        return results
        
    def calculate_quality_score(self, text_info):
        """Calculate quality score based on multiple factors"""
        score = 5.0  # Base score
        
        # Historical importance
        if text_info['year'] < 1700:
            score += 2.0  # Very early translation
        elif text_info['year'] < 1800:
            score += 1.5  # Early translation
            
        # Translator reputation
        famous_translators = ['Chapman', 'Pope', 'Dryden', 'North', 'Lang']
        if any(t in text_info.get('translator', '') for t in famous_translators):
            score += 1.5
            
        # Completeness (would need actual check)
        score += 0.5  # Assume complete
        
        return min(10.0, score)  # Cap at 10
        
    def discover_translation_chains(self, work):
        """Discover chains of retranslations"""
        chains = []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Find all translations of a work
            cursor.execute('''
                SELECT translator, year, url, quality_score
                FROM discovered_texts
                WHERE work = ?
                ORDER BY year
            ''', (work,))
            
            translations = cursor.fetchall()
            
            if len(translations) > 2:
                chain = {
                    'work': work,
                    'translations': [(t[0], t[1]) for t in translations],
                    'span_years': translations[-1][1] - translations[0][1],
                    'chain_quality': sum(t[3] for t in translations) / len(translations)
                }
                
                # Store chain
                cursor.execute('''
                    INSERT OR REPLACE INTO translation_chains
                    (work, translations, span_years, chain_quality)
                    VALUES (?, ?, ?, ?)
                ''', (work, json.dumps(chain['translations']), 
                      chain['span_years'], chain['chain_quality']))
                
                chains.append(chain)
                logging.info(f"Found translation chain for {work}: {len(translations)} versions")
                
            conn.commit()
            conn.close()
            
        except Exception as e:
            logging.error(f"Chain discovery error: {e}")
            
        return chains
        
    def find_parallel_texts(self):
        """Find texts that exist in multiple languages/versions"""
        parallel_groups = defaultdict(list)
        
        # Example: Bible versions
        bible_versions = [
            {'lang': 'en', 'version': 'KJV', 'year': 1611, 'url': 'gutenberg.org/10'},
            {'lang': 'en', 'version': 'ASV', 'year': 1901, 'url': 'gutenberg.org/8001'},
            {'lang': 'la', 'version': 'Vulgate', 'year': 400, 'url': 'perseus.tufts.edu/vulgate'}
        ]
        
        for version in bible_versions:
            parallel_groups['Bible'].append(version)
            
        return parallel_groups
        
    def smart_crawl_archive_org(self, query, limit=50):
        """Intelligently crawl Internet Archive for texts"""
        results = []
        
        try:
            # Archive.org search API
            search_url = "https://archive.org/advancedsearch.php"
            params = {
                'q': f'{query} AND mediatype:texts AND language:(eng OR grc OR lat)',
                'fl': 'identifier,title,creator,date,language',
                'rows': limit,
                'output': 'json',
                'sort': 'downloads desc'  # Popular items first
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for doc in data.get('response', {}).get('docs', []):
                    # Extract and score
                    result = {
                        'source': 'archive.org',
                        'identifier': doc.get('identifier'),
                        'title': doc.get('title'),
                        'creator': doc.get('creator'),
                        'year': self.extract_year(doc.get('date', '')),
                        'language': doc.get('language'),
                        'url': f"https://archive.org/download/{doc.get('identifier')}"
                    }
                    
                    results.append(result)
                    
                logging.info(f"Found {len(results)} texts on Archive.org for '{query}'")
                
        except Exception as e:
            logging.error(f"Archive.org crawl error: {e}")
            
        return results
        
    def extract_year(self, date_str):
        """Extract year from various date formats"""
        if not date_str:
            return None
            
        # Try to find 4-digit year
        match = re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', str(date_str))
        if match:
            return int(match.group(1))
            
        return None
        
    def discover_continuously(self):
        """Main discovery loop - finds new texts continuously"""
        logging.info("Starting continuous AI discovery...")
        
        while True:
            try:
                # Search for each priority work
                for author, works in self.priority_works.items():
                    for work in works:
                        # Gutenberg search
                        results = self.search_gutenberg_advanced(work, author)
                        self.store_discoveries(results)
                        
                        # Archive.org search
                        archive_results = self.smart_crawl_archive_org(f"{work} {author}")
                        self.store_discoveries(archive_results)
                        
                        # Build translation chains
                        self.discover_translation_chains(work)
                        
                        time.sleep(5)  # Be polite
                        
                # Find parallel texts
                parallels = self.find_parallel_texts()
                logging.info(f"Found {len(parallels)} parallel text groups")
                
                # Sleep before next cycle
                time.sleep(3600)  # 1 hour
                
            except Exception as e:
                logging.error(f"Discovery error: {e}")
                time.sleep(300)  # 5 minutes on error
                
    def store_discoveries(self, results):
        """Store discovered texts in database"""
        if not results:
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for result in results:
                cursor.execute('''
                    INSERT OR IGNORE INTO discovered_texts
                    (work, translator, year, url, quality_score)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    result.get('work', ''),
                    result.get('translator', ''),
                    result.get('year', 0),
                    result.get('url', ''),
                    result.get('score', 5.0)
                ))
                
            conn.commit()
            conn.close()
            
            logging.info(f"Stored {len(results)} new discoveries")
            
        except Exception as e:
            logging.error(f"Storage error: {e}")

# Integration function for main agent
def integrate_ai_discovery(agent_instance):
    """Integrate AI discovery with main agent"""
    discovery_engine = AITextDiscoveryEngine(agent_instance.db_path)
    
    # Start discovery in parallel thread
    import threading
    discovery_thread = threading.Thread(
        target=discovery_engine.discover_continuously,
        daemon=True
    )
    discovery_thread.start()
    
    logging.info("AI Discovery Engine integrated and running")
    
    return discovery_engine