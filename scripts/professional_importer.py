import logging
from pathlib import Path
from datasets import load_dataset

# --- SETUP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

project_root = Path(__file__).resolve().parent.parent
OUTPUT_DIR = project_root / "corpus_texts" / "universal_dependencies"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- CORE LOGIC ---
def import_ud_corpus(dataset_name, subset_name, output_prefix):
    """
    Downloads a corpus from Hugging Face's datasets and saves it as a text file.
    """
    logger.info(f"Attempting to download '{subset_name}' from the '{dataset_name}' dataset...")
    try:
        dataset = load_dataset(dataset_name, subset_name)
        
        if 'train' not in dataset:
            logger.error("Could not find a 'train' split in the dataset.")
            return

        sentences = [example['text'] for example in dataset['train']]
        logger.info(f"Successfully downloaded {len(sentences)} sentences.")

        output_file = OUTPUT_DIR / f"{output_prefix}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for sentence in sentences:
                f.write(sentence + "\n")
        
        logger.info(f"SUCCESS: Corpus saved to {output_file.name}")

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    logger.info("--- Professional Corpus Importer Initialized ---")
    
    # --- THIS IS THE FIX ---
    # We are now requesting the 'grc_proiel' version which the error told us is available.
    import_ud_corpus("universal_dependencies", "grc_proiel", "ud_proiel_greek")
    
    logger.info("--- Import process complete. ---")