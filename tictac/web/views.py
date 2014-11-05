from flask import request, session, render_template, \
    abort, flash, redirect, url_for

import random

from tictac import bot
from tictac.board import TTTGameBoard
from tictac.web import app

# intro page
@app.route("/", methods=['GET'])
def index():
    # check to see if they are already playing a game;  if so, direct
    # them to game page.  if they are not already playing a game, ask
    # to start up a new one.
    return render_template('index.html')


@app.route("/game", methods=['GET','POST'])
def game():
    # if the game is over, let the player know and disable any non-reset input
    # if there is no game ongoing, display the start up game dialog
    # if it's the player's turn, display the move form
    # if the player selects a move, make it, then let the bot play
    # if reset is selected, clear the session and direct to index
    
    #if this is a bot vs bot or bot v random game, send them there
    if 'gametype' in session and session['gametype'] in ['2','3']:
        #for bot v random matches, randomize the bot start
        session['player'] = random.choice(['x','o'])
        return redirect(url_for('watch_game'))

    if request.method == 'POST':
        # reset the game and restart
        if 'reset' in request.form:
            session.clear()
            return redirect(url_for('game'))
        # start a new game
        elif 'gametype' in request.form:
            session['gametype'] = request.form['gametype']
            session['player'] = 'x' if request.form['firstplayer'] == 'Y' else 'o'
            session['game'] = TTTGameBoard()
            #if this is a bot vs bot or bot v random game, send them there
            if session['gametype'] in ['2','3']:
                return redirect(url_for('watch_game'))
            #if the player is O, the bot gets a move before they see the board
            if session['player'] == 'o' and session['gametype'] == '1':
                session['game'] = bot.get_next_gamestate(session['game'])
                flash("Bot (playing as {}) moved in square {}.".format(
                    'o' if session['player'] == 'x' else 'x',
                    session['game'].last_move
                    )
                )
        #accept a move
        #game in session check to handle back button resubmits
        elif 'square' in request.form \
                and 'game' in session \
                and session['game'].winner is None \
                and session['game'].depth < 9:

            #check for invalid moves
            if int(request.form['square']) not in session['game'].get_legal_moves():
                flash("That move was invalid.  Please choose another.")
                return redirect(url_for('game'))

            #make the player move
            session['game'] = session['game'].apply_move(
                    int(request.form['square']))

            #let the bot go, if it's their turn
            if session['gametype'] == '1' \
            and session['game'].active_player != session['player']:
                session['game'] = bot.get_next_gamestate(session['game'])
                flash("Bot (playing as {}) moved in square {}.".format(
                    'o' if session['player'] == 'x' else 'x',
                    session['game'].last_move
                    )
                )
        elif 'game' not in session:
            return redirect(url_for('game'))

    #end of POST code

    #if the game is won / over
    #stop any further moves and notify the person
    if 'game' in session and (
            session['game'].winner is not None \
            or session['game'].depth == 9):
        flash("This game is over! {} won.".format(
            session['game'].winner.upper() if session['game'].winner is not None \
                else 'Nobody'
            ))
        session['game'].board = session['game'].board.replace('-',' ')
        
    return render_template("game.html", 
                game=session.get('game',None), 
                player=session.get('player','x')
            )


@app.route("/game/watch", methods=['GET','POST'])
def watch_game():
    # used to display each move in a bot v bot or bot v random game

    # if a reset call is made, honor it
    if request.method == "POST" and 'reset' in request.form:
        session.clear()
        return redirect(url_for('game'))

    # if there is no game, or if the gametype == 1, redirect to /game
    if 'game' not in session \
        or 'gametype' not in session \
        or session['gametype'] == '1':
            return redirect(url_for('game'))

    final = False
    #if there is a game and it is finished, let them know
    if session['game'].winner is not None or session['game'].depth == 9:
        final = True
        flash("This game is over! {} won.".format(
            session['game'].winner.upper() if session['game'].winner is not None \
                else 'Nobody'
            ))

    # if the game is not over, make the next bot move
    else:
        #if it's bot v random and it's random's turn
        if session['gametype'] == '3' and session['player'] != session['game'].active_player:
            #apply a random legal move
            legal_moves = session['game'].get_legal_moves()
            session['game'] = session['game'].apply_move(random.choice(legal_moves))
            flash("Crazy Bot (playing as {}) moved in square {}.".format(
                'o' if session['player'] == 'x' else 'x',
                session['game'].last_move
                ))
        else:
            session['game'] = bot.get_next_gamestate(session['game'])
            flash("Bot (playing as {}) moved in square {}.".format(
                'o' if session['game'].active_player == 'x' else 'x',
                session['game'].last_move
                ))

    return render_template("watchgame.html", game=session['game'], final=final)
