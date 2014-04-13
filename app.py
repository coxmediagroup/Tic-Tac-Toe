from itertools import chain
from uuid import uuid4

from flask import Flask, render_template, request, jsonify, session

from game import Game


COOKIE_GAME_ID = 'tictactoe_game_id'


app = Flask(__name__)
app.secret_key = 'Fdln30_#& H#(#H @_!$*FN#* #_@M'


current_games = {}


@app.route('/')
def index():
    return render_template('index.j2')

@app.route('/start')
def start_game():
    clear_game_session()
    
    new_game_id = uuid4().hex
    current_games[new_game_id] = Game()
    
    session[COOKIE_GAME_ID] = new_game_id
    return json_success()

@app.route('/end')
def end_game():
    clear_game_session()
    return json_success()

@app.route('/move')
def move():
    try:
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        assert x in range(Game.BOARD_SIZE)
        assert y in range(Game.BOARD_SIZE)
    except (KeyError, ValueError, TypeError, AssertionError):
        return json_error('wrong_arguments')

    try:
        game_id = session[COOKIE_GAME_ID]
        game = current_games[game_id]
    except KeyError:
        return json_error('not_initiated', 'The game is not initiated')

    move_success = game.move(x, y)
    if not move_success:
        return json_error('cell_taken', 'Cell already taken')
        
    return json_success()


def clear_game_session():
    old_game_id = session.get(COOKIE_GAME_ID)
    if old_game_id and current_games.get(old_game_id):
        del current_games[old_game_id]


def json_error(code, message=None):
    if not message:
        message = code.capitalize().replace('_', ' ')
    return jsonify({'success': False, 'error': code, 'message': message})

def json_success():
    return jsonify({'success': True})


if __name__ == "__main__":
    app.run(debug=True)