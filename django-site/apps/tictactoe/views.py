from django.http import HttpResponse
import json, random, game, board

ID_PLAYER = 1
ID_COMPUTER = 2

def newgame(request):
    request.session['board'] = board.GameBoard(3)
    response = {
        'success': True
    }
    
    return HttpResponse(json.dumps(response), mimetype="application/json")

def makemove(request, x, y):
    board = request.session['board']
    result = game.makemove(board, int(x), int(y))
    if result:
        request.session['board'] = board
        
        response = {
            'success': True,
            'win': result.win
        }
        if result.win:
            response['winner'] = ID_PLAYER
    else:
        response = {
            'success': False,
            'message': 'Invalid move: spot already taken.'
        }
        
    return HttpResponse(json.dumps(response), mimetype="application/json")

def getmove(request):
    board = request.session['board']
    result = game.getmove(board)
    
    if result:
        board.plot((result.x, result.y), ID_COMPUTER)
        request.session['board'] = board
        
        win = board.checkforwin(ID_COMPUTER)
    
        response = {
            'success': True,
            'x': result.x,
            'y': result.y,
            'win': win
        }
        if win:
            response['winner'] = ID_COMPUTER
    else:
        response = {
            'success': False,
            'message': 'Tie!'
        }
    
    # place mark, save in session, and check for win
    return HttpResponse(json.dumps(response), mimetype="application/json")