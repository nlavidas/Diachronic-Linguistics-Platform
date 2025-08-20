import sqlite3
from pathlib import Path
import pandas as pd

db_path = Path("corpus.db")
conn = sqlite3.connect(db_path)

# Get top Greek verbs
query = """
    SELECT lemma, COUNT(*) as frequency 
    FROM tokens 
    WHERE pos = 'VERB' 
    GROUP BY lemma 
    ORDER BY frequency DESC 
    LIMIT 20
"""

df = pd.read_sql_query(query, conn)

print("\n=== TOP 20 GREEK VERBS IN YOUR CORPUS ===\n")
for idx, row in df.iterrows():
    print(f"{idx+1:2}. {row['lemma']:20} - {row['frequency']:,} occurrences")

# Get valency patterns
query2 = """
    SELECT DISTINCT lemma, dependency, COUNT(*) as count
    FROM tokens
    WHERE pos = 'VERB'
    GROUP BY lemma, dependency
    ORDER BY count DESC
    LIMIT 20
"""

df2 = pd.read_sql_query(query2, conn)
print("\n=== VALENCY PATTERNS ===\n")
for idx, row in df2.iterrows():
    print(f"{row['lemma']:20} + {row['dependency']:15} = {row['count']:,} times")

conn.close()
