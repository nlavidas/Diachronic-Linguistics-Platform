# 🚀 Workflow Optimization Guide

## Quick Setup (3 Steps)

```powershell
cd Z:\GlossaChronos

# Step 1: Create folder structure
.\setup_project_structure.ps1

# Step 2: Configure Git
.\setup_git.ps1

# Step 3: Setup automation
.\setup_automation.ps1
```

---

## 📁 Optimized Structure

```
Z:\
├── 0_raw_texts/        # Raw collected texts
├── 1_processed_texts/  # Normalized, annotated
├── 2_scripts/          # All scripts
├── 3_models/           # Mistral outputs, models
├── 4_docs/             # Logs, reports
└── 5_backups/          # Automated backups
```

---

## 🤖 Automated Tasks

| Task | Time | What It Does |
|------|------|--------------|
| **Git Sync** | 10:00 AM | Auto-commit and push to GitHub |
| **Daily Backup** | 11:00 PM | Backup to D: drive |
| **Daily Report** | 9:00 AM | Generate statistics CSV |
| **Activity Log** | Always | Record all commands |

---

## 🎯 Key Commands

```powershell
# Manual operations
.\2_scripts\sync_git.ps1              # Sync now
.\2_scripts\backup_zdrive.ps1         # Backup now
.\2_scripts\generate_daily_report.ps1 # Report now
.\2_scripts\batch_annotate.ps1        # Annotate with Mistral

# Check automation
Get-ScheduledJob                       # View all jobs
Get-Content Z:\4_docs\logs\*.log -Tail 20  # View logs
```

---

## ✅ Benefits

- ✅ Organized structure (no clutter)
- ✅ Auto-sync to GitHub (10 AM daily)
- ✅ Auto-backup (11 PM daily)
- ✅ Activity logging (always on)
- ✅ Daily reports (9 AM)
- ✅ Fast workflow (everything optimized)

---

## 🚀 Next Steps

1. Run setup scripts
2. Verify scheduled jobs: `Get-ScheduledJob`
3. Test manual sync: `.\2_scripts\sync_git.ps1`
4. Start working!

**Your workflow is now optimized for fast, uninterrupted collaboration!** ⚡
