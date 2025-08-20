from pathlib import Path
import re

# Read both files
greek_file = Path('corpus_texts/perseus_greek/Argonautica_book1_greek.txt')
english_file = Path('corpus_texts/perseus_translations/english/Argonautica_book1_english.txt')

greek_text = greek_file.read_text(encoding='utf-8')
english_text = english_file.read_text(encoding='utf-8')

# Create metadata summary
summary = {
    'title': 'Argonautica Book 1',
    'author': 'Apollonius Rhodius',
    'period': 'Hellenistic (3rd century BCE)',
    'genre': 'Epic Poetry',
    'subject': 'Jason and the Golden Fleece',
    'greek_length': len(greek_text),
    'english_length': len(english_text),
    'greek_words': len(greek_text.split()),
    'english_words': len(english_text.split())
}

print('=== ARGONAUTICA METADATA SUMMARY ===')
for key, value in summary.items():
    print(f'{key}: {value}')

# Save summary to file
summary_file = Path('corpus_texts/summaries/Argonautica_book1_summary.txt')
summary_file.parent.mkdir(parents=True, exist_ok=True)
with open(summary_file, 'w', encoding='utf-8') as f:
    for key, value in summary.items():
        f.write(f'{key}: {value}\n')

print(f'\nSummary saved to: {summary_file}')
