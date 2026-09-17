from flask import Flask, redirect, render_template, request, jsonify
from game import get_requested_game, get_favorites
from waitress import serve
import sqlite3

app = Flask(__name__)

globalGames = []

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/game')
def get_game():
    global globalGames
    name = request.args.get('game')

    if name != None and not bool(name.strip()):
        return render_template('invalid.html', error="Please enter a game name.")
    elif name == None:
        return render_template('game.html', games=globalGames, game=globalGames[0]['name'] if globalGames else None)
    game_data = get_requested_game(name)
    try:
        if game_data['results'][0]['rating'] == 0:
            raise IndexError

        games = []

        for game in game_data['results']:
            if game['rating'] > 0:
                games.append({
                    'name': game['name'],
                    'released': game['released'],
                    'rating': game['rating'],
                    'image': game['background_image']
                })

        
        globalGames = games
        return render_template(
            'game.html', 
            games=games,
            game=name)
    except IndexError:
        return render_template('invalid.html', error=f"No results found for '{name}'. Please try again.")

@app.route('/favorites_page')
def favorites_page():
    favorites = get_favorites()

    return render_template('favorites_page.html', favorites=favorites)

@app.route('/process_favorite', methods=['POST'])
def process_favorite():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid payload'}), 400

    title = data.get('title')
    image_url = data.get('image_url')
    released = data.get('released')
    rating = data.get('rating')
    #title = request.form['title']
    #image_url = request.form['image_url']
    #released = request.form['released']
    #rating = request.form['rating']
    print("running")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO games (name, released, rating, image) VALUES (?, ?, ?, ?)", (title, released, rating, image_url))
    connection.commit()
    connection.close()


    return jsonify({'title': title, 'image_url': image_url, 'released': released, 'rating': rating})


#@app.route('/favorite/<string:game_name>', methods=['POST'])
#def favorite_game():
    print("hi")
    title = request.form['title']
    image_url = request.form['image_url']
    released = request.form['released']
    rating = request.form['rating']

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO games (name, released, rating, image) VALUES (?, ?, ?, ?)", (title, released, rating, image_url))
    connection.commit()
    #connection.close()

    cursor.execute("SELECT * FROM games")
    results = cursor.fetchall()
    print(results)
    
    #return render_template('favorite_success.html', title=title)
    return render_template("game.html")


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)