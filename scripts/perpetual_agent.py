import logging
from pathlib import Path
import time
import sys

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from scripts.agent_actions import parse_perseus_xml

# --- SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(project_root / "agent_log.txt", mode='a', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

QUEUE_FILE = project_root / "task_queue.txt"
PERSEUS_REPO_PATH = project_root / "_archive" / "canonical-greekLit" / "data"
OUTPUT_FOLDER = project_root / "corpus_texts" / "perseus_harvest"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# --- AGENT CORE LOGIC ---

def discover_new_tasks():
    """
    Scans the Perseus repository and adds unprocessed files to the queue.
    """
    logger.info("--- Starting Discovery Phase ---")
    
    # Get all potential source files
    all_source_files = set(PERSEUS_REPO_PATH.rglob("*.perseus-grc*.xml"))
    
    # Get all already-processed files
    processed_files_stems = {f.stem.replace('Perseus_', '') for f in OUTPUT_FOLDER.glob("*.txt")}
    
    tasks_to_add = []
    for source_file in all_source_files:
        if source_file.stem not in processed_files_stems:
            tasks_to_add.append(str(source_file))
            
    if tasks_to_add:
        logger.info(f"Discovered {len(tasks_to_add)} new tasks. Adding to queue.")
        with open(QUEUE_FILE, 'a', encoding='utf-8') as f:
            for task in tasks_to_add:
                f.write(task + '\n')
    else:
        logger.info("No new tasks discovered.")
    
    return len(tasks_to_add)

def process_task(task):
    logger.info(f"Starting task: PARSE {task}")
    clean_text = parse_perseus_xml(task)
    if clean_text:
        input_path = Path(task)
        output_filename = f"Perseus_{input_path.stem}.txt"
        output_path = OUTPUT_FOLDER / output_filename
        output_path.write_text(clean_text, encoding='utf-8')
        logger.info(f"SUCCESS: Saved parsed text to {output_path.name}")
    else:
        logger.error(f"FAILED to process task: {task}")

def get_next_task():
    if not QUEUE_FILE.exists() or QUEUE_FILE.stat().st_size == 0:
        return None
    with open(QUEUE_FILE, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        next_task = lines.pop(0).strip()
        f.seek(0)
        f.truncate()
        f.writelines(lines)
    return next_task if next_task else None

# --- MAIN 24/7 LOOP ---
def main():
    logger.info("🚀 Perpetual Agent v2.0 (Autonomous Harvester) Initialized...")
    
    while True:
        try:
            task = get_next_task()
            
            if task:
                process_task(task)
                time.sleep(1) # Brief pause between tasks
            else:
                logger.info("Queue is empty. Running discovery scan...")
                new_tasks_found = discover_new_tasks()
                if new_tasks_found == 0:
                    logger.info("No new tasks found. Agent will sleep for 1 hour.")
                    time.sleep(3600) # Sleep for an hour if no work is found

        except KeyboardInterrupt:
            logger.info("Shutdown signal received. Exiting gracefully.")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred in the main loop: {e}", exc_info=True)
            logger.error("Agent will rest for 5 minutes before resuming.")
            time.sleep(300)

if __name__ == "__main__":
    main()