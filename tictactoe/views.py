from django.http import HttpResponse
from django.shortcuts import render_to_response
import tictactoe

def show_game(request):
    ctx =[]
    return render_to_response("board.html", ctx)

