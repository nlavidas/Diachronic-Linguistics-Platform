#!/usr/bin/env python3
"""
Fixed Smart Text Scraper with Better Filename Handling
"""

import requests
import json
import time
import re
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime
import unicodedata

class SmartScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Academic Research Bot)'
        })
        self.stats = {
            'downloaded': 0,
            'failed': 0,
            'skipped': 0
        }
        self.processed_files = []
    
    def sanitize_filename(self, title):
        """Create safe filename from title"""
        # Remove or replace problematic characters
        title = title.strip()
        
        # Normalize unicode
        title = unicodedata.normalize('NFKD', title)
        
        # Remove non-ASCII characters for safety
        title = ''.join(c for c in title if ord(c) < 128)
        
        # Remove Windows-forbidden characters
        forbidden = '<>:"/\\|?*\r\n\t'
        for char in forbidden:
            title = title.replace(char, '')
        
        # Replace multiple spaces with single space
        title = re.sub(r'\s+', ' ', title)
        
        # Truncate to reasonable length
        title = title[:80].strip()
        
        # If title is empty after cleaning, use hash
        if not title:
            title = f"text_{hashlib.md5(title.encode()).hexdigest()[:8]}"
        
        return title
    
    def extract_text_from_html(self, html_content):
        """Extract clean text from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def download_and_extract(self, url_entry):
        """Download and extract text based on source"""
        url = url_entry['url']
        source = url_entry.get('source', '')
        
        try:
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                return None
            
            content = response.text
            
            # Process based on source
            if source == 'gutenberg':
                # Remove Gutenberg headers/footers
                content = self.clean_gutenberg(content)
            elif source == 'wikisource':
                # Extract from HTML
                content = self.extract_text_from_html(content)
            elif source == 'sacred_texts':
                # Extract from HTML
                content = self.extract_text_from_html(content)
            else:
                # Try to detect format
                if '<html' in content.lower():
                    content = self.extract_text_from_html(content)
            
            return content
            
        except Exception as e:
            print(f"    Error downloading: {e}")
            return None
    
    def clean_gutenberg(self, text):
        """Remove Project Gutenberg headers and footers"""
        markers = [
            '*** START OF THIS PROJECT GUTENBERG',
            '*** START OF THE PROJECT GUTENBERG',
            '*** END OF THIS PROJECT GUTENBERG',
            '*** END OF THE PROJECT GUTENBERG',
            '*END*THE SMALL PRINT',
            'End of the Project Gutenberg'
        ]
        
        for marker in markers:
            if marker in text:
                if 'START' in marker:
                    text = text.split(marker, 1)[-1]
                else:
                    text = text.split(marker, 1)[0]
        
        return text.strip()
    
    def is_primary_text(self, title, text):
        """Check if this is a primary text (not dictionary/grammar)"""
        # Skip obvious non-primary texts
        skip_keywords = [
            'Dictionary', 'Lexicon', 'Grammar', 'Primer', 
            'Commentary', 'Index', 'Glossary', 'Encyclopedia',
            'How to', 'Art of', 'Guide to'
        ]
        
        for keyword in skip_keywords:
            if keyword.lower() in title.lower():
                return False
        
        # Check content for dictionary patterns
        if text:
            lines = text.split('\n')[:50]  # Check first 50 lines
            definition_count = sum(1 for line in lines if '--' in line or '=' in line)
            if definition_count > 10:  # Likely a dictionary
                return False
        
        return True
    
    def scrape_all(self):
        """Main scraping function"""
        print("Starting Smart Scraping...")
        print("Filtering for PRIMARY TEXTS only (no dictionaries/grammars)...")
        
        # Load URLs
        urls_dir = Path('corpus_urls/universal')
        if not urls_dir.exists():
            print(f"Error: {urls_dir} not found. Run universal_harvester.py first.")
            return
            
        # Find latest URL file
        url_files = list(urls_dir.glob('universal_urls_*.json'))
        if not url_files:
            print("No URL files found. Run universal_harvester.py first.")
            return
            
        latest_file = max(url_files)
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            urls = json.load(f)
        
        print(f"Processing {len(urls)} URLs...")
        
        # Create output directories by category
        base_dir = Path('corpus_texts')
        categories = {
            'greek': base_dir / 'greek_texts' / 'harvested',
            'latin': base_dir / 'latin_texts',
            'french': base_dir / 'middle_french_texts',
            'biblical': base_dir / 'biblical_texts',
            'classical': base_dir / 'classical_texts',
            'medieval': base_dir / 'medieval_texts',
            'english': base_dir / 'english_retranslations',
            'uncategorized': base_dir / 'all_texts'
        }
        
        for cat_dir in categories.values():
            cat_dir.mkdir(parents=True, exist_ok=True)
        
        for i, url_entry in enumerate(urls, 1):
            title = url_entry.get('title', 'Untitled')
            category = url_entry.get('category', 'uncategorized')
            
            print(f"\n[{i}/{len(urls)}] {title}")
            
            # Download and extract text
            text = self.download_and_extract(url_entry)
            
            if text and len(text) > 500:  # Minimum 500 characters
                # Check if primary text
                if not self.is_primary_text(title, text):
                    print(f"    Skipped: Not a primary text (likely dictionary/grammar)")
                    self.stats['skipped'] += 1
                    continue
                
                # Determine output directory
                output_dir = categories.get(category, categories['uncategorized'])
                
                # Create safe filename
                safe_title = self.sanitize_filename(title)
                filename = output_dir / f"{safe_title}.txt"
                
                # Handle duplicates
                counter = 1
                while filename.exists():
                    filename = output_dir / f"{safe_title}_{counter}.txt"
                    counter += 1
                
                try:
                    filename.write_text(text, encoding='utf-8')
                    self.stats['downloaded'] += 1
                    self.processed_files.append({
                        'filename': str(filename),
                        'title': title,
                        'category': category,
                        'size': len(text)
                    })
                    print(f"    Saved: {len(text)} characters to {category}")
                except Exception as e:
                    print(f"    Error saving file: {e}")
                    self.stats['failed'] += 1
            else:
                self.stats['skipped'] += 1
                print(f"    Skipped: Too short or empty")
            
            time.sleep(0.5)  # Rate limiting
        
        # Save processing log
        self.save_processing_log()
        
        # Print statistics
        print("\n" + "="*60)
        print("SCRAPING COMPLETE")
        print(f"Downloaded: {self.stats['downloaded']} PRIMARY TEXTS")
        print(f"Skipped: {self.stats['skipped']} (dictionaries/grammars/short texts)")
        print(f"Failed: {self.stats['failed']}")
        print("\nTexts saved to categorized folders in corpus_texts/")
    
    def save_processing_log(self):
        """Save detailed log of processed files"""
        log_dir = Path('corpus_metadata')
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f'scraping_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'statistics': self.stats,
            'processed_files': self.processed_files
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nProcessing log saved to: {log_file}")

if __name__ == '__main__':
    scraper = SmartScraper()
    scraper.scrape_all()