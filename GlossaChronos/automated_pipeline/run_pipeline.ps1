# Run 24/7 Processing Pipeline
# PowerShell script to start automated text processing

param(
    [Parameter()]
    [switch]$SingleCycle,
    [switch]$Continuous,
    [switch]$Setup
)

$ErrorActionPreference = "Stop"

Write-Host "24/7 Text Processing Pipeline" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

$PipelineDir = "Z:\GlossaChronos\automated_pipeline"

# Setup mode
if ($Setup) {
    Write-Host "`nSETUP MODE" -ForegroundColor Yellow
    Write-Host "Setting up pipeline environment..." -ForegroundColor Yellow
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "✗ Python not found. Please install Python 3.8+." -ForegroundColor Red
        exit 1
    }
    
    # Create virtual environment
    Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
    if (Test-Path "$PipelineDir\venv") {
        Write-Host "Virtual environment already exists." -ForegroundColor Yellow
    } else {
        python -m venv "$PipelineDir\venv"
        Write-Host "✓ Virtual environment created" -ForegroundColor Green
    }
    
    # Activate and install requirements
    Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
    & "$PipelineDir\venv\Scripts\Activate.ps1"
    pip install --upgrade pip
    pip install -r "$PipelineDir\requirements.txt"
    
    Write-Host "`n✓ Setup complete!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "  1. Single cycle test:  .\run_pipeline.ps1 -SingleCycle" -ForegroundColor White
    Write-Host "  2. Continuous mode:    .\run_pipeline.ps1 -Continuous" -ForegroundColor White
    exit 0
}

# Check if setup done
if (-not (Test-Path "$PipelineDir\venv")) {
    Write-Host "✗ Virtual environment not found. Run with -Setup first." -ForegroundColor Red
    Write-Host "  .\run_pipeline.ps1 -Setup" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& "$PipelineDir\venv\Scripts\Activate.ps1"

# Change to pipeline directory
Set-Location $PipelineDir

# Single cycle mode
if ($SingleCycle) {
    Write-Host "`nRUNNING SINGLE CYCLE" -ForegroundColor Yellow
    Write-Host "This will:" -ForegroundColor White
    Write-Host "  1. Collect new texts" -ForegroundColor White
    Write-Host "  2. Process up to 10 pending texts" -ForegroundColor White
    Write-Host "  3. Extract valency patterns" -ForegroundColor White
    Write-Host "  4. Generate reports" -ForegroundColor White
    Write-Host ""
    
    python pipeline_orchestrator.py
    
    Write-Host "`n✓ Single cycle complete!" -ForegroundColor Green
    Write-Host "`nCheck outputs in:" -ForegroundColor Cyan
    Write-Host "  - Processed texts: $PipelineDir\corpus\processed" -ForegroundColor White
    Write-Host "  - Valency patterns: $PipelineDir\output\valency_patterns" -ForegroundColor White
    Write-Host "  - Reports: $PipelineDir\logs" -ForegroundColor White
    exit 0
}

# Continuous mode
if ($Continuous) {
    Write-Host "`nSTARTING 24/7 CONTINUOUS MODE" -ForegroundColor Yellow
    Write-Host "Pipeline will run continuously with:" -ForegroundColor White
    Write-Host "  - Processing every hour" -ForegroundColor White
    Write-Host "  - Collection daily at 2 AM" -ForegroundColor White
    Write-Host "  - Press Ctrl+C to stop" -ForegroundColor White
    Write-Host ""
    
    # Run in continuous mode (requires modification to orchestrator)
    Write-Host "Starting pipeline..." -ForegroundColor Green
    python pipeline_orchestrator.py --continuous
    
    exit 0
}

# Default: Show help
Write-Host "`nUSAGE" -ForegroundColor Yellow
Write-Host "  .\run_pipeline.ps1 -Setup         Setup environment" -ForegroundColor White
Write-Host "  .\run_pipeline.ps1 -SingleCycle   Run one processing cycle" -ForegroundColor White
Write-Host "  .\run_pipeline.ps1 -Continuous    Run 24/7 continuous mode" -ForegroundColor White
Write-Host ""
Write-Host "EXAMPLES" -ForegroundColor Yellow
Write-Host "  # First time setup" -ForegroundColor Gray
Write-Host "  .\run_pipeline.ps1 -Setup" -ForegroundColor White
Write-Host ""
Write-Host "  # Test with single cycle" -ForegroundColor Gray
Write-Host "  .\run_pipeline.ps1 -SingleCycle" -ForegroundColor White
Write-Host ""
Write-Host "  # Start 24/7 processing" -ForegroundColor Gray
Write-Host "  .\run_pipeline.ps1 -Continuous" -ForegroundColor White
