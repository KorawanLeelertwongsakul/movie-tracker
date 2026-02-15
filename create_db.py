import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""

CREATE TABLE movies (

id INTEGER PRIMARY KEY AUTOINCREMENT,

title TEXT,

genre TEXT,

rating TEXT

)

""")

conn.close()

print("Database created")