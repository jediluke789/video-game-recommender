import sqlite3

# define a connection and a cursor

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

# create a table for the games
command1 = """CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    name TEXT,
    released TEXT,
    rating TEXT,
    image TEXT
)"""

cursor.execute(command1)
connection.commit()
connection.close()
print("Database initialized successfully with user_id support.")

# add to games

# get results
#cursor.execute("SELECT * FROM games")
#results = cursor.fetchall()
#print(results)



