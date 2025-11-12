# WORKSPACE REORGANIZATION PLAN

**Organize your diachronic linguistics workspaces logically**

Date: November 12, 2025, 11:16 PM  
Status: **PLANNING**  

---

## CURRENT SITUATION

You have multiple workspaces with random names that need proper organization:
- Collection of texts and metadata
- Metadata correction
- Parsers
- GitHub websites

---

## RECOMMENDED STRUCTURE

### Option A: SEPARATED (3 Workspaces)

**Workspace 1: Corpus Collection & Curation**
- **Name:** `GlossaChronos-Corpus`
- **Purpose:** Text collection, metadata management, quality control
- **Contains:**
  - Text harvesting scripts
  - Metadata extraction tools
  - Metadata correction/validation
  - Quality assurance systems
  - Database management

**Workspace 2: NLP Processing & Parsing**
- **Name:** `GlossaChronos-NLP`
- **Purpose:** All linguistic processing, parsing, analysis
- **Contains:**
  - Parsers (all types)
  - AI annotation systems
  - Training systems
  - Diachronic analysis
  - Format exporters

**Workspace 3: Web & Documentation**
- **Name:** `GlossaChronos-Web`
- **Purpose:** GitHub Pages, documentation, public-facing content
- **Contains:**
  - Website files
  - Documentation
  - Research outputs
  - Publications
  - Demo notebooks

---

### Option B: INTEGRATED (2 Workspaces) ⭐ RECOMMENDED

**Workspace 1: GlossaChronos-Platform** ⭐
- **Name:** `GlossaChronos-Platform` or `Diachronic-Platform`
- **Purpose:** Complete integrated platform (collection + processing)
- **Contains:**
  - Text collection & metadata (current automated_pipeline)
  - All parsers
  - AI annotation
  - Training systems
  - Quality validation
  - Everything we built tonight!
  
**Why combine?**
- Collection and parsing are tightly integrated
- Metadata flows directly to parsers
- Single database
- Unified pipeline
- Easier development

**Workspace 2: GlossaChronos-Web**
- **Name:** `GlossaChronos-Web` or `GlossaChronos-Docs`
- **Purpose:** Public website and documentation
- **Contains:**
  - GitHub Pages site
  - Documentation
  - Research outputs
  - Demo notebooks
  - Publications

---

### Option C: MONOREPO (1 Workspace)

**Single Workspace: GlossaChronos**
- **Structure:**
```
GlossaChronos/
├── platform/          # Main processing platform
│   ├── collection/    # Text collection
│   ├── processing/    # Parsers, NLP
│   ├── training/      # Model training
│   └── exports/       # Output systems
├── website/           # GitHub Pages
│   ├── docs/
│   ├── demos/
│   └── publications/
└── research/          # Research notebooks
```

---

## MY RECOMMENDATION: OPTION B (2 Workspaces)

### ✅ Workspace 1: GlossaChronos-Platform

