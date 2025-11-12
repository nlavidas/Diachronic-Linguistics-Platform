# 📋 Corpus Validation Framework - Complete Guide

## What Was Added ✅

**File:** `corpus_validator.py`

A comprehensive 5-phase validation system for diachronic corpus projects.

---

## 5-Phase Validation System

### **Phase 1: Text Type Validation** 📋
**Purpose:** Distinguish original texts from monographs

**Checks:**
- ✅ Primary source indicators (TEI elements, textpart structure)
- ✅ Known author names (Homer, Virgil, Caesar, Plato)
- ❌ Monograph patterns (commentary, introduction, notes, bibliography)
- ❌ Modern chapter style
- ❌ Editorial content

**Pass Criteria:** Score ≥ 75%

---

### **Phase 2: Diachronic Assessment** 📅
**Purpose:** Validate period appropriateness and influence

**Checks:**
- ✅ Language identification (grc, lat, en, fro)
- ✅ Period classification:
  - **Ancient Greek:** Archaic, Classical, Hellenistic, Byzantine
  - **Latin:** Classical, Vulgar, Medieval, Renaissance
  - **English:** Old, Middle, Early Modern, Modern
  - **French:** Old, Middle, Classical
- ✅ Influential works identification
- ✅ Representative text assessment

**Pass Criteria:** Score ≥ 75%

---

### **Phase 3: PROIEL Compliance** 🔍
**Purpose:** Validate PROIEL XML format compliance

**Checks:**
- ✅ Valid XML structure
- ✅ PROIEL schema (versions 2.1, 3.0)
- ✅ Sentence elements present
- ✅ Token elements present
- ✅ Proper hierarchy (source → sentence → token)
- ✅ Minimum content (>10 tokens)

**Pass Criteria:** Score ≥ 75%

---

### **Phase 4: Penn-Helsinki Segmentation** ✂️
**Purpose:** Validate sentence segmentation standards

**Checks:**
- ✅ Proper sentence boundaries
- ✅ Reasonable sentence length (5-50 tokens)
- ✅ Segmentation consistency
- ✅ Syntactic criteria adherence

**Pass Criteria:** Score ≥ 75%

---

### **Phase 5: Quality Metrics** 📊
**Purpose:** Overall technical quality

**Checks:**
- ✅ File size (>10KB)
- ✅ UTF-8 encoding
- ✅ Well-formed XML
- ✅ Proper structure

**Pass Criteria:** Score ≥ 75%

---

## VS Code Terminal Commands

### **1. Validate Single File**
```powershell
cd Z:\GlossaChronos
.\venv\Scripts\Activate.ps1
python corpus_validator.py
```

### **2. Validate Directory**
```powershell
# Validate all XML files in harvested_texts/
python -c "from corpus_validator import CorpusValidator; CorpusValidator().validate_directory('Z:/GlossaChronos/harvested_texts')"
```

### **3. Check Validation Results**
```powershell
# Query validation results from database
python -c "import sqlite3; conn = sqlite3.connect('corpus.db'); results = conn.execute('SELECT filename, overall_score, pass_status FROM validation_results ORDER BY overall_score DESC').fetchall(); print('\n'.join([f'{r[0]}: {r[1]:.2%} ({\"PASS\" if r[2] else \"FAIL\"})' for r in results]))"
```

---

## Expected Output

```
================================================================================
VALIDATING: Homer_-_Iliad.xml
================================================================================

📋 Phase 1: Text Type Validation
  Text Type: ✅ PASS (Score: 1.00)
  Primary Source: True
  Monograph: False

📅 Phase 2: Diachronic Assessment
  Diachronic: ✅ PASS (Score: 1.00)
  Language: grc
  Period: Archaic
  Influential: True

🔍 Phase 3: PROIEL Compliance
  PROIEL: ✅ PASS (Score: 1.00)
  Sentences: 15,693
  Tokens: 112,345

✂️  Phase 4: Penn-Helsinki Segmentation
  Segmentation: ✅ PASS (Score: 1.00)
  Avg sentence length: 7.2 tokens

📊 Phase 5: Quality Metrics
  Quality: ✅ PASS (Score: 1.00)
  File size: 1,234,567 bytes
  Encoding: utf-8

================================================================================
VALIDATION SUMMARY
================================================================================
File: Homer_-_Iliad.xml
Overall Score: 100.00%
Status: ✅ PASS

Phase Scores:
  Text Type: 100.00%
  Diachronic: 100.00%
  Proiel: 100.00%
  Penn Helsinki: 100.00%
  Quality: 100.00%
================================================================================
```

---

## Integration with Existing System

The validator integrates with your existing components:

```
Multi-Source Harvester
    ↓
Harvested Texts
    ↓
[CORPUS VALIDATOR] ← NEW!
    ↓
    ├─ PASS → Enhanced Parser → AI Annotation → Database
    └─ FAIL → Rejected Files (with report)
```

---

## Validation Database

Results are saved to `corpus.db`:

```sql
SELECT 
    filename,
    overall_score,
    language,
    period,
    token_count,
    sentence_count,
    pass_status
FROM validation_results
WHERE pass_status = 1
ORDER BY overall_score DESC;
```

---

## What Gets Rejected ❌

### **Rejected as Monographs:**
- Scholarly commentaries
- Modern introductions
- Critical essays
- Bibliographies
- Editorial notes

### **Rejected for Format:**
- Non-XML files
- Malformed XML
- Missing sentence structure
- Empty files (<10KB)

### **Rejected for Period:**
- Cannot determine language
- Anachronistic content
- Non-Indo-European languages
- Modern compositions (unless documented retranslations)

---

## Complete Workflow

```powershell
# 1. Harvest texts
python multi_source_harvester.py

# 2. Validate harvested texts
python corpus_validator.py

# 3. Process validated texts
python integrated_pipeline.py

# 4. Export validated corpus
python multi_format_exporter.py
```

---

## Validation Criteria Summary

| Phase | Minimum Score | Critical Checks |
|-------|---------------|-----------------|
| Text Type | 75% | Is primary source, not monograph |
| Diachronic | 75% | IE language, identifiable period |
| PROIEL | 75% | Valid XML, has tokens |
| Segmentation | 75% | Proper sentence boundaries |
| Quality | 75% | UTF-8, >10KB |

**Overall Pass:** Average ≥ 75% across all phases

---

## Next Steps

### **Immediate:**
```powershell
cd Z:\GlossaChronos
.\venv\Scripts\Activate.ps1

# Harvest texts
python multi_source_harvester.py

# Validate them
python corpus_validator.py
```

### **Review Results:**
Check `validation_results` table in `corpus.db` to see which files passed/failed.

### **Process Valid Files:**
Only process files that passed validation:
```powershell
python integrated_pipeline.py
```

---

**You now have a complete quality control system!** ✅

Reply **"next step"** for the exact commands to test the validation system.
