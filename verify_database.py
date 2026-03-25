"""
Verify the database contents after update.
"""
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('nyc_places.db')

# Read places table
places_df = pd.read_sql_query("SELECT * FROM places", conn)

print("="*70)
print("DATABASE VERIFICATION")
print("="*70)
print(f"\nTotal Places: {len(places_df)}")
print(f"\nColumns: {list(places_df.columns)}")

print("\n" + "="*70)
print("FIRST 5 PLACES:")
print("="*70)
print(places_df[['Place_ID', 'Name_of_place', 'Type', 'Category', 'Neighborhood', 'Price_Level']].head())

print("\n" + "="*70)
print("LAST 5 PLACES:")
print("="*70)
print(places_df[['Place_ID', 'Name_of_place', 'Type', 'Category', 'Neighborhood', 'Price_Level']].tail())

print("\n" + "="*70)
print("CATEGORY BREAKDOWN:")
print("="*70)
print(places_df['Category'].value_counts())

print("\n" + "="*70)
print("PRICE TIER DISTRIBUTION:")
print("="*70)
print(places_df['Price_Level'].value_counts().head(10))

conn.close()

print("\n✅ Database verification complete!")
