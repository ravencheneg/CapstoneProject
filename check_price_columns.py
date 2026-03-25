"""
Check for price_level, price_symbol, and price_midpoint columns in the database.
"""
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('nyc_places.db')

# Read places table
places_df = pd.read_sql_query("SELECT * FROM places", conn)

print("="*70)
print("CHECKING PRICE COLUMNS")
print("="*70)

print("\nAll columns in database:")
for i, col in enumerate(places_df.columns, 1):
    print(f"{i}. {col}")

print("\n" + "="*70)
print("SEARCHING FOR PRICE-RELATED COLUMNS:")
print("="*70)

price_columns = [col for col in places_df.columns if 'price' in col.lower()]
print(f"\nFound {len(price_columns)} price-related columns:")
for col in price_columns:
    print(f"  - {col}")

# Check specific columns
print("\n" + "="*70)
print("CHECKING SPECIFIC COLUMNS:")
print("="*70)

columns_to_check = ['price_level', 'price_symbol', 'price_midpoint', 'Price_Level']

for col in columns_to_check:
    if col in places_df.columns:
        print(f"✅ '{col}' EXISTS")
        print(f"   Sample values: {places_df[col].head(5).tolist()}")
        print(f"   Non-null count: {places_df[col].notna().sum()} / {len(places_df)}")
    else:
        print(f"❌ '{col}' NOT FOUND")

# Show first few rows with all price-related data
if price_columns:
    print("\n" + "="*70)
    print("SAMPLE DATA (First 10 places):")
    print("="*70)
    display_cols = ['Place_ID', 'Name_of_place'] + price_columns
    print(places_df[display_cols].head(10).to_string())

conn.close()
