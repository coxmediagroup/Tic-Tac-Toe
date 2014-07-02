from gevent import monkey
monkey.patch_all()

import time
import random
from threading import Thread

from flask import Flask, session, request, render_template
from flask.ext.socketio import SocketIO, emit, join_room, leave_room

from tictac.settings import dev as settings
from coxtactoe import tictactoe as ttt
from coxtactoe.ai import MinMaxPlayer
from coxtactoe.exceptions import InvalidGameError, InvalidMoveError
from coxtactoe import const as C

import logging as log
log.basicConfig(level=log.DEBUG)


# MarvMin the Paranoid Android
# See http://en.wikipedia.org/wiki/Marvin_the_Paranoid_Android
MARVIN_QUOTES = [
    "Wrong. You see?",
    "Any ideas? I have a million ideas. They all point to certain death.",
    "I could calculate your chance of survival, but you won't like it.",
    "I'd give you advice, but you wouldn't listen. No one ever does.",
    "Here I am, brain the size of a planet and they ask me to play Tic-Tac-Toe.",
    "I think you ought to know, I'm feeling very depressed.",
    "I've got this terrible pain in all the diodes down my left side."]

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)
thread = None



def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)  # Uses gevent.sleep()
        count += 1
        socketio.emit('server taunt',
                      {'data': random.choice(MARVIN_QUOTES), 'count': count},
                      namespace='')

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('index.html')

@socketio.on('connect')
def connect():
    log.debug('Client connected')
    emit('server msg', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def disconnect():
    log.debug('Client disconnected')
    emit('server msg', {'data': 'Connected', 'count': 0})

def handle_join_error():
    pass

@socketio.on('join')
def join(msg):
    game_id = msg['game_id']
    session['receive_count'] = session.get('receive_count', 0) + 1
    try:
        game = ttt.Game(id=game_id)
    except InvalidGameError as e:
        emit('server msg', {'data': str(e), 'error': True,
                            'count': session['receive_count']},
             callback=handle_join_error)
    else:
        join_room(game_id)
        log.debug('Player joined game ' + game_id)
        emit('server msg',
             {'data': 'Joined game ' + game_id,
              'board': game.board.json,
              'turn': repr(game.board.turn),
              'count': session['receive_count']},
             room=game_id)


@socketio.on('leave')
def leave(msg):
    game_id = msg['game_id']
    leave_room(game_id)
    # TODO: Call ttt API
    log.debug('Player left game ' + game_id)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('server msg',
         {'data': 'Left game ' + game_id,
          'player': 'x',  # TODO: Get player from game.board.turn
          'count': session['receive_count']},
         room=game_id)


@socketio.on('move')
def move(msg):
    game_id = msg['game_id']
    player = msg['player']
    square = msg['move']
    session['receive_count'] = session.get('receive_count', 0) + 1
    # TODO: Call ttt API
    log.debug('{0} in game {1} moved to square {3}'
              .format(player, game_id, square))
    emit('server msg',
         {'data': msg['data'],
          'turn': 'x',  # TODO: Get turn from game.board.turn
          'count': session['receive_count']},
         room=game_id)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8001)
