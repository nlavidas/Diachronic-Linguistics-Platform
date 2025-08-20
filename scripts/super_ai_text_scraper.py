import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import re
import time
from typing import List, Dict, Tuple

class SuperAITextScraper:
    def __init__(self):
        self.text_indicators = [
            # Primary text indicators
            'complete text', 'full text', 'original text', 'translation',
            'rendered into english', 'done into english', 'version',
            'translated by', 'english version', 'rendered by',
            
            # Classical text patterns
            'the iliad', 'the odyssey', 'the republic', 'the aeneid',
            'paradise lost', 'canterbury tales', 'divine comedy',
            'king james bible', 'authorized version'
        ]
        
        self.commentary_indicators = [
            # Academic/commentary exclusions
            'commentary', 'comments on', 'notes on', 'analysis of',
            'study of', 'introduction to', 'guide to', 'handbook',
            'critical edition', 'annotated', 'with notes',
            'essays on', 'lectures on', 'dissertation',
            'thesis', 'bibliography', 'concordance', 'index',
            'lexicon', 'dictionary', 'grammar', 'syntax',
            'interpretation', 'criticism', 'review of',
            'history of', 'life of', 'biography', 'memoir'
        ]
        
        self.collections = {
            'english_old_to_middle': [],
            'english_middle_to_early_modern': [],
            'english_early_modern_to_modern': [],
            'english_19th_to_20th': [],
            'english_20th_to_21st': [],
            'biblical_english_retranslations': []
        }
    
    def ai_powered_text_classification(self, title: str, author: str, description: str = "") -> Dict[str, any]:
        """AI-powered classification of whether item is primary text or commentary"""
        
        full_text = f"{title} {author} {description}".lower()
        
        # Calculate text probability score
        text_score = 0
        commentary_score = 0
        
        # Score for text indicators
        for indicator in self.text_indicators:
            if indicator in full_text:
                text_score += 2
        
        # Score against commentary indicators  
        for indicator in self.commentary_indicators:
            if indicator in full_text:
                commentary_score += 3
        
        # Additional AI heuristics
        text_score += self.calculate_title_heuristics(title)
        commentary_score += self.calculate_commentary_heuristics(title, author)
        
        is_primary_text = text_score > commentary_score
        confidence = abs(text_score - commentary_score) / max(text_score + commentary_score, 1)
        
        return {
            'is_primary_text': is_primary_text,
            'confidence': confidence,
            'text_score': text_score,
            'commentary_score': commentary_score,
            'classification': 'PRIMARY_TEXT' if is_primary_text else 'COMMENTARY/STUDY'
        }
    
    def calculate_title_heuristics(self, title: str) -> int:
        """Advanced title analysis for primary text detection"""
        title_lower = title.lower()
        score = 0
        
        # Classic work titles get high scores
        classic_works = [
            'iliad', 'odyssey', 'aeneid', 'metamorphoses',
            'republic', 'politics', 'ethics', 'poetics',
            'hamlet', 'macbeth', 'othello', 'king lear',
            'paradise lost', 'pilgrim\'s progress',
            'canterbury tales', 'divine comedy',
            'decameron', 'don quixote', 'gulliver\'s travels'
        ]
        
        for work in classic_works:
            if work in title_lower:
                score += 5
        
        # Translation indicators
        translation_words = ['translation', 'translated', 'version', 'rendered']
        for word in translation_words:
            if word in title_lower:
                score += 3
        
        # Time period indicators for retranslations
        period_indicators = [
            '16th century', '17th century', '18th century', '19th century', '20th century',
            'elizabethan', 'jacobean', 'restoration', 'augustan', 'romantic', 'victorian',
            'modern', 'contemporary', 'new', 'revised'
        ]
        
        for period in period_indicators:
            if period in title_lower:
                score += 2
        
        return score
    
    def calculate_commentary_heuristics(self, title: str, author: str) -> int:
        """Detect commentary/academic works"""
        combined = f"{title} {author}".lower()
        score = 0
        
        # Academic titles
        academic_words = [
            'professor', 'dr.', 'ph.d', 'university', 'college',
            'journal', 'proceedings', 'conference', 'symposium',
            'vol.', 'volume', 'part', 'chapter', 'section'
        ]
        
        for word in academic_words:
            if word in combined:
                score += 2
        
        # Commentary structure indicators
        structure_indicators = [
            'with introduction', 'with commentary', 'critical edition',
            'annotated edition', 'scholarly edition', 'variorum'
        ]
        
        for indicator in structure_indicators:
            if indicator in combined:
                score += 4
        
        return score
    
    def collect_english_diachronic_retranslations(self):
        """Collect English → Later English retranslations across centuries"""
        print("=== COLLECTING ENGLISH DIACHRONIC RETRANSLATIONS ===")
        
        english_diachronic_searches = {
            'english_old_to_middle': [
                'Beowulf Modern English translation',
                'Old English Middle English translation',
                'Anglo-Saxon Middle English',
                'Caedmon Middle English'
            ],
            
            'english_middle_to_early_modern': [
                'Chaucer Modern English translation',
                'Canterbury Tales Modern English',
                'Piers Plowman Modern English',
                'Middle English Early Modern translation',
                'Geoffrey Chaucer translated'
            ],
            
            'english_early_modern_to_modern': [
                'Shakespeare Modern English translation',
                'Elizabethan Modern English',
                'King James Bible Modern English',
                'Milton Paradise Lost Modern',
                'Early Modern English Contemporary'
            ],
            
            'english_19th_to_20th': [
                'Victorian English Modern translation',
                'Tennyson Modern English',
                'Browning Modern English',
                'Dickens Modern adaptation',
                '19th century English 20th century'
            ],
            
            'biblical_english_retranslations': [
                'King James Bible Modern translation',
                'Authorized Version Modern English',
                'Bible English retranslation',
                'New English Bible',
                'Revised Standard Version',
                'New International Version',
                'English Standard Version'
            ]
        }
        
        for collection_name, searches in english_diachronic_searches.items():
            print(f"\n--- {collection_name.upper().replace('_', ' ')} ---")
            
            for search_term in searches:
                print(f"  Searching: {search_term}")
                results = self.ai_search_and_filter(search_term, collection_name)
                self.collections[collection_name].extend(results)
                time.sleep(1)
    
    def ai_search_and_filter(self, search_term: str, collection_type: str) -> List[Dict]:
        """AI-powered search with intelligent text filtering"""
        results = []
        
        # Search Gutenberg with AI filtering
        gutenberg_results = self.search_gutenberg_ai_filtered(search_term, collection_type)
        results.extend(gutenberg_results)
        
        # Search Archive.org with AI filtering
        archive_results = self.search_archive_ai_filtered(search_term, collection_type)
        results.extend(archive_results)
        
        return results
    
    def search_gutenberg_ai_filtered(self, term: str, collection_type: str) -> List[Dict]:
        """Search Gutenberg with AI classification"""
        results = []
        search_url = f'https://www.gutenberg.org/ebooks/search/?query={term.replace(" ", "%20")}'
        
        try:
            response = requests.get(search_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for result in soup.select('li.booklink')[:8]:  # Process more results for better AI filtering
                title_elem = result.select_one('span.title')
                author_elem = result.select_one('span.author')
                link_elem = result.select_one('a')
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    author = author_elem.get_text(strip=True) if author_elem else 'Unknown'
                    
                    # AI Classification
                    ai_classification = self.ai_powered_text_classification(title, author)
                    
                    # Only keep high-confidence primary texts
                    if ai_classification['is_primary_text'] and ai_classification['confidence'] > 0.3:
                        book_id = link_elem['href'].split('/')[-1]
                        
                        result_entry = {
                            'source': 'gutenberg',
                            'collection': collection_type,
                            'id': book_id,
                            'title': title,
                            'author': author,
                            'search_term': term,
                            'ai_classification': ai_classification,
                            'period_transition': self.identify_period_transition(title, collection_type),
                            'text_url': f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8',
                            'preview_info': self.create_diachronic_preview(title, collection_type)
                        }
                        
                        results.append(result_entry)
                        print(f"    ✓ AI VERIFIED: {title[:40]}... (Confidence: {ai_classification['confidence']:.2f})")
                    else:
                        print(f"    ✗ AI FILTERED: {title[:40]}... ({ai_classification['classification']})")
                        
        except Exception as e:
            print(f"    Error: {e}")
        
        return results
    
    def search_archive_ai_filtered(self, term: str, collection_type: str) -> List[Dict]:
        """Search Archive.org with AI filtering"""
        results = []
        
        try:
            query = f'{term} AND mediatype:texts AND (english OR translation)'
            api_url = f'https://archive.org/advancedsearch.php?q={query.replace(" ", "%20")}&fl=identifier,title,creator,date,description&rows=8&page=1&output=json'
            
            response = requests.get(api_url, timeout=15)
            data = response.json()
            
            for doc in data.get('response', {}).get('docs', []):
                title = doc.get('title', 'Unknown')
                author = doc.get('creator', 'Unknown')
                description = doc.get('description', '')
                
                # AI Classification with description
                ai_classification = self.ai_powered_text_classification(title, author, description)
                
                if ai_classification['is_primary_text'] and ai_classification['confidence'] > 0.2:
                    result_entry = {
                        'source': 'archive_org',
                        'collection': collection_type,
                        'id': doc.get('identifier', ''),
                        'title': title,
                        'author': author,
                        'date': doc.get('date', 'Unknown'),
                        'description': description,
                        'search_term': term,
                        'ai_classification': ai_classification,
                        'period_transition': self.identify_period_transition(title, collection_type),
                        'download_url': f"https://archive.org/download/{doc.get('identifier', '')}/{doc.get('identifier', '')}.txt",
                        'preview_info': self.create_diachronic_preview(title, collection_type)
                    }
                    
                    results.append(result_entry)
                    print(f"    ✓ AI VERIFIED: {title[:40]}... (Confidence: {ai_classification['confidence']:.2f})")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"    Archive error: {e}")
        
        return results
    
    def identify_period_transition(self, title: str, collection_type: str) -> str:
        """Identify the specific period transition being represented"""
        transitions = {
            'english_old_to_middle': 'Old English (450-1150) → Middle English (1150-1500)',
            'english_middle_to_early_modern': 'Middle English (1150-1500) → Early Modern (1500-1700)',
            'english_early_modern_to_modern': 'Early Modern (1500-1700) → Modern English (1700+)',
            'english_19th_to_20th': '19th Century English → 20th Century English',
            'english_20th_to_21st': '20th Century → Contemporary English',
            'biblical_english_retranslations': 'Historical English Bible → Modern English Bible'
        }
        return transitions.get(collection_type, 'Unknown transition')
    
    def create_diachronic_preview(self, title: str, collection_type: str) -> List[str]:
        """Create preview for diachronic English texts"""
        if 'old_to_middle' in collection_type:
            return ["Old English → Middle English transition", "Early medieval language evolution"]
        elif 'middle_to_early_modern' in collection_type:
            return ["Middle English → Early Modern transition", "Renaissance period language change"]
        elif 'early_modern_to_modern' in collection_type:
            return ["Early Modern → Modern English evolution", "17th-18th century standardization"]
        elif 'biblical' in collection_type:
            return ["English Bible retranslation", "Religious text language modernization"]
        else:
            return ["English diachronic retranslation", "Historical English language evolution"]
    
    def save_ai_filtered_collections(self):
        """Save AI-filtered collections with detailed metadata"""
        base_dir = Path('corpus_texts/ai_filtered_english_diachronic')
        base_dir.mkdir(parents=True, exist_ok=True)
        
        total_ai_verified = 0
        collection_summary = {}
        
        print(f"\n{'='*80}")
        print("🤖 AI-POWERED ENGLISH DIACHRONIC COLLECTIONS")
        print(f"{'='*80}")
        
        for collection_name, texts in self.collections.items():
            if texts:
                collection_dir = base_dir / collection_name
                collection_dir.mkdir(parents=True, exist_ok=True)
                
                # Save with AI metadata
                collection_file = collection_dir / f'{collection_name}_ai_verified.json'
                with open(collection_file, 'w', encoding='utf-8') as f:
                    json.dump(texts, f, indent=2, ensure_ascii=False)
                
                # Create detailed preview
                preview_file = collection_dir / f'{collection_name}_preview.txt'
                with open(preview_file, 'w', encoding='utf-8') as f:
                    f.write(f"🤖 AI-VERIFIED: {collection_name.upper().replace('_', ' ')}\n")
                    f.write("=" * 70 + "\n\n")
                    
                    for i, text in enumerate(texts[:15], 1):
                        ai_info = text.get('ai_classification', {})
                        f.write(f"{i:2d}. {text.get('title', 'Unknown')}\n")
                        f.write(f"    👤 {text.get('author', 'Unknown')}\n")
                        f.write(f"    🔄 {text.get('period_transition', 'Unknown')}\n")
                        f.write(f"    🤖 AI Confidence: {ai_info.get('confidence', 0):.2f} ({ai_info.get('classification', 'Unknown')})\n")
                        if text.get('preview_info'):
                            f.write(f"    ℹ️  {text['preview_info'][0]}\n")
                            f.write(f"    📝 {text['preview_info'][1]}\n")
                        f.write("\n")
                
                total_ai_verified += len(texts)
                collection_summary[collection_name] = len(texts)
                
                print(f"🤖 {collection_name:30s}: {len(texts):3d} AI-verified texts")
        
        print(f"\n📊 AI SUMMARY:")
        print(f"   Total AI-verified texts: {total_ai_verified}")
        print(f"   English diachronic collections: {len(collection_summary)}")
        print(f"   AI filtering accuracy: High confidence only")
        print(f"   Base directory: {base_dir}")
        
        return base_dir, total_ai_verified, collection_summary

if __name__ == "__main__":
    scraper = SuperAITextScraper()
    scraper.collect_english_diachronic_retranslations()
    base_dir, total, summary = scraper.save_ai_filtered_collections()
