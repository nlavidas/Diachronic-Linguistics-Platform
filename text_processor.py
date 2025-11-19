import re
import nltk
import spacy
import textstat
from datetime import datetime
from typing import Dict, Any, List
import string

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextProcessor:
    def __init__(self):
        # Load spaCy model (you may need to download it: python -m spacy download en_core_web_sm)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy English model not found. Please install it with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
    
    def process_text(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process text data including cleaning, tokenization, and analysis
        """
        # Extract text components
        title = data.get('title', '')
        abstract = data.get('abstract', '')
        full_text = data.get('full_text', '')
        language = data.get('language', 'en')
        
        # Combine all text for processing
        combined_text = f"{title} {abstract} {full_text}".strip()
        
        # Clean the text
        cleaned_text = self._clean_text(combined_text)
        
        # Process with spaCy if available
        if self.nlp:
            doc = self.nlp(cleaned_text)
            processed_text = self._process_with_spacy(doc)
            keywords = self._extract_keywords_spacy(doc)
        else:
            processed_text = self._process_with_nltk(cleaned_text)
            keywords = self._extract_keywords_nltk(cleaned_text)
        
        # Calculate metrics
        word_count = len(cleaned_text.split())
        readability_score = self._calculate_readability(cleaned_text)
        
        # Extract subject areas from text
        subject_areas = self._extract_subject_areas(cleaned_text)
        
        # Update the data with processed information
        processed_data = data.copy()
        processed_data.update({
            'processed_text': processed_text,
            'word_count': word_count,
            'readability_score': readability_score,
            'keywords': keywords,
            'subject_areas': subject_areas,
            'language': language
        })
        
        return processed_data
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        
        # Remove multiple punctuation
        text = re.sub(r'[.,!?;:]{2,}', '.', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _process_with_spacy(self, doc) -> str:
        """Process text using spaCy"""
        processed_tokens = []
        
        for token in doc:
            # Skip stop words, punctuation, and whitespace
            if (not token.is_stop and 
                not token.is_punct and 
                not token.is_space and
                not token.is_digit and
                len(token.text) > 2):
                processed_tokens.append(token.lemma_.lower())
        
        return ' '.join(processed_tokens)
    
    def _process_with_nltk(self, text: str) -> str:
        """Process text using NLTK as fallback"""
        # Tokenize
        tokens = nltk.word_tokenize(text.lower())
        
        # Remove stop words and short words
        processed_tokens = []
        for token in tokens:
            if (token not in self.stop_words and
                token not in string.punctuation and
                len(token) > 2 and
                token.isalpha()):
                processed_tokens.append(token)
        
        return ' '.join(processed_tokens)
    
    def _extract_keywords_spacy(self, doc) -> List[str]:
        """Extract keywords using spaCy"""
        keywords = []
        
        # Extract noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:  # Limit to 3-word phrases
                keywords.append(chunk.text.lower())
        
        # Extract named entities
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE', 'EVENT', 'WORK_OF_ART']:
                keywords.append(ent.text.lower())
        
        # Remove duplicates and return top keywords
        unique_keywords = list(set(keywords))
        return unique_keywords[:20]  # Return top 20 keywords
    
    def _extract_keywords_nltk(self, text: str) -> List[str]:
        """Extract keywords using NLTK as fallback"""
        # Simple keyword extraction based on frequency
        words = text.split()
        word_freq = {}
        
        for word in words:
            if len(word) > 3 and word.isalpha():
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:20]]
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score using textstat"""
        if not text:
            return 0.0
        
        try:
            # Use Flesch Reading Ease score
            score = textstat.flesch_reading_ease(text)
            return round(score, 2)
        except:
            return 0.0
    
    def _extract_subject_areas(self, text: str) -> List[str]:
        """Extract subject areas based on keywords in the text"""
        subject_keywords = {
            'computer science': ['algorithm', 'programming', 'software', 'computer', 'data', 'machine learning', 'ai', 'artificial intelligence'],
            'mathematics': ['theorem', 'proof', 'equation', 'mathematical', 'statistics', 'probability', 'calculus'],
            'physics': ['quantum', 'particle', 'energy', 'force', 'wave', 'electromagnetic', 'thermodynamics'],
            'biology': ['cell', 'dna', 'protein', 'organism', 'evolution', 'genetics', 'molecular'],
            'medicine': ['patient', 'clinical', 'treatment', 'disease', 'medical', 'health', 'diagnosis'],
            'chemistry': ['molecule', 'chemical', 'reaction', 'compound', 'synthesis', 'catalyst'],
            'economics': ['market', 'economy', 'financial', 'economic', 'trade', 'investment', 'gdp'],
            'psychology': ['behavior', 'cognitive', 'mental', 'psychological', 'brain', 'consciousness'],
            'engineering': ['design', 'system', 'structure', 'mechanical', 'electrical', 'construction'],
            'environmental': ['climate', 'environment', 'sustainability', 'pollution', 'ecosystem', 'green']
        }
        
        text_lower = text.lower()
        detected_areas = []
        
        for area, keywords in subject_keywords.items():
            keyword_count = sum(1 for keyword in keywords if keyword in text_lower)
            if keyword_count >= 2:  # Require at least 2 keywords to classify
                detected_areas.append(area)
        
        return detected_areas
    
    def get_text_statistics(self, text: str) -> Dict[str, Any]:
        """Get comprehensive text statistics"""
        if not text:
            return {}
        
        stats = {
            'word_count': len(text.split()),
            'character_count': len(text),
            'sentence_count': textstat.sentence_count(text),
            'paragraph_count': len([p for p in text.split('\n\n') if p.strip()]),
            'readability_score': self._calculate_readability(text),
            'avg_words_per_sentence': textstat.avg_sentence_length(text),
            'avg_syllables_per_word': textstat.avg_syllables_per_word(text)
        }
        
        return stats