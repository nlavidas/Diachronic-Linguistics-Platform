import os

# Portable configuration
CORPUS_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CORPUS_ROOT, "corpus_data")
REPORTS_DIR = os.path.join(CORPUS_ROOT, "reports")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

print(f"Corpus root: {CORPUS_ROOT}")