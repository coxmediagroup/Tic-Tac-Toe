#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route('/', defaults={'first_player': None}, methods=['GET', 'POST'])
@app.route('/<first_player>', methods=['GET', 'POST'])
def tic_tac_toe(first_player=None):
    if request.method == 'POST':
        return request.form['layout']
    return render_template('tictactoe.html', layout=[[" ", " ", " "],
                                                     [" ", " ", " "],
                                                     [" ", " ", " "]])

if __name__ == '__main__':
    app.debug = True
    app.run()
