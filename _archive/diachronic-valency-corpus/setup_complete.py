#!/usr/bin/env python3
"""
COMPLETE SETUP AND LAUNCH SCRIPT
Run this to set up and start your corpus agent
"""

import os
import sys
import subprocess
import sqlite3
import shutil
from datetime import datetime

def setup_corpus_environment():
    """Complete setup for the diachronic corpus"""
    
    print("DIACHRONIC CORPUS SETUP")
    print("="*50)
    
    # 1. Check Z: drive
    corpus_path = "Z:\\DiachronicValencyCorpus"
    if not os.path.exists("Z:\\"):
        print("ERROR: Z: drive not found!")
        print("Please ensure your external drive is connected and mapped to Z:")
        return False
        
    # 2. Change to corpus directory
    os.makedirs(corpus_path, exist_ok=True)
    os.chdir(corpus_path)
    print(f"Working directory: {corpus_path}")
    
    # 3. Create all necessary directories
    print("\nCreating directory structure...")
    directories = [
        "corpus/collected",
        "corpus/processed",
        "corpus/aligned",
        "corpus/valency",
        "reports/daily",
        "reports/consultation",
        "reports/statistics",
        "github_platform/docs",
        "github_platform/data",
        "github_platform/api",
        "github_platform/frontend",
        "statistics/hourly",
        "statistics/daily",
        "tools/scripts",
        "tools/configs"
    ]
    
    for d in directories:
        os.makedirs(d, exist_ok=True)
        print(f"  Created: {d}")
        
    # 4. Check existing data
    print("\nChecking existing data...")
    existing_files = {
        "Greek NT (PROIEL)": "texts/greek/koine/proiel_greek_nt.xml",
        "KJV Bible": "texts/collected/Bible_KJV_1611.txt",
        "Iliad (Butler)": "texts/collected/Iliad_Butler_1898.txt",
        "Iliad (Chapman)": "texts/collected/Iliad_Chapman_1611.txt",
        "Iliad (Pope)": "texts/collected/Iliad_Pope_1720.txt",
        "Metamorphoses (More)": "texts/collected/Metamorphoses_More_1922.txt"
    }
    
    found_count = 0
    for name, path in existing_files.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  Found: {name} ({size:,} bytes)")
            found_count += 1
            
    print(f"\nTotal existing texts: {found_count}")
    
    # 5. Check/migrate databases
    print("\nChecking databases...")
    databases = [
        "corpus.db",
        "massive_corpus.db",
        "valency_patterns.db",
        "immediate_agent.db"
    ]
    
    for db in databases:
        if os.path.exists(db):
            print(f"  Found: {db}")
            
    # 6. Install required packages
    print("\nChecking Python packages...")
    required_packages = [
        "requests",
        "beautifulsoup4",
        "lxml",
        "pandas",
        "schedule"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  {package}: OK")
        except ImportError:
            print(f"  Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            
    # 7. Create consolidated database
    print("\nCreating consolidated database...")
    create_consolidated_database()
    
    # 8. Create launch scripts
    print("\nCreating launch scripts...")
    
    # Windows batch file
    with open("start_agent.bat", "w") as f:
        f.write("""@echo off
echo Starting Diachronic Corpus Agent...
cd /d Z:\\DiachronicValencyCorpus
python corpus_agent.py
pause
""")
    
    # PowerShell script
    with open("start_agent.ps1", "w") as f:
        f.write("""Write-Host "Starting Diachronic Corpus Agent..." -ForegroundColor Green
Set-Location Z:\\DiachronicValencyCorpus
python corpus_agent.py
Read-Host "Press Enter to exit"
""")
    
    print("\nSetup complete!")
    return True

def create_consolidated_database():
    """Create a consolidated database from existing data"""
    
    db = sqlite3.connect('consolidated_corpus.db')
    cursor = db.cursor()
    
    # Create comprehensive schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS corpus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work TEXT,
            author TEXT,
            translator TEXT,
            year INTEGER,
            period TEXT,
            language TEXT,
            source TEXT,
            url TEXT,
            file_path TEXT,
            size_bytes INTEGER,
            word_count INTEGER,
            token_count INTEGER,
            sentence_count INTEGER,
            unique_words INTEGER,
            collected_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            processed BOOLEAN DEFAULT 0,
            aligned BOOLEAN DEFAULT 0,
            quality_score REAL
        )
    ''')
    
    # Import from existing databases
    existing_dbs = ['corpus.db', 'massive_corpus.db', 'immediate_agent.db']
    
    for db_file in existing_dbs:
        if os.path.exists(db_file):
            print(f"  Importing from {db_file}...")
            try:
                source_db = sqlite3.connect(db_file)
                source_cursor = source_db.cursor()
                
                # Try to get data
                source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = source_cursor.fetchall()
                
                for table in tables:
                    if 'corpus' in table[0] or 'texts' in table[0]:
                        source_cursor.execute(f"SELECT * FROM {table[0]}")
                        data = source_cursor.fetchall()
                        print(f"    Found {len(data)} records in {table[0]}")
                        
                source_db.close()
            except Exception as e:
                print(f"    Error: {e}")
                
    db.commit()
    db.close()

def display_current_status():
    """Display current corpus status"""
    
    print("\nCURRENT CORPUS STATUS")
    print("="*50)
    
    # Count texts
    collected_dir = "corpus/collected"
    if os.path.exists(collected_dir):
        files = os.listdir(collected_dir)
        total_size = sum(os.path.getsize(os.path.join(collected_dir, f)) for f in files)
        
        print(f"Collected texts: {len(files)}")
        print(f"Total size: {total_size / (1024*1024):.1f} MB")
        
    # Check databases
    if os.path.exists('corpus.db'):
        db = sqlite3.connect('corpus.db')
        cursor = db.cursor()
        
        try:
            cursor.execute('SELECT COUNT(*), SUM(word_count), SUM(token_count) FROM texts')
            count, words, tokens = cursor.fetchone()
            
            if count:
                print(f"\nDatabase statistics:")
                print(f"  Texts: {count}")
                print(f"  Words: {words:,}" if words else "  Words: N/A")
                print(f"  Tokens: {tokens:,}" if tokens else "  Tokens: N/A")
                
        except:
            pass
            
        db.close()

def launch_agent():
    """Launch the corpus agent"""
    
    print("\nLAUNCHING CORPUS AGENT")
    print("="*50)
    
    # Save the agent script
    print("Saving agent script...")
    
    # Copy the robust agent code here
    agent_code = open('robust_corpus_agent.py', 'r').read() if os.path.exists('robust_corpus_agent.py') else ""
    
    if not agent_code:
        print("ERROR: Agent script not found!")
        print("Please ensure robust_corpus_agent.py is in the directory")
        return
        
    with open('corpus_agent.py', 'w', encoding='utf-8') as f:
        f.write(agent_code)
        
    print("Starting agent...")
    print("\nNOTE: The agent will:")
    print("- Run 24/7 (never stop)")
    print("- Have daily consultation at 12:30")
    print("- Collect retranslations automatically")
    print("- Update GitHub platform")
    print("- Track all statistics")
    
    # Launch
    subprocess.run([sys.executable, 'corpus_agent.py'])

def main():
    """Main setup function"""
    
    print("DIACHRONIC CORPUS COMPLETE SETUP")
    print("================================")
    print(f"Date: {datetime.now()}")
    print()
    
    # Run setup
    if setup_corpus_environment():
        
        # Display status
        display_current_status()
        
        # Ask to launch
        print("\nSETUP COMPLETE!")
        print("\nWould you like to:")
        print("1. Launch the agent now")
        print("2. Exit and launch manually later")
        
        choice = input("\nYour choice (1 or 2): ")
        
        if choice == '1':
            launch_agent()
        else:
            print("\nTo start the agent later, run:")
            print("  python corpus_agent.py")
            print("or")
            print("  start_agent.bat")
            
    else:
        print("\nSetup failed. Please check the errors above.")

if __name__ == "__main__":
    main()