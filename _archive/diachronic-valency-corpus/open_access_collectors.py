"""
Open-Access Source Collectors for Diachronic Valency Corpus
- Perseus Digital Library (CTS API)
- First1KGreek (GitHub)
- Project Gutenberg
- PROIEL treebanks (GitHub)
- Internet Archive (API)
- Handles polite rate limiting
"""
import requests
import time
import os
import logging

DATA_DIR = "collected_sources"
os.makedirs(DATA_DIR, exist_ok=True)

RATE_LIMIT_SECONDS = 2  # polite delay between requests

# 1. Perseus Digital Library (CTS API)
def collect_perseus(work_urn, out_path=None):
    base_url = "https://cts.perseids.org/api/cts"
    params = {"request": "GetPassage", "urn": work_urn}
    r = requests.get(base_url, params=params)
    time.sleep(RATE_LIMIT_SECONDS)
    if r.status_code == 200:
        out_path = out_path or os.path.join(DATA_DIR, f"perseus_{work_urn.replace(':','_')}.xml")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        logging.info(f"Downloaded Perseus work {work_urn} to {out_path}")
        return out_path
    else:
        logging.error(f"Failed to download Perseus work {work_urn}")
        return None

# 2. First1KGreek (GitHub)
def collect_first1kgreek(repo_url="https://github.com/OpenGreekAndLatin/First1KGreek", out_dir=None):
    import git
    out_dir = out_dir or os.path.join(DATA_DIR, "First1KGreek")
    if not os.path.exists(out_dir):
        git.Repo.clone_from(repo_url, out_dir)
        logging.info(f"Cloned First1KGreek to {out_dir}")
    else:
        logging.info(f"First1KGreek already exists at {out_dir}")
    return out_dir

# 3. Project Gutenberg
def collect_gutenberg(book_id, out_path=None):
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
    r = requests.get(url)
    time.sleep(RATE_LIMIT_SECONDS)
    if r.status_code == 200:
        out_path = out_path or os.path.join(DATA_DIR, f"gutenberg_{book_id}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        logging.info(f"Downloaded Gutenberg book {book_id} to {out_path}")
        return out_path
    else:
        logging.error(f"Failed to download Gutenberg book {book_id}")
        return None

# 4. PROIEL treebanks (GitHub)
def collect_proiel_treebank(repo_url="https://github.com/proiel/proiel-treebank", out_dir=None):
    import git
    out_dir = out_dir or os.path.join(DATA_DIR, "proiel-treebank")
    if not os.path.exists(out_dir):
        git.Repo.clone_from(repo_url, out_dir)
        logging.info(f"Cloned PROIEL treebank to {out_dir}")
    else:
        logging.info(f"PROIEL treebank already exists at {out_dir}")
    return out_dir

# 5. Internet Archive (API)
def collect_internet_archive(query, max_results=10, out_dir=None):
    base_url = "https://archive.org/advancedsearch.php"
    params = {
        "q": query,
        "fl[]": "identifier,title,creator,year",
        "rows": max_results,
        "output": "json"
    }
    r = requests.get(base_url, params=params)
    time.sleep(RATE_LIMIT_SECONDS)
    out_dir = out_dir or os.path.join(DATA_DIR, "internet_archive")
    os.makedirs(out_dir, exist_ok=True)
    if r.status_code == 200:
        results = r.json()["response"]["docs"]
        for doc in results:
            identifier = doc["identifier"]
            meta_path = os.path.join(out_dir, f"{identifier}.json")
            with open(meta_path, "w", encoding="utf-8") as f:
                f.write(str(doc))
        logging.info(f"Downloaded metadata for {len(results)} Internet Archive items to {out_dir}")
        return out_dir
    else:
        logging.error(f"Failed to query Internet Archive for {query}")
        return None
