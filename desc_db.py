import sqlite3
from config import SQLITE_DB

conn = sqlite3.connect(SQLITE_DB)
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("="*80)
print("TABLES IN DATABASE")
print("="*80)

for table in tables:
    table_name = table[0]
    print(f"\n\n📋 TABLE: {table_name}")
    print("-" * 80)
    
    # Get column info for each table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print("Columns:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Get all rows from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    if rows:
        print(f"\nRows ({len(rows)} total):")
        print("-" * 80)
        # Print column headers
        col_names = [description[0] for description in cursor.description]
        print(" | ".join(col_names))
        print("-" * 80)
        # Print each row
        for row in rows:
            print(" | ".join(str(val) for val in row))
    else:
        print("\n(No rows)")

print("\n" + "="*80)
conn.close()