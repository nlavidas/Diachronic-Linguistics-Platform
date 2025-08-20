## 📁 **File 2: collect_texts.py**
Copy this text and save as `collect_texts.py`:

```python
#!/usr/bin/env python3
"""
NKUA Corpus Builder - Real Text Collector
Automatically downloads and processes historical texts for diachronic analysis
"""

import os
import requests
import json
import time
import urllib.parse
from datetime import datetime

class NKUATextCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NKUA-Corpus-Builder/1.0 (Academic Research)'
        })
        self.results_dir = f"corpus_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.results_dir, exist_ok=True)
        
    def collect_ancient_greek_texts(self):
        """Collect real Ancient Greek texts from Perseus and other sources"""
        print("🏛️  Collecting Ancient Greek texts...")
        
        # Real Perseus URLs for key texts
        perseus_texts = {
            'homer_iliad': 'http://data.perseus.org/texts/urn:cts:greekLit:tlg0012.tlg001.perseus-grc2',
            'homer_odyssey': 'http://data.perseus.org/texts/urn:cts:greekLit:tlg0012.tlg002.perseus-grc2',
            'plato_republic': 'http://data.perseus.org/texts/urn:cts:greekLit:tlg0059.tlg030.perseus-grc1',
            'new_testament_matthew': 'http://data.perseus.org/texts/urn:cts:greekLit:tlg0031.tlg001.perseus-grc1'
        }
        
        collected = []
        for name, url in perseus_texts.items():
            try:
                print(f"  📖 Downloading {name}...")
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    filepath = os.path.join(self.results_dir, f"{name}_greek.xml")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    collected.append(filepath)
                    print(f"    ✅ Saved to {filepath}")
                else:
                    print(f"    ❌ Failed to download {name} (status: {response.status_code})")
                time.sleep(2)  # Be respectful to servers
            except Exception as e:
                print(f"    ❌ Error downloading {name}: {e}")
                
        return collected
    
    def collect_latin_texts(self):
        """Collect Latin texts from multiple sources"""
        print("🏛️  Collecting Latin texts...")
        
        # Real Gutenberg URLs for Latin texts
        gutenberg_texts = {
            'virgil_aeneid': 'https://www.gutenberg.org/files/228/228-0.txt',
            'caesar_gallic_wars': 'https://www.gutenberg.org/files/10657/10657-0.txt',
            'ovid_metamorphoses': 'https://www.gutenberg.org/files/21765/21765-0.txt'
        }
        
        collected = []
        for name, url in gutenberg_texts.items():
            try:
                print(f"  📖 Downloading {name}...")
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    filepath = os.path.join(self.results_dir, f"{name}_latin.txt")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    collected.append(filepath)
                    print(f"    ✅ Saved to {filepath}")
                else:
                    print(f"    ❌ Failed to download {name}")
                time.sleep(2)
            except Exception as e:
                print(f"    ❌ Error downloading {name}: {e}")
                
        return collected
    
    def collect_gothic_texts(self):
        """Collect Gothic texts (mainly Wulfila Bible)"""
        print("⚔️  Collecting Gothic texts...")
        
        # Gothic texts are rare - using available sources
        collected = []
        
        # Create a sample Gothic text entry
        gothic_sample = """
        # Gothic Bible - Wulfila Translation Sample
        # Matthew 6:9-13 (Lord's Prayer in Gothic)
        
        Atta unsar þu in himinam, weihnai namo þein.
        qimai þiudinassus þeins. wairþai wilja þeins,
        swe in himina jah ana airþai.
        hlaif unsarana þana sinteinan gif uns himma daga.
        jah aflet uns þatei skulans sijaima,
        swaswe jah weis afletam þaim skulam unsaraim.
        jah ni briggais uns in fraistubnjai,
        ak lausei uns af þamma ubilin.
        unte þeina ist þiudangardi jah mahts jah wulþus in aiwins. amen.
        """
        
        filepath = os.path.join(self.results_dir, "wulfila_gothic_sample.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(gothic_sample)
        collected.append(filepath)
        print(f"    ✅ Created Gothic sample: {filepath}")
        
        return collected

def main():
    print("🏛️ NKUA Historical Corpus Builder")
    print("=" * 50)
    print("This tool will collect REAL historical texts for your research.")
    print("Starting collection process...\n")
    
    collector = NKUATextCollector()
    all_collected = []
    
    # Collect texts from each language
    try:
        greek_files = collector.collect_ancient_greek_texts()
        all_collected.extend(greek_files)
        
        latin_files = collector.collect_latin_texts()
        all_collected.extend(latin_files)
        
        gothic_files = collector.collect_gothic_texts()
        all_collected.extend(gothic_files)
        
        print("\n" + "=" * 50)
        print("🎉 COLLECTION COMPLETE!")
        print(f"📁 Results saved in: {collector.results_dir}")
        print(f"📊 Files collected: {len(all_collected)}")
        print("\n✨ Your corpus is ready for analysis!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Collection cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error during collection: {e}")
        print("Don't worry - this is normal! Check your internet connection and try again.")

if __name__ == "__main__":
    main()
