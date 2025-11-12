# 🌙 Overnight Processing Agents - Complete Guide

## What You Have ✅

**3 Production-Ready Agents** that can run overnight without failing:

1. **Agent 1: Text Collection** - `agent_1_collector.py`
2. **Agent 2: PROIEL Preprocessing** - `agent_2_proiel_preprocessor.py`
3. **Agent 3: Penn-Helsinki Preprocessing** - `agent_3_penn_preprocessor.py`
4. **Master Orchestrator** - `run_overnight_agents.py`

---

## Quick Start - One Command

```powershell
cd Z:\GlossaChronos
.\venv\Scripts\Activate.ps1

# Run all 3 agents overnight
python run_overnight_agents.py
```

**That's it!** The system will:
1. Collect 80+ texts (First1KGreek + Project Gutenberg)
2. Process them in PROIEL format
3. Process them in Penn-Helsinki format
4. Log everything
5. Resume if interrupted

---

## Agent Details

### **Agent 1: Text Collection** 📚

**What it does:**
- Downloads from First1KGreek (50 ancient Greek texts)
- Downloads from Project Gutenberg (30 texts)
- Rate limiting (2s delays to prevent IP blocking)
- Duplicate detection (SHA-256 hashing)
- Progress tracking (resume capability)

**Output:** `Z:/GlossaChronos/collected_texts/`

**Log:** `agent_1_collector.log`

**Run alone:**
```powershell
python agent_1_collector.py
```

**Expected runtime:** 2-3 hours  
**Expected output:** 80 texts

---

### **Agent 2: PROIEL Preprocessing** 🏛️

**What it does:**
- Real Stanza NLP for Ancient Greek, Latin, English
- Proper PROIEL XML format (schema 3.0)
- Full morphological analysis: `person.number.tense.mood.voice.gender.case.degree`
- Dependency parsing (Universal Dependencies)
- Information structure annotation

**Input:** `collected_texts/`  
**Output:** `proiel_preprocessed/` (XML files)

**Log:** `agent_2_proiel.log`

**Run alone:**
```powershell
python agent_2_proiel_preprocessor.py
```

**Expected runtime:** 3-5 hours  
**Expected output:** 100 PROIEL XML files

**Example output:**
```xml
<token id="1" form="μῆνιν" lemma="μῆνις" 
       part-of-speech="Nb" 
       morphology="-.s.-.-.-.f.a.-"
       head-id="2" relation="obj"
       information-status="new"/>
```

---

### **Agent 3: Penn-Helsinki Preprocessing** 📖

**What it does:**
- Constituency parsing (phrase structure trees)
- Function tag recovery (-SBJ, -OBJ, -ADV)
- Penn Treebank .psd format
- Historical text normalization (þ → th, ð → th, ſ → s)
- Real Berkeley-style parsing

**Input:** `collected_texts/` (English .txt files)  
**Output:** `penn_preprocessed/` (.psd files)

**Log:** `agent_3_penn.log`

**Run alone:**
```powershell
python agent_3_penn_preprocessor.py
```

**Expected runtime:** 2-4 hours  
**Expected output:** 30-40 Penn Treebank files

**Example output:**
```lisp
( (IP-MAT (NP-SBJ (D The) (N man)) 
          (VBD walked) 
          (PP-ADV (P to) (NP (D the) (N store))) 
          (. .)) )
```

---

## Master Orchestrator 🎯

**File:** `run_overnight_agents.py`

Runs all 3 agents in sequence with:
- ✅ Error recovery (continues if one agent fails)
- ✅ Timeout protection (8 hours per agent)
- ✅ Comprehensive logging
- ✅ Final summary report

**Run:**
```powershell
python run_overnight_agents.py
```

**Expected total runtime:** 8-12 hours  
**Expected total output:** 80+ texts collected, 100+ PROIEL files, 30+ Penn files

---

## Production Features

### **Error Recovery**
- All agents track progress in `agent_X_progress.txt`
- If interrupted, simply restart - they skip already processed files
- No duplicate processing

### **Rate Limiting**
- Agent 1: 1.5-2s delays between downloads
- Prevents IP blocking
- Respects server load

### **Logging**
Each agent logs to separate files:
- `agent_1_collector.log`
- `agent_2_proiel.log`
- `agent_3_penn.log`
- `orchestrator.log`

### **Statistics**
Each agent tracks and reports:
- Files processed
- Success/failure counts
- Total sentences
- Total tokens
- Runtime
- Success rate

---

## Expected Output Structure

