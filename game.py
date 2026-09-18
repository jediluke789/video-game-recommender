from dotenv import load_dotenv
import requests
import os
import pprint
import sqlite3

load_dotenv()

def main():
    game_name = input("Enter a game name: ")
    if not bool(game_name.strip()):
        game_name = "Minecraft"

    pprint.pprint(get_requested_game(game_name))
    #game_data = get_requested_game(game_name)
    #print(f"Name: {game_data['results'][0]['name']}, Released: {game_data['results'][0]['released']}, Rating: {game_data['results'][0]['rating']}")

    

def get_requested_game(game_name="Minecraft"):
    request_url = requests.get(f"https://api.rawg.io/api/games?key={os.getenv('API_KEY')}&search={game_name}")
    game_data = request_url.json()
    #print(game_data)
    #print(game_data["results"][0]["name"])
    return game_data
    #response = ""
    #for game in o['results']:
    #    if game['rating'] > 0:
    #        response += f"Name: {game['name']}, Released: {game['released']}, Rating: {game['rating']}\n"
    #return response

def get_favorites(user_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name, released, rating, image FROM games WHERE user_id = ?",
        (user_id,)
    )
    rows = cursor.fetchall()
    connection.close()
    #cursor.execute("INSERT INTO games (name, released, rating, image) VALUES (?, ?, ?, ?)", ("Minecraft", "2011-11-18", "4.5", "https://media.rawg.io/media/games/b4e/b4e4c73d5aa4ec66bbf75375c4847a2b.jpg"))
    #cursor.execute("INSERT INTO games (name, released, rating, image) VALUES (?, ?, ?, ?)", ("The Legend of Zelda: Breath of the Wild", "2017-03-03", "4.8", "https://media.rawg.io/media/games/cc1/cc196a5ad763955d6532cdba236f730c.jpg"))

    favorites = []
    for row in rows:
        favorites.append({
            'name': row[0],
            'released': row[1],
            'rating': row[2],
            'image': row[3]
        })
    return favorites

def deleteRow(user_id, title):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM games WHERE user_id = ? AND name = ?",
        (user_id, title)
    )
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()