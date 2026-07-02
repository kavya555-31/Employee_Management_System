import sqlite3

conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE employees
ADD COLUMN photo TEXT
""")

conn.commit()
conn.close()

print("Photo column added")