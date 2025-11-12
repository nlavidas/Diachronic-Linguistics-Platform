# 🚀 Next Steps - VS Code Terminal Commands

## Step 1: Test Enhanced Parser
```powershell
cd Z:\GlossaChronos
.\venv\Scripts\Activate.ps1
python enhanced_universal_parser.py
```

## Step 2: Install Dependencies
```powershell
pip install ollama langdetect
```

## Step 3: Download Stanza Models
```powershell
python -c "import stanza; stanza.download('grc')"
python -c "import stanza; stanza.download('la')"
```

## Step 4: Run Integrated Pipeline
```powershell
python integrated_pipeline.py
```

## Expected Output
- Scans Z: drive
- Parses TEI-XML (all structures)
- AI quality assessment
- Real morphological annotation
- Saves to database

**Reply "next step" for commands**
