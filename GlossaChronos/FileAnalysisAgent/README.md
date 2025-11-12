# 🤖 Multi-Agent File Analysis System

Complete automated file analysis with PowerShell, LLM, and PowerPoint reporting.

## Quick Start

```powershell
cd Z:\GlossaChronos\FileAnalysisAgent

# Install dependencies
pip install -r requirements.txt

# Run once
python main.py

# Run scheduled (daily at 9 AM)
python main.py --schedule
```

## Features

- ✅ **Scanner Agent** - PowerShell file discovery
- ✅ **Analyzer Agent** - LLM + NLP analysis
- ✅ **Reporter Agent** - PowerPoint generation
- ✅ **Email Agent** - Automated delivery
- ✅ **Queue-based** - Multi-agent communication
- ✅ **Parallel mode** - Fast processing

## Configuration

Edit `config/config.json`:
- `input_directory` - Z: drive folder to scan
- `llm_model` - Model name (llama3.2, mistral, etc.)
- `llm_provider` - "ollama" (local, FREE) or "mistral" (cloud)

## Output

Reports saved to: `Z:\GlossaChronos\FileAnalysisAgent\reports\`

Each report includes:
- Summary (LLM-generated)
- Keywords and statistics
- Word cloud visualization
- File metadata

## Requirements

- Python 3.8+
- Ollama (for local LLM) - https://ollama.ai
- PowerShell (Windows)

**Complete multi-agent system ready to run!** 🚀
