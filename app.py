#!/usr/bin/env python
import argparse

from flask import Flask, render_template, session, jsonify

import game

app = Flask(__name__)
app.secret_key = 'ox\xc7o`\x14g0\xe52\x003,\xd6Y\x9c\x12\xca\xdfHk\xfe~\xe5'


@app.route('/')
def index():
    return render_template('main.html', **dict(host=app.config['HOST'], port=app.config['PORT']))


@app.route('/player_first/')
def player_first():
    return jsonify(dict())


@app.route('/ai_first/', methods=['GET'])
def ai_first():
    cell = game.ai_move_one()
    session['game_state'] = dict(
        ai_cells=[cell],
        player_cells=[],
    )
    data = dict(
        mark_cell=cell,
    )
    return jsonify(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tic Tac Toe: The Crucible')
    parser.add_argument('--debug', dest='debug', action='store_true', help='run app in debug mode')
    parser.add_argument('--host', dest='host', default='127.0.0.1', help='host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', dest='port', type=int, default=5000, help='port to bind to (default: 5000)')
    args = parser.parse_args()
    app.config['HOST'] = args.host
    app.config['PORT'] = args.port
    app.run(host=args.host, port=args.port, debug=args.debug)
