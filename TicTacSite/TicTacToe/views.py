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
    row = []
    for i in range(0,9):
        # determine what the board would look like if the player moved here.
        movestring = boardstring[:i] + 'o' + boardstring[i+1:]
        row.append([boardstring[i],movestring])
        if i % 3 == 2:
            board.append(row)
            row = []
    
    return render_to_response('tictactoe.html', {'board': board})
