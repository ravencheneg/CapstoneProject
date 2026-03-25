"""
Script to create SQLite database from CSV files.
Run this once to convert Users.csv and Places.csv into nyc_places.db
"""
import sqlite3
import pandas as pd

# Create database connection
conn = sqlite3.connect('nyc_places.db')

# Read CSV files
print("Reading CSV files...")
users_df = pd.read_csv('Users.csv')
places_df = pd.read_csv('Places.csv')

# Create tables from DataFrames
print("Creating users table...")
users_df.to_sql('users', conn, if_exists='replace', index=False)

print("Creating places table...")
places_df.to_sql('places', conn, if_exists='replace', index=False)

# Verify data was inserted
print("\nDatabase created successfully!")
print(f"Users table: {len(users_df)} rows")
print(f"Places table: {len(places_df)} rows")

# Show table info
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("\nTables in database:", cursor.fetchall())

conn.close()
print("\nDatabase saved as: nyc_places.db")
