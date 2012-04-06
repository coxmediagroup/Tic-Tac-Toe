from django.http import HttpResponse
import json, random, game, gameboard

def newGame(request):
    
    board = gameboard.GameBoard()
    request.session['board'] = board
    response = {
        'success': True,
        'message': 'Game Initiated'
    }
    
    return HttpResponse(json.dumps(response), mimetype="application/json")

def makeMove(request, x, y):
    board = request.session['board']
    result = game.makeMove(board, int(x), int(y))
    if result:
        request.session['board'] = board
        
        status = game.isGameOver(board)
        
        response = {
            'success': True,
            'gameover': status
        }
    else:
        response = {
            'success': False,
            'message': 'Invalid move: spot already taken.'
        }
        
    return HttpResponse(json.dumps(response), mimetype="application/json")

def getMove(request):
    board = request.session['board']
    next_move = game.getMove(board)
    
    if next_move:
        board.makeMove(next_move, game.ID_COMPUTER)
        request.session['board'] = board
        
        status = game.isGameOver(board)
        
    
        response = {
            'success': True,
            'x': next_move[0],
            'y': next_move[1],
            'gameover': status
        }
    else:
        response = {
            'success': False,
            'message': 'No safe place to move. This isn\'t possible!'
        }
    
    # place mark, save in session, and check for win
    return HttpResponse(json.dumps(response), mimetype="application/json")