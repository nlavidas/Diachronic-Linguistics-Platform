# Check what needs review
import sqlite3

conn = sqlite3.connect('feedback.db')
c = conn.cursor()
c.execute("SELECT id, original_text, confidence_score FROM corrections")
items = c.fetchall()
print(f"\nItems for human review: {len(items)}")
for item in items[:5]:
    print(f"  ID {item[0]}: {item[1][:50]}... (confidence: {item[2]})")
conn.close()
