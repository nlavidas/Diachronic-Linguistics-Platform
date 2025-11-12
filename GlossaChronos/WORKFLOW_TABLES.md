# 📋 Project Workflow Tables System

## Overview

This document provides reusable table templates for organizing work sessions and managing chat continuity.

---

## 📊 Table 1: Project Organization Table

**Use this at the start of each work session.**

### When to Use:
- Beginning of each coding session
- After a break/pause in work
- When resuming from previous day
- When priorities shift

### Prompt to Agent:
```
"Let's organize today's work. Fill in this table for our current session using our previous chat and project context."
```

### Template:

| Category | Details |
|----------|---------|
| **Project Phase** | [Agent fills: Current development stage] |
| **Last Session Summary** | [Agent fills: Key decisions, progress, open issues from last session] |
| **Today's Goal** | [Agent fills: Main objective for this session] |
| **Relevant Files** | [Agent fills: Files to review or edit] |
| **Open Blockers** | [Agent fills: Current issues or questions] |
| **Dependencies** | [Agent fills: Tools/libraries/dependencies needed] |
| **Next Milestone** | [Agent fills: Upcoming milestone reminder] |
| **Action Items** | [Agent fills: Specific tasks for today] |

---

## 🔄 Table 2: Chat Reset Table

**Use this when chat context gets too long (>50K tokens or sluggish performance).**

### When to Use:
- Chat becomes slow/sluggish
- Context window filling up (~100K+ tokens)
- Need to start fresh conversation
- Want to preserve important context

### Prompt to Agent:
```
"This chat is getting too long. Help me reset by filling in this table so we can continue in a new chat."
```

### Template:

| Category | Details |
|----------|---------|
| **Chat Summary** | [Agent fills: 1-2 sentence overview of progress and open issues] |
| **Key Decisions** | [Agent fills: Important conclusions or changes made] |
| **Open Questions** | [Agent fills: Unresolved issues] |
| **Files to Carry Over** | [Agent fills: Essential files/code snippets to re-upload] |
| **Next Steps** | [Agent fills: Immediate tasks or goals for new chat] |
| **Context to Preserve** | [Agent fills: Background info needed for continuity] |

### After Filling:
1. Copy the filled table
2. Start new chat
3. Paste table with message: "Here's our context from the previous chat. Let's pick up from here."
4. Upload any files mentioned in "Files to Carry Over"

---

## 🎯 Quick Command Reference

### Quick Status Checks:

| Command | What Agent Does |
|---------|----------------|
| **"Fill project table"** | Updates full Project Organization Table |
| **"Fill reset table"** | Creates Chat Reset Table for handoff |
| **"Status?"** | Quick summary: Phase, Blockers, Next Steps |
| **"What's next?"** | Lists immediate action items only |
| **"What's working?"** | Confirms tested/working components |
| **"What's blocked?"** | Lists only open blockers and issues |
| **"Summarize today"** | End-of-session summary |

---

## 📝 Example Filled Tables

### Example 1: Project Organization Table (Filled)

