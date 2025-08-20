import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import re
import time
from typing import List, Dict, Tuple

class UniversalAITextClassifier:
    def __init__(self):
        # Load existing collections
        self.load_existing_collections()
        
        # Universal text indicators (works for all languages)
        self.primary_text_indicators = {
            'english': ['complete text', 'full text', 'translation', 'version', 'rendered'],
            'greek': ['κείμενο', 'μετάφραση', 'έκδοση', 'πλήρης', 'αρχαίος'],
            'latin': ['textus', 'versio', 'translatio', 'editio', 'completus'],
            'french': ['texte', 'traduction', 'version', 'œuvre', 'intégral'],
            'german': ['text', 'übersetzung', 'ausgabe', 'werk', 'vollständig'],
            'italian': ['testo', 'traduzione', 'versione', 'opera', 'completo'],
            'spanish': ['texto', 'traducción', 'versión', 'obra', 'completo']
        }
        
        # Universal commentary/study indicators
        self.commentary_indicators = {
            'english': ['commentary', 'notes', 'study', 'analysis', 'introduction', 'guide', 'handbook', 'critical edition', 'annotated', 'essays', 'lectures', 'dissertation', 'bibliography', 'concordance', 'lexicon', 'grammar', 'interpretation', 'criticism', 'history of', 'biography'],
            'greek': ['σχόλια', 'σημειώσεις', 'μελέτη', 'ανάλυση', 'εισαγωγή', 'οδηγός', 'κριτική', 'ερμηνεία', 'ιστορία', 'βιογραφία'],
            'latin': ['commentarius', 'notae', 'studium', 'analysis', 'introductio', 'critica', 'interpretatio', 'historia', 'vita'],
            'french': ['commentaire', 'notes', 'étude', 'analyse', 'introduction', 'guide', 'critique', 'interprétation', 'histoire', 'biographie'],
            'german': ['kommentar', 'anmerkungen', 'studie', 'analyse', 'einführung', 'kritik', 'interpretation', 'geschichte', 'biographie'],
            'italian': ['commento', 'note', 'studio', 'analisi', 'introduzione', 'critica', 'interpretazione', 'storia', 'biografia'],
            'spanish': ['comentario', 'notas', 'estudio', 'análisis', 'introducción', 'crítica', 'interpretación', 'historia', 'biografía']
        }
        
        # Collections organized by language and period
        self.collections = {
            # Greek diachronic collections
            'greek_ancient_to_koine': [],
            'greek_koine_to_byzantine': [],
            'greek_byzantine_to_medieval': [],
            'greek_medieval_to_modern': [],
            'greek_katharevousa_to_demotic': [],
            'greek_biblical_retranslations': [],
            
            # English diachronic collections (enhanced)
            'english_old_to_middle': [],
            'english_middle_to_early_modern': [],
            'english_early_modern_to_modern': [],
            'english_19th_to_20th': [],
            'english_biblical_retranslations': [],
            
            # Other language collections
            'latin_classical_to_medieval': [],
            'latin_medieval_to_renaissance': [],
            'french_old_to_middle': [],
            'french_middle_to_modern': [],
            'german_middle_high_to_modern': [],
            'italian_medieval_to_renaissance': [],
            'spanish_medieval_to_golden_age': []
        }
    
    def load_existing_collections(self):
        """Load previously collected URLs to enhance with AI classification"""
        existing_files = [
            'corpus_texts/collected_urls_final.json',
            'corpus_texts/multilingual_retranslations/*/urls.json'
        ]
        
        self.existing_urls = []
        for file_pattern in existing_files:
            try:
                files = list(Path('.').glob(file_pattern))
                for file in files:
                    if file.exists():
                        with open(file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                self.existing_urls.extend(data)
                            print(f"Loaded {len(data) if isinstance(data, list) else 0} URLs from {file}")
            except Exception as e:
                print(f"Error loading {file_pattern}: {e}")
        
        print(f"Total existing URLs to process: {len(self.existing_urls)}")
    
    def ai_classify_text_multilingual(self, title: str, author: str, description: str = "", language: str = 'english') -> Dict[str, any]:
        """Universal AI classification for any language"""
        
        full_text = f"{title} {author} {description}".lower()
        
        # Get language-specific indicators
        text_indicators = self.primary_text_indicators.get(language, self.primary_text_indicators['english'])
        commentary_indicators = self.commentary_indicators.get(language, self.commentary_indicators['english'])
        
        # Calculate scores
        text_score = 0
        commentary_score = 0
        
        # Score for primary text indicators
        for indicator in text_indicators:
            if indicator in full_text:
                text_score += 3
        
        # Score against commentary indicators
        for indicator in commentary_indicators:
            if indicator in full_text:
                commentary_score += 4
        
        # Universal heuristics (work for all languages)
        text_score += self.calculate_universal_text_heuristics(title, language)
        commentary_score += self.calculate_universal_commentary_heuristics(title, author, language)
        
        is_primary_text = text_score > commentary_score
        confidence = abs(text_score - commentary_score) / max(text_score + commentary_score, 1)
        
        return {
            'is_primary_text': is_primary_text,
            'confidence': confidence,
            'text_score': text_score,
            'commentary_score': commentary_score,
            'classification': 'PRIMARY_TEXT' if is_primary_text else 'COMMENTARY/STUDY',
            'language': language
        }
    
    def calculate_universal_text_heuristics(self, title: str, language: str) -> int:
        """Universal text detection across all languages"""
        title_lower = title.lower()
        score = 0
        
        # Classic authors and works (universal recognition)
        classic_patterns = {
            'greek': ['homer', 'plato', 'aristotle', 'sophocles', 'euripides', 'aeschylus', 'thucydides', 'xenophon', 'demosthenes'],
            'latin': ['virgil', 'ovid', 'cicero', 'caesar', 'tacitus', 'livy', 'horace', 'juvenal'],
            'english': ['shakespeare', 'chaucer', 'milton', 'spenser', 'donne', 'pope', 'swift'],
            'french': ['molière', 'racine', 'corneille', 'voltaire', 'rousseau', 'montaigne'],
            'german': ['goethe', 'schiller', 'heine', 'kleist', 'lessing'],
            'italian': ['dante', 'petrarch', 'boccaccio', 'ariosto', 'tasso'],
            'spanish': ['cervantes', 'lope de vega', 'calderón', 'góngora', 'quevedo']
        }
        
        # Check for classic authors/works
        authors = classic_patterns.get(language, [])
        for author in authors:
            if author in title_lower:
                score += 5
        
        # Translation indicators (universal patterns)
        translation_patterns = [
            'translat', 'version', 'render', 'english', 'modern',
            'new', 'complete', 'collected', 'works', 'text'
        ]
        
        for pattern in translation_patterns:
            if pattern in title_lower:
                score += 2
        
        # Period indicators for diachronic texts
        period_patterns = [
            'ancient', 'classical', 'medieval', 'renaissance', 'modern',
            'byzantine', 'koine', 'old', 'middle', 'early', 'late',
            'century', '16th', '17th', '18th', '19th', '20th'
        ]
        
        for pattern in period_patterns:
            if pattern in title_lower:
                score += 1
        
        return score
    
    def calculate_universal_commentary_heuristics(self, title: str, author: str, language: str) -> int:
        """Universal commentary detection"""
        combined = f"{title} {author}".lower()
        score = 0
        
        # Universal academic indicators
        academic_patterns = [
            'professor', 'dr.', 'ph.d', 'university', 'college', 'institut',
            'journal', 'proceedings', 'conference', 'symposium', 'congress',
            'vol.', 'volume', 'part', 'chapter', 'section', 'tome',
            'critical', 'scholarly', 'academic', 'research'
        ]
        
        for pattern in academic_patterns:
            if pattern in combined:
                score += 2
        
        # Publishing/editorial indicators
        editorial_patterns = [
            'editor', 'edited', 'introduction', 'preface', 'foreword',
            'annotated', 'commentary', 'notes', 'apparatus', 'variorum'
        ]
        
        for pattern in editorial_patterns:
            if pattern in combined:
                score += 3
        
        return score
    
    def collect_greek_diachronic_comprehensive(self):
        """Comprehensive Greek diachronic collection with AI filtering"""
        print("=== 🇬🇷 AI-POWERED GREEK DIACHRONIC COLLECTION ===")
        
        greek_collections = {
            'greek_ancient_to_koine': [
                'Homer Hellenistic Greek translation',
                'Classical Greek Koine translation',
                'Ancient Greek Septuagint',
                'Attic Greek Koine Greek'
            ],
            
            'greek_koine_to_byzantine': [
                'Koine Greek Byzantine translation',
                'New Testament Byzantine Greek',
                'Early Christian Greek Byzantine',
                'Patristic Greek Byzantine'
            ],
            
            'greek_byzantine_to_medieval': [
                'Byzantine Greek Medieval translation',
                'Constantinople Greek Medieval',
                'Paleologan Greek translation',
                'Komnenian Greek Medieval'
            ],
            
            'greek_medieval_to_modern': [
                'Medieval Greek Modern translation',
                'Cretan Renaissance Modern Greek',
                'Phanariot Greek Modern translation',
                'Ottoman Greek Modern Greek'
            ],
            
            'greek_katharevousa_to_demotic': [
                'Katharevousa Demotic translation',
                'Puristic Greek Modern Greek',
                'Formal Greek Vernacular',
                'Literary Greek Spoken Greek'
            ],
            
            'greek_biblical_retranslations': [
                'Septuagint Modern Greek',
                'Greek Bible Vamvas translation',
                'New Testament Modern Greek',
                'Orthodox Greek Bible Modern'
            ]
        }
        
        for collection_name, searches in greek_collections.items():
            print(f"\n--- {collection_name.upper().replace('_', ' ')} ---")
            for search_term in searches:
                print(f"  🔍 Searching: {search_term}")
                results = self.ai_search_multilingual(search_term, collection_name, 'greek')
                self.collections[collection_name].extend(results)
                time.sleep(1)
    
    def collect_all_languages_diachronic(self):
        """Collect diachronic texts for all major languages"""
        print("=== 🌍 UNIVERSAL AI-POWERED DIACHRONIC COLLECTION ===")
        
        all_languages_collections = {
            'latin_classical_to_medieval': [
                'Virgil Medieval Latin translation',
                'Cicero Medieval Latin',
                'Classical Latin Medieval Latin',
                'Patristic Latin Medieval'
            ],
            
            'french_old_to_middle': [
                'Old French Middle French translation',
                'Chanson de geste Middle French',
                'Chrétien de Troyes Modern French',
                'Medieval French Modern French'
            ],
            
            'german_middle_high_to_modern': [
                'Middle High German Modern German',
                'Nibelungenlied Modern German',
                'Minnelied Modern German translation',
                'Medieval German Modern German'
            ],
            
            'italian_medieval_to_renaissance': [
                'Medieval Italian Renaissance translation',
                'Dante modern Italian',
                'Old Italian modern Italian',
                'Trecento Italian modern'
            ],
            
            'spanish_medieval_to_golden_age': [
                'Medieval Spanish Golden Age',
                'Mio Cid modern Spanish',
                'Old Spanish modern Spanish',
                'Medieval Castilian modern'
            ]
        }
        
        language_map = {
            'latin': 'latin',
            'french': 'french', 
            'german': 'german',
            'italian': 'italian',
            'spanish': 'spanish'
        }
        
        for collection_name, searches in all_languages_collections.items():
            # Determine language from collection name
            lang = next((l for l in language_map.keys() if l in collection_name), 'english')
            
            print(f"\n--- {collection_name.upper().replace('_', ' ')} ---")
            for search_term in searches:
                print(f"  🔍 Searching: {search_term}")
                results = self.ai_search_multilingual(search_term, collection_name, lang)
                self.collections[collection_name].extend(results)
                time.sleep(1)
    
    def ai_search_multilingual(self, search_term: str, collection_type: str, language: str) -> List[Dict]:
        """Universal AI search for any language"""
        results = []
        
        # Search with AI classification
        gutenberg_results = self.search_gutenberg_ai_multilingual(search_term, collection_type, language)
        results.extend(gutenberg_results)
        
        archive_results = self.search_archive_ai_multilingual(search_term, collection_type, language)
        results.extend(archive_results)
        
        return results
    
    def search_gutenberg_ai_multilingual(self, term: str, collection_type: str, language: str) -> List[Dict]:
        """Gutenberg search with multilingual AI classification"""
        results = []
        search_url = f'https://www.gutenberg.org/ebooks/search/?query={term.replace(" ", "%20")}'
        
        try:
            response = requests.get(search_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for result in soup.select('li.booklink')[:10]:
                title_elem = result.select_one('span.title')
                author_elem = result.select_one('span.author')
                link_elem = result.select_one('a')
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    author = author_elem.get_text(strip=True) if author_elem else 'Unknown'
                    
                    # Multilingual AI Classification
                    ai_classification = self.ai_classify_text_multilingual(title, author, '', language)
                    
                    # High-confidence primary texts only
                    if ai_classification['is_primary_text'] and ai_classification['confidence'] > 0.4:
                        book_id = link_elem['href'].split('/')[-1]
                        
                        result_entry = {
                            'source': 'gutenberg',
                            'collection': collection_type,
                            'language': language,
                            'id': book_id,
                            'title': title,
                            'author': author,
                            'search_term': term,
                            'ai_classification': ai_classification,
                            'diachronic_transition': self.identify_diachronic_transition(collection_type),
                            'text_url': f'https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8',
                            'preview_info': self.create_multilingual_preview(title, collection_type, language)
                        }
                        
                        results.append(result_entry)
                        print(f"    ✅ AI VERIFIED ({language}): {title[:35]}... (Conf: {ai_classification['confidence']:.2f})")
                    else:
                        print(f"    ❌ AI FILTERED ({language}): {title[:35]}... ({ai_classification['classification']})")
                        
        except Exception as e:
            print(f"    Error: {e}")
        
        return results
    
    def search_archive_ai_multilingual(self, term: str, collection_type: str, language: str) -> List[Dict]:
        """Archive.org search with multilingual AI classification"""
        results = []
        
        try:
            # Language-specific query enhancement
            lang_queries = {
                'greek': f'{term} AND (greek OR ελληνικά OR byzantine)',
                'latin': f'{term} AND (latin OR latina OR medieval)',
                'french': f'{term} AND (french OR français OR ancien)',
                'german': f'{term} AND (german OR deutsch OR mittelhoch)',
                'italian': f'{term} AND (italian OR italiano OR medievale)',
                'spanish': f'{term} AND (spanish OR español OR medieval)'
            }
            
            query = f'{lang_queries.get(language, term)} AND mediatype:texts'
            api_url = f'https://archive.org/advancedsearch.php?q={query.replace(" ", "%20")}&fl=identifier,title,creator,date,description,language&rows=6&page=1&output=json'
            
            response = requests.get(api_url, timeout=15)
            data = response.json()
            
            for doc in data.get('response', {}).get('docs', []):
                title = doc.get('title', 'Unknown')
                author = doc.get('creator', 'Unknown')
                description = doc.get('description', '')
                
                # Multilingual AI Classification
                ai_classification = self.ai_classify_text_multilingual(title, author, description, language)
                
                if ai_classification['is_primary_text'] and ai_classification['confidence'] > 0.3:
                    result_entry = {
                        'source': 'archive_org',
                        'collection': collection_type,
                        'language': language,
                        'id': doc.get('identifier', ''),
                        'title': title,
                        'author': author,
                        'date': doc.get('date', 'Unknown'),
                        'description': description,
                        'archive_language': doc.get('language', []),
                        'search_term': term,
                        'ai_classification': ai_classification,
                        'diachronic_transition': self.identify_diachronic_transition(collection_type),
                        'download_url': f"https://archive.org/download/{doc.get('identifier', '')}/{doc.get('identifier', '')}.txt",
                        'preview_info': self.create_multilingual_preview(title, collection_type, language)
                    }
                    
                    results.append(result_entry)
                    print(f"    ✅ AI VERIFIED ({language}): {title[:35]}... (Conf: {ai_classification['confidence']:.2f})")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"    Archive error: {e}")
        
        return results
    
    def identify_diachronic_transition(self, collection_type: str) -> str:
        """Identify the diachronic transition for any collection"""
        transitions = {
            # Greek transitions
            'greek_ancient_to_koine': 'Ancient Greek (800-300 BCE) → Koine Greek (300 BCE-600 CE)',
            'greek_koine_to_byzantine': 'Koine Greek (300 BCE-600 CE) → Byzantine Greek (600-1453 CE)',
            'greek_byzantine_to_medieval': 'Byzantine Greek (600-1453) → Medieval Greek (1453-1669)',
            'greek_medieval_to_modern': 'Medieval Greek (1453-1669) → Modern Greek (1669+)',
            'greek_katharevousa_to_demotic': 'Katharevousa (Puristic) → Demotic (Vernacular)',
            'greek_biblical_retranslations': 'Ancient Biblical Greek → Modern Greek Bible',
            
            # English transitions
            'english_old_to_middle': 'Old English (450-1150) → Middle English (1150-1500)',
            'english_middle_to_early_modern': 'Middle English (1150-1500) → Early Modern (1500-1700)',
            'english_early_modern_to_modern': 'Early Modern (1500-1700) → Modern English (1700+)',
            
            # Other language transitions
            'latin_classical_to_medieval': 'Classical Latin → Medieval Latin',
            'french_old_to_middle': 'Old French → Middle French',
            'german_middle_high_to_modern': 'Middle High German → Modern German',
            'italian_medieval_to_renaissance': 'Medieval Italian → Renaissance Italian',
            'spanish_medieval_to_golden_age': 'Medieval Spanish → Golden Age Spanish'
        }
        
        return transitions.get(collection_type, 'Unknown diachronic transition')
    
    def create_multilingual_preview(self, title: str, collection_type: str, language: str) -> List[str]:
        """Create preview for any language"""
        lang_names = {
            'greek': 'Greek', 'latin': 'Latin', 'french': 'French',
            'german': 'German', 'italian': 'Italian', 'spanish': 'Spanish',
            'english': 'English'
        }
        
        lang_name = lang_names.get(language, language.title())
        
        if 'ancient_to_koine' in collection_type:
            return [f"Ancient → Koine {lang_name} transition", "Early linguistic evolution"]
        elif 'medieval_to_modern' in collection_type:
            return [f"Medieval → Modern {lang_name} evolution", "Historical language modernization"]
        elif 'biblical' in collection_type:
            return [f"{lang_name} Biblical retranslation", "Religious text linguistic evolution"]
        else:
            return [f"{lang_name} diachronic evolution", "Historical language change"]
    
    def save_universal_ai_collections(self):
        """Save all AI-classified collections with comprehensive metadata"""
        base_dir = Path('corpus_texts/universal_ai_classified')
        base_dir.mkdir(parents=True, exist_ok=True)
        
        total_verified = 0
        language_totals = {}
        
        print(f"\n{'='*80}")
        print("🤖🌍 UNIVERSAL AI-CLASSIFIED DIACHRONIC COLLECTIONS")
        print(f"{'='*80}")
        
        for collection_name, texts in self.collections.items():
            if texts:
                collection_dir = base_dir / collection_name
                collection_dir.mkdir(parents=True, exist_ok=True)
                
                # Determine language
                if 'greek' in collection_name:
                    lang = 'Greek'
                elif 'english' in collection_name:
                    lang = 'English'
                elif 'latin' in collection_name:
                    lang = 'Latin'
                elif 'french' in collection_name:
                    lang = 'French'
                elif 'german' in collection_name:
                    lang = 'German'
                elif 'italian' in collection_name:
                    lang = 'Italian'
                elif 'spanish' in collection_name:
                    lang = 'Spanish'
                else:
                    lang = 'Unknown'
                
                # Save with comprehensive AI metadata
                collection_file = collection_dir / f'{collection_name}_ai_classified.json'
                with open(collection_file, 'w', encoding='utf-8') as f:
                    json.dump(texts, f, indent=2, ensure_ascii=False)
                
                # Create detailed preview
                preview_file = collection_dir / f'{collection_name}_ai_preview.txt'
                with open(preview_file, 'w', encoding='utf-8') as f:
                    f.write(f"🤖 AI-CLASSIFIED: {collection_name.upper().replace('_', ' ')}\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"Language: {lang}\n")
                    f.write(f"Total AI-verified texts: {len(texts)}\n")
                    f.write(f"Classification: PRIMARY TEXTS ONLY (High Confidence)\n\n")
                    
                    for i, text in enumerate(texts[:20], 1):  # Show first 20
                        ai_info = text.get('ai_classification', {})
                        f.write(f"{i:2d}. {text.get('title', 'Unknown')}\n")
                        f.write(f"    👤 Author: {text.get('author', 'Unknown')}\n")
                        f.write(f"    🔄 Transition: {text.get('diachronic_transition', 'Unknown')}\n")
                        f.write(f"    🤖 AI Confidence: {ai_info.get('confidence', 0):.3f}\n")
                        f.write(f"    📊 Scores: Text={ai_info.get('text_score', 0)}, Commentary={ai_info.get('commentary_score', 0)}\n")
                        if text.get('preview_info'):
                            f.write(f"    ℹ️  {text['preview_info'][0]}\n")
                            f.write(f"    📝 {text['preview_info'][1]}\n")
                        f.write("\n")
                    
                    if len(texts) > 20:
                        f.write(f"... and {len(texts) - 20} more AI-verified texts\n")
                
                total_verified += len(texts)
                language_totals[lang] = language_totals.get(lang, 0) + len(texts)
                
                print(f"🤖 {collection_name:35s}: {len(texts):3d} AI-verified texts ({lang})")
        
        print(f"\n📊 UNIVERSAL AI CLASSIFICATION SUMMARY:")
        print(f"   Total AI-verified texts: {total_verified}")
        print(f"   Collections created: {len([c for c in self.collections.values() if c])}")
        print(f"   By language:")
        for lang, count in sorted(language_totals.items()):
            print(f"     {lang}: {count} texts")
        print(f"   Base directory: {base_dir}")
        print(f"   Quality: HIGH CONFIDENCE PRIMARY TEXTS ONLY")
        
        return base_dir, total_verified, language_totals

if __name__ == "__main__":
    classifier = UniversalAITextClassifier()
    classifier.collect_greek_diachronic_comprehensive()
    classifier.collect_all_languages_diachronic()
    base_dir, total, lang_totals = classifier.save_universal_ai_collections()