**Current Location:** `Z:\GlossaChronos\`  
**New Name:** Keep as `GlossaChronos` or rename to `GlossaChronos-Platform`  

**Structure:**
```
GlossaChronos/
├── automated_pipeline/          # ⭐ Tonight's integration (KEEP)
│   ├── ultimate_text_collector.py
│   ├── ai_annotator.py
│   ├── continuous_trainer.py
│   ├── quality_validator.py
│   ├── diachronic_analyzer.py
│   ├── enhanced_parser.py
│   ├── format_exporter.py
│   ├── master_orchestrator_v2.py
│   ├── run_all_night_production.py
│   └── configure_systems.py
│
├── legacy_scripts/              # Old scripts (archive)
│   ├── gutenberg_bulk_downloader.py
│   ├── multi_source_harvester.py
│   └── ... (all original scripts)
│
├── corpus/                      # Data storage
│   ├── raw/                    # Collected texts
│   ├── processed/              # Processed data
│   └── metadata/               # Metadata files
│
├── trained_models/              # Model checkpoints
├── exports/                     # Export outputs
├── logs/                        # System logs
└── docs/                        # Technical docs
```

**What goes here:**
- ✅ Text collection (6 sources)
- ✅ Metadata extraction & correction
- ✅ All parsers (enhanced, PROIEL, Penn, etc.)
- ✅ AI annotation (4 LLMs)
- ✅ Training systems
- ✅ Quality validation
- ✅ Diachronic analysis
- ✅ Format exporters
- ✅ All-night production system

### ✅ Workspace 2: GlossaChronos-Web

**New Location:** Create new workspace  
**Name:** `GlossaChronos-Web`  

**Structure:**
```
GlossaChronos-Web/
├── index.html                   # Main website
├── about.html                   # About page
├── research.html                # Research outputs
├── documentation/               # User guides
│   ├── getting-started.md
│   ├── api-reference.md
│   └── tutorials/
├── demos/                       # Interactive demos
│   ├── semantic-shifts.html
│   ├── parser-demo.html
│   └── notebooks/
├── publications/                # Papers & citations
│   ├── papers/
│   ├── posters/
│   └── presentations/
├── assets/                      # Images, CSS, JS
└── _config.yml                 # GitHub Pages config
```

**What goes here:**
- ✅ GitHub Pages website
- ✅ Documentation for users
- ✅ Research publications
- ✅ Demo notebooks
- ✅ Visualizations
- ✅ API documentation

---

## RENAMING ACTIONS

### Step 1: Organize Main Platform

**Current:** `Z:\GlossaChronos\` (has everything mixed)

**Action:**
1. Keep `automated_pipeline/` as-is (our new integrated system)
2. Create `legacy_scripts/` folder
3. Move old standalone scripts to `legacy_scripts/`
4. Keep active corpus, logs, exports folders
5. Clean up root directory

### Step 2: Create Web Workspace

**Action:**
1. Create new directory: `Z:\GlossaChronos-Web\`
2. Initialize Git repository
3. Set up GitHub Pages structure
4. Move any existing website files
5. Create documentation structure

### Step 3: Update Repository Names

**On GitHub:**
1. Rename main repo to `GlossaChronos-Platform` (or keep `GlossaChronos`)
2. Create new repo: `GlossaChronos-Web`
3. Enable GitHub Pages on web repo

---

## MIGRATION SCRIPT

I'll create a PowerShell script to help you reorganize:

**Features:**
- Backup current structure
- Move files to correct locations
- Update paths in code
- Create new web workspace
- Generate summary report

---

## RECOMMENDATION SUMMARY

### ✨ Best Structure: 2 Workspaces

**1. GlossaChronos-Platform** (Main Development)
- Collection + Metadata + Parsers + Everything
- This is what we built tonight
- Keep at `Z:\GlossaChronos\`
- ~90% of your work happens here

**2. GlossaChronos-Web** (Public Website)
- GitHub Pages site
- Documentation
- Publications
- Demos
- Create new at `Z:\GlossaChronos-Web\`

### Why This Works:

**✅ Advantages:**
- Collection and parsing naturally together (they're one pipeline)
- Single codebase for all processing
- Website separated (different audience/purpose)
- Easy to maintain
- Clear separation of concerns

**✅ Workflow:**
- Develop in Platform workspace
- Export results to Web workspace
- Publish from Web workspace
- Keep them synchronized

---

## NEXT STEPS

### Tonight (After Morning Report):

1. **Review all-night run results**
   - Check MORNING_REPORT.md
   - Verify everything worked
   - Note any issues

2. **Tomorrow: Reorganize** 
   - Run migration script (I'll create it)
   - Reorganize files
   - Update Git repositories
   - Clean up structure

3. **Then: Set Up Web Workspace**
   - Create GlossaChronos-Web
   - Initialize GitHub Pages
   - Add documentation
   - Deploy first version

---

## QUESTIONS FOR YOU

Before I create the migration script:

1. **Workspace names - which do you prefer?**
   - A) `GlossaChronos` + `GlossaChronos-Web`
   - B) `GlossaChronos-Platform` + `GlossaChronos-Web`
   - C) `Diachronic-Platform` + `Diachronic-Web`

2. **Keep parsers with collection? (Recommended: YES)**
   - ✅ YES - One integrated platform
   - ❌ NO - Separate workspaces

3. **Current random workspace names?**
   - Tell me what they are so I can help rename them properly

---

## WHAT I'LL CREATE NEXT

Once you confirm preferences:

1. **Migration Script** (`reorganize_workspaces.ps1`)
   - Backs up current structure
   - Creates new folders
   - Moves files intelligently
   - Updates paths in code
   - Generates report

2. **Web Workspace Template**
   - GitHub Pages structure
   - Documentation framework
   - Research section
   - Demo templates

3. **Integration Guide**
   - How to work across both workspaces
   - Git workflow
   - Deployment process
   - Best practices

---

**READY TO HELP YOU REORGANIZE!**

**Just confirm:**
1. Use 2-workspace structure? (Platform + Web)
2. Preferred names?
3. Any specific files/folders to preserve?

Then I'll create the complete migration system! 🚀

---

**END OF WORKSPACE REORGANIZATION PLAN**
