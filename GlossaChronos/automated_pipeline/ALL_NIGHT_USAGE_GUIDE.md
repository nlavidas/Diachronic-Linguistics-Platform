# ALL-NIGHT PRODUCTION RUN - USAGE GUIDE

**Run the platform overnight and get comprehensive morning report**

---

## QUICK START (3 Steps)

### Step 1: Configure Systems
```powershell
# Quick configuration with presets
python configure_systems.py --quick

# Or interactive configuration
python configure_systems.py
```

**Presets:**
1. **Conservative** - Safe systems only (no AI, no training)
2. **Standard** - Most systems enabled (includes AI)
3. **Full Power** - All systems running (maximum capability)
4. **Custom** - Interactive selection

### Step 2: Review Configuration
Check `config.json` to verify your selections:
- Which systems are enabled
- Cycle interval (default: 30 minutes)
- Maximum cycles (default: 20)

### Step 3: Start All-Night Run
```powershell
python run_all_night_production.py
```

**The platform will now run automatically all night!**

---

## WHAT HAPPENS OVERNIGHT

### Automatic Processing Cycles

Each cycle (default 30 minutes) runs:

1. **Text Collection** (if enabled)
   - Collects texts from 6 sources
   - Saves to `corpus/raw/`
   - Tracks statistics

2. **AI Annotation** (if enabled)
   - Annotates with selected LLM
   - Uses local Ollama by default (FREE)
   - Saves annotations to database

3. **Continuous Training** (if enabled)
   - Trains models on gold treebanks
   - Improves accuracy each cycle
   - Saves model checkpoints

4. **Quality Validation** (always recommended)
   - Validates all collected texts
   - 5-phase comprehensive check
   - Scores and reports quality

5. **Diachronic Analysis** (if enabled)
   - Detects semantic shifts
   - Compares periods
   - Tracks meaning changes

6. **Enhanced Parsing** (if enabled)
   - Parses with UD compliance
   - Recognizes historical patterns
   - Generates dependency trees

7. **Format Export** (if enabled)
   - Exports to 5 formats
   - CONLL-U, PROIEL, Penn, JSON, TXT
   - Saves to `exports/`

### What You Get in the Morning

**Automatic Morning Report:**
- `MORNING_REPORT.md` - Comprehensive summary
- Total texts processed
- Validation scores
- Performance metrics
- Error analysis
- Recommendations

**Processed Data:**
- `corpus/processed/` - All processed texts
- `exports/` - Exported formats
- `trained_models/` - Model checkpoints
- `logs/` - Detailed logs

---

## CONFIGURATION OPTIONS

### System Selection

**Edit `config.json` or use configurator:**

```json
{
  "systems_enabled": {
    "text_collector": true,      // Collect texts
    "ai_annotator": false,        // AI annotation (costs $)
    "continuous_trainer": false,  // Model training (intensive)
    "quality_validator": true,    // Quality checks (recommended)
    "diachronic_analyzer": true,  // Semantic shifts
    "enhanced_parser": true,      // Advanced parsing
    "format_exporter": true,      // Multi-format export
    "master_orchestrator": true   // Coordination
  }
}
```

### All-Night Mode Settings

```json
{
  "all_night_mode": {
    "enabled": true,
    "cycle_interval_minutes": 30,   // Time between cycles
    "max_cycles": 20,                // Maximum cycles (10 hours)
    "generate_reports": true,        // Create morning report
    "save_checkpoints": true         // Save cycle data
  }
}
```

### Text Collection Sources

```json
{
  "text_collection": {
    "enabled_sources": {
      "gutenberg": true,      // Project Gutenberg
      "first1kgreek": true,   // First1K GitHub
      "wikisource": false,    // Wikisource (slower)
      "perseus": false,       // Perseus (API required)
      "proiel": true          // PROIEL treebank
    },
    "limits": {
      "gutenberg_limit": 10,     // Texts per cycle
      "first1k_limit": 10,
      "wikisource_limit": 5
    }
  }
}
```

### AI Annotation Settings

```json
{
  "ai_annotation": {
    "preferred_llm": "ollama_local",  // FREE local option
    "fallback_enabled": true,          // Use backup LLM if primary fails
    "cost_limit_per_session": 1.0     // Max $ to spend (cloud APIs)
  }
}
```

**Available LLMs:**
- `ollama_local` - FREE (requires Ollama installed)
- `google_gemini` - $0.00125/1K tokens (cheapest cloud)
- `anthropic_claude` - $0.015/1K tokens
- `openai_gpt4` - $0.03/1K tokens

---

## PRESET CONFIGURATIONS

### Conservative (8 hours, safe)
**Best for:** First run, testing, limited resources

**Enabled:**
- Text Collection
- Quality Validation
- Diachronic Analysis
- Enhanced Parsing
- Format Export

**Disabled:**
- AI Annotation (costs money)
- Continuous Training (CPU intensive)

**Expected Output:**
- 100-200 texts collected
- Full validation reports
- Semantic shift analysis
- All export formats

### Standard (8 hours, balanced)
**Best for:** Regular production use

**Enabled:**
- All Conservative features
- AI Annotation (local Ollama only)

