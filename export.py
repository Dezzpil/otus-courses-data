import sqlite3
import csv

# Step 1: Connect to the SQLite database
database_path = 'otus.db'  # Replace with your database file path
table_name = 'courses'  # Replace with your table name
csv_file_path = 'output.csv'  # Replace with your desired CSV file path

# Connect to the database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Step 2: Execute a query to fetch all rows from the table
query = f"SELECT * FROM {table_name};"
cursor.execute(query)
rows = cursor.fetchall()

# Step 3: Get column names (headers)
column_names = [description[0] for description in cursor.description]

# Step 4: Write rows to a CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')

    # Write the header (column names)
    writer.writerow(column_names)

    # Write the rows
    writer.writerows(rows)

# Step 5: Close the database connection
conn.close()

print(f"Data exported to {csv_file_path}")