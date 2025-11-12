# 🌐 Complete Web Platform Implementation Plan

## **System 10: Django + React Web Application**

**Integrates all 9 previous systems into one unified web platform**

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              REACT FRONTEND (Port 3000)                 │
│  - Interactive corpus browser                           │
│  - Annotation editor                                    │
│  - Visualization dashboards                             │
│  - User authentication                                  │
└────────────────────┬────────────────────────────────────┘
                     │ REST API
                     ▼
┌─────────────────────────────────────────────────────────┐
│           DJANGO BACKEND (Port 8000)                    │
│  - Django REST Framework                                │
│  - User management                                      │
│  - API endpoints                                        │
│  - Celery task queue                                    │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│PostgreSQL│  │  Redis   │  │  Stanza  │
│ Database │  │  Cache   │  │   NLP    │
└──────────┘  └──────────┘  └──────────┘
```

---

## 📊 Complete Feature Set

### **Frontend (React):**
1. **Corpus Browser** - Browse and search texts
2. **Annotation Editor** - Edit morphology, syntax, valency
3. **Visualization Dashboard** - Charts, trees, statistics
4. **User Management** - Login, permissions, profiles
5. **Export Tools** - Download in multiple formats

### **Backend (Django):**
1. **REST API** - All data access via API
2. **NLP Pipeline** - Integrated Stanza/spaCy
3. **Task Queue** - Celery for long-running tasks
4. **Database** - PostgreSQL with full-text search
5. **Authentication** - JWT tokens

### **Integration Points:**
- ✅ System 1: Git auto-sync
- ✅ System 2: Local LLM API
- ✅ System 3: Gutenberg harvester
- ✅ System 4: IE annotation logic
- ✅ System 5: Streamlit as alternative UI
- ✅ System 7: Multi-agent processing
- ✅ System 8: ERC valency project
- ✅ System 9: Production NLP pipeline

---

## 🚀 Quick Start (30 minutes)

### **Prerequisites:**
```powershell
# Install Python 3.11+
python --version

# Install Node.js 18+
node --version

# Install PostgreSQL 15+
# Download from: https://www.postgresql.org/download/

# Install Docker (optional but recommended)
# Download from: https://www.docker.com/products/docker-desktop
```

### **Backend Setup:**
```powershell
cd Z:\GlossaChronos\django_web_platform\backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### **Frontend Setup:**
```powershell
cd Z:\GlossaChronos\django_web_platform\frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Access:**
- Backend API: `http://localhost:8000/api/`
- Frontend UI: `http://localhost:3000`
- Admin Panel: `http://localhost:8000/admin/`

---

## 📁 Project Structure

```
django_web_platform/
│
├── backend/                      # Django backend
│   ├── manage.py
│   ├── config/                   # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── texts/                # Text models
│   │   ├── annotations/          # Annotation models
│   │   ├── nlp/                  # NLP processing
│   │   ├── users/                # User management
│   │   └── api/                  # REST API
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                     # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CorpusBrowser/
│   │   │   ├── AnnotationEditor/
│   │   │   ├── Dashboard/
│   │   │   └── Auth/
│   │   ├── services/             # API calls
│   │   ├── store/                # Redux state
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml            # Full stack deployment
├── nginx.conf                    # Reverse proxy
└── IMPLEMENTATION_PLAN.md        # This file
```

---

## 💾 Database Schema

### **Core Models:**

```python
# texts/models.py
class Text(models.Model):
    """Stored text"""
    title = models.CharField(max_length=500)
    content = models.TextField()
    language = models.CharField(max_length=10)
    period = models.CharField(max_length=50)
    source_url = models.URLField(blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Sentence(models.Model):
    """Sentence within text"""
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    position = models.IntegerField()
    content = models.TextField()
    
class Token(models.Model):
    """Annotated token"""
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    position = models.IntegerField()
    form = models.CharField(max_length=200)
    lemma = models.CharField(max_length=200)
    pos = models.CharField(max_length=50)
    morphology = models.CharField(max_length=200)
    head = models.IntegerField()
    deprel = models.CharField(max_length=50)
    
class ValencyPattern(models.Model):
    """Verb valency pattern"""
    verb_lemma = models.CharField(max_length=200)
    language = models.CharField(max_length=10)
    pattern = models.JSONField()
    frequency = models.IntegerField(default=1)
    examples = models.TextField(blank=True)
```

