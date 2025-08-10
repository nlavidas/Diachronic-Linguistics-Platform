import logging
from pathlib import Path
import time
import sys

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from scripts.agent_actions import parse_perseus_xml, preprocess_file

# --- SETUP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler(), logging.FileHandler(project_root / "agent_log.txt", mode='a', encoding='utf-8')])
logger = logging.getLogger(__name__)

QUEUE_FILE = project_root / "master_task_list.txt"
PERSEUS_REPO_PATH = project_root / "_archive" / "canonical-greekLit" / "data"
HARVEST_OUTPUT_FOLDER = project_root / "corpus_texts" / "perseus_harvest"
HARVEST_OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# --- HIGH-LEVEL ACTIONS ---
def run_perseus_harvest():
    logger.info("--- MISSION: Starting Full Perseus Harvest ---")
    all_source_files = list(PERSEUS_REPO_PATH.rglob("*.perseus-grc*.xml"))
    logger.info(f"Found {len(all_source_files)} total Greek text files to process.")
    for i, xml_path in enumerate(all_source_files):
        logger.info(f"--- Harvesting [{i+1}/{len(all_source_files)}]: {xml_path.name} ---")
        output_filename = f"Perseus_{xml_path.stem}.txt"
        output_path = HARVEST_OUTPUT_FOLDER / output_filename
        if output_path.exists():
            logger.info("Output file already exists. Skipping.")
            continue
        clean_text = parse_perseus_xml(str(xml_path))
        if clean_text:
            output_path.write_text(clean_text, encoding='utf-8')
            logger.info(f"SUCCESS: Saved to {output_path.name}")
        time.sleep(0.5)
    logger.info("--- MISSION: Perseus Harvest Complete ---")

def run_corpus_preprocessing(target_folder_path_str, language):
    target_folder = Path(target_folder_path_str)
    logger.info(f"--- MISSION: Starting Preprocessing of {language} Corpus in {target_folder} ---")
    text_files = list(target_folder.glob("*.txt"))
    for i, text_file in enumerate(text_files):
         logger.info(f"--- Preprocessing [{i+1}/{len(text_files)}]: {text_file.name} ---")
         preprocess_file(str(text_file))
    logger.info(f"--- MISSION: Preprocessing of {language} Corpus Complete ---")

# --- AGENT CORE ---
def process_task(task_string):
    logger.info(f"Received high-level command: '{task_string}'")
    if task_string == "HARVEST_PERSEUS":
        run_perseus_harvest()
    elif task_string == "PREPROCESS_GREEK_CORPUS":
        run_corpus_preprocessing(str(HARVEST_OUTPUT_FOLDER), "greek")
    else:
        logger.warning(f"Unknown command: {task_string}")

def get_next_task():
    if not QUEUE_FILE.exists() or QUEUE_FILE.stat().st_size == 0: return None
    try:
        with open(QUEUE_FILE, 'r+', encoding='utf-8') as f:
            lines = f.readlines(); next_task = lines.pop(0).strip(); f.seek(0); f.truncate(); f.writelines(lines)
        return next_task if next_task else None
    except Exception as e:
        logger.error(f"Error reading queue file: {e}"); time.sleep(10); return None

def main():
    logger.info("🚀 Autonomous Agent Initialized for Weekend Mission...")
    while True:
        try:
            task = get_next_task()
            if task:
                process_task(task)
            else:
                logger.info("All missions complete. Agent is now idle.")
                time.sleep(3600)
        except KeyboardInterrupt:
            logger.info("Shutdown signal received."); break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True); time.sleep(60)

if __name__ == "__main__":
    main()