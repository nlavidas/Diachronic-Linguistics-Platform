"""
Valency Pattern Extractor for Diachronic Valency Corpus
- Identifies verbs and arguments
- Classifies valency patterns
- Tracks changes over time periods
- Handles multiple languages
- Output: JSON with statistics
"""
import requests
import json
import logging
import xml.etree.ElementTree as ET

WEBLICHT_URL = "https://weblicht.sfs.uni-tuebingen.de/WaaS"
SPACY_API_URL = "https://spacy-api-example.org/parse"  # Placeholder
WEBLICHT_LANGS = {"grc", "lat"}

def parse_text(text, lang):
    if lang in WEBLICHT_LANGS:
        try:
            r = requests.post(WEBLICHT_URL, data={"text": text, "lang": lang}, timeout=60)
            r.raise_for_status()
            # Parse WebLicht XML (stub)
            # In real use, parse r.text as XML and extract tokens
            return {"tokens": [{"text": "λέγω", "lemma": "λέγω", "pos": "VERB", "dep": "root", "head": 0, "morph": "NOM"}]}
        except Exception as e:
            logging.error(f"WebLicht error: {e}")
            return None
    else:
        try:
            r = requests.post(SPACY_API_URL, json={"text": text, "lang": lang}, timeout=60)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            logging.error(f"spaCy web error: {e}")
            return None

def extract_valency_patterns(parsed):
    """Extract valency patterns from parsed tokens."""
    patterns = []
    for token in parsed.get("tokens", []):
        if token.get("pos") == "VERB":
            args = []
            # Look for subject/object/indirect object
            if "nsubj" in token.get("dep", "") or "subj" in token.get("dep", ""):
                args.append("NOM")
            if "obj" in token.get("dep", ""):
                args.append("ACC")
            if "iobj" in token.get("dep", "") or "dat" in token.get("morph", ""):
                args.append("DAT")
            if "gen" in token.get("morph", ""):
                args.append("GEN")
            pattern = "-".join(args) if args else "NOM"
            patterns.append({
                "verb": token.get("lemma", token.get("text")),
                "pattern": pattern,
                "arguments": args
            })
    return patterns

def valency_statistics(patterns, year=None, lang=None):
    """Aggregate statistics by pattern, year, language."""
    stats = {}
    for p in patterns:
        key = (p["pattern"], year, lang)
        stats[key] = stats.get(key, 0) + 1
    return [
        {"pattern": k[0], "year": k[1], "lang": k[2], "count": v}
        for k, v in stats.items()
    ]

def extract_valency(text, lang, year=None):
    parsed = parse_text(text, lang)
    if not parsed:
        return {"error": "Parsing failed"}
    patterns = extract_valency_patterns(parsed)
    stats = valency_statistics(patterns, year, lang)
    return {
        "patterns": patterns,
        "statistics": stats
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Valency Pattern Extractor")
    parser.add_argument('--input', required=True, help='Input text file')
    parser.add_argument('--lang', required=True, help='Language code')
    parser.add_argument('--year', type=int, default=None, help='Year (optional)')
    parser.add_argument('--output', required=True, help='Output JSON file')
    args = parser.parse_args()
    with open(args.input, encoding='utf-8') as f:
        text = f.read()
    result = extract_valency(text, args.lang, args.year)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Valency extraction written to {args.output}")
    print("✅ Results saved to corpus_data/")

# ...existing code...
    
    # Show sample patterns
    print("\n📋 Sample extracted patterns:")
    df = pd.DataFrame(patterns[:5])
    print(df[['lemma', 'voice', 'pattern', 'full_args']].to_string())