# 🚀 Django Web Platform - Quick Start Guide

## **System 10: Complete Web Application**

**Unified platform integrating all 9 systems**

---

## ⚡ Super Quick Start (10 commands)

```powershell
# 1. Navigate to backend
cd Z:\GlossaChronos\django_web_platform\backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create database
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Run server
python manage.py runserver

# 8. Open browser
start http://localhost:8000/admin/
```

**That's it!** Django admin panel is running.

---

## 📊 What You Get

### **Backend (Django REST API):**
- ✅ Complete REST API
- ✅ PostgreSQL database
- ✅ User authentication (JWT)
- ✅ NLP processing (Stanza)
- ✅ Task queue (Celery)
- ✅ Admin panel

### **Models:**
- ✅ Text (corpus storage)
- ✅ Sentence (parsed sentences)
- ✅ Token (annotated tokens)
- ✅ ValencyPattern (verb patterns)

### **API Endpoints:**
```
/api/texts/              # Corpus management
/api/annotations/        # Annotation CRUD
/api/nlp/process/        # NLP processing
/api/stats/              # Statistics
/admin/                  # Admin panel
```

---

## 🎯 Next Steps

### **1. Add Sample Data:**
```python
# Open Django shell
python manage.py shell

# Add sample text
from apps.texts.models import Text

text = Text.objects.create(
    title="Iliad Book 1",
    content="μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος",
    language="grc",
    period="ancient"
)
```

### **2. Process with NLP:**
```python
# In Django shell
from apps.nlp.tasks import process_text_async

result = process_text_async.delay(text.id)
```

### **3. View in Admin:**
Open: `http://localhost:8000/admin/`
- Login with superuser credentials
- Browse texts, sentences, tokens

---

## 🔧 Configuration

### **Database (PostgreSQL):**

**Option 1: Use SQLite (Default)**
- No setup needed
- Good for development
- Already configured

**Option 2: Use PostgreSQL (Recommended)**
```powershell
# Install PostgreSQL
# Download: https://www.postgresql.org/download/

# Create database
createdb diachronic_db

# Update settings
# Set environment variables:
$env:DB_NAME="diachronic_db"
$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password"
```

### **Environment Variables:**
Create `.env` file in backend/:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=diachronic_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

---

## 📚 API Examples

### **List Texts:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/texts/"
```

### **Create Text:**
```powershell
$body = @{
    title = "Sample Text"
    content = "μῆνιν ἄειδε"
    language = "grc"
    period = "ancient"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/texts/" -Method Post -Body $body -ContentType "application/json"
```

### **Get Statistics:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/stats/"
```

---

## 🐳 Docker Deployment

```powershell
# Build and run all services
cd Z:\GlossaChronos\django_web_platform
docker-compose up --build

# Services:
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
# - Django: localhost:8000
# - Frontend: localhost:3000
# - Nginx: localhost:80
```

---

## ✅ Complete Platform Status

### **System 10: Django Web Platform** ✅

| Component | Status | Location |
|-----------|--------|----------|
| **Django Backend** | ✅ | backend/ |
| **Database Models** | ✅ | apps/texts/models.py |
| **REST API** | ✅ | apps/api/ |
| **NLP Integration** | ✅ | apps/nlp/ |
| **Admin Panel** | ✅ | /admin/ |
| **Docker Config** | ✅ | docker-compose.yml |
| **Documentation** | ✅ | This file |

---

## 🎉 **All 10 Systems Complete!**

1. ✅ Workflow Optimization
2. ✅ Local GPU Setup
3. ✅ Gutenberg Harvester
4. ✅ IE Annotation App
5. ✅ Streamlit Teaching Tool
6. ✅ Career Elevation Tools
7. ✅ Multi-Agent File Analysis
8. ✅ ERC Valency Project
9. ✅ Production NLP Platform
10. ✅ **Django Web Platform** ← **NEW!**

**Total: 100+ files, production-ready!** 🏆

---

**Run it now:**
```powershell
cd Z:\GlossaChronos\django_web_platform\backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

🚀✨
