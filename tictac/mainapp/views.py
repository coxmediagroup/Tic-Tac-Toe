# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

def hello(request):
    return HttpResponse("hello world")

def paint_board(request):
    board = [[0,1,2],[3,4,5],[6,7,8]]
    b0 = board[0][0]
    b1 = board[0][1]
    b2 = board[0][2]
    b3 = board[1][0]
    b4 = board[1][1]
    b5 = board[1][2]
    b6 = board[2][0]
    b7 = board[2][1]
    b8 = board[2][2]
    return render_to_response('board.html', locals())
    
def process_move(request):
    move = request.GET.get('button')
    return HttpResponse("you pressed button "+move)
