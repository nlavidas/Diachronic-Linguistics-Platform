from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Paths
gdir = Path('corpus_texts/perseus_greek')
edir = Path('corpus_texts/perseus_translations/english')
gdir.mkdir(parents=True, exist_ok=True)
edir.mkdir(parents=True, exist_ok=True)

# Copy existing Greek file
src_greek = Path('corpus_texts/perseus_greek/Perseus_tlg0001.tlg001.perseus-grc2.txt')
dest_greek = gdir / 'Argonautica_book1_greek.txt'
dest_greek.write_text(src_greek.read_text(encoding='utf-8'), encoding='utf-8')

# Fetch English translation
url = 'http://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0227'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
eng_text = soup.get_text()

dest_english = edir / 'Argonautica_book1_english.txt'
dest_english.write_text(eng_text, encoding='utf-8')

print('Saved Greek to', dest_greek)
print('Saved English to', dest_english)
