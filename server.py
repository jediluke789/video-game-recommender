from flask import Flask, render_template, request
from game import get_requested_game
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/game')
def get_game():
    name = request.args.get('game')
    if not bool(name.strip()):
        return render_template('invalid.html', error="Please enter a game name.")
    game_data = get_requested_game(name)
    try:
        if game_data['results'][0]['rating'] == 0:
            raise IndexError
        return render_template(
            'game.html', 
            game= game_data['results'][0]['name'], 
            name=game_data['results'][0]['name'], 
            released=game_data['results'][0]['released'],
            rating=game_data['results'][0]['rating'])
    except IndexError:
        return render_template('invalid.html', error=f"No results found for '{name}'. Please try again.")

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)