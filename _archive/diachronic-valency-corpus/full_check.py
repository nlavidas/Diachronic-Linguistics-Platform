import os
import sqlite3
from datetime import datetime

base_dir = r"Z:\DiachronicValencyCorpus"
os.chdir(base_dir)

print("📊 FULL CORPUS STATUS CHECK")
print(f"Directory: {base_dir}")
print(f"Time: {datetime.now()}")
print("="*60)

# Check collected texts
collected_dir = os.path.join(base_dir, "texts", "collected")
print(f"\n📁 Checking: {collected_dir}")

if os.path.exists(collected_dir):
    files = os.listdir(collected_dir)
    if files:
        print(f"✅ Found {len(files)} collected texts:")
        for f in files:
            filepath = os.path.join(collected_dir, f)
            size = os.path.getsize(filepath)
            print(f"  - {f}: {size:,} bytes")
    else:
        print("❌ Directory exists but is empty")
else:
    print("❌ Directory doesn't exist yet")
    # Create it
    os.makedirs(collected_dir, exist_ok=True)
    print("✅ Created directory")

# Check all databases
print("\n💾 DATABASES:")
for db_name in ['agent_simple.db', 'immediate_agent.db', 'agent_24_7.db']:
    db_path = os.path.join(base_dir, db_name)
    if os.path.exists(db_path):
        print(f"\n📊 {db_name}:")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"  - {table[0]}: {count} records")
                
                # Show sample records
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table[0]} LIMIT 3")
                    rows = cursor.fetchall()
                    for row in rows[:1]:  # Just show first row
                        print(f"    Sample: {row}")
            
            conn.close()
        except Exception as e:
            print(f"  Error reading: {e}")

# Check log files
print("\n📄 LOG FILES:")
for log_name in ['agent_simple.log', 'corpus_agent.log', 'agent_24_7.log']:
    log_path = os.path.join(base_dir, log_name)
    if os.path.exists(log_path):
        size = os.path.getsize(log_path)
        print(f"  - {log_name}: {size:,} bytes")
        # Show last line
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                print(f"    Last entry: {lines[-1].strip()}")

# Check if agent is still running
print("\n🔄 AGENT STATUS:")
import psutil
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        if 'python' in proc.info['name'].lower():
            cmdline = proc.info.get('cmdline', [])
            if any('agent' in str(arg) for arg in cmdline):
                print(f"✅ Agent running: PID {proc.info['pid']}")
                print(f"   Command: {' '.join(cmdline)}")
    except:
        pass