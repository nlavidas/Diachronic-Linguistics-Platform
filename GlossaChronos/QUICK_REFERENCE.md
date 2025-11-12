# ⚡ Quick Reference Card

## 🚀 Setup (One Time)

```powershell
cd Z:\GlossaChronos
.\setup_project_structure.ps1  # Create folders
.\setup_git.ps1                # Configure Git
.\setup_automation.ps1         # Schedule tasks
```

---

## 📋 Daily Commands

```powershell
# Sync to GitHub
.\2_scripts\sync_git.ps1

# Backup immediately
.\2_scripts\backup_zdrive.ps1

# Generate report
.\2_scripts\generate_daily_report.ps1

# Annotate texts with Mistral
.\2_scripts\batch_annotate.ps1
```

---

## 📁 Where Things Go

| Type | Location |
|------|----------|
| **Raw texts** | `Z:\0_raw_texts\` |
| **Processed** | `Z:\1_processed_texts\` |
| **Scripts** | `Z:\2_scripts\` |
| **Models** | `Z:\3_models\` |
| **Logs** | `Z:\4_docs\logs\` |
| **Reports** | `Z:\4_docs\reports\` |

---

## 🤖 Automation Schedule

- **9:00 AM** - Daily report generated
- **10:00 AM** - Git auto-sync
- **11:00 PM** - Backup runs

---

## 🔧 Useful Commands

```powershell
# Check scheduled jobs
Get-ScheduledJob

# View today's log
Get-Content Z:\4_docs\logs\activity_$(Get-Date -Format 'yyyyMMdd').log -Tail 20

# Check Git status
git status

# Count files
Get-ChildItem Z:\0_raw_texts -Recurse -File | Measure-Object
```

---

## 📊 Complete Workflow

```powershell
# 1. Download texts
python gutenberg_bulk_downloader.py

# 2. Annotate with LLM
python llm_enhanced_annotator.py

# 3. Preprocess PROIEL
python agent_2_proiel_preprocessor.py

# 4. Preprocess Penn-Helsinki
python agent_3_penn_preprocessor.py

# 5. Analyze semantics
python temporal_semantic_analyzer.py

# 6. Sync to GitHub
.\2_scripts\sync_git.ps1
```

---

**Keep this handy for quick reference!** 📌
