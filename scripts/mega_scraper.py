import logging
from pathlib import Path
import time

# Make sure Python can find our parser script
import sys
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from scripts.perseus_parser import parse_perseus_xml

# --- SETUP ---
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Define the source and destination for our harvest
perseus_repo_path = project_root / "_archive" / "canonical-greekLit" / "data"
output_folder = project_root / "corpus_texts" / "greek_perseus"
output_folder.mkdir(parents=True, exist_ok=True)


# --- MAIN HARVESTER LOGIC ---
def main():
    logger.info("--- PERSEUS HARVESTER INITIALIZED ---")
    logger.info(f"Scanning for Greek XML files in: {perseus_repo_path}")

    # Use .rglob to recursively find all Greek text files
    xml_files = list(perseus_repo_path.rglob("*.perseus-grc*.xml"))
    logger.info(f"Found {len(xml_files)} total Greek text files to process.")

    for i, xml_path in enumerate(xml_files):
        try:
            logger.info(f"--- [{i+1}/{len(xml_files)}] Processing: {xml_path.name} ---")
            
            # Create a clean output filename
            output_filename = f"Perseus_{xml_path.stem}.txt"
            output_path = output_folder / output_filename
            
            # Skip if we've already created this file in a previous run
            if output_path.exists():
                logger.info(f"File already exists. Skipping.")
                continue

            # Call our trusted parser to extract the text
            clean_text = parse_perseus_xml(xml_path)

            if clean_text:
                output_path.write_text(clean_text, encoding='utf-8')
                logger.info(f"SUCCESS: Saved to {output_path.name}")
            
            time.sleep(0.1) # Small pause to prevent overwhelming the system

        except Exception as e:
            logger.error(f"Failed to process {xml_path.name}. Error: {e}")

    logger.info("--- Perseus Harvest Complete! ---")


if __name__ == "__main__":
    main()