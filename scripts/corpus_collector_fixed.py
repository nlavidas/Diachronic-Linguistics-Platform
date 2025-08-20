import logging
import sqlite3
from pathlib import Path
import requests
import trafilatura
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project_root = Path(__file__).resolve().parent.parent
DB_PATH = project_root / 'corpus.db'

class DiachronicCorpusCollector:
    def __init__(self):
        self.setup_database()