---

## 🔌 API Endpoints

### **Authentication:**
```
POST   /api/auth/register/        # Register new user
POST   /api/auth/login/           # Login (get JWT token)
POST   /api/auth/logout/          # Logout
GET    /api/auth/user/            # Get current user
```

### **Texts:**
```
GET    /api/texts/                # List all texts
POST   /api/texts/                # Create new text
GET    /api/texts/{id}/           # Get specific text
PUT    /api/texts/{id}/           # Update text
DELETE /api/texts/{id}/           # Delete text
GET    /api/texts/{id}/sentences/ # Get sentences
POST   /api/texts/{id}/process/   # Trigger NLP processing
```

### **Annotations:**
```
GET    /api/annotations/          # List annotations
POST   /api/annotations/          # Create annotation
PUT    /api/annotations/{id}/     # Update annotation
DELETE /api/annotations/{id}/     # Delete annotation
GET    /api/annotations/export/   # Export (CONLL-U, TEI)
```

### **NLP Processing:**
```
POST   /api/nlp/tokenize/         # Tokenize text
POST   /api/nlp/parse/             # Parse with Stanza
POST   /api/nlp/valency/           # Extract valency
GET    /api/nlp/status/{task_id}/  # Check processing status
```

### **Statistics:**
```
GET    /api/stats/                # Overall statistics
GET    /api/stats/language/       # By language
GET    /api/stats/valency/        # Valency patterns
```

---

## 🎨 Frontend Components

### **1. Corpus Browser**
```jsx
// components/CorpusBrowser/CorpusBrowser.jsx
import React, { useState, useEffect } from 'react';
import { getTexts } from '../../services/api';

function CorpusBrowser() {
    const [texts, setTexts] = useState([]);
    const [filters, setFilters] = useState({
        language: '',
        period: ''
    });
    
    useEffect(() => {
        loadTexts();
    }, [filters]);
    
    const loadTexts = async () => {
        const data = await getTexts(filters);
        setTexts(data);
    };
    
    return (
        <div className="corpus-browser">
            <h1>Corpus Browser</h1>
            <Filters onChange={setFilters} />
            <TextList texts={texts} />
        </div>
    );
}
```

### **2. Annotation Editor**
```jsx
// components/AnnotationEditor/AnnotationEditor.jsx
import React, { useState } from 'react';
import { updateAnnotation } from '../../services/api';

function AnnotationEditor({ token, onUpdate }) {
    const [editing, setEditing] = useState(false);
    const [form, setForm] = useState(token);
    
    const handleSave = async () => {
        await updateAnnotation(token.id, form);
        onUpdate(form);
        setEditing(false);
    };
    
    return (
        <div className="annotation-editor">
            {editing ? (
                <EditForm 
                    data={form}
                    onChange={setForm}
                    onSave={handleSave}
                    onCancel={() => setEditing(false)}
                />
            ) : (
                <TokenView 
                    token={token}
                    onEdit={() => setEditing(true)}
                />
            )}
        </div>
    );
}
```

### **3. Visualization Dashboard**
```jsx
// components/Dashboard/Dashboard.jsx
import React from 'react';
import { Chart } from 'react-chartjs-2';
import { DependencyTree } from './DependencyTree';

function Dashboard({ stats }) {
    return (
        <div className="dashboard">
            <h1>Statistics Dashboard</h1>
            
            <div className="stats-grid">
                <StatCard title="Texts" value={stats.texts} />
                <StatCard title="Tokens" value={stats.tokens} />
                <StatCard title="Languages" value={stats.languages} />
            </div>
            
            <Chart data={stats.languageDistribution} />
            <DependencyTree sentence={stats.exampleSentence} />
        </div>
    );
}
```

