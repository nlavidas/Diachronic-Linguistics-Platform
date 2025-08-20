Write-Host "Starting Fault-Tolerant Dashboard..." -ForegroundColor Green
Write-Host "Opening browser at http://localhost:8502" -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
streamlit run scripts\dashboard.py --server.port 8502