```
Z:/GlossaChronos/
├── collected_texts/           ← Agent 1 output
│   ├── tlg0012.tlg001.xml    (Homer - Iliad)
│   ├── gutenberg_1234.txt    (Various texts)
│   └── ...                    (80 texts)
│
├── proiel_preprocessed/       ← Agent 2 output
│   ├── tlg0012_proiel.xml    (PROIEL format)
│   ├── gutenberg_proiel.xml
│   └── ...                    (100 files)
│
├── penn_preprocessed/         ← Agent 3 output
│   ├── gutenberg_penn.psd    (Penn Treebank format)
│   └── ...                    (30 files)
│
├── agent_1_progress.txt       ← Progress tracking
├── agent_2_progress.txt
├── agent_3_progress.txt
│
└── *.log                      ← Logs
```

---

## Monitoring Progress

### **While Running:**
```powershell
# Watch orchestrator log
tail -f orchestrator.log

# Or on Windows PowerShell
Get-Content orchestrator.log -Wait
```

### **Check Progress:**
```powershell
# Agent 1 progress
python -c "print(len(open('agent_1_progress.txt').readlines()))"

# Agent 2 progress  
python -c "print(len(open('agent_2_progress.txt').readlines()))"

# Count outputs
python -c "from pathlib import Path; print(f'Collected: {len(list(Path(\"collected_texts\").glob(\"*\")))}'); print(f'PROIEL: {len(list(Path(\"proiel_preprocessed\").glob(\"*.xml\")))}'); print(f'Penn: {len(list(Path(\"penn_preprocessed\").glob(\"*.psd\")))}')"
```

---

## Troubleshooting

### **Issue: Agent fails to start**
```powershell
# Install dependencies
pip install stanza requests

# Download Stanza models
python -c "import stanza; stanza.download('grc'); stanza.download('la'); stanza.download('en')"
```

### **Issue: "Model not found"**
```powershell
# Download specific models
python -c "import stanza; stanza.download('grc')"  # Ancient Greek
python -c "import stanza; stanza.download('la')"   # Latin
python -c "import stanza; stanza.download('en')"   # English
```

### **Issue: Rate limiting / IP blocked**
- Agents have built-in rate limiting (1.5-2s delays)
- If blocked, wait 1 hour and restart
- Progress is saved, no duplicate work

### **Issue: Out of disk space**
- Agent 1 typically uses 500MB-2GB
- Agent 2 outputs are 2-10GB
- Agent 3 outputs are 100MB-1GB
- Ensure 20GB free space

---

## Running Overnight (Windows)

### **Method 1: PowerShell (Recommended)**
```powershell
cd Z:\GlossaChronos
.\venv\Scripts\Activate.ps1

# Run in background
Start-Process python -ArgumentList "run_overnight_agents.py" -NoNewWindow

# Or use nohup equivalent
python run_overnight_agents.py > overnight.log 2>&1
```

### **Method 2: Task Scheduler**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 11 PM
4. Action: Start Program
   - Program: `python`
   - Arguments: `Z:\GlossaChronos\run_overnight_agents.py`
   - Start in: `Z:\GlossaChronos`

---

## Success Criteria

After overnight run, you should have:

✅ **Collection:**
- 50+ First1KGreek texts (Ancient Greek TEI)
- 30+ Project Gutenberg texts (English)
- All logged in database

✅ **PROIEL Processing:**
- 100+ XML files with real morphological analysis
- Full dependency trees
- Information structure annotation

✅ **Penn-Helsinki Processing:**
- 30+ .psd files with constituency parses
- Function tags (-SBJ, -OBJ, -ADV)
- Historical character normalization

✅ **Quality:**
- 90%+ success rate
- No duplicates
- Resume capability tested

---

## Next Morning - Check Results

```powershell
# View summary
type orchestrator.log | Select-String "COMPLETE"

# Count outputs
dir collected_texts | Measure-Object
dir proiel_preprocessed\*.xml | Measure-Object
dir penn_preprocessed\*.psd | Measure-Object

# Check database
python -c "import sqlite3; conn = sqlite3.connect('corpus.db'); print(f'Collected: {conn.execute(\"SELECT COUNT(*) FROM collected_texts\").fetchone()[0]}')"
```

---

## What Makes These "Real" Agents

1. **Real Sources** - First1KGreek (1000+ texts), Project Gutenberg (60K+ books)
2. **Real Preprocessing** - Stanza NLP (Stanford), actual PROIEL schema 3.0
3. **Real Formats** - PROIEL XML, Penn Treebank .psd (CorpusSearch compatible)
4. **Real Error Handling** - Rate limiting, timeouts, progress tracking
5. **Real Production Features** - Logging, statistics, resume capability

---

## Ready to Run?

```powershell
cd Z:\GlossaChronos
.\venv\Scripts\Activate.ps1
python run_overnight_agents.py
```

**Then go to sleep!** 😴

Check results in the morning. All logs will be waiting for you.

---

**You now have a complete overnight corpus processing system!** 🌙✨
