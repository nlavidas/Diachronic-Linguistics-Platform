# 📚 Diachronic Linguistics AI Assistant

**Streamlit-based research and teaching tool for historical linguistics**

---

## 🚀 Quick Start

### **Step 1: Install Dependencies**

```powershell
cd Z:\GlossaChronos\streamlit_app
pip install -r requirements.txt
```

### **Step 2: Launch App**

```powershell
streamlit run app.py
```

### **Step 3: Open in Browser**

Open: `http://localhost:8501`

---

## 🎯 Features

### **1. Corpus Analysis 🔍**
- Upload PROIEL/Penn-Helsinki/CONLL-U data
- Analyze word order, syntax, morphology
- Visualize diachronic trends
- Export results (CSV, PDF)

### **2. Paper Summarizer 📄**
- Upload PDF research papers
- Get AI summaries
- Extract key points
- Generate citations (APA, MLA, Chicago)

### **3. Slide Generator 📊**
- Generate PowerPoint/LaTeX slides
- Multiple templates (Modern, Academic, Minimalist)
- Include examples, trees, charts
- Export to PPTX/PDF/LaTeX

### **4. Quiz Creator ❓**
- Generate quizzes from corpus/papers
- Multiple question types
- Adjustable difficulty
- Export to PDF/DOCX/HTML

---

## 📁 Directory Structure

```
streamlit_app/
├── app.py                 # Main Streamlit app
├── utils/
│   ├── corpus_utils.py    # Corpus analysis
│   ├── paper_utils.py     # Paper summarization
│   ├── slide_utils.py     # Slide generation
│   └── quiz_utils.py      # Quiz creation
├── corpora/               # Upload your corpora here
├── papers/                # Upload PDFs here
├── outputs/               # Generated files
└── requirements.txt       # Dependencies
```

---

## 💡 Usage Examples

### **Analyze a Corpus**
1. Navigate to "Corpus Analysis"
2. Upload PROIEL XML or CONLL-U file
3. Select analyses (Word Order, Syntax, etc.)
4. Click "Analyze"
5. View interactive charts and insights

### **Summarize a Paper**
1. Navigate to "Paper Summarizer"
2. Upload PDF
3. Choose summary length and options
4. Click "Summarize"
5. Download summary/citation

### **Generate Slides**
1. Navigate to "Slide Generator"
2. Enter topic or upload paper
3. Configure options (template, examples)
4. Click "Generate"
5. Download PowerPoint

### **Create Quiz**
1. Navigate to "Quiz Creator"
2. Select source (corpus/paper)
3. Choose question types
4. Set difficulty
5. Click "Generate"
6. Export to PDF/DOCX

---

## ⚙️ Configuration

### **LLM Integration**

Set up Ollama (local, FREE):
```powershell
# Install Ollama
# Download: https://ollama.ai

# Pull models
ollama pull llama3.2
ollama pull mistral

# Start service
ollama serve
```

Configure in app Settings → AI Models

---

## 📊 Sample Data

Sample PROIEL and Penn-Helsinki data included:
- `corpora/sample_proiel.xml` - Ancient Greek sample
- `corpora/sample_conllu.conllu` - Latin sample
- `papers/sample_paper.pdf` - Sample linguistics paper

---

## 🎓 Research Applications

**Perfect for:**
- Corpus linguistics research
- Diachronic syntax studies
- Teaching historical linguistics
- Creating lecture materials
- Student exercises and quizzes
- Paper review and summarization

---

## 🔧 Troubleshooting

### **Port already in use**
```powershell
streamlit run app.py --server.port 8502
```

### **Module not found**
```powershell
pip install -r requirements.txt --upgrade
```

### **Slow performance**
- Reduce corpus size
- Use smaller models
- Increase cache size in Settings

---

## 📚 Documentation

- **Streamlit**: https://docs.streamlit.io
- **Plotly**: https://plotly.com/python/
- **PROIEL**: https://proiel.github.io/
- **Universal Dependencies**: https://universaldependencies.org/

---

## ✅ Complete Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Corpus Upload** | ✅ | PROIEL, CONLL-U, Penn |
| **Word Order Analysis** | ✅ | SOV/SVO trends |
| **Syntax Analysis** | ✅ | Construction changes |
| **Language Contact** | ✅ | Loanword analysis |
| **PDF Summarization** | ✅ | AI-powered summaries |
| **Citation Generation** | ✅ | APA, MLA, Chicago |
| **Slide Generation** | ✅ | PPTX, LaTeX, PDF |
| **Quiz Creation** | ✅ | Multiple types |
| **Interactive Charts** | ✅ | Plotly visualizations |
| **Export Options** | ✅ | CSV, PDF, DOCX, HTML |

---

## 🚀 Next Steps

1. ✅ Install dependencies
2. ✅ Launch app
3. ✅ Upload sample data
4. ✅ Explore all features
5. ✅ Generate your first slides
6. ✅ Create your first quiz

**Start teaching and researching smarter!** 📚✨
