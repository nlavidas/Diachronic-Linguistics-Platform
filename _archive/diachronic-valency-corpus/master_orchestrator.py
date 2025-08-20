"""
Master Orchestrator for Diachronic Valency Corpus Agents
------------------------------------------------------
- Manages all agent modules
- Ensures single shared database
- Handles Stanza fallback to web APIs
- Automates GitHub pushes
------------------------------------------------------
"""
import os
import threading
import time
import logging
import psycopg2
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(os.path.abspath("master_orchestrator.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("Master Orchestrator starting up...")

# Get API configuration
from api_config_manager import get_configured_apis
API_KEYS = get_configured_apis()

from ultimate_24_7_agent_with_ai import Ultimate24_7AgentWithAI
from ai_discovery_module import AITextDiscoveryEngine
from ai_preprocessing_24_7_agent import AIPreprocessingAgent
from valency_resources_24_7_agent import ValencyResourcesAgent

# --- Academic and Methodology Integration ---
from super_corpus_methodology import SuperCorpusMethodology
from academic_resource_integration import main as academic_resource_main

# --- Valency Extraction Automation ---
import sys
import importlib
def run_valency_extractor():
    import time
    import glob
    valency_extractor = importlib.import_module('valency_extractor')
    TEXT_DIR = 'data/texts'
    os.makedirs(TEXT_DIR, exist_ok=True)
    while True:
        # Scan for all .txt files in the directory
        for txt_path in glob.glob(os.path.join(TEXT_DIR, '*.txt')):
            json_path = txt_path.rsplit('.', 1)[0] + '.valency.json'
            # Only process if new or updated
            if not os.path.exists(json_path) or os.path.getmtime(txt_path) > os.path.getmtime(json_path):
                try:
                    # TODO: Improve language/year detection from filename or metadata
                    lang = 'grc'  # Default: Ancient Greek
                    year = 200    # Default: 200 CE
                    # Simulate CLI arguments for valency_extractor
                    sys.argv = [
                        'valency_extractor.py',
                        '--input', txt_path,
                        '--lang', lang,
                        '--year', str(year),
                        '--output', json_path
                    ]
                    valency_extractor.__main__()
                    logging.info(f"Valency extraction complete for {txt_path}")
                    # --- Automated downstream processing: import valency JSON into database ---
                    try:
                        import_valency_json_to_db(json_path)
                        logging.info(f"Valency JSON imported to database for {txt_path}")
                    except Exception as e2:
                        logging.error(f"Valency DB import failed for {txt_path}: {e2}")
                except Exception as e:
                    logging.error(f"Valency extractor failed for {txt_path}: {e}")
        time.sleep(10)  # Sleep to avoid busy waiting

def import_valency_json_to_db(json_path):
    """
    Import valency JSON output into the main PostgreSQL database.
    """
    import json
    import re
    conn = get_postgres_conn()
    cur = conn.cursor()
    try:
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
        m = re.search(r'(\d+)', os.path.basename(json_path))
        text_id = int(m.group(1)) if m else None
        for entry in data.get('patterns', []):
            try:
                cur.execute(
                    "INSERT INTO valency_patterns (verb, pattern, arguments, text_id) VALUES (%s, %s, %s, %s)",
                    (entry['verb'], entry['pattern'], ','.join(entry['arguments']), text_id)
                )
            except Exception as e:
                logging.error(f"Valency DB insert error for {json_path}: {e}")
                continue
        conn.commit()
    except Exception as e:
        logging.error(f"Valency DB import failed for {json_path}: {e}")
    finally:
        cur.close()
        conn.close()


DB_PATH = os.path.abspath("corpus_complete.db")
LOG_PATH = os.path.abspath("master_orchestrator.log")

# --- Shared DB connection for legacy agents (sqlite fallback, not used in Docker) ---
def get_shared_db():
    import sqlite3
    return sqlite3.connect(DB_PATH)


# Logging to both file and Unicode-safe console
# Logging to both file and Unicode-safe console

class AsciiOnlyStreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            # Remove non-ASCII characters for Windows console
            record.msg = (record.getMessage().encode('ascii', errors='ignore').decode('ascii'))
            self.stream.write(self.format(record) + self.terminator)
        except Exception:
            self.handleError(record)
import threading as _threading
_db_lock = _threading.Lock()
import os
POSTGRES_DSN = os.getenv("DATABASE_URL", "dbname=corpus user=postgres password=postgres host=localhost port=5432")
def get_postgres_conn():
    with _db_lock:
        return psycopg2.connect(POSTGRES_DSN)


# Importable stanza fallback for agents
def stanza_fallback(text, lang):
    """
    Try stanza, fallback to web API if PermissionError.
    """
    try:
        import stanza
        nlp = stanza.Pipeline(lang=lang)
        return nlp(text)
    except PermissionError:
        logging.warning("Stanza PermissionError, using web API fallback.")
        # Call your web API fallback here
        import requests
        try:
            resp = requests.post('https://api.example.com/parse', json={'text': text, 'lang': lang}, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logging.error(f"Web API fallback failed: {e}")
            return {"error": "Web API fallback failed"}

# --- File content validation: quarantine mismatches ---
def validate_file_content(file_path):
    """
    Validate file content and quarantine if issues found.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if len(content.strip()) == 0:
            logger.warning(f"Empty file detected: {file_path}")
            return False
            
        # Add more validation as needed
        return True
    except Exception as e:
        logger.error(f"File validation failed for {file_path}: {e}")
        return False

import datetime


# --- Agent pausing/resuming for consultation window ---
consultation_active = threading.Event()

def consultation_handler():
    logging.info("Consultation window active: 1 hour real consultation. Pausing all agents.")
    consultation_active.set()  # Signal agents to pause
    # You can add logic here to expose a web endpoint or allow manual review
    time.sleep(3600)  # 1 hour consultation
    consultation_active.clear()  # Resume agents
    logging.info("Consultation window ended. Agents resumed.")


# Helper to start and restart threads, pausing if consultation is active
def start_thread(target, *args, **kwargs):
    def wrapper():
        while True:
            if consultation_active.is_set():
                logging.info(f"{target.__name__} paused for consultation window.")
                time.sleep(10)
                continue
            try:
                target(*args, **kwargs)
            except Exception as e:
                logging.error(f"Thread {target.__name__} crashed: {e}")
                time.sleep(5)
    t = threading.Thread(target=wrapper, daemon=True)
    t.start()
    return t


def run_agent(agent, method=None):
    if method:
        getattr(agent, method)()
    else:
        agent.run() if hasattr(agent, 'run') else agent()

def run_academic_resource_integration():
    try:
        academic_resource_main()
    except Exception as e:
        logging.error(f"Academic resource integration failed: {e}")

def github_push():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-am", "Automated commit"], check=True)
        subprocess.run(["git", "push"], check=True)
        logging.info("GitHub push complete.")
    except subprocess.CalledProcessError as e:
        logging.error(f"GitHub push failed: {e}")

def main(push_interval=3600):
    # Instantiate agents with shared DB or path
    ultimate_agent = Ultimate24_7AgentWithAI()
    ai_discovery = AITextDiscoveryEngine(DB_PATH)
    ai_preproc = AIPreprocessingAgent()
    valency_agent = ValencyResourcesAgent()
    methodology = SuperCorpusMethodology()

    # Start agents in resilient threads
    agent_threads = [
        start_thread(run_agent, ultimate_agent, "run_24_7"),
        start_thread(run_agent, ai_discovery, "discover_continuously"),
        start_thread(run_agent, ai_preproc, "run_24_7"),
        start_thread(run_agent, valency_agent, "run_24_7"),
        start_thread(run_agent, methodology, "generate_super_platform_data"),
        start_thread(run_academic_resource_integration),
        start_thread(run_valency_extractor),
    ]

    # Main orchestrator loop: 24/7, with daily 1-hour consultation window
    import datetime
    try:
        while True:
            now = datetime.datetime.utcnow()
            # Consultation window: every day 12:00–13:00 UTC
            if now.hour == 12:
                logging.info("Starting daily consultation window.")
                consultation_handler()
                # After consultation, continue normal operation
            # GitHub push every push_interval seconds
            github_push()
            time.sleep(push_interval)
    except KeyboardInterrupt:
        logging.info("Master orchestrator shutting down gracefully.")
        # Optionally join threads or cleanup

if __name__ == "__main__":
    main()
