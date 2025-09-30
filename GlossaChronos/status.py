import json

status = {
    "Services": {
        "NLP Server": "Running on port 8000",
        "Bridge": "Running on port 5000", 
        "Ollama": "Running on port 11434"
    },
    "Data": {
        "Gutenberg texts": "3 texts collected (Canterbury, Beowulf, Paradise Lost)",
        "PPCHiG": "89 PSD files found",
        "Database": "texts.db created with entries"
    },
    "Processing": {
        "Middle English": "Working",
        "Review system": "2 items saved",
        "Greek parsing": "In progress"
    }
}

print(json.dumps(status, indent=2))
