import json
import sqlite3
from pathlib import Path
import datetime
from typing import Dict, List

class CheckpointDashboard:
    def __init__(self):
        self.checkpoint_dir = Path('corpus_texts/checkpoints')
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.dashboard_dir = Path('web/dashboard_data')
        self.dashboard_dir.mkdir(parents=True, exist_ok=True)
        
    def create_progress_checkpoint(self):
        """Create a comprehensive checkpoint of current progress"""
        checkpoint_time = datetime.datetime.now().isoformat()
        
        # Load collected URLs
        urls_file = Path('corpus_texts/ultimate_open_access_collection/ultimate_open_access_urls.json')
        if urls_file.exists():
            with open(urls_file, 'r', encoding='utf-8') as f:
                collected_urls = json.load(f)
        else:
            collected_urls = {}
        
        # Create checkpoint data
        checkpoint_data = {
            'timestamp': checkpoint_time,
            'phase': 'URL_COLLECTION_COMPLETE',
            'next_phase': 'BULK_TEXT_SCRAPING',
            'progress': {
                'urls_collected': sum(len(urls) for urls in collected_urls.values()),
                'repositories_harvested': 14,
                'categories': len(collected_urls),
                'ready_for_scraping': True
            },
            'collections': {
                category: {
                    'count': len(urls),
                    'sample_urls': urls[:3] if urls else [],
                    'status': 'READY_FOR_DOWNLOAD'
                }
                for category, urls in collected_urls.items()
            },
            'next_steps': [
                '1. Run bulk text scraping system',
                '2. Download all 3,552 texts', 
                '3. Process and analyze texts',
                '4. Create searchable corpus database'
            ]
        }
        
        # Save checkpoint
        checkpoint_file = self.checkpoint_dir / f'checkpoint_{checkpoint_time.replace(":", "-")}.json'
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
        
        # Save latest checkpoint
        latest_file = self.checkpoint_dir / 'latest_checkpoint.json'
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ CHECKPOINT CREATED: {checkpoint_file}")
        return checkpoint_data
    
    def create_progress_dashboard_html(self, checkpoint_data: Dict):
        """Create HTML dashboard for monitoring progress"""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diachronic Corpus Collection Progress</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; color: #4a90e2; margin-bottom: 10px; }}
        .stat-label {{ font-size: 1.1em; color: #666; }}
        .collections-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }}
        .collection-card {{ background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .collection-title {{ font-size: 1.3em; font-weight: bold; margin-bottom: 15px; color: #333; }}
        .collection-count {{ font-size: 2em; font-weight: bold; color: #27ae60; margin-bottom: 10px; }}
        .status-badge {{ display: inline-block; padding: 5px 15px; background: #27ae60; color: white; border-radius: 20px; font-size: 0.9em; }}
        .next-steps {{ background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-top: 30px; }}
        .step-item {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
        .step-item:last-child {{ border-bottom: none; }}
        .phase-indicator {{ background: #4a90e2; color: white; padding: 10px 20px; border-radius: 25px; display: inline-block; margin-bottom: 20px; }}
        .url-sample {{ font-family: monospace; font-size: 0.8em; color: #666; background: #f8f9fa; padding: 5px; border-radius: 3px; margin: 2px 0; }}
        .progress-bar {{ width: 100%; height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden; margin: 10px 0; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #4a90e2, #27ae60); width: 75%; transition: width 0.3s; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 Diachronic Corpus Collection Dashboard</h1>
            <p>📅 Last Updated: {checkpoint_data['timestamp']}</p>
            <div class="phase-indicator">📊 Current Phase: {checkpoint_data['phase'].replace('_', ' ')}</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{checkpoint_data['progress']['urls_collected']:,}</div>
                <div class="stat-label">📚 Total URLs Collected</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{checkpoint_data['progress']['repositories_harvested']}</div>
                <div class="stat-label">🏛️ Repositories Harvested</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{checkpoint_data['progress']['categories']}</div>
                <div class="stat-label">📂 Text Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100%</div>
                <div class="stat-label">✅ URL Collection Progress</div>
                <div class="progress-bar"><div class="progress-fill"></div></div>
            </div>
        </div>

        <h2>📚 Collection Categories</h2>
        <div class="collections-grid">
"""
        
        # Add collection cards
        for category, info in checkpoint_data['collections'].items():
            category_title = category.replace('_', ' ').title()
            html_content += f"""
            <div class="collection-card">
                <div class="collection-title">{category_title}</div>
                <div class="collection-count">{info['count']:,}</div>
                <div class="stat-label">URLs collected</div>
                <div class="status-badge">{info['status'].replace('_', ' ')}</div>
                <h4>Sample URLs:</h4>
"""
            for url in info['sample_urls']:
                html_content += f'<div class="url-sample">{url}</div>'
            
            html_content += "</div>"
        
        # Add next steps
        html_content += f"""
        </div>

        <div class="next-steps">
            <h2>🚀 Next Steps</h2>
"""
        for step in checkpoint_data['next_steps']:
            html_content += f'<div class="step-item">{step}</div>'
        
        html_content += f"""
        </div>

        <div class="next-steps">
            <h2>📋 Resume Instructions</h2>
            <div class="step-item"><strong>To continue tomorrow:</strong></div>
            <div class="step-item">1. Open PowerShell in project directory</div>
            <div class="step-item">2. Activate virtual environment: <code>.\\venv\\Scripts\\Activate.ps1</code></div>
            <div class="step-item">3. Run: <code>python .\\scripts\\bulk_text_scraper.py</code></div>
            <div class="step-item">4. Monitor progress in this dashboard</div>
        </div>

        <div style="text-align: center; margin-top: 40px; color: #666;">
            <p>💎 Diachronic Linguistics Platform - Open Access Text Collection</p>
            <p>🔄 Auto-refresh: <span id="countdown">60</span> seconds</p>
        </div>
    </div>

    <script>
        // Auto-refresh countdown
        let countdown = 60;
        setInterval(() => {{
            countdown--;
            document.getElementById('countdown').textContent = countdown;
            if (countdown <= 0) {{
                location.reload();
            }}
        }}, 1000);
    </script>
</body>
</html>
"""
        
        # Save dashboard
        dashboard_file = self.dashboard_dir / 'progress_dashboard.html'
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🎯 DASHBOARD CREATED: {dashboard_file}")
        return dashboard_file
    
    def create_resume_script(self):
        """Create a script to easily resume tomorrow"""
        resume_script = """
# RESUME DIACHRONIC CORPUS COLLECTION
# Run this tomorrow to continue from where you left off

Write-Host "🌍 DIACHRONIC CORPUS COLLECTION - RESUME SESSION" -ForegroundColor Green
Write-Host "=" * 60

# Check checkpoint
if (Test-Path "corpus_texts\\checkpoints\\latest_checkpoint.json") {
    $checkpoint = Get-Content "corpus_texts\\checkpoints\\latest_checkpoint.json" | ConvertFrom-Json
    Write-Host "✅ Found checkpoint from: $($checkpoint.timestamp)" -ForegroundColor Green
    Write-Host "📊 Current phase: $($checkpoint.phase)" -ForegroundColor Yellow
    Write-Host "📚 URLs collected: $($checkpoint.progress.urls_collected)" -ForegroundColor Cyan
} else {
    Write-Host "❌ No checkpoint found!" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& .\\venv\\Scripts\\Activate.ps1

# Show dashboard
Write-Host "📊 Opening progress dashboard..." -ForegroundColor Green
Start-Process "web\\dashboard_data\\progress_dashboard.html"

# Ready for next phase
Write-Host "🚀 Ready for PHASE 2: BULK TEXT SCRAPING" -ForegroundColor Green
Write-Host "Run: python .\\scripts\\bulk_text_scraper.py" -ForegroundColor Yellow
"""
        
        resume_file = Path('resume_corpus_collection.ps1')
        with open(resume_file, 'w', encoding='utf-8') as f:
            f.write(resume_script)
        
        print(f"🔄 RESUME SCRIPT CREATED: {resume_file}")
        return resume_file

if __name__ == "__main__":
    dashboard = CheckpointDashboard()
    checkpoint_data = dashboard.create_progress_checkpoint()
    dashboard_file = dashboard.create_progress_dashboard_html(checkpoint_data)
    resume_script = dashboard.create_resume_script()
    
    print(f"\\n{'='*60}")
    print("✅ CHECKPOINT & DASHBOARD SYSTEM READY")
    print(f"{'='*60}")
    print(f"📊 Progress Dashboard: {dashboard_file}")
    print(f"🔄 Resume Script: {resume_script}")
    print(f"💾 Checkpoint Data: Safe to close laptop")
    print(f"🚀 Next Phase: Bulk text scraping (3,552 texts)")
    
    print(f"\\n🌙 SAFE TO CLOSE - RESUME TOMORROW:")
    print(f"1. Open PowerShell in project directory")
    print(f"2. Run: .\\resume_corpus_collection.ps1")
    print(f"3. Continue with bulk scraping")
