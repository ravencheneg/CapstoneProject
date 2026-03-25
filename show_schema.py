"""
Display the complete schema of the nyc_places.db database.
"""
import sqlite3
import pandas as pd

conn = sqlite3.connect('nyc_places.db')
cursor = conn.cursor()

print("="*80)
print("NYC PLACES DATABASE SCHEMA")
print("="*80)

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print(f"\nTotal Tables: {len(tables)}")
print(f"Tables: {[t[0] for t in tables]}\n")

# For each table, show schema
for table in tables:
    table_name = table[0]

    print("="*80)
    print(f"TABLE: {table_name}")
    print("="*80)

    # Get table info
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    print(f"\nTotal Columns: {len(columns)}\n")
    print(f"{'#':<5} {'Column Name':<30} {'Type':<15} {'Not Null':<10} {'Default':<15}")
    print("-"*80)

    for col in columns:
        col_id, name, col_type, not_null, default_val, pk = col
        not_null_str = "NOT NULL" if not_null else ""
        default_str = str(default_val) if default_val else ""
        print(f"{col_id:<5} {name:<30} {col_type:<15} {not_null_str:<10} {default_str:<15}")

    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    print(f"\nTotal Rows: {count}")

    # Show sample data
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 3", conn)
    print(f"\nSample Data (First 3 rows):")
    print("-"*80)
    print(df.to_string(index=False))
    print("\n")

conn.close()

print("="*80)
print("SCHEMA DISPLAY COMPLETE")
print("="*80)
