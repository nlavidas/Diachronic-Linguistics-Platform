#!/usr/bin/env python3
"""
manage_corpus.py
Unified corpus management script for quality control, migration, and reporting
"""

import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
import re
import unicodedata
from collections import defaultdict, Counter

class CorpusManager:
    """Manages the entire Open-Access Texts Corpus"""
    
    def __init__(self):
        self.corpus_root = Path('corpus_texts')
        self.metadata_root = Path('corpus_metadata')
        self.urls_root = Path('corpus_urls')
        self.stats = defaultdict(lambda: defaultdict(int))
        
    def migrate_ancient_greek(self):
        """Migrate existing ancient_greek_texts/ to new structure"""
        print("Migrating ancient Greek texts to new structure...")
        
        old_dir = self.corpus_root / 'ancient_greek_texts'
        new_dir = self.corpus_root / 'greek_texts' / 'ancient'
        
        if old_dir.exists() and not new_dir.exists():
            new_dir.mkdir(parents=True, exist_ok=True)
            
            # Move all text files
            text_files = list(old_dir.glob('*.txt'))
            for file in text_files:
                shutil.move(str(file), str(new_dir / file.name))
                print(f"  Moved: {file.name}")
            
            # Remove old directory if empty
            if not list(old_dir.iterdir()):
                old_dir.rmdir()
                print(f"  Removed empty directory: {old_dir}")
            
            print(f"Migration complete: {len(text_files)} files moved")
        else:
            print("  No migration needed")
    
    def analyze_corpus(self):
        """Comprehensive corpus analysis"""
        print("\n" + "="*60)
        print("CORPUS ANALYSIS")
        print("="*60)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'categories': {},
            'totals': {
                'files': 0,
                'words': 0,
                'unique_hashes': 0,
                'size_bytes': 0
            }
        }
        
        all_hashes = set()
        
        # Define corpus structure
        corpus_structure = {
            'greek_texts': ['ancient', 'medieval', 'early_modern', 'modern'],
            'latin_texts': [''],
            'middle_french_texts': [''],
            'english_retranslations': [''],
            'all_texts': [''],
            'ai_filtered_english_diachronic': ['']
        }
        
        for category, subdirs in corpus_structure.items():
            category_path = self.corpus_root / category
            
            if not category_path.exists():
                continue
            
            category_stats = {
                'files': 0,
                'words': 0,
                'size_bytes': 0,
                'duplicates': [],
                'subdirectories': {}
            }
            
            for subdir in subdirs:
                if subdir:
                    search_path = category_path / subdir
                    subdir_key = subdir
                else:
                    search_path = category_path
                    subdir_key = 'root'
                
                if not search_path.exists():
                    continue
                
                subdir_stats = self.analyze_directory(search_path, all_hashes)
                category_stats['subdirectories'][subdir_key] = subdir_stats
                
                # Aggregate stats
                category_stats['files'] += subdir_stats['files']
                category_stats['words'] += subdir_stats['words']
                category_stats['size_bytes'] += subdir_stats['size_bytes']
            
            results['categories'][category] = category_stats
            
            # Update totals
            results['totals']['files'] += category_stats['files']
            results['totals']['words'] += category_stats['words']
            results['totals']['size_bytes'] += category_stats['size_bytes']
        
        results['totals']['unique_hashes'] = len(all_hashes)
        
        # Print summary
        self.print_analysis_summary(results)
        
        # Save detailed report
        report_file = self.metadata_root / 'corpus_analysis.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nDetailed report saved to: {report_file}")
        
        return results
    
    def analyze_directory(self, directory: Path, all_hashes: Set[str]) -> Dict:
        """Analyze a single directory"""
        stats = {
            'files': 0,
            'words': 0,
            'size_bytes': 0,
            'duplicates': [],
            'language_distribution': Counter(),
            'file_sizes': []
        }
        
        for file in directory.glob('*.txt'):
            stats['files'] += 1
            
            try:
                text = file.read_text(encoding='utf-8')
                stats['words'] += len(text.split())
                stats['size_bytes'] += file.stat().st_size
                stats['file_sizes'].append(file.stat().st_size)
                
                # Check for duplicates
                text_hash = hashlib.sha256(text.encode()).hexdigest()
                if text_hash in all_hashes:
                    stats['duplicates'].append(file.name)
                else:
                    all_hashes.add(text_hash)
                
                # Detect primary language
                lang = self.detect_language(text)
                stats['language_distribution'][lang] += 1
                
            except Exception as e:
                print(f"    Error analyzing {file.name}: {e}")
        
        # Calculate statistics
        if stats['file_sizes']:
            stats['avg_size_bytes'] = sum(stats['file_sizes']) / len(stats['file_sizes'])
            stats['min_size_bytes'] = min(stats['file_sizes'])
            stats['max_size_bytes'] = max(stats['file_sizes'])
        
        del stats['file_sizes']  # Remove raw data from final stats
        
        return stats
    
    def detect_language(self, text: str) -> str:
        """Simple language detection based on character ranges"""
        sample = text[:1000]  # Sample first 1000 chars
        
        char_counts = {
            'greek': 0,
            'latin': 0,
            'french': 0,
            'english': 0
        }
        
        for char in sample:
            code = ord(char)
            
            # Greek ranges
            if 0x0370 <= code <= 0x03FF or 0x1F00 <= code <= 0x1FFF:
                char_counts['greek'] += 1
            # Basic Latin with French accents
            elif char in 'àâäçèéêëîïôùûüÿœæ':
                char_counts['french'] += 1
            # Common English-only patterns
            elif char.lower() in 'abcdefghijklmnopqrstuvwxyz':
                char_counts['english'] += 1
                char_counts['latin'] += 1  # Could be either
        
        # Return most likely language
        if char_counts['greek'] > 10:
            return 'greek'
        elif char_counts['french'] > 5:
            return 'french'
        elif char_counts['latin'] > char_counts['english']:
            return 'latin'
        else:
            return 'english'
    
    def print_analysis_summary(self, results: Dict):
        """Print formatted analysis summary"""
        print("\nCORPUS SUMMARY")
        print("-" * 40)
        print(f"Total Files: {results['totals']['files']:,}")
        print(f"Total Words: {results['totals']['words']:,}")
        print(f"Total Size: {results['totals']['size_bytes'] / (1024*1024):.2f} MB")
        print(f"Unique Texts: {results['totals']['unique_hashes']:,}")
        
        print("\nBY CATEGORY:")
        for category, stats in results['categories'].items():
            print(f"\n{category}:")
            print(f"  Files: {stats['files']:,}")
            print(f"  Words: {stats['words']:,}")
            print(f"  Size: {stats['size_bytes'] / (1024*1024):.2f} MB")
            
            if stats['subdirectories']:
                for subdir, subdir_stats in stats['subdirectories'].items():
                    if subdir != 'root' and subdir_stats['files'] > 0:
                        print(f"    {subdir}: {subdir_stats['files']} files, "
                              f"{subdir_stats['words']:,} words")
    
    def quality_check(self):
        """Run quality checks on the corpus"""
        print("\n" + "="*60)
        print("QUALITY CHECK")
        print("="*60)
        
        issues = {
            'empty_files': [],
            'encoding_errors': [],
            'duplicate_names': defaultdict(list),
            'suspicious_content': [],
            'missing_metadata': []
        }
        
        # Check all text files
        for text_file in self.corpus_root.rglob('*.txt'):
            rel_path = text_file.relative_to(self.corpus_root)
            
            # Check for empty files
            if text_file.stat().st_size == 0:
                issues['empty_files'].append(str(rel_path))
            
            # Check encoding
            try:
                text = text_file.read_text(encoding='utf-8')
                
                # Check for suspicious content (e.g., HTML/XML remnants)
                if '<html' in text.lower() or '<?xml' in text.lower():
                    issues['suspicious_content'].append(str(rel_path))
                    
            except UnicodeDecodeError:
                issues['encoding_errors'].append(str(rel_path))
            
            # Track duplicate filenames
            issues['duplicate_names'][text_file.name].append(str(rel_path))
        
        # Check for metadata
        for category in ['greek', 'latin', 'french', 'english']:
            metadata_dir = self.metadata_root / category
            if not metadata_dir.exists():
                issues['missing_metadata'].append(category)
        
        # Report issues
        print("\nQuality Check Results:")
        print("-" * 40)
        
        if issues['empty_files']:
            print(f"\n⚠ Empty files found: {len(issues['empty_files'])}")
            for file in issues['empty_files'][:5]:
                print(f"  - {file}")
        
        if issues['encoding_errors']:
            print(f"\n⚠ Encoding errors: {len(issues['encoding_errors'])}")
            for file in issues['encoding_errors'][:5]:
                print(f"  - {file}")
        
        duplicate_count = sum(1 for files in issues['duplicate_names'].values() if len(files) > 1)
        if duplicate_count:
            print(f"\n⚠ Duplicate filenames: {duplicate_count}")
            for name, paths in list(issues['duplicate_names'].items())[:5]:
                if len(paths) > 1:
                    print(f"  - {name}: {len(paths)} occurrences")
        
        if issues['suspicious_content']:
            print(f"\n⚠ Files with HTML/XML content: {len(issues['suspicious_content'])}")
            for file in issues['suspicious_content'][:5]:
                print(f"  - {file}")
        
        if not any(issues.values()):
            print("✓ No issues found!")
        
        # Save detailed QC report
        qc_report = {
            'timestamp': datetime.now().isoformat(),
            'issues': issues
        }
        
        qc_file = self.metadata_root / 'quality_check.json'
        with open(qc_file, 'w', encoding='utf-8') as f:
            json.dump(qc_report, f, indent=2)
        
        print(f"\nDetailed QC report saved to: {qc_file}")
    
    def generate_manifest(self):
        """Generate a manifest of all corpus files"""
        print("\n" + "="*60)
        print("GENERATING MANIFEST")
        print("="*60)
        
        manifest = {
            'generated': datetime.now().isoformat(),
            'version': '1.0',
            'files': []
        }
        
        for text_file in sorted(self.corpus_root.rglob('*.txt')):
            rel_path = text_file.relative_to(self.corpus_root)
            
            try:
                text = text_file.read_text(encoding='utf-8')
                file_info = {
                    'path': str(rel_path),
                    'name': text_file.name,
                    'size_bytes': text_file.stat().st_size,
                    'word_count': len(text.split()),
                    'hash': hashlib.sha256(text.encode()).hexdigest()[:16],
                    'language': self.detect_language(text)
                }
                
                # Determine category and period
                parts = rel_path.parts
                if len(parts) >= 2:
                    file_info['category'] = parts[0]
                    if len(parts) >= 3:
                        file_info['period'] = parts[1]
                
                manifest['files'].append(file_info)
                
            except Exception as e:
                print(f"  Error processing {rel_path}: {e}")
        
        # Save manifest
        manifest_file = self.corpus_root / 'MANIFEST.json'
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"Manifest generated: {len(manifest['files'])} files")
        print(f"Saved to: {manifest_file}")
        
        return manifest

def main():
    """Main execution with menu"""
    manager = CorpusManager()
    
    print("="*60)
    print("OPEN-ACCESS TEXTS CORPUS MANAGER")
    print("="*60)
    
    while True:
        print("\nOptions:")
        print("1. Migrate ancient Greek texts to new structure")
        print("2. Analyze corpus statistics")
        print("3. Run quality checks")
        print("4. Generate manifest")
        print("5. Run all tasks")
        print("0. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            manager.migrate_ancient_greek()
        elif choice == '2':
            manager.analyze_corpus()
        elif choice == '3':
            manager.quality_check()
        elif choice == '4':
            manager.generate_manifest()
        elif choice == '5':
            print("\nRunning all tasks...")
            manager.migrate_ancient_greek()
            manager.analyze_corpus()
            manager.quality_check()
            manager.generate_manifest()
            print("\nAll tasks complete!")
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid option")

if __name__ == '__main__':
    main()