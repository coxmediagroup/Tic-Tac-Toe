# Create your views here.
from datetime import datetime
import random

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.utils import simplejson

from models import Player, Game

END_WIN = 0
END_LOSS = 1
END_DRAW = 2

random.seed(42)

def home(request):
    return render_to_response('home.html',
            context_instance=RequestContext(request))

def login(request):
    playerName = request.POST.get("playerName")
    if not playerName:
        return None # TODO: Throw an exception

    player = Player.objects.get_or_create(name=playerName)[0]
    player.lastLogin = datetime.now()
    game = __setupNewGame(player)
    player.save()
    game.save()
    request.session['player'] = player
    request.session['game'] = game
    return HttpResponseRedirect('/game/')

def newGameJAX(request):
    if 'player' not in request.session:
        return HttpResponseRedirect('/home/')

    player = request.session['player']
    game = __setupNewGame(player)
    game.save()
    request.session['game'] = game
    response = { 'board': game.board, 'ended': False }
    serialized = simplejson.dumps(response)
    return HttpResponse(serialized, mimetype="application/json")

def game(request):
    if 'player' not in request.session:
        return HttpResponseRedirect('/home/')
    if 'game' not in request.session:
        return HttpResponseRedirect('/home/')

    request, game, player, endState = __gameMove(request)

    return render_to_response('game.html',
            {'game': game, 'ended': game.ended},
            context_instance=RequestContext(request))

def gameJAX(request):
    # TODO: Check for 'player' and 'game' in the session,
    # and return errors to be handled by AJAX caller.
    request, game, player, endState = __gameMove(request)
    response = { 'board': game.board,
                 'ended': game.ended,
                 'endState': endState,
                 'wins': player.wins,
                 'losses': player.losses,
                 'draws': player.draws}
    serialized = simplejson.dumps(response)
    return HttpResponse(serialized, mimetype="application/json")

def __setupNewGame(player):
    game = Game(player1=player)

    # Randomize whether computer starts, or player
    if random.randint(1,2) == 1:
        game.nextTurn()

    return game

def __gameMove(request):
    game = request.session['game']
    player = request.session['player']
    player.lastActive = datetime.now()

    endState = None
    if not game.ended and request.method == 'POST':
        index = int(request.POST['gridIndex'])
        playerChar = game.O if player == game.player1 else game.X
        otherPlayerChar = game.X if playerChar == game.O else game.O

        game.playerTurn(playerChar, index)

        if game.checkWinner(playerChar):
            game.winner = player
            game.ended = True
            player.wins += 1
            endState = END_WIN

        if game.nextTurn(otherPlayerChar):
            game.winner = game.player2
            game.ended = True
            player.losses += 1
            endState = END_LOSS

        if not game.ended and game.turn >= 9:
            game.ended = True
            player.draws += 1
            endState = END_DRAW

        game.save()
        request.session['game'] = game

    player.save()
    request.session['player'] = player
    return request, game, player, endState


