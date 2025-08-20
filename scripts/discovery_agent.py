import logging
from pathlib import Path
import time
from googlesearch import search
import requests
from bs4 import BeautifulSoup

# (Setup remains the same)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)
project_root = Path(__file__).resolve().parent.parent
DISCOVERY_TOPICS_FILE = project_root / "discovery_topics.txt"
DISCOVERED_URLS_FILE = project_root / "discovered_urls.csv"

# (get_page_details function remains the same)
def get_page_details(url):
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string.strip() if soup.title else "No Title Found"
        first_p = soup.find('p')
        snippet = first_p.get_text(strip=True)[:200] + "..." if first_p else "No snippet available."
        return title.replace('"', "'"), snippet.replace('"', "'") # Sanitize for CSV
    except Exception:
        return "Fetch Error", "N/A"

def run_discovery_cycle():
    logger.info("--- Starting new discovery cycle. ---")
    topics = DISCOVERED_URLS_FILE.read_text(encoding='utf-8').strip().split('\n')
    for topic in topics:
        if topic.strip() and not topic.startswith('#'):
            logger.info(f"--- Searching for topic: '{topic}' ---")
            query = f'"{topic}" "open access" OR "public domain" site:archive.org OR site:gutenberg.org OR site:gallica.bnf.fr'
            try:
                results = list(search(query, num_results=50, sleep_interval=5)) # Increased to 50 results
                if results:
                    logger.info(f"Found {len(results)} URLs. Fetching details...")
                    with open(DISCOVERED_URLS_FILE, 'a', encoding='utf-8') as f:
                        for url in results:
                            title, snippet = get_page_details(url)
                            f.write(f'"{url}","{title}","{snippet}"\n')
                            time.sleep(1)
            except Exception as e:
                logger.error(f"An error occurred during search for '{topic}': {e}")
            time.sleep(30) # Be polite between topics

# --- MAIN 24/7 LOOP ---
if __name__ == "__main__":
    logger.info("🚀 24/7 Discovery Agent Initialized...")
    if not DISCOVERED_URLS_FILE.exists():
        DISCOVERED_URLS_FILE.write_text("URL,Title,Snippet\n", encoding='utf-8')

    while True:
        try:
            run_discovery_cycle()
            logger.info("--- Discovery cycle complete. Agent sleeping for 6 hours. ---")
            time.sleep(21600) # Sleep for 6 hours (60 * 60 * 6)
        except KeyboardInterrupt:
            logger.info("Shutdown signal received."); break
        except Exception as e:
            logger.error(f"A critical error occurred in main loop: {e}"); time.sleep(300)