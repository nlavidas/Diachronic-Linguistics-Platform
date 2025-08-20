import sqlite3
import pandas as pd
import os

# Connect to database
db_path = "Z:\\DiachronicValencyCorpus\\valency\\valency_patterns.db"
conn = sqlite3.connect(db_path)

print("=== DATABASE DIAGNOSTICS ===\n")

# Check tables
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"Tables in database: {[t[0] for t in tables]}\n")

# Check valency_patterns table
cursor.execute("SELECT COUNT(*) FROM valency_patterns")
total_patterns = cursor.fetchone()[0]
print(f"Total patterns in database: {total_patterns}")

if total_patterns > 0:
    # Get sample patterns
    print("\n=== SAMPLE PATTERNS ===")
    query = """
    SELECT lemma, voice, case_frame, COUNT(*) as freq
    FROM valency_patterns
    WHERE case_frame IS NOT NULL AND case_frame != ''
    GROUP BY lemma, voice, case_frame
    ORDER BY freq DESC
    LIMIT 20
    """
    df = pd.read_sql_query(query, conn)
    print(df)
    
    # Check case frames
    print("\n=== CASE FRAME DISTRIBUTION ===")
    cursor.execute("""
        SELECT case_frame, COUNT(*) as count 
        FROM valency_patterns 
        GROUP BY case_frame 
        ORDER BY count DESC
    """)
    for frame, count in cursor.fetchall()[:10]:
        print(f"{frame}: {count}")
    
    # Check voice distribution
    print("\n=== VOICE DISTRIBUTION ===")
    cursor.execute("""
        SELECT voice, COUNT(*) as count 
        FROM valency_patterns 
        WHERE voice IS NOT NULL
        GROUP BY voice
    """)
    for voice, count in cursor.fetchall():
        print(f"{voice}: {count}")

# Check greek_case_patterns table
cursor.execute("SELECT COUNT(*) FROM greek_case_patterns")
greek_patterns = cursor.fetchone()[0]
print(f"\nGreek case patterns: {greek_patterns}")

conn.close()

# Also check what files were downloaded
print("\n=== DOWNLOADED FILES ===")
texts_dir = "Z:\\DiachronicValencyCorpus\\texts"
for root, dirs, files in os.walk(texts_dir):
    for file in files:
        filepath = os.path.join(root, file)
        size = os.path.getsize(filepath)
        print(f"{file}: {size:,} bytes")