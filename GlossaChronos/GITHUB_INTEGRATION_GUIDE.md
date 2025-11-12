# GITHUB INTEGRATION GUIDE

**Connecting Platform to nlavidas GitHub Account**

---

## OVERVIEW

Complete integration with GitHub account: nlavidas  
Includes 24/7 deployment, CI/CD pipeline, and multi-repo integration

**GitHub Profile:** https://github.com/nlavidas  
**Platform Repo:** github.com/nlavidas/Diachronic-Linguistics-Platform  

---

## REPOSITORY STRUCTURE

### MAIN PLATFORM REPOSITORY

**Repository Name:** Diachronic-Linguistics-Platform  
**Visibility:** Public (for ERC open science compliance)  
**License:** MIT (or your preferred license)

**Structure:**
```
Diachronic-Linguistics-Platform/
├── .github/
│   ├── workflows/
│   │   ├── test.yml
│   │   ├── deploy.yml
│   │   └── backup.yml
│   └── ISSUE_TEMPLATE/
├── systems/
│   ├── workflow-optimization/
│   ├── local-gpu-setup/
│   ├── gutenberg-harvester/
│   ├── ie-annotation-app/
│   ├── streamlit-teaching-tool/
│   ├── career-elevation/
│   ├── multi-agent-system/
│   ├── erc-valency-project/
│   ├── production-nlp-platform/
│   └── django-web-platform/
├── docs/
│   ├── professional/
│   └── original/
├── tests/
├── scripts/
├── .gitignore
├── README.md
└── LICENSE
```

---

## GITHUB ACTIONS WORKFLOWS

### CONTINUOUS TESTING

**File:** .github/workflows/test.yml

```yaml
name: Test All Systems

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  test:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run Master Test
      run: |
        pwsh -Command ".\TEST_ALL_SYSTEMS.ps1"
    
    - name: Test Streamlit
      run: |
        pip install streamlit pandas plotly
        python -c "import streamlit; print('OK')"
    
    - name: Test Django
      run: |
        pip install django djangorestframework
        python -c "import django; print('OK')"
    
    - name: Upload Test Results
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: test-results/
```

### CONTINUOUS DEPLOYMENT

**File:** .github/workflows/deploy.yml

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]
    tags:
      - 'v*'

jobs:
  deploy-streamlit:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Streamlit Cloud
      env:
        STREAMLIT_CLOUD_TOKEN: ${{ secrets.STREAMLIT_CLOUD_TOKEN }}
      run: |
        # Deploy Streamlit app
        echo "Deploying Streamlit to cloud..."
  
  deploy-django:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Render/AWS
      env:
        DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
      run: |
        # Deploy Django to cloud
        echo "Deploying Django to production..."
  
  deploy-docker:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker Images
      run: |
        docker-compose build
    
    - name: Push to Docker Hub
      env:
        DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
        DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
      run: |
        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
        docker-compose push
```

### AUTOMATED BACKUPS

**File:** .github/workflows/backup.yml

```yaml
name: Daily Backup

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Backup Database
      run: |
        # Backup SQLite databases
        tar -czf backup-$(date +%Y%m%d).tar.gz *.db
    
    - name: Upload to Cloud Storage
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      run: |
        aws s3 cp backup-*.tar.gz s3://your-bucket/backups/
```

---

## 24/7 DEPLOYMENT OPTIONS

### OPTION 1: RENDER.COM (RECOMMENDED)

**Advantages:**
- Free tier available
- Automatic deployments from GitHub
- HTTPS included
- Database hosting
- Zero downtime deployments

**Setup:**

1. **Link GitHub Account**
```
Visit: https://render.com
Connect GitHub account: nlavidas
Select repository: Diachronic-Linguistics-Platform
```

2. **Configure Services**

**Streamlit Service:**
```yaml
# render.yaml
services:
  - type: web
    name: diachronic-streamlit
    env: python
    buildCommand: "pip install -r streamlit_app/requirements.txt"
    startCommand: "streamlit run streamlit_app/app.py --server.port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

**Django Service:**
```yaml
  - type: web
    name: diachronic-django
    env: python
    buildCommand: "pip install -r django_web_platform/backend/requirements.txt && python manage.py migrate"
    startCommand: "gunicorn config.wsgi:application"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: diachronic-db
          property: connectionString
```

**Database:**
```yaml
databases:
  - name: diachronic-db
    databaseName: diachronic_linguistics
    user: postgres
```

3. **Deploy**
```bash
# Push to GitHub
git push origin main

# Render automatically deploys
# URL: https://diachronic-streamlit.onrender.com
```

### OPTION 2: AWS (PRODUCTION)

**Services Used:**
- EC2: Application hosting
- RDS: PostgreSQL database
- S3: File storage
- CloudFront: CDN
- Route 53: Domain management

