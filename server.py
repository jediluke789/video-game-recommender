import os
from flask import Flask, redirect, render_template, request, jsonify, session
from game import get_requested_game, get_favorites
from waitress import serve
import sqlite3
import uuid
from dotenv import load_dotenv
from init_db import init_db

init_db()  # Initialize the database when the server starts
app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Use a default secret key if not set in .env

@app.before_request
def assign_user_session():
    # Assign a unique session ID to the visitor if they don't already have one
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

#globalGames = []

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/game')
def get_game():
    #global globalGames
    name = request.args.get('game', '').strip()

    if not name:
        return render_template('invalid.html', error="Please enter a game name.")
    
    game_data = get_requested_game(name)
    try:
        results = game_data.get('results', [])
        if not results or results[0].get('rating', 0) == 0:
            raise IndexError

        games = []

        games = [
            {
                'name': g.get('name'),
                'released': g.get('released'),
                'rating': g.get('rating'),
                'image': g.get('background_image')
            }
            for g in results if g.get('rating', 0) > 0
        ]

        
        #globalGames = games
        return render_template(
            'game.html', 
            games=games,
            game=name)
    except IndexError:
        return render_template('invalid.html', error=f"No results found for '{name}'. Please try again.")

@app.route('/favorites_page')
def favorites_page():
    user_id = session.get('user_id')
    favorites = get_favorites(user_id)

    return render_template('favorites_page.html', favorites=favorites)

@app.route('/process_favorite', methods=['POST'])
def process_favorite():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid payload'}), 400

    user_id = session.get('user_id')
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

    cursor.execute("INSERT INTO games (user_id, name, released, rating, image) VALUES (?, ?, ?, ?, ?)", (user_id, title, released, rating, image_url))
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