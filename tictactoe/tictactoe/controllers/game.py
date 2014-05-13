from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from tictactoe.models import Board
import json

from tictactoe.models import *

def index(request):
    if 'email' in request.session:
        return render_to_response("game.html")
    else:
        return HttpResponseRedirect("new.html")

def new(request):
    if 'form.submitted' in request.GET:
        addy = request.GET['email']
        request.session['email'] = addy
        request.session.save()
        return HttpResponseRedirect("game.html")
    else:
        request.session.clear()
        request.session.save()
        return render_to_response("new.html")

def newgame(request):
    id = request.session['email']
    board = getBoard(id)
    board.newBoard()
    board.printBoard()
    return HttpResponse(board.__json__(), content_type="application/json")

def play(request, place):
    id = request.session['email']
    board = getBoard(id)
    board.addPlay(int(place),1)
    board.computerPlay()
    board.printBoard()
    return HttpResponse(board.__json__(), content_type="application/json")

def cpuplay(request):
    id = request.session['email']
    board = getBoard(id)
    board.computerPlay()
    board.printBoard()
    return HttpResponse(board.__json__(), content_type="application/json")

def returnBoard(request):
    id = request.session['email']
    board = getBoard(id)
    board.printBoard()
    return HttpResponse(board.__json__(), content_type="application/json")

def getBoard(id):
    try:
        board = Board.objects.get(player_id=id)
    except:
        board = Board.objects.create(player_id=id)
    return board
