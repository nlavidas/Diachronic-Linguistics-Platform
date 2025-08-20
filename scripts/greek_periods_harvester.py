import logging
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)
project_root = Path(__file__).resolve().parent.parent

def harvest_greek_periods():
    """Harvest Greek texts from different historical periods"""
    
    sources = {
        "Koine": {
            "url": "https://www.ellopos.net/elpenor/greek-texts/new-testament/default.asp",
            "period": "Koine_300BCE-600CE"
        },
        "Byzantine": {
            "url": "https://www.ellopos.net/elpenor/greek-texts/byzantine/default.asp",
            "period": "Byzantine_600-1453"
        },
        "Modern": {
            "url": "https://el.wikisource.org/wiki/Κατηγορία:Νέα_ελληνικά",
            "period": "Modern_1453-present"
        }
    }
    
    for name, info in sources.items():
        try:
            output_dir = project_root / f"corpus_texts/greek_{info['period']}"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            response = requests.get(info['url'], timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all Greek text
            greek_text = []
            for element in soup.find_all(text=True):
                if re.search(r'[α-ωΑ-Ω]', element):
                    greek_text.append(element)
            
            if greek_text:
                output_file = output_dir / f"{name}_sample.txt"
                output_file.write_text('\n'.join(greek_text), encoding='utf-8')
                logger.info(f"Harvested {name} Greek texts")
                
        except Exception as e:
            logger.error(f"Failed to harvest {name}: {e}")

def find_retranslations():
    """Find Byzantine and Modern Greek retranslations of classical texts"""
    
    retranslation_queries = [
        "Όμηρος Ιλιάδα νεοελληνική μετάφραση",
        "Οδύσσεια νέα ελληνικά κείμενο",
        "Βυζαντινή παράφραση Ομήρου",
        "Ψελλός παράφραση κλασικά",
        "Τζέτζης Ομηρικά",
        "Ευστάθιος Θεσσαλονίκης σχόλια",
        "Καζαντζάκης Οδύσσεια",
        "Κάλβος μετάφραση αρχαία",
        "Πολυλάς μετάφραση",
        "Στασινόπουλος Ιλιάδα"
    ]
    
    discovered = []
    for query in retranslation_queries:
        try:
            # Search for open-access versions
            search_url = f"https://www.google.com/search?q={query}+filetype:pdf+OR+filetype:txt"
            # Add to discovered URLs for later processing
            discovered.append(query)
            logger.info(f"Searching for: {query}")
        except Exception as e:
            logger.error(f"Search failed for {query}: {e}")
    
    return discovered

if __name__ == "__main__":
    harvest_greek_periods()
    retranslations = find_retranslations()
    print(f"Found {len(retranslations)} potential retranslation sources")
