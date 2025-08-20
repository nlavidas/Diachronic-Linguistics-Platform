import os
import sqlite3
from datetime import datetime

print("📊 CORPUS STATUS CHECK")
print(f"Time: {datetime.now()}")
print("="*60)

# Check collected texts
collected_dir = "texts/collected"
if os.path.exists(collected_dir):
    files = os.listdir(collected_dir)
    print(f"\n📚 Collected texts: {len(files)}")
    for f in files:
        size = os.path.getsize(os.path.join(collected_dir, f))
        print(f"  - {f}: {size:,} bytes")
else:
    print("\n❌ No texts collected yet")

# Check databases
for db_name in ['agent_simple.db', 'immediate_agent.db']:
    if os.path.exists(db_name):
        print(f"\n💾 Database: {db_name}")
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"  - {table[0]}: {count} records")
        
        conn.close()