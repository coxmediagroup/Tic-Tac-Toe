from django.shortcuts import render_to_response

def index(request):
    # If we didn't get a board state, or got an invalid board state,
    # then reset the board.
    if "b" in request.GET and len(request.GET["b"]) == 9:
        boardstring = request.GET["b"]
    else:
        boardstring = "---------"

    # Divide the boardstring up into a proper 3x3 tic-tac-toe board.
    board = []
    board.append(boardstring[:3])
    board.append(boardstring[3:6])
    board.append(boardstring[6:9])
    
    return render_to_response('tictactoe.html', {'board': board})
