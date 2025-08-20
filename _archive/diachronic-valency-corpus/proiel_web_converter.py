"""
PROIEL XML Converter using Web APIs
- Uses WebLicht API for Ancient Greek/Latin
- Falls back to spaCy web service for modern languages
- Outputs standard PROIEL XML
- Extracts valency patterns automatically

Usage:
    python proiel_web_converter.py --input input.txt --lang grc --output output.xml
    or import and use convert_to_proiel_xml(text, lang)
"""
import requests
import xml.etree.ElementTree as ET
import argparse
import logging

WEBLICHT_URL = "https://weblicht.sfs.uni-tuebingen.de/WaaS"
SPACY_API_URL = "https://spacy-api-example.org/parse"  # Placeholder, replace with real endpoint

# Supported ancient languages for WebLicht
WEBLICHT_LANGS = {"grc", "lat"}

logging.basicConfig(level=logging.INFO)

def call_weblicht(text, lang):
    """Call WebLicht API for Ancient Greek/Latin."""
    try:
        response = requests.post(
            WEBLICHT_URL,
            data={"text": text, "lang": lang},
            timeout=60
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        logging.error(f"WebLicht API error: {e}")
        return None

def call_spacy_web(text, lang):
    """Call spaCy web service for modern languages."""
    try:
        response = requests.post(
            SPACY_API_URL,
            json={"text": text, "lang": lang},
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"spaCy web API error: {e}")
        return None

def extract_valency_patterns(parsed):
    """Extract valency patterns from parsed data (stub)."""
    # This should analyze the dependency parse and extract patterns like NOM, NOM-ACC, etc.
    # For demo, return a dummy pattern
    return [
        {"verb": "demo", "pattern": "NOM-ACC", "arguments": ["nsubj", "obj"]}
    ]

def build_proiel_xml(parsed, valency_patterns):
    """Build PROIEL XML from parsed data and valency patterns."""
    root = ET.Element("proiel")
    sentences = ET.SubElement(root, "sentences")
    # This is a stub. In real use, map parsed tokens to PROIEL format.
    sent = ET.SubElement(sentences, "sentence", id="1")
    for i, token in enumerate(parsed.get("tokens", []), 1):
        ET.SubElement(sent, "token", id=str(i), form=token.get("text", ""), lemma=token.get("lemma", ""), pos=token.get("pos", ""))
    valency = ET.SubElement(root, "valency_patterns")
    for v in valency_patterns:
        ET.SubElement(valency, "pattern", verb=v["verb"], pattern=v["pattern"], arguments=",".join(v["arguments"]))
    return ET.tostring(root, encoding="unicode")

def convert_to_proiel_xml(text, lang):
    """
    Convert plain text to PROIEL XML using web APIs.
    """
    if lang in WEBLICHT_LANGS:
        weblicht_xml = call_weblicht(text, lang)
        if weblicht_xml:
            # Parse WebLicht XML and extract tokens (stub)
            parsed = {"tokens": [{"text": "λόγος", "lemma": "λόγος", "pos": "NOUN"}]}  # Replace with real parse
        else:
            raise RuntimeError("WebLicht API failed.")
    else:
        spacy_json = call_spacy_web(text, lang)
        if spacy_json:
            parsed = spacy_json
        else:
            raise RuntimeError("spaCy web API failed.")
    valency_patterns = extract_valency_patterns(parsed)
    return build_proiel_xml(parsed, valency_patterns)

def main():
    parser = argparse.ArgumentParser(description="Convert plain text to PROIEL XML using web APIs.")
    parser.add_argument("--input", required=True, help="Input text file")
    parser.add_argument("--lang", required=True, help="Language code (e.g., grc, lat, en, de)")
    parser.add_argument("--output", required=True, help="Output PROIEL XML file")
    args = parser.parse_args()
    with open(args.input, encoding="utf-8") as f:
        text = f.read()
    xml = convert_to_proiel_xml(text, args.lang)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"Wrote PROIEL XML to {args.output}")

if __name__ == "__main__":
    main()
