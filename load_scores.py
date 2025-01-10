import pandas as pd
import sqlite3

# Load the CSV file into a DataFrame
df = pd.read_csv('scores.csv')

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('scores.db')

# Write the DataFrame to a SQL table
df.to_sql('scores', conn, if_exists='replace', index=False)

# Close the connection
conn.close()