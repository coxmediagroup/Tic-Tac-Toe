# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
import tictactoe.tictactoe as tictactoe

def home(request):

    da_board = tictactoe.drawBoard(board = ['']*9)
    return render_to_response('play/home.html',locals())