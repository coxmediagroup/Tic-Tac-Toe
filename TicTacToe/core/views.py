"""
Copyright (C) 2014 Ryan Hansen.  All rights reserved.
This source code (including its associated software) is owned by Ryan Hansen and
is protected by United States and international intellectual property law, including copyright laws, patent laws,
and treaty provisions.
"""

from django.shortcuts import render, Http404, HttpResponse

import json
import random

from time import sleep

from core.const import WIN_VECTORS
from core.game import Game


def index(request):
    return render(request, 'index.html')

def standard(request, **kwargs):
    """
    The "standard" unwinnable game control.
    """
    # Get the move from the GET args, if any
    move = kwargs.get('move', None)
    if move:
        try:
            # Start the game and set initialize some useful variables
            g = Game()
            over = False
            result = {'result': ''}
            context = dict()
            # Take the position indicated by <move>
            g.take('human', int(move))
            if len(g.available()) != 0:
                # There are still moves available, so just make it feel like the computer is thinking a bit.
                # Response is otherwise pretty much instantaneous and doesn't "feel" very real.
                sleep(2)
                # Normally, I would expect this next operation to be necessary.  Since there is no actual session being
                # started, any game state would be lost when the request completes so any subsequent requests would
                # have no memory of what moves had previously been made.  It appears, however, that the Django runserver
                # preserves the game state between requests, so this isn't necessary if using the runserver.  In the
                # real world, this would take all the moves that have been made so far, which are submitted from the UI,
                # and reconstruct the game state from them.
                # x = request.GET.get('x', None)
                # if x:
                #     g.x = [int(i) for i in x.strip(',').split(',')]
                # o = request.GET.get('o', None)
                # if o:
                #     g.o = [int(i) for i in o.strip(',').split(',')]
                if 4 not in g.o and 4 not in g.x:
                    # Take the center position first, if available (avoid unnecessary processing of minimax)
                    take = 4
                elif g.o[0] == 4 and len(g.x) == 0:
                    # If the opponent takes center first, take the first corner (again, avoiding minimax)
                    take = 0
                else:
                    # If either the machine or the human has a winnable move to make, take appropriate action
                    # (i.e. win or block as necessary--still avoiding minimax to save overhead)
                    win = g.winnable('machine')
                    block = g.winnable('human')
                    if win:
                        take = win
                    elif block:
                        take = block
                    else:
                        # Now let minimax go to work to find the best move.
                        take = g.eval_game('machine')
                g.take('machine', take)
                winner = g.winner('machine')
                # If the machine has won, set game over and the winning vector for return to UI
                if winner:
                    over = True
                    result = {'result': list(winner)}
            else:
                take = 9999  # No other moves are taken
                over = True
                result = {'result': 'draw'}
            if over:
                # The game is over, so reset the game--this actually doesn't seem to work with the runserver though for
                # some reason.  You actually have to stop and restart the runserver to reset the game.  Not sure why.
                g.reset()
            # Set up the response dictionary and resturn as JSON for handling by the UI
            context['move'] = take
            context['over'] = over
            context['result'] = result
            return HttpResponse(json.dumps(context), content_type="application/json")
        except Exception, ex:
            raise Http404
    return render(request, 'standard.html')


def jerk(request, **kwargs):
    """
    The Jerk Computer game.  This is the opponent that accomplishes exactly what the instructions say--never lose--but
    he's kind of a jerk about it.  He doesn't follow the official tic-tac-toe rules (it's not explicitly required by
    the instructions).
    """
    move = kwargs.get('move', None)
    if move:
        winners = []
        sleep(1) # Again, just make it feel like a bit of thinking, just for "realism" of the game play.
        for v in WIN_VECTORS:
            # Iterate over the possible wins.  Store all vectors that do not include the human's move.
            if int(move) not in v:
                winners.append(list(v))
        # Just to make it a bit more interesting, return a randomly selected win vector from the matches so it's not
        # the same one every time you play.
        winner = winners[random.randint(0, len(winners) - 1)]
        context = dict(
            winner=winner
        )
        return HttpResponse(json.dumps(context), content_type="application/json")
    return render(request, 'jerk.html')


def nsa(request, **kwargs):
    """
    The NSA game.  They're always listening...

    Basically, the "NSA" listens to every event, so even a hover by the human triggers a move by the NSA.  With each
    move, the occupied positions are sent to the view to determine when there is a win.  Only NSA moves are recorded, so
    naturally, the human can't win against the NSA.  (Just like life, man)
    """
    move = kwargs.get('move', None)
    if move:
        try:
            g = Game()
            over = False
            result = {'result': ''}
            context = dict()
            g.take('machine', int(move))
            winner = g.winner('machine')
            if winner:
                over = True
                result = {'result': list(winner)}
            context['move'] = 999
            context['over'] = over
            context['result'] = result
            return HttpResponse(json.dumps(context), content_type="application/json")
        except:
            raise Http404
    return render(request, 'nsa.html')