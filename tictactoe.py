#!/usr/bin/env python
from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

from game import Board
import ai

import json

@app.route('/', defaults={'first_player': None}, methods=['GET', 'POST'])
@app.route('/<first_player>', methods=['GET', 'POST'])
def tic_tac_toe(first_player=None):
    if request.method == 'POST':
        return request.form['layout']
    return render_template('tictactoe.html', layout=[[" ", " ", " "],
                                                     [" ", " ", " "],
                                                     [" ", " ", " "]])

@app.route('/is-draw')
def is_draw():
    layout = request.args.get('layout')
    layout = json.loads(layout)
    board = Board(setup=layout)
    return str(board.is_draw())

@app.route('/is-win')
def is_win():
    layout = request.args.get('layout')
    layout = json.loads(layout)
    board = Board(setup=layout)
    return str(board.is_win())

@app.route('/ai-move')
def ai_move():
    try:
        layout = request.args.get('layout')
        layout = json.loads(layout)
        board = Board(setup=layout)
        ai.move(board)
        layout = board.board()
        layout = json.dumps(layout)
        return layout
    except Exception:
        import traceback
        print(traceback.format_exc())

if __name__ == '__main__':
    app.run(debug=True)
