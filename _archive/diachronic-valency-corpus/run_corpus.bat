@echo off
cd /d Z:\DiachronicValencyCorpus
echo Starting Diachronic Corpus from portable drive...
echo.
python --version
echo.
echo Choose an option:
echo 1. View existing results
echo 2. Run valency extractor
echo 3. Run autonomous agent
echo 4. Open corpus folder
echo.
set /p choice=Enter choice (1-4): 

if %choice%==1 (
    type corpus_data\valency_report.md
    pause
)
if %choice%==2 (
    python valency_extractor_fixed.py
    pause
)
if %choice%==3 (
    python autonomous_agent.py
    pause
)
if %choice%==4 (
    explorer Z:\DiachronicValencyCorpus
)