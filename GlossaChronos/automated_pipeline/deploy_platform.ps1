# DEPLOYMENT AUTOMATION FOR GLOSSACHRONOS PLATFORM
# Integrated from artifacts/7_Deployment_Operations_Guide.ps1
# Enhanced for complete platform setup

param(
    [switch]$SkipVenv = $false,
    [switch]$SkipModels = $false,
    [switch]$Quick = $false
)

Write-Host "="*80 -ForegroundColor Cyan
Write-Host "GLOSSACHRONOS PLATFORM - AUTOMATED DEPLOYMENT" -ForegroundColor Cyan
Write-Host "="*80 -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"
$baseDir = "Z:\GlossaChronos\automated_pipeline"

# Navigate to platform directory
Set-Location $baseDir
Write-Host "[INFO] Working directory: $baseDir" -ForegroundColor Green

# Step 1: Virtual Environment
if (-not $SkipVenv -and -not $Quick) {
    Write-Host ""
    Write-Host "[STEP 1/6] Creating virtual environment..." -ForegroundColor Yellow
    
    if (Test-Path "venv") {
        Write-Host "  Virtual environment already exists" -ForegroundColor Gray
    } else {
        python -m venv venv
        Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
    }
    
    Write-Host "  Activating virtual environment..." -ForegroundColor Gray
    .\venv\Scripts\Activate.ps1
    Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green
}

# Step 2: Core Dependencies
Write-Host ""
Write-Host "[STEP 2/6] Installing core dependencies..." -ForegroundColor Yellow

if (-not $Quick) {
    # Core packages
    Write-Host "  Installing: requests, beautifulsoup4, lxml..." -ForegroundColor Gray
    pip install -q requests beautifulsoup4 lxml
    
    Write-Host "  Installing: pandas, numpy..." -ForegroundColor Gray
    pip install -q pandas numpy
    
    Write-Host "  ✓ Core dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  Skipped (quick mode)" -ForegroundColor Gray
}

# Step 3: NLP Dependencies
Write-Host ""
Write-Host "[STEP 3/6] Installing NLP dependencies..." -ForegroundColor Yellow

if (-not $Quick) {
    Write-Host "  Installing: stanza (Ancient Greek support)..." -ForegroundColor Gray
    pip install -q stanza
    
    Write-Host "  Installing: torch (for training)..." -ForegroundColor Gray
    pip install -q torch --index-url https://download.pytorch.org/whl/cpu
    
    Write-Host "  ✓ NLP dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  Skipped (quick mode)" -ForegroundColor Gray
}

# Step 4: Visualization & Dashboard
Write-Host ""
Write-Host "[STEP 4/6] Installing visualization tools..." -ForegroundColor Yellow

if (-not $Quick) {
    Write-Host "  Installing: streamlit, plotly..." -ForegroundColor Gray
    pip install -q streamlit plotly
    
    Write-Host "  ✓ Visualization tools installed" -ForegroundColor Green
} else {
    Write-Host "  Skipped (quick mode)" -ForegroundColor Gray
}

# Step 5: Download Stanza Models
if (-not $SkipModels -and -not $Quick) {
    Write-Host ""
    Write-Host "[STEP 5/6] Downloading Stanza NLP models..." -ForegroundColor Yellow
    
    Write-Host "  Downloading Ancient Greek model (grc)..." -ForegroundColor Gray
    python -c "import stanza; stanza.download('grc', verbose=False)"
    
    Write-Host "  Downloading Latin model (la)..." -ForegroundColor Gray
    python -c "import stanza; stanza.download('la', verbose=False)"
    
    Write-Host "  Downloading English model (en)..." -ForegroundColor Gray
    python -c "import stanza; stanza.download('en', verbose=False)"
    
    Write-Host "  ✓ Stanza models downloaded" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[STEP 5/6] Skipping Stanza models download" -ForegroundColor Gray
}

# Step 6: Create Directory Structure
Write-Host ""
Write-Host "[STEP 6/6] Creating directory structure..." -ForegroundColor Yellow

$directories = @(
    "corpus/raw",
    "corpus/processed",
    "corpus/metadata",
    "trained_models",
    "exports",
    "logs",
    "legacy_scripts",
    "docs/technical",
    "docs/research"
)

foreach ($dir in $directories) {
    $fullPath = Join-Path $baseDir $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "  ✓ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "  Already exists: $dir" -ForegroundColor Gray
    }
}

Write-Host "  ✓ Directory structure complete" -ForegroundColor Green

# Verification
Write-Host ""
Write-Host "="*80 -ForegroundColor Cyan
Write-Host "DEPLOYMENT VERIFICATION" -ForegroundColor Cyan
Write-Host "="*80 -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[CHECK] Python version:" -ForegroundColor Yellow
python --version

# Check pip packages
Write-Host ""
Write-Host "[CHECK] Key packages:" -ForegroundColor Yellow
$packages = @("requests", "beautifulsoup4", "pandas", "stanza", "torch", "streamlit")
foreach ($pkg in $packages) {
    $installed = pip show $pkg 2>$null
    if ($installed) {
        $version = ($installed | Select-String "Version:").ToString().Split(":")[1].Trim()
        Write-Host "  ✓ $pkg : $version" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $pkg : Not installed" -ForegroundColor Red
    }
}

# Check system files
Write-Host ""
Write-Host "[CHECK] System files:" -ForegroundColor Yellow
$systemFiles = @(
    "config.json",
    "configure_systems.py",
    "run_all_night_production.py",
    "ultimate_text_collector.py",
    "ai_annotator.py",
    "continuous_trainer.py",
    "quality_validator.py",
    "diachronic_analyzer.py",
    "enhanced_parser.py",
    "format_exporter.py",
    "master_orchestrator_v2.py",
    "web_dashboard.py"
)

foreach ($file in $systemFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file : Missing" -ForegroundColor Red
    }
}

# Summary
Write-Host ""
Write-Host "="*80 -ForegroundColor Cyan
Write-Host "DEPLOYMENT COMPLETE" -ForegroundColor Cyan
Write-Host "="*80 -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Configure systems:" -ForegroundColor White
Write-Host "     python configure_systems.py --quick" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Run all-night test:" -ForegroundColor White
Write-Host "     python run_all_night_production.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "  3. Launch web dashboard:" -ForegroundColor White
Write-Host "     streamlit run web_dashboard.py" -ForegroundColor Yellow
Write-Host ""

Write-Host "Documentation:" -ForegroundColor White
Write-Host "  - ALL_NIGHT_USAGE_GUIDE.md" -ForegroundColor Gray
Write-Host "  - README_COMPLETE_INTEGRATION.md" -ForegroundColor Gray
Write-Host "  - MORNING_CHECKLIST.md" -ForegroundColor Gray
Write-Host ""

Write-Host "Platform ready!" -ForegroundColor Green -BackgroundColor DarkGreen
Write-Host ""
