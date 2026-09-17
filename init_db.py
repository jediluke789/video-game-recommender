import sqlite3

# define a connection and a cursor

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

# create a table for the games
command1 = """CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    released TEXT,
    rating TEXT,
    image TEXT
)"""

cursor.execute(command1)

# add to games

# get results
#cursor.execute("SELECT * FROM games")
#results = cursor.fetchall()
#print(results)



