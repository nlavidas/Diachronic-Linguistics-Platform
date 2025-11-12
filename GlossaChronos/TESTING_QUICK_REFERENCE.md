# 🧪 Testing Quick Reference Card

**PRINT THIS AND KEEP IT HANDY!**

---

## ⚡ Ultra Quick Test (30 seconds)

```powershell
cd Z:\GlossaChronos
.\TEST_ALL_SYSTEMS.ps1
```

**Tests all 10 systems instantly!**

---

## 🎯 Individual System Tests

### **Test Streamlit (EASIEST!)** ⭐
```powershell
.\test_streamlit.ps1
```
Opens browser automatically!

### **Test Django**
```powershell
.\test_django.ps1
```
Creates admin panel at localhost:8000

### **Test ERC**
```powershell
.\test_erc.ps1
```
Checks pipeline and models

---

## 🚀 Manual Quick Tests

### **1. Streamlit (2 commands)**
```powershell
cd streamlit_app
streamlit run app.py
```

### **2. Django (4 commands)**
```powershell
cd django_web_platform\backend
python -m venv venv && .\venv\Scripts\activate
pip install django
python manage.py migrate && python manage.py runserver
```

### **3. Production NLP (2 commands)**
```powershell
cd production_nlp_platform
python dashboard.py
```

### **4. Gutenberg Harvester (1 command)**
```powershell
python gutenberg_bulk_downloader.py
```

### **5. Multi-Agent (2 commands)**
```powershell
cd FileAnalysisAgent
python main.py
```

---

## 📊 Expected Results

| System | Test Time | Expected Output |
|--------|-----------|----------------|
| **Streamlit** | 5 sec | Browser opens |
| **Django** | 1 min | Admin panel |
| **ERC** | 5 min | Pipeline ready |
| **Production NLP** | 10 sec | Dashboard at :5000 |
| **Gutenberg** | 2 min | Downloads 2-3 texts |

---

## ✅ Quick Checklist

**Before testing:**
- [ ] Python 3.8+ installed
- [ ] pip working
- [ ] Z: drive accessible
- [ ] Internet connection (for downloads)

**After testing:**
- [ ] Master test passes (10/10)
- [ ] Streamlit app opens
- [ ] Django admin accessible
- [ ] At least 3 systems tested

---

## 🚨 Quick Fixes

**"Module not found"**
```powershell
pip install [module_name]
```

**"Port already in use"**
```powershell
# Use different port
streamlit run app.py --server.port 8502
# or
python manage.py runserver 8001
```

**"Permission denied"**
```powershell
# Run PowerShell as Administrator
```

---

## 🎓 Recommended Testing Order

1. ✅ **Master Test** (30 sec) - `.\TEST_ALL_SYSTEMS.ps1`
2. ✅ **Streamlit** (2 min) - `.\test_streamlit.ps1`
3. ✅ **Django** (5 min) - `.\test_django.ps1`
4. ✅ **ERC** (10 min) - `.\test_erc.ps1`
5. ✅ **Others** (as needed) - See TESTING_GUIDE.md

---

## 📞 Help Commands

```powershell
# View master summary
notepad MASTER_SUMMARY.md

# View testing guide
notepad TESTING_GUIDE.md

# View system documentation
notepad COMPLETE_PLATFORM_SUMMARY.md

# Quick commands reference
notepad QUICK_COMMANDS.md
```

---

## 🎉 Success Indicators

**✓ Platform is working if:**
- Master test shows 10/10 PASS
- Streamlit opens in browser
- Django admin panel accessible
- Can process sample data
- No critical errors

---

**🧪 START TESTING NOW!**

```powershell
.\TEST_ALL_SYSTEMS.ps1
```

🚀✨
