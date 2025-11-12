# 🧪 Complete Testing Guide - All 10 Systems

## **Comprehensive Testing Strategy**

**Test everything systematically to ensure all systems work correctly!**

---

## ⚡ Quick Test (1 minute)

```powershell
# Run master test suite
cd Z:\GlossaChronos
.\TEST_ALL_SYSTEMS.ps1
```

**This tests all 10 systems and reports results!**

---

## 📊 Individual System Tests

### **SYSTEM 1: Workflow Optimization**

```powershell
# Test setup scripts exist
ls setup_*.ps1

# Test Git configuration (dry run)
# Don't actually run setup scripts yet - just verify they exist
Get-Content setup_git.ps1 | Select-Object -First 10
```

**Expected:** 3 setup scripts present  
**Status:** ✅ Files exist, ready to run

---

### **SYSTEM 2: Local GPU Setup**

```powershell
# Test 1: Check if local_llm_api.py exists
Test-Path local_llm_api.py

# Test 2: Check Ollama is running (optional)
Test-NetConnection -ComputerName localhost -Port 11434

# Test 3: Quick Python syntax check
python -c "import ast; ast.parse(open('local_llm_api.py').read())"
```

**Expected:** File exists, syntax valid  
**Ollama:** Optional (install from https://ollama.ai)

---

### **SYSTEM 3: Gutenberg Harvester**

```powershell
# Test 1: File exists
Test-Path gutenberg_bulk_downloader.py

# Test 2: Syntax check
python -c "import ast; ast.parse(open('gutenberg_bulk_downloader.py').read())"

# Test 3: Dry run (check imports)
python -c "import sqlite3, requests; print('Dependencies OK')"

# Test 4: ACTUAL RUN (downloads 1-2 texts)
# python gutenberg_bulk_downloader.py
# (Uncomment to test actual download)
```

**Expected:** All dependencies present  
**Time:** <5 seconds for checks

---

### **SYSTEM 4: IE Annotation App**

```powershell
# Test 1: Documentation exists
Test-Path IE_ANNOTATION_APP_GUIDE.md

# Test 2: Check if Node.js installed (required for full test)
node --version
npm --version
```

**Expected:** Documentation present  
**Full test:** Requires Node.js setup

---

### **SYSTEM 5: Streamlit Teaching Tool** ⭐

```powershell
# Test 1: App file exists
Test-Path streamlit_app\app.py

# Test 2: Check Streamlit installed
python -c "import streamlit; print(f'Streamlit {streamlit.__version__}')"

# If not installed:
pip install streamlit pandas plotly

# Test 3: RUN THE APP! (Easiest system to test)
cd streamlit_app
streamlit run app.py
# Opens browser automatically!
```

**Expected:** App launches in browser  
**Time:** 5 seconds  
**✨ THIS IS THE EASIEST AND BEST FIRST TEST!**

---

### **SYSTEM 6: Career Elevation Tools**

```powershell
# Test 1: Check all documentation exists
$files = @(
    "STRATEGIC_CAREER_PLAN.md",
    "grants\CIVIS_1_Pager_Template.md",
    "networking\Cold_Email_Templates.md",
    "ACTION_CHECKLIST_NOV2025.md"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✓ $file" -ForegroundColor Green
    } else {
        Write-Host "✗ $file" -ForegroundColor Red
    }
}

# Test 2: Open strategic plan
notepad STRATEGIC_CAREER_PLAN.md
```

**Expected:** All documentation files present  
**Time:** Instant

---

### **SYSTEM 7: Multi-Agent File Analysis**

```powershell
# Test 1: Check main file
Test-Path FileAnalysisAgent\main.py

# Test 2: Check agents
ls FileAnalysisAgent\agents\*.py

# Test 3: Check config
Test-Path FileAnalysisAgent\config\config.json

# Test 4: Verify Python dependencies
python -c "import nltk, wordcloud; print('Dependencies OK')"

# Test 5: RUN WITH TEST DATA
cd FileAnalysisAgent

# Create test file
"This is a test file for analysis." | Out-File -FilePath "test_input.txt"

# Run (will analyze files in input directory)
# python main.py
```

**Expected:** All agent files present  
**Time:** Depends on number of files

---

### **SYSTEM 8: ERC Valency Project**

```powershell
# Test 1: Check pipeline exists
Test-Path ERC_VALENCY_PROJECT\master_pipeline.py

# Test 2: Check structure
ls ERC_VALENCY_PROJECT

# Test 3: Check if models downloaded
ls ERC_VALENCY_PROJECT\models\*.udpipe

# If no models:
cd ERC_VALENCY_PROJECT
.\scripts\download_models.ps1

# Test 4: Verify Python dependencies
python -c "import ufal.udpipe, pandas; print('Dependencies OK')"

# Test 5: DRY RUN (just imports)
cd ERC_VALENCY_PROJECT
python -c "from master_pipeline import ERCValencyPipeline; print('Pipeline imports OK')"
```

**Expected:** Structure present, ready for corpus  
**Time:** Model download 5-10 minutes (one-time)

---

### **SYSTEM 9: Production NLP Platform**

```powershell
# Test 1: Check processor exists
Test-Path production_nlp_platform\unified_processor.py

# Test 2: Check dashboard exists
Test-Path production_nlp_platform\dashboard.py

# Test 3: Check database setup
Test-Path production_nlp_platform\setup_database.py

# Test 4: Initialize database
cd production_nlp_platform
python setup_database.py

# Test 5: Run dashboard (Flask)
python dashboard.py
# Visit: http://localhost:5000

# Test 6: Run processor (dry run)
python -c "from unified_processor import UltimateLinguisticProcessor; print('Processor imports OK')"
```

**Expected:** Database created, dashboard accessible  
**Time:** <1 minute

---

### **SYSTEM 10: Django Web Platform**

```powershell
# Test 1: Check Django files
Test-Path django_web_platform\backend\config\settings.py

# Test 2: Check models
Test-Path django_web_platform\backend\apps\texts\models.py

# Test 3: Setup virtual environment
cd django_web_platform\backend
python -m venv venv
.\venv\Scripts\activate

# Test 4: Install dependencies
pip install -r requirements.txt

# Test 5: Initialize database
python manage.py makemigrations
python manage.py migrate

# Test 6: Create superuser
python manage.py createsuperuser
# Enter: username, email, password

# Test 7: RUN SERVER!
python manage.py runserver
# Visit: http://localhost:8000/admin/
```

**Expected:** Django admin panel accessible  
**Time:** 5 minutes (first time setup)

---

## 🎯 Recommended Testing Order

### **Phase 1: Quick Validation (5 minutes)**
1. Run `TEST_ALL_SYSTEMS.ps1`
2. Check all systems PASS

### **Phase 2: Interactive Tests (15 minutes)**
1. ✅ **Streamlit** (easiest!) - `cd streamlit_app && streamlit run app.py`
2. ✅ **Production NLP Dashboard** - `python dashboard.py`
3. ✅ **Django Admin** - `python manage.py runserver`

### **Phase 3: Processing Tests (30 minutes)**
1. ✅ **Gutenberg Harvester** - Download 2-3 texts
2. ✅ **Multi-Agent** - Analyze test files
3. ✅ **ERC Pipeline** - Process 1 sample text

### **Phase 4: Full Integration (1 hour)**
1. ✅ Run complete ERC pipeline on small corpus
2. ✅ View results in Django admin
3. ✅ Analyze with Streamlit
4. ✅ Generate reports with Multi-Agent

---

## 🔧 Dependency Installation

### **Core Python Dependencies:**
```powershell
pip install streamlit pandas plotly nltk wordcloud stanza spacy django djangorestframework
```

### **Optional Dependencies:**
```powershell
# For UDPipe
pip install ufal.udpipe

# For NLP processing
pip install transformers torch

# For web dashboards
pip install flask gunicorn
```

---

## 📊 Test Results Template

```
=== TEST RESULTS ===
Date: [Current Date]
Tester: [Your Name]

System 1 (Workflow):        [ ] PASS  [ ] FAIL
System 2 (GPU):             [ ] PASS  [ ] FAIL
System 3 (Gutenberg):       [ ] PASS  [ ] FAIL
System 4 (IE App):          [ ] PASS  [ ] FAIL
System 5 (Streamlit):       [ ] PASS  [ ] FAIL
System 6 (Career):          [ ] PASS  [ ] FAIL
System 7 (Multi-Agent):     [ ] PASS  [ ] FAIL
System 8 (ERC):             [ ] PASS  [ ] FAIL
System 9 (Production NLP):  [ ] PASS  [ ] FAIL
System 10 (Django):         [ ] PASS  [ ] FAIL

Overall: ___/10 PASS
```

---

## 🚨 Troubleshooting

### **"Module not found"**
```powershell
pip install [module_name]
```

### **"Port already in use"**
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process
taskkill /PID [process_id] /F
```

### **"Permission denied"**
```powershell
# Run as administrator
# Right-click PowerShell → Run as Administrator
```

### **"Database locked"**
```powershell
# Only run one instance at a time
# Or delete .db file and recreate
```

---

## ✅ Success Criteria

### **System is PASSING if:**
- ✅ All files present
- ✅ Dependencies installed
- ✅ Can run without errors
- ✅ Produces expected output

### **Platform is READY if:**
- ✅ 10/10 systems PASS
- ✅ At least 3 systems tested interactively
- ✅ Can process sample data
- ✅ Documentation accessible

---

## 🎓 **START TESTING NOW!**

```powershell
# 1. Run master test (1 minute)
.\TEST_ALL_SYSTEMS.ps1

# 2. Test Streamlit (easiest!)
cd streamlit_app
pip install streamlit
streamlit run app.py

# 3. Test Django
cd django_web_platform\backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Everything is ready to test!** 🧪✨

---

## 📚 Additional Test Scripts

Individual test scripts available:
- `test_streamlit.ps1` - Test Streamlit app
- `test_django.ps1` - Test Django platform
- `test_erc.ps1` - Test ERC pipeline
- `test_nlp.ps1` - Test NLP processors

Run any test individually for detailed results!

---

**🧪 TESTING MADE EASY - START NOW!** 🚀