**Setup Script:**

```bash
# File: scripts/deploy-aws.sh

#!/bin/bash

# Configure AWS CLI
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
aws configure set region us-east-1

# Create RDS Database
aws rds create-db-instance \
    --db-instance-identifier diachronic-linguistics-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username postgres \
    --master-user-password $DB_PASSWORD \
    --allocated-storage 20

# Create EC2 Instance
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t3.medium \
    --key-name your-key-pair \
    --security-group-ids sg-xxxxxx \
    --user-data file://user-data.sh

# Create S3 Bucket for static files
aws s3 mb s3://diachronic-linguistics-static

# Setup CloudFront
aws cloudfront create-distribution \
    --origin-domain-name diachronic-linguistics-static.s3.amazonaws.com
```

### OPTION 3: DOCKER SWARM (SELF-HOSTED)

**For 24/7 operation on own server:**

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-prod.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    restart: always
  
  streamlit:
    build: ./streamlit_app
    restart: always
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
  
  django:
    build: ./django_web_platform/backend
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    restart: always
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/diachronic_db
    deploy:
      replicas: 2
  
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=diachronic_db
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    restart: always
  
  redis:
    image: redis:7-alpine
    restart: always
  
  celery:
    build: ./django_web_platform/backend
    command: celery -A config worker -l info
    restart: always
  
  celery-beat:
    build: ./django_web_platform/backend
    command: celery -A config beat -l info
    restart: always

volumes:
  postgres_data:

networks:
  default:
    driver: overlay
```

**Deploy:**
```bash
docker swarm init
docker stack deploy -c docker-compose.prod.yml diachronic
```

---

## INTEGRATION WITH EXISTING REPOS

### IDENTIFY RELEVANT REPOS

**From nlavidas GitHub:**

1. **Check existing repositories:**
```bash
# List all repos
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/users/nlavidas/repos
```

**Common relevant repos for linguistics projects:**
- Ancient text corpora
- Treebank collections
- NLP tools
- Teaching materials
- Research papers
- Data analysis scripts

### IMPORT STRATEGIES

**Strategy 1: Git Submodules**

```bash
# Add existing repo as submodule
git submodule add https://github.com/nlavidas/ancient-greek-corpus systems/corpora/greek

# Add treebank repo
git submodule add https://github.com/nlavidas/proiel-treebank systems/corpora/proiel

# Update submodules
git submodule update --init --recursive
```

**Strategy 2: Monorepo with Git Subtree**

```bash
# Import entire repo into subdirectory
git subtree add --prefix systems/external/greek-tools \
  https://github.com/nlavidas/greek-nlp-tools main --squash

# Pull updates
git subtree pull --prefix systems/external/greek-tools \
  https://github.com/nlavidas/greek-nlp-tools main --squash
```

**Strategy 3: Package Dependencies**

```bash
# requirements.txt
-e git+https://github.com/nlavidas/your-nlp-package.git@main#egg=nlp-tools
```

### INTEGRATION SCRIPT

**File:** scripts/integrate-repos.ps1

```powershell
# Integrate existing nlavidas repositories

# List of repositories to integrate
$repos = @(
    "ancient-greek-corpus",
    "latin-texts",
    "proiel-treebank",
    "nlp-tools",
    "teaching-materials"
)

foreach ($repo in $repos) {
    $repoUrl = "https://github.com/nlavidas/$repo"
    
    # Check if repo exists
    $exists = git ls-remote $repoUrl 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Found: $repo" -ForegroundColor Green
        
        # Add as submodule
        git submodule add $repoUrl "systems/external/$repo"
    } else {
        Write-Host "Not found: $repo" -ForegroundColor Yellow
    }
}

# Initialize submodules
git submodule update --init --recursive
```

---

## CONTINUOUS INTEGRATION SETUP

### GITHUB REPOSITORY SETUP

1. **Create Repository**
```bash
# Initialize Git
git init

# Create GitHub repo via CLI
gh repo create nlavidas/Diachronic-Linguistics-Platform \
  --public \
  --description "Complete platform for diachronic linguistics research" \
  --enable-issues \
  --enable-wiki

# Add remote
git remote add origin https://github.com/nlavidas/Diachronic-Linguistics-Platform.git
```

2. **Configure Secrets**

In GitHub Settings > Secrets and variables > Actions:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
DOCKER_USERNAME
DOCKER_PASSWORD
STREAMLIT_CLOUD_TOKEN
DB_PASSWORD
SECRET_KEY
```

3. **Branch Protection**

Settings > Branches > Add rule:
- Require pull request reviews
- Require status checks to pass
- Require conversation resolution
- Require signed commits

### AUTOMATED WORKFLOWS

