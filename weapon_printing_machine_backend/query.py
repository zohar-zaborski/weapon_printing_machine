import sqlite3

# Path to your database file
db_path = "./app.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Run the query
cursor.execute("SELECT username, email, password FROM users WHERE username = 'adi';")
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()
