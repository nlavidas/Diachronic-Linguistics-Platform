import logging
from lxml import etree

logger = logging.getLogger(__name__)

def parse_perseus_xml(file_path):
    """
    Parses a single Perseus XML file and returns its text content.
    """
    logger.info(f"Parsing {file_path.name}...")
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
        logger.error(f"Could not parse {file_path.name}: {e}")
        return None