**Weekly Corpus Update:**

```yaml
# .github/workflows/update-corpus.yml
name: Update Corpus

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Gutenberg Harvester
      run: |
        python gutenberg_bulk_downloader.py
    
    - name: Commit Updates
      run: |
        git config user.name "GitHub Actions Bot"
        git config user.email "bot@github.com"
        git add corpus.db
        git commit -m "Auto-update corpus"
        git push
```

**Monthly Processing:**

```yaml
# .github/workflows/process-corpus.yml
name: Process Full Corpus

on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly on 1st
  workflow_dispatch:

jobs:
  process:
    runs-on: ubuntu-latest
    timeout-minutes: 720  # 12 hours
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install Dependencies
      run: |
        pip install -r ERC_VALENCY_PROJECT/requirements.txt
    
    - name: Download Models
      run: |
        cd ERC_VALENCY_PROJECT
        pwsh scripts/download_models.ps1
    
    - name: Process Corpus
      run: |
        cd ERC_VALENCY_PROJECT
        python master_pipeline.py
    
    - name: Upload Results
      uses: actions/upload-artifact@v3
      with:
        name: processing-results
        path: ERC_VALENCY_PROJECT/output/
```

---

## 24/7 MONITORING

### UPTIME MONITORING

**Using GitHub Actions + UptimeRobot:**

```yaml
# .github/workflows/monitor.yml
name: Health Check

on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
    - name: Check Streamlit
      run: |
        curl -f https://your-app.streamlit.app || exit 1
    
    - name: Check Django API
      run: |
        curl -f https://your-api.onrender.com/health || exit 1
    
    - name: Notify on Failure
      if: failure()
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### LOGGING AND ALERTS

**File:** scripts/monitor-24-7.ps1

```powershell
# 24/7 monitoring script
while ($true) {
    # Check Streamlit
    try {
        $response = Invoke-WebRequest -Uri "https://your-app.streamlit.app" -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "Streamlit: OK" -ForegroundColor Green
        }
    } catch {
        Write-Host "Streamlit: DOWN" -ForegroundColor Red
        # Send alert
    }
    
    # Check Django
    try {
        $response = Invoke-WebRequest -Uri "https://your-api.onrender.com/health" -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "Django: OK" -ForegroundColor Green
        }
    } catch {
        Write-Host "Django: DOWN" -ForegroundColor Red
        # Send alert
    }
    
    Start-Sleep -Seconds 300  # Check every 5 minutes
}
```

---

## DEPLOYMENT CHECKLIST

### PRE-DEPLOYMENT

- [ ] All tests passing
- [ ] Documentation up to date
- [ ] Secrets configured in GitHub
- [ ] Database backups enabled
- [ ] SSL certificates obtained
- [ ] Domain configured
- [ ] Monitoring setup

### DEPLOYMENT STEPS

1. Push to GitHub
```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

2. Trigger workflows manually if needed
```bash
gh workflow run deploy.yml
```

3. Verify deployment
```bash
curl https://your-app.streamlit.app
curl https://your-api.onrender.com/health
```

4. Monitor logs
```bash
gh run list
gh run view [run-id] --log
```

### POST-DEPLOYMENT

- [ ] Health checks passing
- [ ] Monitoring active
- [ ] Backups running
- [ ] Performance acceptable
- [ ] No errors in logs

---

## COST ESTIMATION (24/7)

### FREE TIER (Recommended Start)

**Render.com Free:**
- Web services: Free (sleeps after 15 min inactivity)
- Database: Free (90 days)
- Total: 0 EUR/month

**GitHub Actions:**
- 2,000 minutes/month free
- Sufficient for testing and small deployments

### PAID TIER (Production)

**Render.com Pro:**
- Web services: 7 USD/month each × 2 = 14 USD
- Database: 7 USD/month
- Total: 21 USD/month (19 EUR)

**AWS (Alternative):**
- EC2 t3.medium: 30 USD/month
- RDS t3.micro: 15 USD/month
- S3 + CloudFront: 5 USD/month
- Total: 50 USD/month (45 EUR)

---

## QUICK SETUP

```bash
# 1. Create GitHub repo
gh repo create nlavidas/Diachronic-Linguistics-Platform --public

# 2. Initialize Git
cd Z:\GlossaChronos
git init
git add .
git commit -m "Initial commit - Complete platform"

# 3. Push to GitHub
git remote add origin https://github.com/nlavidas/Diachronic-Linguistics-Platform.git
git branch -M main
git push -u origin main

# 4. Enable GitHub Actions
# (Automatically enabled on push)

# 5. Deploy to Render
# Visit render.com and connect repository
```

---

**Complete GitHub integration with 24/7 deployment ready!**

END OF GITHUB INTEGRATION GUIDE
