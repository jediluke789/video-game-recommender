import os
from flask import Flask, redirect, render_template, request, jsonify, session
from game import get_requested_game, get_favorites, deleteRow
from waitress import serve
import sqlite3
import uuid
from dotenv import load_dotenv
from init_db import init_db

init_db()  # Initialize the database when the server starts
app = Flask(__name__) # Create a Flask application instance
load_dotenv() # Load environment variables from a .env file
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Use a default secret key if not set in .env

@app.before_request
def assign_user_session():
    # Assign a unique session ID to the visitor if they don't already have one
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())



@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/game')
def get_game():
    # Get the game name from the query parameters and strip any leading/trailing whitespace
    name = request.args.get('game', '').strip()
    # Check for errors in the input and handle them appropriately
    if not name:
        return render_template('invalid.html', error="Please enter a game name.")
    
    game_data = get_requested_game(name)
    try:
        results = game_data.get('results', [])
        if not results or results[0].get('rating', 0) == 0:
            raise IndexError

        games = []
        favorited_games = []
        # Get favorites for the current user and check if any of the results are in the favorites list
        favorites = get_favorites(session.get('user_id'))
        for g in results:
            for h in favorites:
                if g.get('name') == h.get('name'):
                    favorited_games.append(g.get('name'))
        # Create a list of games with relevant details, filtering out those with a rating of 0
        games = [
            {
                'name': g.get('name'),
                'released': g.get('released'),
                'rating': g.get('rating'),
                'image': g.get('background_image')
            }
            for g in results if g.get('rating', 0) > 0
        ]

        #print(favorites)  # Debugging line to check the list of favorited games
        #print(favorited_games)  # Debugging line to check the list of favorited game names
        return render_template(
            'game.html', 
            games=games,
            game=name,
            favorite_names=favorited_games)
    except IndexError:
        return render_template('invalid.html', error=f"No results found for '{name}'. Please try again.")

@app.route('/favorites_page')
def favorites_page():
    user_id = session.get('user_id')
    favorites = get_favorites(user_id)

    return render_template('favorites_page.html', favorites=favorites)

@app.route('/process_favorite', methods=['POST'])
def process_favorite():
    # Get the JSON payload from the request
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid payload'}), 400
    
    user_id = session.get('user_id')
    # Extract relevant fields from the JSON payload
    title = data.get('title')
    image_url = data.get('image_url')
    released = data.get('released')
    rating = data.get('rating')
    #print("running")
    # Connect to the SQLite database and insert the favorite game details
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO games (user_id, name, released, rating, image) VALUES (?, ?, ?, ?, ?)", (user_id, title, released, rating, image_url))
    connection.commit()
    connection.close()


    return jsonify({'title': title, 'image_url': image_url, 'released': released, 'rating': rating})

@app.route('/remove_favorite')
def remove_favorite():
    user_id = session.get('user_id')
    title = request.args.get('title')
    deleteRow(user_id, title)
    return favorites_page()  # Return the updated favorites page


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)