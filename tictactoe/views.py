from django.http import HttpResponse
from django.shortcuts import render_to_response
import tictactoe

def show_game(request):
    ctx = {}
    ctx['b'] = tictactoe.Board()
    request.session['game'] = ctx
    return render_to_response("board.html", ctx)

def make_move(request):
    move = request.GET['selection']
    possible_moves = dict([(board.getMoveName(move), move) for move in board.getValidMoves()])
    move = raw_input("Enter your move (%s): " % (', '.join(sorted(possible_moves))))
    while move not in possible_moves:
        print "Sorry, '%s' is not a valid move. Please try again." % move
        move = raw_input("Enter your move (%s): " % (', '.join(sorted(possible_moves))))
    board.makeMove(possible_moves[move], player)

    return HttpResponse("good")

