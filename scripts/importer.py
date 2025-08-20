import logging
from pathlib import Path
import sys
from nltk.corpus.reader import BracketParseCorpusReader

# --- SETUP ---
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from scripts.agent_actions import import_psd_file

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    ppchig_path = project_root / "_archive" / "PPCHiG"
    
    if not ppchig_path.exists():
        logger.error(f"Corpus directory not found: {ppchig_path}")
    else:
        logger.info(f"Scanning for PPCHiG corpus files in: {ppchig_path}")
        corpus_reader = BracketParseCorpusReader(str(ppchig_path), r'.*\.psd')
        file_ids = corpus_reader.fileids()
        
        logger.info(f"Found {len(file_ids)} corpus files to import.")
        
        for file_id in file_ids:
            full_path = ppchig_path / file_id
            import_psd_file(str(full_path), corpus_reader)
            
        logger.info("--- Professional Corpus Import Complete ---")