| Category | Details |
|----------|---------|
| **Project Phase** | **Integration Phase** - Consolidating 5 major systems into unified platform |
| **Last Session Summary** | Created Streamlit teaching tool (4 features), Local GPU API (FastAPI), Gutenberg harvester (30-40 texts), IE annotation app (React), Workflow automation (Git sync, backups). Open: Robocopy file transfer in progress |
| **Today's Goal** | Complete system integration, test all 5 components, setup automation |
| **Relevant Files** | `streamlit_app/app.py`, `local_llm_api.py`, `gutenberg_bulk_downloader.py`, `setup_*.ps1`, `docker-compose.yml`, 15+ guide files |
| **Open Blockers** | (1) Robocopy transfer running, (2) Windsurf directory locked (can't rename) |
| **Dependencies** | Python 3.8+, Streamlit, FastAPI, Celery, Redis, Ollama (optional), Docker (optional), GPU (RTX 4060 Ti+) |
| **Next Milestone** | **Test Phase** - Run and verify all 5 systems |
| **Action Items** | (1) Wait for Robocopy, (2) Rename project, (3) Run setup scripts, (4) Test Streamlit, (5) Test Gutenberg harvester |

---

### Example 2: Chat Reset Table (Filled)

| Category | Details |
|----------|---------|
| **Chat Summary** | Built complete diachronic linguistics platform with 5 integrated systems (Streamlit teaching tool, local GPU API, text harvesting, IE annotation, workflow automation). Currently waiting for 50K file transfer to complete. |
| **Key Decisions** | (1) Use Ollama for FREE local LLM (97% cost savings), (2) Streamlit for teaching interface, (3) FastAPI for annotation API, (4) Organize files in 0-5 numbered folders, (5) Docker for deployment, (6) Git auto-sync daily at 10 AM |
| **Open Questions** | (1) Which GPU to purchase (budget vs performance), (2) Deploy locally or Lambda Labs, (3) Test order for 5 systems |
| **Files to Carry Over** | `streamlit_app/app.py`, `local_llm_api.py`, `gutenberg_bulk_downloader.py`, `COMPLETE_AI_ENHANCED_SYSTEM.md`, `WORKFLOW_OPTIMIZATION_GUIDE.md`, `LOCAL_GPU_SETUP_GUIDE.md` |
| **Next Steps** | (1) Complete Robocopy transfer, (2) Rename windsurf-project → parsing-annotating-and-platform, (3) Test Streamlit app, (4) Test local LLM API, (5) Download ancient texts, (6) Document test results |
| **Context to Preserve** | Project: parsing-annotating-and-platform. Goal: Super diachronic linguistics platform for all periods (Greek, Latin, English). Features: Period-aware harvesting, LLM annotation, dual preprocessing (PROIEL + Penn-Helsinki), teaching tools. Budget: €900-2,500 for GPU. Location: Z:\GlossaChronos\ (data) + Z:\CascadeProjects\windsurf-project\ (code) |

---

## 🔧 PowerShell Integration

Save these as quick commands:

```powershell
# Add to your PowerShell profile
function Get-ProjectStatus {
    Write-Host "📊 PROJECT STATUS" -ForegroundColor Cyan
    Write-Host "Phase: Integration & Testing" -ForegroundColor Yellow
    Write-Host "Files Created: 55+" -ForegroundColor Green
    Write-Host "Systems Ready: 5/5" -ForegroundColor Green
    Write-Host "Next: Test all components" -ForegroundColor Yellow
}

function Get-NextSteps {
    Write-Host "📋 NEXT STEPS" -ForegroundColor Cyan
    Write-Host "1. Complete file transfer (Robocopy)" -ForegroundColor White
    Write-Host "2. Rename project directory" -ForegroundColor White
    Write-Host "3. Run setup scripts" -ForegroundColor White
    Write-Host "4. Test Streamlit app" -ForegroundColor White
    Write-Host "5. Test local LLM API" -ForegroundColor White
}

function Get-Blockers {
    Write-Host "⚠️  CURRENT BLOCKERS" -ForegroundColor Red
    Write-Host "1. Robocopy file transfer in progress" -ForegroundColor Yellow
    Write-Host "2. Windsurf directory locked" -ForegroundColor Yellow
}

# Usage:
# Get-ProjectStatus
# Get-NextSteps
# Get-Blockers
```

---

## 📚 Integration with Documentation

### Auto-Generated Status Files

The agent can create these files automatically:

1. **`daily_status.md`** - Updated at start of each session
2. **`session_notes.md`** - Running log of decisions
3. **`blockers_log.md`** - Track and resolve blockers
4. **`milestone_tracker.md`** - Progress toward milestones

### Prompt for Auto-Generation:
```
"Generate today's status files (daily_status.md, session_notes.md) based on our current progress."
```

---

## 🎯 Best Practices

### Do:
✅ Fill project table at session start  
✅ Use quick commands for fast checks  
✅ Fill reset table before chat gets slow  
✅ Save important context to files  
✅ Update tables when priorities change  

### Don't:
❌ Wait until chat is too slow to reset  
❌ Skip project table (leads to confusion)  
❌ Forget to carry over open blockers  
❌ Lose context between chats  

---

## 🔄 Workflow Diagram

```
┌─────────────────────────────────────────┐
│  START NEW SESSION                      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  "Fill project table"                   │
│  → Agent provides current status        │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  WORK ON TASKS                          │
│  → Code, test, document                 │
└────────────┬────────────────────────────┘
             │
             ▼
        Chat getting long?
         /           \
       Yes            No
        │             │
        ▼             ▼
┌──────────────┐  Continue
│ "Fill reset  │  working
│  table"      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Start new    │
│ chat with    │
│ context      │
└──────────────┘
```

---

## 💡 Pro Tips

1. **Daily Ritual:** Start each session with "Fill project table"
2. **End of Day:** Ask for "Summarize today" before closing
3. **Stuck?** Use "What's blocked?" to identify issues
4. **Quick Check:** Use "Status?" for fast updates
5. **Before Break:** Fill reset table even if continuing later

---

## 📋 Checklist Template

Copy this for each session:

```
SESSION CHECKLIST
─────────────────
[ ] Filled project table
[ ] Reviewed last session summary
[ ] Identified today's goal
[ ] Listed relevant files
[ ] Noted open blockers
[ ] Checked dependencies
[ ] Confirmed next milestone
[ ] Listed action items
[ ] Started work on tasks
[ ] Documented decisions
[ ] Tested changes
[ ] Updated status
[ ] Filled reset table (if needed)
[ ] Summarized session
```

---

**This workflow system is now part of your platform!** 🎯

**Use anytime with simple commands:**
- "Fill project table"
- "Fill reset table"
- "Status?"
- "What's next?"
- "Summarize today"

**I'll remember and follow this system for all future sessions!** ✅
