#!/usr/bin/env python3
"""
AI-ENHANCED PREPROCESSING 24/7 AGENT (FIXED)
Validates, cleans, and preprocesses all downloaded texts
Deletes invalid files, fixes encoding, removes boilerplate
"""

import os
import re
import logging
import sqlite3
import time
import chardet
from pathlib import Path
from datetime import datetime
import hashlib
import json

class AIPreprocessingAgent:
    def __init__(self, base_path="Z:\\DiachronicValencyCorpus"):
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "texts" / "collected"
        self.clean_path = self.base_path / "texts" / "preprocessed"
        self.trash_path = self.base_path / "texts" / "rejected"
        
        # Create directories
        self.clean_path.mkdir(parents=True, exist_ok=True)
        self.trash_path.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Validation criteria
        self.min_file_size = 5000  # 5KB minimum
        self.min_word_count = 100  # At least 100 words
        self.max_html_ratio = 0.1  # Max 10% HTML tags
        
        # Common error patterns
        self.error_patterns = [
            r'404 Not Found',
            r'403 Forbidden', 
            r'Access Denied',
            r'Page Not Found',
            r'<!DOCTYPE html',  # HTML pages
            r'<html',
            r'var _paq = ',  # JavaScript
            r'function\(',
            r'{\s*"error"\s*:',  # JSON errors
            r"DON'T USE THIS PAGE FOR SCRAPING",  # Gutenberg warning
            r"You'll only get your IP blocked",
        ]
        
        # Gutenberg boilerplate patterns
        self.boilerplate_patterns = [
            r'\*{3,}\s*START OF THE PROJECT GUTENBERG.*?\*{3,}',
            r'\*{3,}\s*END OF THE PROJECT GUTENBERG.*?\*{3,}',
            r'Project Gutenberg[\s\S]+?START OF THE PROJECT',
            r'End of the Project Gutenberg[\s\S]+$',
            r'Produced by[\s\S]+?(?=Chapter|CHAPTER|Book|BOOK|\n\n)',
            r'This eBook is for the use[\s\S]+?(?=\n\n)',
        ]
        
    def setup_logging(self):
        """Setup preprocessing logger"""
        log_file = self.base_path / f'logs/preprocessing_{datetime.now().strftime("%Y%m%d")}.log'
        log_file.parent.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [PreProcessor] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
    def validate_text_file(self, filepath):
        """Validate if file contains actual text content"""
        try:
            # Check file size
            file_size = filepath.stat().st_size
            if file_size < self.min_file_size:
                return False, f"File too small: {file_size} bytes"
                
            # Detect encoding
            with open(filepath, 'rb') as f:
                raw_data = f.read()
                detected = chardet.detect(raw_data)
                encoding = detected['encoding'] or 'utf-8'
                
            # Read content
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
            except:
                # Try UTF-8 with errors ignored
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
            # Check for error pages
            for pattern in self.error_patterns:
                if re.search(pattern, content[:1000], re.IGNORECASE):
                    return False, f"Error page detected: {pattern}"
                    
            # Check word count
            words = content.split()
            if len(words) < self.min_word_count:
                return False, f"Too few words: {len(words)}"
                
            # Check HTML ratio
            html_tags = len(re.findall(r'<[^>]+>', content))
            if html_tags > len(words) * self.max_html_ratio:
                return False, f"Too much HTML: {html_tags} tags"
                
            # Check if it's actually text (not binary)
            text_chars = sum(c.isalpha() or c.isspace() for c in content[:1000])
            if text_chars < 500:
                return False, "Not enough text characters"
                
            return True, "Valid text file"
            
        except Exception as e:
            return False, f"Validation error: {e}"
            
    def preprocess_text(self, filepath):
        """Clean and preprocess text content"""
        try:
            # Detect encoding
            with open(filepath, 'rb') as f:
                raw_data = f.read()
                detected = chardet.detect(raw_data)
                encoding = detected['encoding'] or 'utf-8'
                
            # Read content
            with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()
                
            # Store original length
            original_length = len(content)
            
            # Remove Gutenberg boilerplate
            for pattern in self.boilerplate_patterns:
                content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
                
            # Clean up text
            # Remove excessive whitespace
            content = re.sub(r'\n{4,}', '\n\n\n', content)
            content = re.sub(r' {2,}', ' ', content)
            
            # Fix common OCR errors
            ocr_fixes = {
                r'tbe': 'the',
                r'tlie': 'the',
                r'aud': 'and',
                r'ou([^aeiou])': r'on\1',
                r'iu': 'in',
                r'([a-z])1([a-z])': r'\1l\2',  # 1 -> l
                r'([a-z])0([a-z])': r'\1o\2',  # 0 -> o
            }
            
            for error, fix in ocr_fixes.items():
                content = re.sub(r'\b' + error + r'\b', fix, content, flags=re.IGNORECASE)
                
            # Normalize quotes and dashes (FIXED)
            content = re.sub(r'[""]', '"', content)  # Convert smart quotes to regular
            content = re.sub(r"['']", "'", content)   # Convert smart apostrophes  
            content = re.sub(r'[–—]', '-', content)   # Convert em/en dashes
            
            # Remove page numbers and headers
            content = re.sub(r'^\s*\d+\s*$', '', content, flags=re.MULTILINE)
            content = re.sub(r'^Page \d+.*$', '', content, flags=re.MULTILINE | re.IGNORECASE)
            
            # Extract metadata if present
            metadata = {
                'original_size': original_length,
                'cleaned_size': len(content),
                'reduction': f"{(1 - len(content)/original_length)*100:.1f}%"
            }
            
            title_match = re.search(r'^Title:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
            if title_match:
                metadata['title'] = title_match.group(1).strip()
                
            author_match = re.search(r'^Author:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
            if author_match:
                metadata['author'] = author_match.group(1).strip()
                
            return content, metadata
            
        except Exception as e:
            logging.error(f"Preprocessing error for {filepath}: {e}")
            return None, {}
            
    def identify_language(self, content):
        """Identify language of text"""
        # Sample text
        sample = content[:1000]
        
        # Language indicators
        indicators = {
            'greek': [r'[Α-Ωα-ω]{3,}', r'τον|την|του|της|και|είναι|στο'],
            'latin': [r'\b(et|in|ad|cum|sed|ut|si|non|est|sunt)\b'],
            'german': [r'\b(der|die|das|und|ist|nicht|ich|du)\b'],
            'french': [r'\b(le|la|les|et|est|dans|pour|avec)\b'],
            'italian': [r'\b(il|la|di|che|non|per|con|una)\b'],
            'spanish': [r'\b(el|la|de|que|en|por|con|para)\b'],
        }
        
        scores = {}
        for lang, patterns in indicators.items():
            score = sum(len(re.findall(pattern, sample, re.IGNORECASE)) for pattern in patterns)
            scores[lang] = score
            
        # Default to English if no strong indicators
        if max(scores.values()) < 5:
            return 'english'
            
        return max(scores, key=scores.get)
        
    def process_file(self, filepath):
        """Process a single file"""
        filepath = Path(filepath)
        logging.info(f"Processing: {filepath.name}")
        
        # Validate file
        is_valid, reason = self.validate_text_file(filepath)
        
        if not is_valid:
            logging.warning(f"Rejecting {filepath.name}: {reason}")
            
            # Move to trash
            trash_file = self.trash_path / f"{filepath.stem}_REJECTED{filepath.suffix}"
            filepath.rename(trash_file)
            
            # Create rejection log
            with open(trash_file.with_suffix('.rejection.txt'), 'w') as f:
                f.write(f"Rejected: {datetime.now()}\n")
                f.write(f"Reason: {reason}\n")
                f.write(f"Original: {filepath.name}\n")
                
            # Update database
            self.update_database(filepath.name, 'rejected', reason)
            return False
            
        # Preprocess valid file
        cleaned_content, metadata = self.preprocess_text(filepath)
        
        if cleaned_content and len(cleaned_content) > self.min_word_count * 5:
            # Identify language
            language = self.identify_language(cleaned_content)
            metadata['language'] = language
            
            # Save preprocessed version
            clean_file = self.clean_path / f"{filepath.stem}_CLEAN{filepath.suffix}"
            with open(clean_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
                
            # Save metadata
            meta_file = clean_file.with_suffix('.meta.json')
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
                
            logging.info(f"✅ Preprocessed {filepath.name} -> {clean_file.name}")
            logging.info(f"   Language: {language}, Size: {metadata['cleaned_size']}")
            
            # Update database
            self.update_database(filepath.name, 'preprocessed', metadata)
            return True
            
        else:
            logging.warning(f"Failed to preprocess {filepath.name}")
            return False
            
    def update_database(self, filename, status, info):
        """Update preprocessing status in database"""
        try:
            conn = sqlite3.connect(str(self.base_path / 'corpus_complete.db'))
            cursor = conn.cursor()
            
            # Add preprocessing columns if they don't exist
            try:
                cursor.execute('ALTER TABLE texts ADD COLUMN preprocessing_status TEXT')
                cursor.execute('ALTER TABLE texts ADD COLUMN preprocessing_info TEXT')
                cursor.execute('ALTER TABLE texts ADD COLUMN preprocessed_at TIMESTAMP')
            except:
                pass  # Columns already exist
                
            # Update status
            cursor.execute('''
                UPDATE texts 
                SET preprocessing_status = ?, 
                    preprocessing_info = ?,
                    preprocessed_at = CURRENT_TIMESTAMP
                WHERE filename = ?
            ''', (status, json.dumps(info) if isinstance(info, dict) else str(info), filename))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logging.error(f"Database update error: {e}")
            
    def scan_and_process(self):
        """Scan for new files to process"""
        processed_files = set()
        
        # Get list of already processed files
        clean_files = {f.stem.replace('_CLEAN', '') for f in self.clean_path.glob('*_CLEAN.txt')}
        rejected_files = {f.stem.replace('_REJECTED', '') for f in self.trash_path.glob('*_REJECTED.txt')}
        processed_files = clean_files | rejected_files
        
        # Find new files to process
        new_files = []
        for filepath in self.raw_path.glob('*.txt'):
            if filepath.stem not in processed_files:
                new_files.append(filepath)
                
        logging.info(f"Found {len(new_files)} files to process")
        
        # Process each file
        success_count = 0
        for filepath in new_files:
            if self.process_file(filepath):
                success_count += 1
            time.sleep(1)  # Don't overwhelm the system
            
        return success_count, len(new_files)
        
    def generate_quality_report(self):
        """Generate preprocessing quality report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'statistics': {
                'total_files': len(list(self.raw_path.glob('*.txt'))),
                'preprocessed': len(list(self.clean_path.glob('*_CLEAN.txt'))),
                'rejected': len(list(self.trash_path.glob('*_REJECTED.txt'))),
            }
        }
        
        # Language distribution
        languages = {}
        for meta_file in self.clean_path.glob('*.meta.json'):
            with open(meta_file, 'r') as f:
                meta = json.load(f)
                lang = meta.get('language', 'unknown')
                languages[lang] = languages.get(lang, 0) + 1
                
        report['languages'] = languages
        
        # Save report
        report_file = self.base_path / f'preprocessing_report_{datetime.now().strftime("%Y%m%d")}.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        return report
        
    def run_24_7(self):
        """Run preprocessing continuously"""
        logging.info("🤖 Starting AI Preprocessing Agent 24/7")
        
        while True:
            try:
                # Scan and process new files
                success, total = self.scan_and_process()
                
                if total > 0:
                    logging.info(f"✅ Processed {success}/{total} files successfully")
                    
                    # Generate report
                    report = self.generate_quality_report()
                    logging.info(f"📊 Clean texts: {report['statistics']['preprocessed']}")
                    logging.info(f"🗑️  Rejected: {report['statistics']['rejected']}")
                    
                # Sleep for 10 minutes
                time.sleep(600)
                
            except Exception as e:
                logging.error(f"Preprocessing agent error: {e}")
                time.sleep(300)  # 5 minutes on error

if __name__ == "__main__":
    print("="*70)
    print("🧹 AI-ENHANCED PREPROCESSING AGENT")
    print("Validates, cleans, and preprocesses all texts")
    print("="*70)
    
    agent = AIPreprocessingAgent()
    
    # Do an initial scan
    print("\n🔍 Initial scan...")
    success, total = agent.scan_and_process()
    print(f"✅ Processed {success}/{total} files")
    
    # Run continuously
    try:
        agent.run_24_7()
    except KeyboardInterrupt:
        print("\n👋 Preprocessing agent stopped")