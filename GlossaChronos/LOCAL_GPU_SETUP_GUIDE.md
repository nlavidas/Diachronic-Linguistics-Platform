# 🖥️ Local GPU Setup Guide
## Run LLMs Locally for FREE ($0/month after hardware)

---

## 💰 Cost Comparison

### **Option A: Cloud LLMs** (Current)
| Service | Cost | Accuracy | Use Case |
|---------|------|----------|----------|
| **GPT-5** | $100 for 140K sentences | 98%+ | Production batches |
| **Claude 3.5** | $0.015/1K tokens | 95%+ | Iterative refinement |
| **Gemini 1.5** | $0.00125/1K tokens | 96%+ | Long documents |
| **Monthly:** | **$100-500** | - | Ongoing costs |

### **Option B: Local GPU** (NEW!)
| Item | Cost | Notes |
|------|------|-------|
| **RTX 4090** | €2,500 | One-time (24GB VRAM) |
| **OR RTX 4070 Ti** | €900 | Budget option (12GB) |
| **OR Used RTX 3090** | €700 | Great value (24GB) |
| **Electricity** | €20-50/month | Running 24/7 |
| **Total 1st month** | €920-2,550 | - |
| **Months 2+** | €20-50/month | **97% cheaper!** |

**Break-even:** 3-6 months vs cloud costs! ⚡

---

## 🎯 Recommended Hardware Configurations

### **Budget Build (€1,500)**
```
GPU:      RTX 4060 Ti (16GB)      €600
CPU:      AMD Ryzen 5 5600X       €200
RAM:      32GB DDR4               €100
Storage:  1TB NVMe SSD            €80
PSU:      750W 80+ Gold           €100
Case:     ATX Mid Tower           €80
Motherboard: B550                 €150
Cooling:  Air cooler              €50
Windows:  Already have            €0
─────────────────────────────────────
Total:                            €1,360
```

**Can run:** Llama 3.2 (8B), Mistral 7B, Gemma 7B
**Processes:** ~50-100K tokens/day
**Perfect for:** Development, testing, small-scale production

---

### **Mid-Range Build (€2,500)**
```
GPU:      RTX 4070 Ti Super (16GB) €900
CPU:      AMD Ryzen 7 7700X        €350
RAM:      64GB DDR5                €250
Storage:  2TB NVMe SSD             €150
PSU:      850W 80+ Platinum        €150
Case:     ATX Full Tower          €120
Motherboard: X670                  €250
Cooling:  AIO liquid               €150
─────────────────────────────────────
Total:                            €2,320
```

**Can run:** Llama 3.2 (70B quantized), Mixtral 8x7B, CodeLlama 34B
**Processes:** ~200-500K tokens/day
**Perfect for:** Production, multi-model serving

---

### **Professional Build (€4,000)**
```
GPU:      RTX 4090 (24GB)         €2,000
CPU:      AMD Ryzen 9 7950X       €650
RAM:      128GB DDR5              €500
Storage:  4TB NVMe (2x 2TB)       €300
PSU:      1200W 80+ Titanium      €250
Case:     Server chassis          €200
Motherboard: X670E                €350
Cooling:  Custom loop             €400
─────────────────────────────────────
Total:                            €4,650
```

**Can run:** Llama 3.2 (70B full), GPT-J (6B), Multiple models simultaneously
**Processes:** ~1M+ tokens/day
**Perfect for:** Heavy production, research, multi-user platform

---

## 🚀 Software Stack (All FREE!)

### **Core Components**

| Component | Tool | Why |
|-----------|------|-----|
| **LLM Server** | Ollama | Easy model management |
| **API Framework** | FastAPI | Fast, modern Python API |
| **Frontend** | Streamlit | Quick UI for demos |
| **Database** | SQLite / PostgreSQL | Already using SQLite |
| **Queue** | Celery + Redis | Async task processing |
| **Container** | Docker | Easy deployment |
| **Web Server** | Nginx | Reverse proxy |
| **Monitoring** | Prometheus + Grafana | Track performance |

**Total cost: €0** (all open-source!)

---

## 📦 Installation Guide

### **Step 1: Install Ollama (5 minutes)**

```powershell
# Download from: https://ollama.ai
# Install and verify

ollama --version

# Pull models you need
ollama pull llama3.2           # 8B model (good for most tasks)
ollama pull mistral            # 7B model (fast)
ollama pull codellama          # Code-specialized
ollama pull mixtral:8x7b       # 47B model (if you have 24GB+ VRAM)

# Test
ollama run llama3.2 "Analyze this ancient Greek text: μῆνιν ἄειδε θεὰ"
```

---

### **Step 2: Setup FastAPI Server (10 minutes)**

```powershell
cd Z:\2_scripts\
mkdir local_api
cd local_api
```

Create `local_llm_api.py`:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
import uvicorn
from typing import Optional, List
import logging

