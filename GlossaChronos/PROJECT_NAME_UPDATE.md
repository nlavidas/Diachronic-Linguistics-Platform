# Project Name Update

## New Project Name: **parsing-annotating-and-platform**

### Directory Rename Instructions

The project is currently located at `Z:\GlossaChronos\`

To rename to `parsing-annotating-and-platform`, run in PowerShell:

```powershell
# Close any programs accessing the directory first
# Then rename:
Rename-Item -Path "Z:\GlossaChronos" -NewName "parsing-annotating-and-platform"

# Or use this command:
Move-Item -Path "Z:\GlossaChronos" -Destination "Z:\parsing-annotating-and-platform"
```

### After Renaming

Update your working directory in all terminals:

```powershell
cd Z:\parsing-annotating-and-platform
.\venv\Scripts\Activate.ps1
```

### Updated Paths

All scripts will now use:
- Old: `Z:\GlossaChronos\`
- New: `Z:\parsing-annotating-and-platform\`

### Database Path

The database path in scripts references will need updating from:
- Old: `Z:/GlossaChronos/corpus.db`
- New: `Z:/parsing-annotating-and-platform/corpus.db`

However, if you simply rename the directory, all relative paths within will continue to work.

---

**Project:** parsing-annotating-and-platform
**Description:** AI-Enhanced Diachronic Corpus Construction & Linguistic Annotation Platform
**Version:** 1.0.0
