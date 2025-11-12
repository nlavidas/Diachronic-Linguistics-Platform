# 📚 Streamlit Teaching & Research Tool - Complete Guide

## 🎯 Overview

**Complete Streamlit-based application** for diachronic linguistics research and teaching:
- ✅ Corpus analysis with interactive visualizations
- ✅ Paper summarization and citation generation
- ✅ Lecture slide generation (PowerPoint/LaTeX)
- ✅ Quiz and exercise creation
- ✅ Local LLM integration (FREE with Ollama)

---

## ⚡ Quick Start (2 minutes)

```powershell
# Navigate to app
cd Z:\GlossaChronos\streamlit_app

# Install dependencies
pip install -r requirements.txt

# Launch app
streamlit run app.py

# Or use quick launch script
.\launch_app.ps1
```

**Open:** `http://localhost:8501`

---

## 📊 Features Overview

### **1. Corpus Analysis 🔍**

**What it does:**
- Analyzes PROIEL, CONLL-U, Penn-Helsinki corpora
- Tracks word order changes (SOV → SVO)
- Identifies syntactic patterns
- Analyzes language contact effects
- Visualizes diachronic trends

**How to use:**
1. Click "Corpus Analysis"
2. Upload corpus file (XML, CONLLU, PSD, CSV)
3. Select analysis types
4. Choose time periods
5. Click "Analyze Corpus"
6. View interactive charts
7. Export results

**Example Analyses:**
- **Word Order**: SOV declining from 65% → 25%
- **Syntax**: Infinitive usage trends
- **Contact**: Turkish loanword distribution
- **Morphology**: Dual number disappearance

---

### **2. Paper Summarizer 📄**

**What it does:**
- Extracts text from PDF papers
- Generates AI-powered summaries
- Identifies key points
- Creates citations (APA, MLA, Chicago, USS)
- Exports to multiple formats

**How to use:**
1. Click "Paper Summarizer"
2. Upload PDF file
3. Select summary length (Very Short → Very Long)
4. Choose sections to include
5. Select citation style
6. Click "Summarize Paper"
7. Download summary/citation

**Output includes:**
- Main summary (customizable length)
- Key points (bullet list)
- Methodology section
- Results section
- Formatted citation
- BibTeX export

---

### **3. Slide Generator 📊**

**What it does:**
- Generates lecture slides automatically
- Multiple templates (Modern, Academic, Minimalist)
- Includes historical examples
- Adds syntax trees and charts
- Exports to PowerPoint, LaTeX, or PDF

**How to use:**
1. Click "Slide Generator"
2. Choose input method:
   - Manual topic entry
   - Upload paper (auto-extract content)
   - Use corpus analysis results
3. Configure slides (5-50 slides)
4. Select template and options
5. Click "Generate Slides"
6. Preview slides
7. Download PPTX/LaTeX/PDF

**Features:**
- Historical examples (e.g., Ancient Greek SOV)
- Syntax tree diagrams
- Interactive charts
- Professional templates

---

### **4. Quiz Creator ❓**

**What it does:**
- Generates quizzes from corpus data or papers
- Multiple question types
- Adjustable difficulty levels
- Answer keys and explanations
- Export to PDF, DOCX, HTML

**How to use:**
1. Click "Quiz Creator"
2. Select source (corpus/paper/manual)
3. Choose question types:
   - Multiple Choice
   - Fill in the Blank
   - True/False
   - Identify Loanword
   - Syntax Tree Analysis
   - Translation
4. Set number and difficulty
5. Click "Generate Quiz"
6. Preview questions
7. Export quiz

**Perfect for:**
- Student assignments
- Exam preparation
- Self-assessment
- Teaching materials

---

## 🎨 User Interface

### **Sidebar:**
- Navigation menu
- Statistics dashboard
- Quick tips

### **Main Panel:**
- Task-specific interface
- Upload areas
- Configuration options
- Results display

### **Interactive Elements:**
- Drag-and-drop file upload
- Sliders and dropdowns
- Real-time preview
- Export buttons

---

## 📈 Sample Outputs

### **Corpus Analysis Chart Example:**

```
Word Order Evolution
━━━━━━━━━━━━━━━━━━━━━━
Ancient:   65% SOV | 30% SVO
Byzantine: 45% SOV | 50% SVO
Modern:    25% SOV | 70% SVO

📊 Interactive Plotly chart with:
- Stacked bars
- Time series
- Hover tooltips
```

### **Paper Summary Example:**

```
MAIN SUMMARY:
This paper investigates diachronic syntactic
changes in Greek from Ancient to Modern period...

KEY POINTS:
- SOV to SVO word order shift
- Loss of dual number and dative case
- Grammaticalization of θα future marker

CITATION (APA):
Smith, J. & Doe, A. (2024). Diachronic Syntax
of Greek. Journal of Historical Linguistics,
15, 123-145.
```

---

## 🔧 Configuration

### **Settings Page:**

**AI Models:**
- Choose LLM provider (Ollama/GPT-5/Claude/Gemini)
- Configure API keys (if using cloud)
- Install Stanza models for languages

**File Paths:**
- Set corpus directory
- Set papers directory
- Set output directory

**Appearance:**
- Theme (Light/Dark/Auto)
- Font size
- Show/hide tips

---

## 💡 Integration with Main Platform

### **Workflow Integration:**

```
1. Collect texts → period_aware_harvester.py
2. Preprocess → IE annotation app
3. Analyze in Streamlit → corpus_utils.py
4. Generate materials → slide_utils.py, quiz_utils.py
5. Export → multi_format_exporter.py
```

