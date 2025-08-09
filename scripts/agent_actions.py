import logging
from pathlib import Path
from lxml import etree

# Get a logger instance for this module
logger = logging.getLogger(__name__)

def parse_perseus_xml(file_path_str):
    """
    Parses a single Perseus XML file and returns its text content.
    This is the core action for harvesting the Perseus data.

    Args:
        file_path_str (str): The full path to the .xml file as a string.

    Returns:
        str: The extracted plain text of the document, or None if an error occurs.
    """
    file_path = Path(file_path_str)
    logger.info(f"ACTION: Parsing {file_path.name}...")
    try:
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None

        tree = etree.parse(str(file_path))
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        text_nodes = tree.xpath('//tei:text/tei:body//text()', namespaces=ns)
        
        if not text_nodes:
            logger.warning(f"Could not find any text nodes in {file_path.name}")
            return ""
        
        full_text = " ".join(text.strip() for text in text_nodes if text.strip())
        logger.info(f"Successfully extracted {len(full_text)} characters.")
        return full_text

    except Exception as e:
        logger.error(f"An error occurred while parsing {file_path.name}: {e}")
        return None

# We can add more functions here in the future for other actions,
# like preprocessing, quality control, etc.