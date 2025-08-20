#!/usr/bin/env python3
"""
AGENT MONITOR - Check if your agent is running
Run this anytime to verify status
"""

import os
import sqlite3
import psutil
from datetime import datetime, timedelta

print("="*60)
print("DIACHRONIC AGENT STATUS CHECK")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)

# 1. Check if agent process is running
agent_running = False
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmdline = proc.info.get('cmdline', [])
        if cmdline and any('final_complete_agent.py' in str(arg) for arg in cmdline):
            agent_running = True
            print(f"\n✅ AGENT IS RUNNING!")
            print(f"   PID: {proc.info['pid']}")
            print(f"   Started: {datetime.fromtimestamp(proc.create_time())}")
            uptime = datetime.now() - datetime.fromtimestamp(proc.create_time())
            print(f"   Uptime: {uptime}")
            break
    except:
        pass

if not agent_running:
    print("\n❌ Agent is NOT running!")
    print("   Start it with: python start_now.py")

# 2. Check recent activity in database
db_path = "Z:\\DiachronicValencyCorpus\\corpus_main.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check total texts
    cursor.execute("SELECT COUNT(*), MAX(download_time) FROM texts")
    count, last_download = cursor.fetchone()
    
    print(f"\n📊 DATABASE STATUS:")
    print(f"   Total texts: {count}")
    if last_download:
        print(f"   Last download: {last_download}")
        # Check if downloaded recently (within 1 hour)
        last_dt = datetime.strptime(last_download, "%Y-%m-%d %H:%M:%S")
        if datetime.now() - last_dt < timedelta(hours=1):
            print(f"   ✅ Actively downloading!")
        else:
            print(f"   ⚠️  No recent downloads")
    
    # Check recent downloads
    cursor.execute("""
        SELECT filename, download_time 
        FROM texts 
        ORDER BY download_time DESC 
        LIMIT 5
    """)
    
    print(f"\n📥 RECENT DOWNLOADS:")
    for filename, dl_time in cursor.fetchall():
        print(f"   - {filename} at {dl_time}")
    
    conn.close()

# 3. Check log file
log_path = "Z:\\DiachronicValencyCorpus\\agent_24_7.log"
if os.path.exists(log_path):
    # Get last 10 lines
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        recent_lines = lines[-10:]
    
    print(f"\n📄 RECENT LOG ENTRIES:")
    for line in recent_lines[-5:]:  # Show last 5
        print(f"   {line.strip()}")

# 4. Check disk space
import shutil
total, used, free = shutil.disk_usage("Z:\\")
print(f"\n💾 DISK SPACE ON Z:")
print(f"   Free: {free // (2**30)} GB")
print(f"   Used: {used // (2**30)} GB")

print("\n" + "="*60)
if agent_running:
    print("✅ AGENT IS RUNNING SUCCESSFULLY!")
    print("   It will continue through the night")
    print("   Check again with: python check_agent_status.py")
else:
    print("❌ AGENT NEEDS TO BE STARTED")
    print("   Run: python start_now.py")
print("="*60)