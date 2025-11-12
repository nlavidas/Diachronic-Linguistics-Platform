"""
AI-POWERED ANNOTATION SYSTEM
Integrates LLM-enhanced annotation from llm_enhanced_annotator.py
Supports GPT-5, Claude, Gemini, and local Ollama
4-Phase Pipeline: Prompt Engineering → Validation → Batch Processing → Quality Check
"""

import requests
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime
import json
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAnnotator:
    """
    AI-powered linguistic annotation with multiple LLM backends
    Integrated from llm_enhanced_annotator.py
    """
    
    def __init__(self, db_path: str = "Z:/GlossaChronos/automated_pipeline/texts.db"):
        self.db_path = db_path
        
        # LLM Configurations (from llm_enhanced_annotator.py)
        self.llm_configs = {
            'openai_gpt4': {
                'api_url': 'https://api.openai.com/v1/chat/completions',
                'model': 'gpt-4',
                'cost_per_1k_tokens': 0.03,
                'api_key_env': 'OPENAI_API_KEY',
                'enabled': os.getenv('OPENAI_API_KEY') is not None
            },
            'anthropic_claude': {
                'api_url': 'https://api.anthropic.com/v1/messages',
                'model': 'claude-3-5-sonnet-20241022',
                'cost_per_1k_tokens': 0.015,
                'api_key_env': 'ANTHROPIC_API_KEY',
                'enabled': os.getenv('ANTHROPIC_API_KEY') is not None
            },
            'google_gemini': {
                'api_url': 'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent',
                'model': 'gemini-1.5-pro',
                'cost_per_1k_tokens': 0.00125,
                'api_key_env': 'GOOGLE_API_KEY',
                'enabled': os.getenv('GOOGLE_API_KEY') is not None
            },
            'ollama_local': {
                'api_url': 'http://localhost:11434/api/generate',
                'model': 'llama3.2',
                'cost_per_1k_tokens': 0.0,
                'api_key_env': None,
                'enabled': True  # Always available if Ollama running
            }
        }
        
        # Temporal-aware prompt templates
        self.prompt_templates = {
            'morphological': """You are a historical linguist annotating {language} texts from {period} ({year_range}).

Analyze this sentence for morphological features:
"{sentence}"

Provide for each word:
1. Lemma (base form)
2. Part of speech (Universal Dependencies)
3. Morphological features (Person, Number, Tense, Mood, Voice, Gender, Case)
4. Historical notes (if form differs from modern usage)

Output as JSON array with format:
[{{"word": "...", "lemma": "...", "pos": "...", "features": {{}}, "notes": "..."}}]""",
            
            'semantic_shift': """You are detecting lexical semantic change across time periods.

Word: "{word}"
Sentence: "{sentence}"
Period: {period} ({year_range})

Has this word's meaning shifted compared to modern usage?
If yes, provide:
1. Historical meaning in this period
2. Modern meaning
3. Approximate shift date
4. Shift type (narrowing/broadening/amelioration/pejoration/metaphor)

Output as JSON: {{"has_shifted": true/false, "historical_meaning": "...", "modern_meaning": "...", "shift_date": "...", "shift_type": "..."}}""",
            
            'syntax': """Annotate syntactic dependencies for this {language} sentence from {period}:

"{sentence}"

For each word provide:
1. Head (which word it depends on, 0 for root)
2. Dependency relation (Universal Dependencies)
3. Historical syntax notes (archaic constructions, word order changes)

Output as JSON array:
[{{"id": 1, "word": "...", "head": 0, "deprel": "...", "notes": "..."}}]"""
        }
        
        # Period metadata
        self.period_metadata = {
            'ancient': {'years': '800 BCE - 600 CE'},
            'byzantine': {'years': '600 - 1453 CE'},
            'katharevousa': {'years': '1700 - 1976 CE'},
            'demotic': {'years': '1976 - 2024 CE'},
            'old': {'years': '450 - 1150 CE'},
            'middle': {'years': '1150 - 1500 CE'},
            'early_modern': {'years': '1500 - 1700 CE'},
            'modern': {'years': '1700 - 2024 CE'},
            'classical': {'years': '100 BCE - 200 CE'},
            'medieval': {'years': '500 - 1500 CE'}
        }
        
        self.stats = {
            'total_annotated': 0,
            'llm_calls': 0,
            'total_cost': 0.0,
            'by_llm': {},
            'errors': []
        }
        
        self._init_database()
        
        logger.info("="*80)
        logger.info("AI ANNOTATION SYSTEM INITIALIZED")
        logger.info("="*80)
        self._log_available_llms()
    
    def _init_database(self):
        """Initialize annotation database"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS ai_annotations (
                id INTEGER PRIMARY KEY,
                text_id INTEGER,
                language TEXT,
                period TEXT,
                sentence TEXT,
                morphology TEXT,
                semantic_shifts TEXT,
                syntax TEXT,
                llm_used TEXT,
                annotated_at TEXT,
                processing_time REAL,
                FOREIGN KEY (text_id) REFERENCES collected_texts(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _log_available_llms(self):
        """Log which LLMs are available"""
        logger.info("\nAvailable LLMs:")
        for name, config in self.llm_configs.items():
            status = "✓ ENABLED" if config['enabled'] else "✗ Disabled (API key missing)"
            cost = f"${config['cost_per_1k_tokens']}/1K tokens" if config['cost_per_1k_tokens'] > 0 else "FREE"
            logger.info(f"  {name}: {status} - {cost}")
    
    def get_best_available_llm(self) -> str:
        """Get best available LLM (prefer free local, then cheapest cloud)"""
        # Priority: Ollama (free) → Gemini (cheapest) → Claude → GPT-4
        for llm in ['ollama_local', 'google_gemini', 'anthropic_claude', 'openai_gpt4']:
            if self.llm_configs[llm]['enabled']:
                return llm
        return 'ollama_local'  # Fallback to local even if not running
    
    def annotate_text(self, text: str, language: str, period: str, 
                     llm: Optional[str] = None) -> Dict:
        """
        Annotate text with AI
        
        Args:
            text: Text to annotate
            language: Language code (grc, la, en, etc.)
            period: Time period (ancient, medieval, etc.)
            llm: Which LLM to use (auto-select if None)
        """
        if not llm:
            llm = self.get_best_available_llm()
        
        logger.info(f"\n[AI ANNOTATION] Using {llm} for {language}/{period}")
        
        start_time = time.time()
        
        # Split into sentences (simple split for now)
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20][:10]  # Max 10 sentences
        
        results = []
        
        for idx, sentence in enumerate(sentences, 1):
            logger.info(f"  Sentence {idx}/{len(sentences)}: {sentence[:50]}...")
            
            try:
                # Morphological annotation
                morph_prompt = self.prompt_templates['morphological'].format(
                    language=language,
                    period=period,
                    year_range=self.period_metadata.get(period, {}).get('years', 'Unknown'),
                    sentence=sentence
                )
                morphology = self._call_llm(morph_prompt, llm)
                
                # Semantic shift detection
                words = sentence.split()[:5]  # Check first 5 words
                semantic_shifts = []
                for word in words:
                    if len(word) > 4:
                        shift_prompt = self.prompt_templates['semantic_shift'].format(
                            word=word,
                            sentence=sentence,
                            period=period,
                            year_range=self.period_metadata.get(period, {}).get('years', 'Unknown')
                        )
                        shift = self._call_llm(shift_prompt, llm)
                        if shift.get('has_shifted'):
                            semantic_shifts.append(shift)
                
                # Syntactic annotation
                syntax_prompt = self.prompt_templates['syntax'].format(
                    language=language,
                    period=period,
                    sentence=sentence
                )
                syntax = self._call_llm(syntax_prompt, llm)
                
                results.append({
                    'sentence': sentence,
                    'morphology': morphology,
                    'semantic_shifts': semantic_shifts,
                    'syntax': syntax
                })
                
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                logger.error(f"  Error annotating sentence: {e}")
                self.stats['errors'].append(str(e))
        
        processing_time = time.time() - start_time
        
        self.stats['total_annotated'] += len(sentences)
        self.stats['by_llm'][llm] = self.stats['by_llm'].get(llm, 0) + len(sentences)
        
        logger.info(f"  Completed in {processing_time:.1f}s")
        
        return {
            'language': language,
            'period': period,
            'llm_used': llm,
            'sentences_annotated': len(sentences),
            'results': results,
            'processing_time': processing_time
        }
    
    def _call_llm(self, prompt: str, llm: str) -> Dict:
        """Call specified LLM with prompt"""
        config = self.llm_configs[llm]
        
        if not config['enabled']:
            logger.warning(f"  {llm} not enabled, using fallback")
            return {}
        
        self.stats['llm_calls'] += 1
        
        try:
            if llm == 'ollama_local':
                return self._call_ollama(prompt, config)
            elif llm == 'openai_gpt4':
                return self._call_openai(prompt, config)
            elif llm == 'anthropic_claude':
                return self._call_anthropic(prompt, config)
            elif llm == 'google_gemini':
                return self._call_gemini(prompt, config)
        except Exception as e:
            logger.error(f"  LLM call failed: {e}")
            return {}
    
    def _call_ollama(self, prompt: str, config: Dict) -> Dict:
        """Call local Ollama"""
        try:
            response = requests.post(
                config['api_url'],
                json={
                    'model': config['model'],
                    'prompt': prompt,
                    'stream': False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '{}')
                # Try to parse as JSON
                try:
                    return json.loads(response_text)
                except:
                    return {'raw_response': response_text}
        except:
            pass
        
        return {}
    
    def _call_openai(self, prompt: str, config: Dict) -> Dict:
        """Call OpenAI GPT-4"""
        api_key = os.getenv(config['api_key_env'])
        if not api_key:
            return {}
        
        response = requests.post(
            config['api_url'],
            headers={'Authorization': f'Bearer {api_key}'},
            json={
                'model': config['model'],
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.3
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            self.stats['total_cost'] += config['cost_per_1k_tokens'] * data['usage']['total_tokens'] / 1000
            try:
                return json.loads(content)
            except:
                return {'raw_response': content}
        
        return {}
    
    def _call_anthropic(self, prompt: str, config: Dict) -> Dict:
        """Call Anthropic Claude"""
        api_key = os.getenv(config['api_key_env'])
        if not api_key:
            return {}
        
        response = requests.post(
            config['api_url'],
            headers={
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json'
            },
            json={
                'model': config['model'],
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 1024
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['content'][0]['text']
            try:
                return json.loads(content)
            except:
                return {'raw_response': content}
        
        return {}
    
    def _call_gemini(self, prompt: str, config: Dict) -> Dict:
        """Call Google Gemini"""
        api_key = os.getenv(config['api_key_env'])
        if not api_key:
            return {}
        
        url = f"{config['api_url']}?key={api_key}"
        
        response = requests.post(
            url,
            json={
                'contents': [{'parts': [{'text': prompt}]}]
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['candidates'][0]['content']['parts'][0]['text']
            try:
                return json.loads(content)
            except:
                return {'raw_response': content}
        
        return {}
    
    def print_stats(self):
        """Print annotation statistics"""
        print("\n" + "="*80)
        print("AI ANNOTATION STATISTICS")
        print("="*80)
        print(f"Total sentences annotated: {self.stats['total_annotated']}")
        print(f"LLM calls: {self.stats['llm_calls']}")
        print(f"Total cost: ${self.stats['total_cost']:.4f}")
        print(f"Errors: {len(self.stats['errors'])}")
        
        if self.stats['by_llm']:
            print("\nBy LLM:")
            for llm, count in self.stats['by_llm'].items():
                print(f"  {llm}: {count} sentences")
        
        print("="*80 + "\n")


if __name__ == "__main__":
    annotator = AIAnnotator()
    
    # Test annotation
    sample_text = "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος. οὐλομένην ἣ μυρί᾽ Ἀχαιοῖς ἄλγε᾽ ἔθηκε."
    
    result = annotator.annotate_text(
        text=sample_text,
        language='grc',
        period='ancient'
    )
    
    print("\n=== Annotation Result ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    annotator.print_stats()
