import sqlite3
conn = sqlite3.connect('corpus.db')
cursor = conn.cursor()
cursor.execute("SELECT id, filename, language FROM texts WHERE filename LIKE '%Argonautica%'")
rows = cursor.fetchall()
print("=== VERIFY ARGONAUTICA ENTRIES ===")
for row in rows:
    print(row)
conn.close()
