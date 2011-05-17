# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from tictac.mainapp.game_rules import test_valid_move

board = ["_","_","_","_","_","_","_","_","_"]

def hello(request):
    return HttpResponse("hello world")

def paint_board(request):
    b0 = board[0]
    b1 = board[1]
    b2 = board[2]
    b3 = board[3]
    b4 = board[4]
    b5 = board[5]
    b6 = board[6]
    b7 = board[7]
    b8 = board[8]
    return render_to_response('board.html', locals())
    
def process_move(request):
    move = request.GET.get('button')
    # todo: might wanna test for exception.. 
    m = int(move)  
    if test_valid_move(board,m) :
       board[m] = "X" # it is a player move
       return HttpResponse("you pressed button "+move)     
    else :
       return HttpResponse("your move "+move+" is invalid")


