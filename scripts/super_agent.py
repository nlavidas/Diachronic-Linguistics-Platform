import logging
from pathlib import Path
import time
import sys
import os

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# --- THIS IS THE CRITICAL FIX ---
# Import all functions from our "toolbox" so the agent can use them.
from scripts.agent_actions import *

# (Setup and other functions remain the same)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler(), logging.FileHandler(project_root / "super_agent_log.txt", mode='a', encoding='utf-8')])
logger = logging.getLogger(__name__)
QUEUE_FILE = project_root / "master_mission.txt"

def process_mission(mission_string):
    logger.info(f"Received mission: '{mission_string}'")
    try:
        command, data = [item.strip() for item in mission_string.split(':', 1)] if ':' in mission_string else (mission_string, None)
        
        if command == "HARVEST":
            if data == "PERSEUS_GREEK": harvest_perseus_mission()
            elif data == "GUTENBERG_ENGLISH_DIACHRONIC": harvest_gutenberg_english()
        elif command == "PROCESS":
            if data == "GREEK_CORPUS": preprocess_corpus_mission("corpus_texts/perseus_greek_classics", "greek")
            elif data == "ENGLISH_CORPUS": preprocess_corpus_mission("corpus_texts/gutenberg_english", "english")
        else:
            logger.warning(f"Unknown mission: {mission_string}")
    except Exception as e:
        logger.error(f"A critical error occurred during mission '{mission_string}': {e}", exc_info=True)

def get_next_mission():
    if not QUEUE_FILE.exists() or os.stat(QUEUE_FILE).st_size == 0: return None
    with open(QUEUE_FILE, 'r+', encoding='utf-8') as f:
        lines = f.readlines(); next_mission = lines.pop(0).strip(); f.seek(0); f.truncate(); f.writelines(lines)
    return next_mission if next_mission else None

def main():
    logger.info("🚀 Super Agent v3.2 (Autonomous Orchestrator) Initialized...")
    while True:
        try:
            mission = get_next_mission()
            if mission:
                process_mission(mission)
            else:
                logger.info("All missions complete. Agent is now idle. Checking again in 1 hour.")
                time.sleep(3600)
        except KeyboardInterrupt:
            logger.info("Shutdown signal received. Exiting gracefully."); break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True); time.sleep(300)

if __name__ == "__main__":
    main()