#!/usr/bin/env python3
"""
GitHub Integration Setup
Connects all your work to github.com/nlavidas/diachronic-indo-european-corpus
"""

import os
import subprocess
from pathlib import Path
import shutil

def setup_github_repo():
    """Setup and organize everything for GitHub"""
    
    base_path = Path("Z:\\DiachronicValencyCorpus")
    
    # 1. Initialize git if needed
    if not (base_path / ".git").exists():
        subprocess.run(["git", "init"], cwd=base_path)
    
    # 2. Create proper .gitignore
    gitignore = """
# Python
__pycache__/
*.py[cod]
*.so
venv/
env/

# Databases
*.db
*.sqlite
*.db-journal

# Logs
*.log
logs/

# API Keys
.env
secrets.json

# Large data files
texts/collected/*.txt
texts/preprocessed/*.txt
texts/rejected/*.txt

# But track some samples
!texts/samples/

# Stanza models (too large)
stanza_resources/
"""
    
    with open(base_path / ".gitignore", "w") as f:
        f.write(gitignore)
    
    # 3. Create README.md
    readme = """# Diachronic Indo-European Valency Corpus

## 🎯 Overview
An open-source platform for tracking verb valency patterns across Indo-European languages over time.

### Features
- 🤖 24/7 automatic text collection and processing
- 📜 PROIEL XML format annotations
- 🔍 Valency pattern extraction (NOM, ACC, DAT, etc.)
- 🌍 Cross-linguistic comparison using ValPaL methodology
- 📊 Diachronic change visualization
- 🔗 Parallel corpus alignment

### Quick Start
```bash
# Clone the repository
git clone https://github.com/nlavidas/diachronic-indo-european-corpus.git

# Install dependencies
pip install -r requirements.txt

# Run the main system
python src/main.py
```

### Components
1. **Collection Agents** - Automatically gather texts from open sources
2. **NLP Pipeline** - Convert texts to PROIEL XML with valency annotation
3. **Web Platform** - Search and visualize patterns
4. **API** - RESTful endpoints for researchers

### Academic Foundation
- ValPaL (Leipzig Valency Patterns Database)
- Ancient Greek Valency Resources
- DiGrec (Diachronic Greek Corpus)
- Diorisis annotation framework

### Citation
```bibtex
@software{lavidas2025diachronic,
  author = {Lavidas, Nikolaos},
  title = {Diachronic Indo-European Valency Corpus},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/nlavidas/diachronic-indo-european-corpus}
}
```

### License
MIT License - Free for academic use

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
"""
    
    with open(base_path / "README.md", "w") as f:
        f.write(readme)
    
    # 4. Organize existing files
    organize_files(base_path)
    
    # 5. Create initial commit
    subprocess.run(["git", "add", "-A"], cwd=base_path)
    subprocess.run(["git", "commit", "-m", "Initial commit: Complete diachronic valency corpus system"], cwd=base_path)
    
    # 6. Add remote if not exists
    try:
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/nlavidas/diachronic-indo-european-corpus.git"], cwd=base_path)
    except:
        pass
    
    # 7. Push to GitHub
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=base_path)
    
    print("✅ GitHub integration complete!")
    print("🌐 Visit: https://github.com/nlavidas/diachronic-indo-european-corpus")

def organize_files(base_path):
    """Organize all existing files into proper structure"""
    
    # Create directories
    dirs = [
        "src/agents",
        "src/web",
        "src/nlp",
        "src/database",
        "data/texts",
        "data/proiel",
        "docs",
        "tests"
    ]
    
    for dir_path in dirs:
        (base_path / dir_path).mkdir(parents=True, exist_ok=True)
    
    # Move files to appropriate locations
    file_mappings = {
        "ultimate_24_7_agent_with_ai.py": "src/agents/main_agent.py",
        "ai_discovery_module.py": "src/agents/discovery_agent.py",
        "ai_preprocessing_24_7_agent.py": "src/agents/preprocessing_agent.py",
        "valency_resources_24_7_agent.py": "src/agents/valency_agent.py",
        "super_corpus_methodology.py": "src/nlp/methodology.py",
        "corpus_complete.db": "data/corpus.db"
    }
    
    for old_name, new_path in file_mappings.items():
        old_file = base_path / old_name
        new_file = base_path / new_path
        if old_file.exists():
            shutil.copy2(old_file, new_file)
            print(f"📁 Moved {old_name} → {new_path}")

if __name__ == "__main__":
    print("🚀 Setting up GitHub integration...")
    setup_github_repo()