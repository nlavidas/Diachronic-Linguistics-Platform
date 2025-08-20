#!/usr/bin/env python3
"""
scrape_greek_period_texts.py
Downloads and processes Greek texts with quality control and language verification
"""

import re
import time
import requests
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Set
from collections import Counter
import unicodedata

class GreekTextScraper:
    """Downloads and processes Greek texts with quality control"""
    
    # Greek character ranges for language detection
    GREEK_RANGES = [
        (0x0370, 0x03FF),  # Greek and Coptic
        (0x1F00, 0x1FFF),  # Greek Extended
    ]
    
    # Minimum text requirements
    MIN_WORDS = 100
    MIN_GREEK_RATIO = 0.3  # At least 30% Greek characters
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.processed_hashes = set()
        self.stats = {
            'downloaded': 0,
            'skipped': 0,
            'failed': 0,
            'duplicates': 0,
            'language_filtered': 0
        }
    
    def is_greek_char(self, char: str) -> bool:
        """Check if character is Greek"""
        code_point = ord(char)
        return any(start <= code_point <= end for start, end in self.GREEK_RANGES)
    
    def verify_greek_content(self, text: str) -> bool:
        """Verify text contains sufficient Greek content"""
        if len(text) < 100:
            return False
        
        # Count Greek vs non-Greek characters
        greek_chars = sum(1 for c in text if self.is_greek_char(c))
        alpha_chars = sum(1 for c in text if c.isalpha())
        
        if alpha_chars == 0:
            return False
        
        greek_ratio = greek_chars / alpha_chars
        return greek_ratio >= self.MIN_GREEK_RATIO
    
    def clean_text(self, text: str, source: str) -> str:
        """Clean text based on source platform"""
        
        # Remove Project Gutenberg headers/footers
        if source == 'gutenberg':
            markers = [
                '*** START OF THIS PROJECT GUTENBERG',
                '*** START OF THE PROJECT GUTENBERG',
                '*** END OF THIS PROJECT GUTENBERG',
                '*** END OF THE PROJECT GUTENBERG'
            ]
            
            for marker in markers:
                if marker in text:
                    if 'START' in marker:
                        text = text.split(marker, 1)[-1]
                    else:
                        text = text.split(marker, 1)[0]
        
        # Remove Perseus headers
        elif source == 'perseus':
            # Remove XML/HTML tags if present
            text = re.sub(r'<[^>]+>', '', text)
            # Remove Perseus citation markers
            text = re.sub(r'\[\d+\]', '', text)
        
        # Clean Archive.org texts
        elif source == 'archive.org':
            # Remove page numbers and headers
            text = re.sub(r'^-?\d+\s*$', '', text, flags=re.MULTILINE)
            text = re.sub(r'^\s*Page \d+\s*$', '', text, flags=re.MULTILINE)
        
        # General cleaning
        text = text.strip()
        
        # Normalize whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        
        # Normalize Unicode
        text = unicodedata.normalize('NFC', text)
        
        return text
    
    def sanitize_filename(self, name: str) -> str:
        """Sanitize filename for filesystem"""
        # Remove invalid characters
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        # Replace multiple spaces with single
        name = re.sub(r'\s+', ' ', name)
        # Truncate to 100 characters
        name = name[:100].strip()
        # Remove trailing dots (Windows issue)
        name = name.rstrip('.')
        
        return name if name else 'untitled'
    
    def download_text(self, url: str, source: str) -> Optional[str]:
        """Download text from URL with error handling"""
        try:
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"    HTTP {response.status_code} for {url}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"    Download error: {e}")
            return None
    
    def compute_hash(self, text: str) -> str:
        """Compute SHA-256 hash of text for deduplication"""
        # Normalize text for hashing (remove whitespace variations)
        normalized = re.sub(r'\s+', ' ', text.strip())
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    
    def process_url_entry(self, entry: Dict, output_dir: Path) -> bool:
        """Process a single URL entry"""
        url = entry['url']
        title = entry['title']
        source = entry['source']
        period = entry['period']
        
        print(f"  Processing [{period}]: {title}")
        
        # Download text
        raw_text = self.download_text(url, source)
        if not raw_text:
            self.stats['failed'] += 1
            return False
        
        # Clean text
        cleaned_text = self.clean_text(raw_text, source)
        
        # Check minimum length
        word_count = len(cleaned_text.split())
        if word_count < self.MIN_WORDS:
            print(f"    Skipped: Too short ({word_count} words)")
            self.stats['skipped'] += 1
            return False
        
        # Verify Greek content
        if not self.verify_greek_content(cleaned_text):
            print(f"    Skipped: Insufficient Greek content")
            self.stats['language_filtered'] += 1
            return False
        
        # Check for duplicates
        text_hash = self.compute_hash(cleaned_text)
        if text_hash in self.processed_hashes:
            print(f"    Skipped: Duplicate content")
            self.stats['duplicates'] += 1
            return False
        
        # Save text
        filename = self.sanitize_filename(title) + '.txt'
        filepath = output_dir / filename
        
        try:
            filepath.write_text(cleaned_text, encoding='utf-8')
            self.processed_hashes.add(text_hash)
            self.stats['downloaded'] += 1
            
            # Save metadata
            self.save_metadata(entry, filepath, text_hash, word_count)
            
            print(f"    Saved: {filename} ({word_count} words)")
            return True
            
        except Exception as e:
            print(f"    Error saving file: {e}")
            self.stats['failed'] += 1
            return False
    
    def save_metadata(self, entry: Dict, filepath: Path, text_hash: str, word_count: int):
        """Save metadata for processed text"""
        metadata_dir = Path('corpus_metadata/greek')
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        period = entry['period']
        metadata_file = metadata_dir / f'{period}_metadata.jsonl'
        
        metadata = {
            'filename': filepath.name,
            'path': str(filepath),
            'url': entry['url'],
            'title': entry['title'],
            'period': period,
            'source': entry['source'],
            'hash': text_hash,
            'word_count': word_count,
            'processed_date': datetime.now().isoformat()
        }
        
        # Append to JSONL file
        with open(metadata_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(metadata, ensure_ascii=False) + '\n')
    
    def scrape_all_texts(self):
        """Main scraping function"""
        print("Starting Greek text scraping...")
        
        # Load URLs
        urls_dir = Path('corpus_urls/greek')
        all_urls_file = urls_dir / 'greek_all_periods_urls.json'
        
        if not all_urls_file.exists():
            print(f"Error: {all_urls_file} not found. Run harvest_greek_period_urls.py first.")
            return
        
        with open(all_urls_file, 'r', encoding='utf-8') as f:
            all_urls = json.load(f)
        
        print(f"Loaded {len(all_urls)} URLs to process\n")
        
        # Process by period
        periods = ['ancient', 'medieval', 'early_modern', 'modern']
        
        for period in periods:
            period_urls = [u for u in all_urls if u['period'] == period]
            
            if not period_urls:
                continue
            
            print(f"\n{'='*60}")
            print(f"Processing {period} Greek texts ({len(period_urls)} URLs)")
            print('='*60)
            
            # Create output directory
            output_dir = Path(f'corpus_texts/greek_texts/{period}')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Process each URL
            for i, entry in enumerate(period_urls, 1):
                print(f"\n[{i}/{len(period_urls)}]", end=' ')
                self.process_url_entry(entry, output_dir)
                
                # Rate limiting
                time.sleep(1)
        
        # Print final statistics
        self.print_statistics()
    
    def print_statistics(self):
        """Print processing statistics"""
        print("\n" + "="*60)
        print("SCRAPING COMPLETE")
        print("="*60)
        print(f"Successfully downloaded: {self.stats['downloaded']}")
        print(f"Failed downloads: {self.stats['failed']}")
        print(f"Skipped (too short): {self.stats['skipped']}")
        print(f"Duplicates removed: {self.stats['duplicates']}")
        print(f"Non-Greek filtered: {self.stats['language_filtered']}")
        print(f"Total processed: {sum(self.stats.values())}")
        
        # Save statistics
        stats_file = Path('corpus_metadata/greek/scraping_stats.json')
        stats_file.parent.mkdir(parents=True, exist_ok=True)
        
        stats_data = {
            'timestamp': datetime.now().isoformat(),
            'statistics': self.stats
        }
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2)
        
        print(f"\nStatistics saved to {stats_file}")

def main():
    """Main execution function"""
    scraper = GreekTextScraper()
    scraper.scrape_all_texts()

if __name__ == '__main__':
    main()