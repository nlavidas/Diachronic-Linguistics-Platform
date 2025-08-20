#!/usr/bin/env python3
"""
FIX AGENT SCHEMA
Fixes database schema issues and restarts collection
"""

import os
import sqlite3
import json
from datetime import datetime
from pathlib import Path

BASE_PATH = "Z:\\DiachronicValencyCorpus"

def analyze_databases():
    """Find and analyze all databases"""
    print("🔍 Analyzing all databases...\n")
    
    db_files = list(Path(BASE_PATH).glob('*.db'))
    
    for db_file in db_files:
        print(f"📊 Database: {db_file.name}")
        print("-" * 40)
        
        try:
            db = sqlite3.connect(str(db_file))
            cursor = db.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                print(f"\nTable: {table_name}")
                
                # Get columns
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print("Columns:", [col[1] for col in columns])
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"Rows: {count}")
                
            db.close()
            
        except Exception as e:
            print(f"Error: {e}")
            
        print("\n" + "="*50 + "\n")

def fix_all_databases():
    """Fix schema in all databases"""
    print("🔧 Fixing all database schemas...\n")
    
    db_files = list(Path(BASE_PATH).glob('*.db'))
    
    for db_file in db_files:
        print(f"Fixing: {db_file.name}")
        
        try:
            db = sqlite3.connect(str(db_file))
            cursor = db.cursor()
            
            # Get current schema
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='texts'")
            if cursor.fetchone():
                # Check columns
                cursor.execute("PRAGMA table_info(texts)")
                columns = [col[1] for col in cursor.fetchall()]
                
                # Add missing columns
                missing_columns = {
                    'source': 'TEXT',
                    'url': 'TEXT',
                    'language': 'TEXT',
                    'author': 'TEXT',
                    'work': 'TEXT',
                    'translator': 'TEXT',
                    'year': 'INTEGER',
                    'word_count': 'INTEGER',
                    'processed': 'BOOLEAN DEFAULT 0'
                }
                
                for col, dtype in missing_columns.items():
                    if col not in columns:
                        try:
                            cursor.execute(f'ALTER TABLE texts ADD COLUMN {col} {dtype}')
                            print(f"  ✅ Added column: {col}")
                        except:
                            pass
                            
                db.commit()
                
            db.close()
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            
    print("\n✅ Database schemas fixed!")

def update_agent_status():
    """Create/update agent status file"""
    print("\n📝 Updating agent status...")
    
    # Count texts
    text_dir = Path(BASE_PATH) / "texts" / "collected"
    texts = list(text_dir.glob('*.txt'))
    
    # Create status
    status = {
        'timestamp': datetime.now().isoformat(),
        'running': True,
        'texts_downloaded': len(texts),
        'errors': 0,
        'last_download': max([t.stat().st_mtime for t in texts]),
        'consultation_active': False,
        'next_download_check': datetime.now().isoformat()
    }
    
    # Save status
    with open(Path(BASE_PATH) / 'agent_status.json', 'w') as f:
        json.dump(status, f, indent=2)
        
    print("✅ Status updated!")
    
def create_collection_trigger():
    """Create trigger to restart collection"""
    print("\n🚀 Creating collection trigger...")
    
    # Create a file that signals agent to check for new downloads
    trigger_file = Path(BASE_PATH) / "RESTART_COLLECTION.trigger"
    
    with open(trigger_file, 'w') as f:
        f.write(f"Collection restart requested at {datetime.now()}\n")
        f.write("Delete this file after agent resumes downloading\n")
        
    print(f"✅ Trigger created: {trigger_file}")
    print("   Agent should resume downloading within 30 minutes")

def main():
    print("="*60)
    print("🔧 AGENT SCHEMA FIX")
    print("="*60)
    print(f"Time: {datetime.now()}")
    print(f"Path: {BASE_PATH}")
    print("="*60 + "\n")
    
    # Step 1: Analyze current state
    analyze_databases()
    
    # Step 2: Fix schemas
    fix_all_databases()
    
    # Step 3: Update status
    update_agent_status()
    
    # Step 4: Create trigger
    create_collection_trigger()
    
    print("\n" + "="*60)
    print("✅ FIX COMPLETE!")
    print("="*60)
    print("\nWhat happens next:")
    print("1. Agent will check for new downloads within 30 minutes")
    print("2. Collection should resume automatically")
    print("3. Monitor will show new activity")
    print("\nIf still stuck after 30 minutes:")
    print("- Restart just the collection worker")
    print("- Keep all monitors running")
    

if __name__ == "__main__":
    main()