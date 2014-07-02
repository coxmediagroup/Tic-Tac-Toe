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

def get_game(id):
    try:
        game = ttt.Game(id=id)
    except InvalidGameError as e:
        emit('server msg',
             {'data': str(e),
              'error': True,
              'count': session['receive_count']},
             callback=handle_join_error)
        return None
    else:
        return game

@socketio.on('join')
def join(msg):
    session['receive_count'] = session.get('receive_count', 0) + 1
    game_id = msg['game_id']

    game = get_game(game_id)
    if game is not None:
        join_room(game_id)
        log.debug('Player joined game ' + game_id)
        emit('server msg',
             {'data': 'Joined game ' + game_id,
              'game_id': game_id,
              'board': game.board.json,
              'xo_choice': repr(game.board.turn),
              'count': session['receive_count']},
             room=game_id)


@socketio.on('leave')
def leave(msg):
    session['receive_count'] = session.get('receive_count', 0) + 1
    game_id = msg['game_id']

    log.debug('Player left game ' + game_id)
    emit('server msg',
         {'data': 'Leaving game ' + game_id, 'count': session['receive_count']},
         room=game_id)
    leave_room(game_id)


@socketio.on('move')
def move(msg):
    session['receive_count'] = session.get('receive_count', 0) + 1
    game_id = msg['game_id']
    player = ttt.Marker(msg['player'])
    opponent = player.opponent
    square = int(msg['square'])

    # TODO: Refactor this mess
    game = get_game(game_id)
    if game is not None:
        game.board.place(player, square)
        emit('server msg', {'data': game.board.json}, room=game_id)
        log.debug(game.board.json)
        ai = MinMaxPlayer(opponent, game.board)
        ai_move = ai.get_best_move()
        emit('server msg', {'data': 'AI chose sq %s' % ai_move}, room=game_id)
        log.debug('AI chose square %s' % ai_move)
        game.board.place(opponent, ai_move)
        game.save()
        log.debug('{0} in game {1} moved to square {2}'
                  .format(player, game_id, square))
        emit('server msg',
             {'data': 'AI played at square %s' % ai_move,
              'board': game.board.json,
              'count': session['receive_count']},
             room=game_id)
        if game.over:
            emit('server msg',
                 {'data': 'Game over. Winner: %s' % game.winner,
                  'winner': game.winner,
                  'count': session['receive_count']},
                 room=game_id)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8001)