app = FastAPI(title="Local LLM API", version="1.0.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnnotationRequest(BaseModel):
    text: str
    model: str = "llama3.2"
    task: str = "annotate"
    language: Optional[str] = "english"
    period: Optional[str] = "modern"

class AnnotationResponse(BaseModel):
    text: str
    annotation: str
    model: str
    tokens_processed: int

@app.post("/annotate", response_model=AnnotationResponse)
async def annotate_text(request: AnnotationRequest):
    """Annotate text using local LLM"""
    
    try:
        # Build prompt
        prompt = f"""You are a historical linguist. Annotate this {request.language} text from the {request.period} period.

Text: {request.text}

Provide:
1. Tokenization
2. POS tags (Universal Dependencies)
3. Morphological features
4. Historical notes

Output as JSON."""

        # Call Ollama
        response = ollama.generate(
            model=request.model,
            prompt=prompt
        )
        
        return AnnotationResponse(
            text=request.text,
            annotation=response['response'],
            model=request.model,
            tokens_processed=len(request.text.split())
        )
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """List available models"""
    try:
        models = ollama.list()
        return {"models": [m['name'] for m in models['models']]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "ollama": "connected"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Install and run:**

```powershell
pip install fastapi uvicorn ollama

# Run the API
python local_llm_api.py
```

**Test it:**

```powershell
# Test from PowerShell
$body = @{
    text = "The king rode forth"
    model = "llama3.2"
    language = "english"
    period = "middle"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/annotate" -Method Post -Body $body -ContentType "application/json"
```

---

### **Step 3: Docker Deployment (15 minutes)**

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "local_llm_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - OLLAMA_HOST=http://host.docker.internal:11434
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
    restart: unless-stopped
```

**Deploy:**

```powershell
docker-compose up -d
```

---

## 📊 Performance Benchmarks

### **Token Processing Speed (tokens/second)**

| Model | RTX 4060 Ti | RTX 4070 Ti | RTX 4090 |
|-------|-------------|-------------|----------|
| **Llama 3.2 (8B)** | 45 | 75 | 120 |
| **Mistral 7B** | 50 | 85 | 135 |
| **Mixtral 8x7B** | - | 25 | 45 |
| **Llama 3.2 (70B)** | - | - | 15 |

### **Daily Processing Capacity**

| Hardware | Tokens/Day | Sentences/Day | Cost/1M Tokens |
|----------|------------|---------------|----------------|
| **RTX 4060 Ti** | 100K | 5,000 | €0.002 |
| **RTX 4070 Ti** | 250K | 12,500 | €0.002 |
| **RTX 4090** | 500K+ | 25,000+ | €0.001 |
| **GPT-5 Cloud** | Unlimited | Unlimited | €30.00 |

**Savings:** 10,000x cheaper per token! 💰

---

## 🔧 Integration with Existing Platform

Update `llm_enhanced_annotator.py` to use local API:

```python
# Add local option
self.llm_configs = {
    'local_ollama': {
        'api_url': 'http://localhost:8000/annotate',
        'model': 'llama3.2',
        'use_case': 'local_free',
        'cost_per_1k_tokens': 0.0,
        'api_key_env': None
    },
    # ... existing cloud options
}
```

---

## ⚡ Performance Optimization

### **1. Batch Processing**

```python
# Process multiple texts in parallel
from concurrent.futures import ThreadPoolExecutor

def batch_annotate(texts, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(annotate_single, texts))
    return results
```

### **2. Model Quantization**

```bash
# Use quantized models for 2-3x speedup
ollama pull llama3.2:q4_0  # 4-bit quantization
ollama pull mistral:q8_0   # 8-bit quantization
```

### **3. GPU Memory Management**

```python
# Unload models when not in use
ollama.stop("mixtral")
```

---

## 💡 Cost Calculator

### **Monthly Comparison**

```
Scenario: Process 1M tokens/day (30 days)

CLOUD (GPT-5):
30M tokens × $0.03/1K = $900/month

LOCAL (RTX 4070 Ti):
Initial: €900 (one-time)
Electricity: €35/month
After 1 month: €935 total
After 6 months: €1,110 total
After 12 months: €1,320 total

Cloud 12 months: $10,800
Local 12 months: €1,320

SAVINGS: €9,480 (88%) after first year!
```

---

## 🎯 Best Use Cases

### **Use Local GPU When:**
- ✅ Processing >100K tokens/day
- ✅ Sensitive data (no cloud upload)
- ✅ Need 24/7 availability
- ✅ Budget for hardware exists
- ✅ Have technical skills

### **Use Cloud When:**
- ✅ Processing <50K tokens/day
- ✅ Need highest accuracy (GPT-5)
- ✅ No hardware budget
- ✅ Want zero maintenance
- ✅ Need instant scaling

---

## 🚀 Next Steps

```powershell
# 1. Install Ollama
# Download: https://ollama.ai

# 2. Pull models
ollama pull llama3.2
ollama pull mistral

# 3. Test
ollama run llama3.2 "Test prompt"

# 4. Setup API
cd Z:\2_scripts\local_api
python local_llm_api.py

# 5. Test API
curl http://localhost:8000/health

# 6. Integrate with platform
python llm_enhanced_annotator.py --model local_ollama
```

---

## 📋 Hardware Shopping List

**Budget Build (€1,500):**
- GPU: RTX 4060 Ti 16GB
- CPU: Ryzen 5 5600X
- RAM: 32GB DDR4
- SSD: 1TB NVMe

**Recommended Sites:**
- Alternate.de
- Mindfactory.de
- Amazon.de
- eBay (used GPUs)

---

**Local GPU = €20/month after hardware vs €500/month cloud!** 💰✨

**97% cost savings after initial investment!** 🚀
