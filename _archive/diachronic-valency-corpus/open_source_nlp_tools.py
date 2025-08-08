#!/usr/bin/env python3
"""
OPEN SOURCE NLP TOOLS INTEGRATION
Light-side, AI-empowered translation and parsing tools
All completely open source and free
"""

import os
import sys
import subprocess
from pathlib import Path
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OpenSourceNLPTools:
    """
    Integration of open source NLP tools for the corpus
    """
    
    def __init__(self, base_path="Z:\\DiachronicValencyCorpus"):
        self.base_path = Path(base_path)
        self.tools_path = self.base_path / "open_source_tools"
        self.tools_path.mkdir(exist_ok=True)
        
        # Open source tools configuration
        self.tools = {
            'spacy': {
                'name': 'spaCy',
                'description': 'Industrial-strength NLP',
                'languages': ['en', 'de', 'fr', 'el', 'it', 'es', 'pt'],
                'features': ['POS', 'NER', 'dependency parsing'],
                'install': 'pip install spacy',
                'models': {
                    'en': 'en_core_web_sm',
                    'de': 'de_core_news_sm',
                    'fr': 'fr_core_news_sm',
                    'el': 'el_core_news_sm'
                }
            },
            'stanza': {
                'name': 'Stanza (Stanford NLP)',
                'description': 'State-of-the-art NLP for many languages',
                'languages': ['grc', 'la', 'en', 'de', 'fr'],  # grc = Ancient Greek, la = Latin
                'features': ['tokenization', 'lemmatization', 'POS', 'dependency'],
                'install': 'pip install stanza',
                'special': 'Excellent for Ancient Greek and Latin!'
            },
            'cltk': {
                'name': 'Classical Language Toolkit',
                'description': 'NLP for ancient languages',
                'languages': ['grc', 'la', 'sa', 'cop', 'akk'],  # Sanskrit, Coptic, Akkadian
                'features': ['lemmatization', 'POS', 'prosody', 'named entities'],
                'install': 'pip install cltk',
                'special': 'Specialized for classical languages!'
            },
            'polyglot': {
                'name': 'Polyglot',
                'description': 'Multilingual NLP',
                'languages': ['165+ languages'],
                'features': ['tokenization', 'NER', 'POS', 'sentiment'],
                'install': 'pip install polyglot'
            },
            'trankit': {
                'name': 'Trankit',
                'description': 'Light-weight Transformer-based NLP',
                'languages': ['100+ languages including Ancient Greek'],
                'features': ['tokenization', 'POS', 'NER', 'dependency parsing'],
                'install': 'pip install trankit',
                'special': 'GPU-optional, very accurate!'
            },
            'argostranslate': {
                'name': 'Argos Translate',
                'description': 'Open source neural machine translation',
                'languages': ['30+ language pairs'],
                'features': ['translation', 'language detection'],
                'install': 'pip install argostranslate',
                'special': 'Completely offline translation!'
            },
            'udpipe': {
                'name': 'UDPipe',
                'description': 'Trainable pipeline for CoNLL-U files',
                'languages': ['Universal Dependencies languages'],
                'features': ['tokenization', 'tagging', 'parsing'],
                'install': 'pip install ufal.udpipe',
                'special': 'Works with PROIEL format!'
            }
        }
        
    def check_installed_tools(self):
        """Check which tools are already installed"""
        logging.info("🔍 Checking installed NLP tools...")
        
        installed = {}
        
        # Check Python packages
        try:
            import pkg_resources
            installed_packages = {pkg.key for pkg in pkg_resources.working_set}
            
            for tool, info in self.tools.items():
                if tool in installed_packages:
                    installed[tool] = True
                    logging.info(f"✅ {info['name']} is installed")
                else:
                    installed[tool] = False
                    logging.info(f"❌ {info['name']} not installed")
                    
        except ImportError:
            logging.warning("Cannot check installed packages")
            
        return installed
        
    def create_installation_script(self):
        """Create script to install all tools"""
        logging.info("📝 Creating installation script...")
        
        install_script = """#!/usr/bin/env python3
'''
INSTALL ALL OPEN SOURCE NLP TOOLS
Run this to get all the AI-powered parsing tools
'''

import subprocess
import sys

print("🚀 Installing Open Source NLP Tools")
print("="*50)

# Core tools
tools = [
    ('spacy', 'Industrial-strength NLP'),
    ('stanza', 'Stanford NLP - great for Ancient Greek!'),
    ('cltk', 'Classical Language Toolkit'),
    ('trankit', 'Transformer-based multilingual NLP'),
    ('argostranslate', 'Offline neural translation'),
    ('ufal.udpipe', 'Universal Dependencies parser')
]

for package, description in tools:
    print(f"\\n📦 Installing {package}: {description}")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f"✅ {package} installed successfully!")
    except:
        print(f"❌ Failed to install {package}")

# Download language models
print("\\n📥 Downloading language models...")

# spaCy models
print("\\nDownloading spaCy models...")
for lang in ['en', 'de', 'fr', 'el']:
    try:
        subprocess.check_call([sys.executable, '-m', 'spacy', 'download', f'{lang}_core_web_sm'])
    except:
        print(f"Could not download {lang} model")

# Stanza models
print("\\nDownloading Stanza models...")
try:
    import stanza
    stanza.download('en')
    stanza.download('grc')  # Ancient Greek!
    stanza.download('la')   # Latin!
except:
    print("Could not download Stanza models")

print("\\n✅ Installation complete!")
print("You now have powerful open source NLP tools!")
"""
        
        script_path = self.tools_path / "install_nlp_tools.py"
        script_path.write_text(install_script)
        
        # Also create requirements.txt
        requirements = """# Open Source NLP Tools for Diachronic Corpus
spacy>=3.0.0
stanza>=1.4.0
cltk>=1.0.0
trankit>=1.0.0
argostranslate>=1.7.0
ufal.udpipe>=1.2.0
polyglot>=16.7.4

# Additional useful tools
nltk>=3.8
gensim>=4.0.0
scikit-learn>=1.0.0
pandas>=1.3.0
numpy>=1.21.0

# For Ancient Greek specifically
greek-accentuation>=1.2.0
pygreek>=0.1.0
"""
        
        req_path = self.tools_path / "requirements.txt"
        req_path.write_text(requirements)
        
        logging.info(f"✅ Created installation script at: {script_path}")
        logging.info(f"✅ Created requirements.txt at: {req_path}")
        
    def create_parsing_pipeline(self):
        """Create unified parsing pipeline using multiple tools"""
        logging.info("🔧 Creating parsing pipeline...")
        
        pipeline_script = '''#!/usr/bin/env python3
"""
UNIFIED PARSING PIPELINE
Combines multiple open source tools for best results
"""

import os
from pathlib import Path

class UnifiedParser:
    """Parse texts using multiple open source tools"""
    
    def __init__(self):
        self.parsers = {}
        self.load_parsers()
        
    def load_parsers(self):
        """Load available parsers"""
        # Try to load each parser
        try:
            import spacy
            self.parsers['spacy'] = spacy
            print("✅ spaCy loaded")
        except:
            print("❌ spaCy not available")
            
        try:
            import stanza
            self.parsers['stanza'] = stanza
            print("✅ Stanza loaded")
        except:
            print("❌ Stanza not available")
            
        try:
            import cltk
            self.parsers['cltk'] = cltk
            print("✅ CLTK loaded")
        except:
            print("❌ CLTK not available")
            
    def parse_text(self, text, language='en'):
        """Parse text with best available tool"""
        results = {}
        
        # Ancient Greek - use Stanza or CLTK
        if language in ['grc', 'ancient_greek']:
            if 'stanza' in self.parsers:
                nlp = self.parsers['stanza'].Pipeline('grc')
                doc = nlp(text)
                results['tokens'] = [(token.text, token.lemma, token.upos) 
                                   for sent in doc.sentences 
                                   for token in sent.tokens]
            elif 'cltk' in self.parsers:
                from cltk.tokenizers.word import WordTokenizer
                from cltk.lemmatize.greek import GreekBackoffLemmatizer
                tokenizer = WordTokenizer('greek')
                lemmatizer = GreekBackoffLemmatizer()
                tokens = tokenizer.tokenize(text)
                results['tokens'] = [(t, lemmatizer.lemmatize(t), 'UNK') 
                                   for t in tokens]
                                   
        # Latin - use Stanza or CLTK
        elif language in ['la', 'latin']:
            if 'stanza' in self.parsers:
                nlp = self.parsers['stanza'].Pipeline('la')
                doc = nlp(text)
                results['tokens'] = [(token.text, token.lemma, token.upos) 
                                   for sent in doc.sentences 
                                   for token in sent.tokens]
                                   
        # Modern languages - use spaCy
        elif language in ['en', 'de', 'fr', 'es', 'it']:
            if 'spacy' in self.parsers:
                nlp = self.parsers['spacy'].load(f'{language}_core_web_sm')
                doc = nlp(text)
                results['tokens'] = [(token.text, token.lemma_, token.pos_) 
                                   for token in doc]
                                   
        return results
        
    def parse_file(self, filepath, language='auto'):
        """Parse a file with automatic language detection"""
        text = Path(filepath).read_text(encoding='utf-8')
        
        # Auto-detect language from filename
        if language == 'auto':
            if 'greek' in filepath.lower() or 'grc' in filepath.lower():
                language = 'grc'
            elif 'latin' in filepath.lower() or 'lat' in filepath.lower():
                language = 'la'
            else:
                language = 'en'
                
        return self.parse_text(text, language)

# Example usage
if __name__ == "__main__":
    parser = UnifiedParser()
    
    # Test with sample text
    greek_text = "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος"
    results = parser.parse_text(greek_text, 'grc')
    print("\\nParsed Ancient Greek:")
    print(results)
'''
        
        pipeline_path = self.tools_path / "unified_parser.py"
        pipeline_path.write_text(pipeline_script)
        
        logging.info(f"✅ Created parsing pipeline at: {pipeline_path}")
        
    def create_translation_tool(self):
        """Create open source translation tool"""
        logging.info("🌐 Creating translation tool...")
        
        translation_script = '''#!/usr/bin/env python3
"""
OPEN SOURCE TRANSLATION TOOL
Using Argos Translate - completely offline!
"""

try:
    import argostranslate.package
    import argostranslate.translate
    
    class OpenTranslator:
        def __init__(self):
            # Download and install language packages
            self.setup_languages()
            
        def setup_languages(self):
            """Download language packages"""
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            
            # Install some useful packages
            needed = [
                ('en', 'el'),  # English to Greek
                ('el', 'en'),  # Greek to English
                ('en', 'la'),  # English to Latin
                ('la', 'en'),  # Latin to English
                ('en', 'fr'),  # English to French
                ('fr', 'en'),  # French to English
            ]
            
            for from_code, to_code in needed:
                package = next((p for p in available_packages 
                              if p.from_code == from_code and p.to_code == to_code), None)
                if package:
                    argostranslate.package.install_from_path(package.download())
                    
        def translate(self, text, from_lang, to_lang):
            """Translate text"""
            return argostranslate.translate.translate(text, from_lang, to_lang)
            
    # Example
    translator = OpenTranslator()
    result = translator.translate("Hello world", "en", "el")
    print(f"Translated: {result}")
    
except ImportError:
    print("Argos Translate not installed. Run: pip install argostranslate")
'''
        
        trans_path = self.tools_path / "open_translator.py"
        trans_path.write_text(translation_script)
        
        logging.info(f"✅ Created translation tool at: {trans_path}")
        
    def create_documentation(self):
        """Create documentation for all tools"""
        logging.info("📚 Creating documentation...")
        
        docs = """# Open Source NLP Tools for Diachronic Corpus

## 🌟 Overview

This collection provides powerful, completely open source tools for:
- Parsing Ancient Greek and Latin
- Modern language processing  
- Neural machine translation
- Dependency parsing
- Valency extraction

## 🛠️ Tools Included

### 1. **Stanza** (Stanford NLP)
- **Best for**: Ancient Greek, Latin
- **Features**: Full morphological analysis, dependency parsing
- **Special**: Trained on Perseus and PROIEL data!

### 2. **CLTK** (Classical Language Toolkit)  
- **Best for**: Classical languages
- **Features**: Specialized tools for ancient texts
- **Special**: Prosody analysis, Greek accentuation

### 3. **spaCy**
- **Best for**: Modern languages
- **Features**: Fast, production-ready NLP
- **Special**: Great for English translations

### 4. **Trankit**
- **Best for**: Multilingual processing
- **Features**: State-of-the-art accuracy
- **Special**: Works on CPU, supports 100+ languages

### 5. **Argos Translate**
- **Best for**: Offline translation
- **Features**: Neural machine translation
- **Special**: No API keys needed!

## 🚀 Quick Start

1. Install all tools:
   ```bash
   python install_nlp_tools.py
   ```

2. Parse Ancient Greek:
   ```python
   from unified_parser import UnifiedParser
   parser = UnifiedParser()
   results = parser.parse_text("μῆνιν ἄειδε θεὰ", "grc")
   ```

3. Translate offline:
   ```python
   from open_translator import OpenTranslator
   translator = OpenTranslator()
   translation = translator.translate("Hello", "en", "el")
   ```

## 📊 Integration with Corpus

These tools integrate with your diachronic corpus to:
- Extract valency patterns automatically
- Align translations
- Generate morphological annotations
- Create Universal Dependencies treebanks

## 🎯 For Your Research

Perfect for studying:
- Argument structure changes (NOM-ACC → NOM-DAT)
- Voice alternations (active/middle/passive)
- Lexical aspect shifts

All tools are:
- ✅ Completely free
- ✅ Open source
- ✅ Work offline
- ✅ No API limits
- ✅ Respect privacy
"""
        
        docs_path = self.tools_path / "README.md"
        docs_path.write_text(docs)
        
        logging.info(f"✅ Created documentation at: {docs_path}")
        
    def setup_all(self):
        """Setup everything"""
        logging.info("🚀 Setting up all open source NLP tools...")
        
        # Check what's installed
        self.check_installed_tools()
        
        # Create all scripts and docs
        self.create_installation_script()
        self.create_parsing_pipeline()
        self.create_translation_tool()
        self.create_documentation()
        
        logging.info("\n✅ Open source NLP tools setup complete!")
        logging.info(f"📁 Location: {self.tools_path}")
        logging.info("\n🎯 Next steps:")
        logging.info("1. Run: python open_source_tools/install_nlp_tools.py")
        logging.info("2. Test: python open_source_tools/unified_parser.py")
        logging.info("3. Translate: python open_source_tools/open_translator.py")

if __name__ == "__main__":
    tools = OpenSourceNLPTools()
    tools.setup_all()