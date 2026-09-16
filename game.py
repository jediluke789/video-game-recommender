from dotenv import load_dotenv
import requests
import os
import pprint

load_dotenv()

def main():
    game_name = input("Enter a game name: ")
    if not bool(game_name.strip()):
        game_name = "Minecraft"

    pprint.pprint(get_requested_game(game_name))
    game_data = get_requested_game(game_name)
    print(f"Name: {game_data['results'][0]['name']}, Released: {game_data['results'][0]['released']}, Rating: {game_data['results'][0]['rating']}")

    

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

if __name__ == "__main__":
    main()