# 🚀 ERC Valency Project - Quick Start Guide

## Goal: Complete 80% of Project in 48-72 Hours

**Current Status:** 20% complete (749 texts, 5,523 verbs)  
**Target:** 100% complete with full automation

---

## ⚡ Super Quick Start (15 minutes)

```powershell
# 1. Navigate to project
cd Z:\GlossaChronos\ERC_VALENCY_PROJECT

# 2. Install dependencies
pip install ufal.udpipe pandas nltk

# 3. Download UDPipe models (run download_models.ps1)
.\scripts\download_models.ps1

# 4. Run master pipeline
python master_pipeline.py
```

**Done!** Pipeline runs for 48-72 hours automatically.

---

## 📊 What Happens

### **Hour 0-4: Annotation**
- Parallel UDPipe annotation (4 processes)
- 749 texts → CoNLL-U format
- Output: `outputs/*.conllu`

### **Hour 4-24: Valency Extraction**
- Extract verb valency frames
- Classify arguments
- Output: `outputs/valency_frames.csv`

### **Hour 24-40: Diachronic Analysis**
- R statistical analysis
- Temporal pattern detection
- Output: `outputs/diachronic_plot.png`

### **Hour 40-52: Visualization**
- RawGraphs interactive charts
- Summary statistics
- Output: `outputs/valency_summary.csv`

### **Hour 52-64: Quality Control**
- 10% sampling for review
- Error detection
- Output: `outputs/quality_control_sample.txt`

### **Hour 64-72: Finalization**
- Generate metadata
- DVC version control
- Output: `outputs/metadata.json`

---

## 📁 Directory Structure

```
Z:\GlossaChronos\ERC_VALENCY_PROJECT\
├── data/
│   └── corpus/               ← PUT YOUR 749 TEXTS HERE
│       ├── greek_text1.txt
│       ├── latin_text2.txt
│       └── ...
├── models/
│   ├── grc.udpipe           ← Auto-downloaded
│   ├── lat.udpipe
│   └── ...
├── outputs/
│   ├── *.conllu             ← Annotated texts
│   ├── valency_frames.csv   ← Main output
│   └── ...
├── scripts/
│   └── diachronic_analysis.R
├── master_pipeline.py        ← RUN THIS
└── QUICK_START.md           ← You are here
```

---

## 🔧 Installation Details

### **Required (Core):**
```powershell
pip install ufal.udpipe pandas nltk
```

### **Optional (Advanced):**
```powershell
# R for diachronic analysis
# Download from: https://cran.r-project.org/

# DVC for version control
pip install dvc

# Doccano for quality control
pip install doccano
```

---

## 🎯 Quick Checks

### **1. Check if models downloaded:**
```powershell
ls models\*.udpipe
```

Should see 5 files (grc, lat, eng, fra, deu)

### **2. Check if texts ready:**
```powershell
ls data\corpus\*.txt
```

Should see 749 files

### **3. Start pipeline:**
```powershell
python master_pipeline.py
```

### **4. Monitor progress:**
```powershell
Get-Content logs\pipeline.log -Tail 20 -Wait
```

---

## 📊 Expected Outputs

After 48-72 hours:

| File | Description | Count |
|------|-------------|-------|
| `*.conllu` | Annotated texts | 749 |
| `valency_frames.csv` | Verb valency data | ~15,000 rows |
| `valency_summary.csv` | Summary statistics | Summary |
| `diachronic_plot.png` | Time-series visualization | 1 |
| `metadata.json` | Project metadata | 1 |

---

## 🚨 Troubleshooting

### **"No texts found"**
- Add .txt files to `data/corpus/`
- Organize by language (greek_*, latin_*, etc.)

### **"No model for language"**
- Run `scripts/download_models.ps1`
- Or download manually from LINDAT

### **"R script not found"**
- R analysis is optional
- Pipeline continues without it

### **Pipeline stuck?**
- Check `logs/pipeline.log` for errors
- Ctrl+C to stop
- Fix issues and re-run

---

## 💡 Pro Tips

1. **Test first:** Run on 10 files before full corpus
2. **Monitor:** Use `Get-Content logs/pipeline.log -Tail 20 -Wait`
3. **Parallel:** Adjust processes in master_pipeline.py (default: 4)
4. **Backup:** Z: drive is backed up, right?
5. **Quality:** Check `quality_control_sample.txt` for review

---

## 📚 Next Steps After Completion

1. Review quality control sample
2. Generate visualizations with RawGraphs
3. Run R analysis for papers
4. Export to PROIEL format if needed
5. Write up results!

---

**Complete 80% of ERC project in 48-72 hours!** 🎓✨

**Questions? Check:**
- `OPTIMIZATION_MATRIX.md` - Detailed tool comparison
- `master_pipeline.py` - Source code
- `logs/pipeline.log` - Execution log