**Expected Output:**
- 100-200 texts collected & annotated
- AI-enhanced linguistic analysis
- Training data prepared

### Full Power (7.5 hours, maximum)
**Best for:** When you need everything

**Enabled:**
- ALL systems running

**Expected Output:**
- Maximum text collection
- AI annotation
- Model training & improvement
- Complete analysis pipeline
- All exports in all formats

---

## MONITORING THE RUN

### While Running

**Check logs in real-time:**
```powershell
# Windows PowerShell
Get-Content all_night_production.log -Wait -Tail 50
```

**Check progress:**
- Log file updates every cycle
- Console shows current activity
- Can stop anytime with Ctrl+C

### Stop Safely

Press `Ctrl+C` to stop gracefully:
- Current cycle completes
- Morning report generates
- All data saved
- No data loss

---

## MORNING REPORT CONTENTS

Your `MORNING_REPORT.md` will include:

### Overview
- Start/end times
- Total duration
- Cycles completed

### Statistics
- Texts processed
- Annotations created
- Validations performed
- Tokens parsed
- Files exported

### Performance
- Average cycle time
- Throughput (texts/hour)
- Success rate
- Resource usage

### System Status
- Which systems ran
- Error count
- Warnings

### Recommendations
- Issues to address
- Optimization suggestions
- Next steps

---

## EXPECTED RESULTS

### Conservative Run (8 hours)
```
Cycles: 16
Texts: 100-200
Validations: 100-200
Parses: ~10,000 tokens
Exports: 80+ files (5 formats × 16 cycles)
```

### Standard Run (8 hours)
```
Cycles: 16
Texts: 100-200
Annotations: 1,000-2,000 sentences
Validations: 100-200
Parses: ~10,000 tokens
Exports: 80+ files
```

### Full Power Run (7.5 hours)
```
Cycles: 10
Texts: 150-300
Annotations: 2,000-4,000 sentences
Training epochs: 30
Validations: 150-300
Parses: ~20,000 tokens
Exports: 50+ files
Models trained: Yes
```

---

## TROUBLESHOOTING

### "No texts collected"
**Cause:** Network issues or rate limiting  
**Solution:** Check internet connection, reduce limits in config

### "AI annotator failed"
**Cause:** Ollama not running or no API keys  
**Solution:** Start Ollama or disable AI annotation

### "High memory usage"
**Cause:** Too many systems enabled  
**Solution:** Use Conservative preset, disable training

### "Slow cycles"
**Cause:** All systems enabled or slow network  
**Solution:** Disable heavy systems (training, AI), increase interval

---

## BEST PRACTICES

### First Run
1. Use Conservative preset
2. Set short interval (15 minutes)
3. Set few cycles (4-6)
4. Monitor first 2-3 cycles
5. Adjust based on results

### Production Runs
1. Standard or Full Power preset
2. 30-45 minute intervals
3. 12-20 cycles (6-12 hours)
4. Let run unattended
5. Review morning report

### Resource Management
- **Conservative:** Low CPU, low network
- **Standard:** Medium CPU, medium network
- **Full Power:** High CPU, high network, high disk I/O

---

## COMMAND REFERENCE

### Configuration
```powershell
# Quick preset selection
python configure_systems.py --quick

# Interactive configuration
python configure_systems.py

# Edit config directly
notepad config.json
```

### Running
```powershell
# Start all-night run
python run_all_night_production.py

# Run single test cycle
python run_all_night_production.py --test-cycle
```

### Monitoring
```powershell
# Watch logs
Get-Content all_night_production.log -Wait -Tail 50

# Check morning report
notepad MORNING_REPORT.md

# View exports
explorer exports
```

---

## FILES GENERATED

### During Run
- `all_night_production.log` - Detailed log
- `config.json` - Active configuration
- `corpus/raw/*.json` - Collected texts
- `corpus/processed/*` - Processed data
- `trained_models/*.pt` - Model checkpoints

### In Morning
- `MORNING_REPORT.md` - Main report
- `exports/night_run_*` - Export files (5 formats per cycle)
- Final statistics in log
- Complete checkpoint data

---

## NEXT STEPS AFTER OVERNIGHT RUN

1. **Review Morning Report**
   - Check `MORNING_REPORT.md`
   - Review statistics
   - Note any errors

2. **Examine Outputs**
   - Check `exports/` for files
   - Review `corpus/processed/` data
   - Verify quality in logs

3. **Optimize for Next Run**
   - Adjust cycle interval
   - Enable/disable systems
   - Fine-tune collection limits

4. **Use the Data**
   - Process exports for research
   - Use annotations for training
   - Analyze semantic shifts
   - Write papers!

---

## SUPPORT

**If issues occur:**
1. Check `all_night_production.log` for errors
2. Review `MORNING_REPORT.md` recommendations
3. Adjust configuration based on errors
4. Try Conservative preset if Full Power fails

**For best results:**
- Start with Conservative
- Monitor first run
- Scale up gradually
- Use appropriate preset for your needs

---

**READY TO RUN ALL NIGHT!**

Just execute:
```powershell
python configure_systems.py --quick
python run_all_night_production.py
```

Go to sleep, wake up to comprehensive results! 🌙 → 🌅

---

**END OF ALL-NIGHT USAGE GUIDE**