---

## 🔧 NLP Integration

### **Stanza Pipeline:**
```python
# apps/nlp/processors.py
import stanza

class StanzaProcessor:
    def __init__(self):
        self.pipelines = {}
        
    def get_pipeline(self, language):
        if language not in self.pipelines:
            stanza.download(language)
            self.pipelines[language] = stanza.Pipeline(language)
        return self.pipelines[language]
    
    def process_text(self, text, language='grc'):
        nlp = self.get_pipeline(language)
        doc = nlp(text)
        
        result = {
            'sentences': []
        }
        
        for sent in doc.sentences:
            sentence_data = {
                'text': sent.text,
                'tokens': []
            }
            
            for word in sent.words:
                sentence_data['tokens'].append({
                    'id': word.id,
                    'form': word.text,
                    'lemma': word.lemma,
                    'pos': word.upos,
                    'head': word.head,
                    'deprel': word.deprel
                })
            
            result['sentences'].append(sentence_data)
        
        return result
```

### **Celery Tasks:**
```python
# apps/nlp/tasks.py
from celery import shared_task
from .processors import StanzaProcessor

@shared_task
def process_text_async(text_id):
    """Process text with Stanza (async)"""
    from apps.texts.models import Text
    
    text = Text.objects.get(id=text_id)
    processor = StanzaProcessor()
    
    result = processor.process_text(text.content, text.language)
    
    # Save results to database
    for sent_data in result['sentences']:
        sentence = Sentence.objects.create(
            text=text,
            content=sent_data['text']
        )
        
        for token_data in sent_data['tokens']:
            Token.objects.create(
                sentence=sentence,
                **token_data
            )
    
    return {'status': 'completed', 'sentences': len(result['sentences'])}
```

---

## 🐳 Docker Deployment

### **docker-compose.yml:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: diachronic_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  backend:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/diachronic_db
      REDIS_URL: redis://redis:6379/0
  
  celery:
    build: ./backend
    command: celery -A config worker -l info
    volumes:
      - ./backend:/app
    depends_on:
      - postgres
      - redis
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
```

---

## 📊 Performance Optimization

### **Database Indexes:**
```python
class Token(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['lemma']),
            models.Index(fields=['pos']),
            models.Index(fields=['sentence', 'position']),
        ]
```

### **API Caching:**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def text_list(request):
    texts = Text.objects.all()
    return JsonResponse({'texts': list(texts.values())})
```

### **Query Optimization:**
```python
# Use select_related for foreign keys
texts = Text.objects.select_related('author').all()

# Use prefetch_related for many-to-many
texts = Text.objects.prefetch_related('sentences__tokens').all()
```

---

## ✅ Implementation Checklist

### **Phase 1: Backend (Week 1-2)**
- [ ] Django project setup
- [ ] Database models
- [ ] REST API endpoints
- [ ] Authentication system
- [ ] Stanza integration
- [ ] Celery tasks

### **Phase 2: Frontend (Week 3-4)**
- [ ] React app setup
- [ ] Corpus browser component
- [ ] Annotation editor component
- [ ] Dashboard component
- [ ] API integration
- [ ] User authentication

### **Phase 3: Integration (Week 5)**
- [ ] Connect all systems
- [ ] Import existing data
- [ ] Test workflows
- [ ] Performance optimization

### **Phase 4: Deployment (Week 6)**
- [ ] Docker setup
- [ ] Cloud deployment
- [ ] CI/CD pipeline
- [ ] Documentation

---

**Complete Django + React web platform specification ready!** 🌐✨

**This integrates ALL 9 previous systems into one unified web application!** 🚀
