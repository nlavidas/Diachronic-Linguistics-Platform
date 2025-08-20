
# RESUME DIACHRONIC CORPUS COLLECTION
# Run this tomorrow to continue from where you left off

Write-Host "🌍 DIACHRONIC CORPUS COLLECTION - RESUME SESSION" -ForegroundColor Green
Write-Host "=" * 60

# Check checkpoint
if (Test-Path "corpus_texts\checkpoints\latest_checkpoint.json") {
    $checkpoint = Get-Content "corpus_texts\checkpoints\latest_checkpoint.json" | ConvertFrom-Json
    Write-Host "✅ Found checkpoint from: $($checkpoint.timestamp)" -ForegroundColor Green
    Write-Host "📊 Current phase: $($checkpoint.phase)" -ForegroundColor Yellow
    Write-Host "📚 URLs collected: $($checkpoint.progress.urls_collected)" -ForegroundColor Cyan
} else {
    Write-Host "❌ No checkpoint found!" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Show dashboard
Write-Host "📊 Opening progress dashboard..." -ForegroundColor Green
Start-Process "web\dashboard_data\progress_dashboard.html"

# Ready for next phase
Write-Host "🚀 Ready for PHASE 2: BULK TEXT SCRAPING" -ForegroundColor Green
Write-Host "Run: python .\scripts\bulk_text_scraper.py" -ForegroundColor Yellow