### **Data Flow:**

```
Z:/GlossaChronos/
  └─ 0_raw_texts/          → Upload to Streamlit
  └─ 1_processed_texts/    → Analyze in Streamlit
  └─ streamlit_app/
      └─ outputs/          → Generated slides/quizzes
```

---

## 📚 Sample Data Included

**Corpora:**
- `sample_proiel.xml` - Ancient Greek
- `sample_conllu.conllu` - Latin
- `sample_penn.psd` - Old English

**Papers:**
- `sample_paper.pdf` - Diachronic syntax study

**Instructions:**
Place in respective folders (`corpora/`, `papers/`) or upload via UI

---

## 🎓 Teaching Use Cases

### **1. Lecture Preparation**
```
Input: "Historical Syntax of Greek"
Output: 15-slide PowerPoint with:
- Introduction
- Word order changes
- Case system evolution
- Historical examples
- Charts and trees
```

### **2. Student Assessment**
```
Source: Corpus analysis results
Output: 20-question quiz with:
- Multiple choice (word order patterns)
- Fill-in-blank (grammaticalization)
- Identify loanword (Turkish/Latin)
- Answer key + explanations
```

### **3. Paper Review**
```
Input: 40-page PDF paper
Output:
- 400-word summary
- 7 key points
- APA citation
- BibTeX export
```

---

## 🚀 Performance

### **Processing Times:**

| Task | Duration | Notes |
|------|----------|-------|
| **Corpus Analysis** | 5-30 sec | Depends on size |
| **Paper Summary** | 10-60 sec | With local LLM |
| **Slide Generation** | 5-15 sec | 15 slides |
| **Quiz Creation** | 3-10 sec | 20 questions |

### **Hardware Requirements:**

**Minimum:**
- 8GB RAM
- Dual-core CPU
- No GPU required

**Recommended:**
- 16GB RAM
- Quad-core CPU
- GPU (for faster LLM)

---

## 📥 Export Formats

### **Supported Exports:**

| Feature | Formats |
|---------|---------|
| **Corpus Analysis** | CSV, PDF, PNG |
| **Paper Summary** | TXT, BibTeX, PDF |
| **Slides** | PPTX, LaTeX, PDF, HTML |
| **Quiz** | PDF, DOCX, HTML |

---

## 🎨 Templates

### **Slide Templates:**

1. **Modern** - Clean, minimalist design
2. **Academic** - Traditional serif fonts
3. **Minimalist** - Maximum content, minimal decoration
4. **Colorful** - Vibrant colors for engagement

### **Quiz Templates:**

1. **Standard** - Traditional quiz format
2. **Interactive** - Web-based with JavaScript
3. **Print** - Optimized for PDF printing

---

## 🔗 External Integrations

### **Can integrate with:**

- Zotero (citation management)
- Mendeley (bibliography)
- LaTeX editors (Overleaf)
- LMS platforms (Moodle, Canvas)
- Google Drive (cloud storage)

---

## ✅ Complete Feature List

### **Core Features:**
- [x] Multi-format corpus upload
- [x] Interactive data visualization
- [x] Diachronic trend analysis
- [x] PDF text extraction
- [x] AI-powered summarization
- [x] Citation generation (4 styles)
- [x] PowerPoint generation
- [x] LaTeX Beamer export
- [x] Quiz creation (6 types)
- [x] Multi-format export

### **Advanced Features:**
- [x] Local LLM integration (Ollama)
- [x] Plotly interactive charts
- [x] Syntax tree visualization
- [x] Language contact analysis
- [x] Morphological change tracking
- [x] Statistical analysis
- [x] Batch processing
- [x] Progress tracking

---

## 🎯 Comparison: Streamlit App vs Other Tools

| Feature | Streamlit App | IE App | Existing Platform |
|---------|---------------|---------|-------------------|
| **UI** | ✅ Web-based | ✅ Web-based | ❌ CLI only |
| **Corpus Analysis** | ✅ Visual | ✅ API | ✅ Scripts |
| **Paper Summary** | ✅ Automated | ❌ | ❌ |
| **Slide Generation** | ✅ Auto | ❌ | ❌ |
| **Quiz Creation** | ✅ Auto | ❌ | ❌ |
| **Teaching Tools** | ✅ Complete | ❌ | ❌ |
| **Export Variety** | ✅ 10+ formats | ✅ 4 formats | ✅ 4 formats |

**Best use:** Teaching and research visualization!

---

## 🚀 Next Steps

```powershell
# 1. Launch app
cd Z:\GlossaChronos\streamlit_app
streamlit run app.py

# 2. Test with sample data
# - Upload sample_proiel.xml
# - Try corpus analysis
# - Generate quiz

# 3. Create your first lecture
# - Enter topic
# - Generate slides
# - Download PowerPoint

# 4. Customize settings
# - Configure LLM (Ollama)
# - Set file paths
# - Choose theme
```

---

## 📚 Resources

**Documentation:**
- App README: `streamlit_app/README.md`
- Quick start: `launch_app.ps1`
- Sample data: `streamlit_app/corpora/`

**External Links:**
- Streamlit Docs: https://docs.streamlit.io
- Plotly Gallery: https://plotly.com/python/
- PROIEL Format: https://proiel.github.io/

---

**🎓 Complete teaching and research tool ready!** ✨

**Perfect for:**
- 📚 Preparing lectures
- 📝 Creating quizzes
- 📄 Reviewing papers
- 📊 Analyzing corpora
- 🎓 Teaching historical linguistics

**Launch now and start creating!** 🚀
