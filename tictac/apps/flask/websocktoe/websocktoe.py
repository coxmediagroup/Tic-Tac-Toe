#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from gevent import monkey
monkey.patch_all()

import os
import time
import random
import traceback

from flask import Flask, session
from simplekv.memory import DictStore
from flask_kvsession import KVSessionExtension
from flask.ext.socketio import SocketIO, join_room, leave_room

from apps.coxtactoe.ai import MinMaxPlayer
from apps.coxtactoe.exceptions import InvalidMoveError

from apps.flask.websocktoe.game_json_encoder import WebSockToeJSONEncoder
from apps.flask.websocktoe.utils import get_game, marvmin_msg_generator
from apps.flask.websocktoe import const as C

from threading import Thread


__docformat__ = 'restructuredtext en'

# Init key/value store.
kvstore = DictStore()

# Flask. It's what's configured.
app = Flask(__name__)
app.json_encoder = WebSockToeJSONEncoder  # for game state encoding
app.config.from_object('tictac.settings.flask.base')
settings_module = os.environ.get('FLASK_SETTINGS_MODULE')
app.config.from_object(settings_module)
kvsession_ext = KVSessionExtension(kvstore, app)  # Replace app session handling
log = app.logger

# Yay, WebSockets!
socketio = SocketIO(app)

thread = None


####   Event Dispatchers   ####################################################

def emit_msg(msg, game_id=None, event='msg'):
    """Sends game message event to client using socket.io"""
    socketio.emit(event, {'msg': msg}, room=game_id)


def emit_game_state(game, event='state'):
    """Sends game state event to client using socket.io"""
    socketio.emit(event, game, room=game.id)


def emit_error(e, trace='', game_id=None):
    """Sends game exception info to client using socket.io"""
    error_info = {'msg': str(e),
                  'traceback': '<span class="error">%s</span>' % trace}
    socketio.emit('error', error_info, room=game_id)


def async_background_thread():
    """Runs periodic tasks from separate server thread

    Tasks:
        - Sends random AI message to client
        - Removes expired sessions.
    """
    marvmin_msgs = marvmin_msg_generator()
    try:
        while True:
            # :meth:`gevent.monkey.patch_all` makes call :meth:`gevent.sleep`
            time.sleep(C.THREAD_SLEEP_TIME)
            # Make MarvMin's melancholy metal mouth move!
            emit_msg(marvmin_msgs.next(), event='ai_msg')
            # Remove expired sessions
            kvsession_ext.cleanup_sessions(app=app)
    except Exception as e:
        emit_error(e, traceback.format_exc())



####   WS Event Listeners   ###################################################

@socketio.on('connect')
def connect():
    """Sends confirmation msg on socketio connect."""
    log.debug('Client connected')
    emit_msg('Connected')


@socketio.on('disconnect')
def disconnect():
    """Sends confirmation msg on SocketIO disconnect."""
    log.debug('Client disconnected')
    emit_msg('Disconnected')


@socketio.on('join')
def join(data):
    """Handles joining a game with the provided ``game_id``"""
    log.debug(session)
    game_id = data.get('game_id', None)
    game = get_game(game_id)
    if game is None:
        emit_error("Unable to get game id %s" % game_id)
        return

    join_room(game_id)
    msg = 'Joined game %s' % game_id
    session['game'] = game

    emit_game_state(game)
    emit_msg(msg, game_id)
    emit_msg(random.choice(C.MARVMIN_GREETS), game_id, event='ai_msg')


@socketio.on('leave')
def leave(data):
    game_id = data.get('game_id', None)
    log.debug('Player left game ' + game_id)
    emit_msg('Leaving game %s' % game_id, game_id)
    leave_room(game_id)


@socketio.on('move')
def move(msg):
    square = int(msg['square'])
    game = session['game']
    player = game.player
    opponent = player.opponent

    if game is None or game.over:
        return
    try:
        # Player's move
        game.board.place(player, square)
        # If player didn't win with move, let AI move
        if not game.over:
            ai = MinMaxPlayer(opponent, game.board)
            ai_move = ai.get_best_move()
            game.board.place(opponent, ai_move)
        game.save()
    except InvalidMoveError as e:
        emit_error(e, traceback.format_exc(), game_id=game.id)
        return
    except Exception as e:
        emit_error(e, traceback.format_exc(), game_id=game.id)
        raise

    if game.over:
        if game.winner is None:
            msg = random.choice(C.MARVMIN_TIE_MSGS)
        if game.winner == player.opponent:
            msg = random.choice(C.MARVMIN_WIN_MSGS)
        emit_msg(msg, game_id=game.id, event='ai_msg')
    emit_game_state(game)



if __name__ == '__main__':
    # Start background thread for MarvMin's motor mouth
    if thread is None:
        thread = Thread(target=async_background_thread)
        thread.daemon = True
        thread.start()
    # Start Flask app
    socketio.run(app, host=C.HOST, port=C.PORT)



