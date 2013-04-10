from django.shortcuts import render_to_response

def index(request):
    # If we didn't get a board state, or got an invalid board state,
    # then reset the board.
    if "b" in request.GET and len(request.GET["b"]) == 9:
        boardstring = request.GET["b"]
        ai_move = determine_ai_move(boardstring)
        if ai_move:
            boardstring = boardstring[:ai_move] + 'x' + boardstring[ai_move+1:] 
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

def determine_ai_move(board):
    """Determines the AI's move for the given boardstring."""
    moves = []
    for space in range(len(board)):
        if board[space] != '-':
            continue  # skip spaces we can't move to.
        moves.append((ai_priority(space,board),space))
    if len(moves) == 0:
        return 
    moves.sort()
    return moves[0][1]
        

def adjacent_pairs(space):
    """Returns the pairs of spaces adjacent to the given space."""
    pairlist = (
        ((1,2),(3,6),(5,8)),
        ((0,2),(4,7)),
        ((0,1),(4,6),(6,8)),
        ((0,6),(4,5)),
        ((0,8),(1,7),(2,6),(3,5)),
        ((3,4),(2,8)),
        ((0,3),(2,4),(7,8)),
        ((1,4),(6,8)),
        ((0,4),(2,5),(6,7)),
    )
    return pairlist[space]

def ai_priority(space,b):
    """Returns the AI priority of the given space, given a boardstring b.
       Lower numbers mean higher priority."""
    adj = adjacent_pairs(space)
    myfork_threat = 0
    theirfork_threat = 0
    for pair in adj:
        if b[pair[0]] == b[pair[1]] == 'x':
            return 1  # victory
        if b[pair[0]] == b[pair[1]] == 'o':
            return 2  # must take this space to block defeat
        if ((b[pair[0]] == 'x' and b[pair[1]] == '-')
         or (b[pair[0]] == '-' and b[pair[1]] == 'x')):
            myfork_threat += 1
        if ((b[pair[0]] == 'o' and b[pair[1]] == '-')
         or (b[pair[0]] == '-' and b[pair[1]] == 'o')):
            theirfork_threat += 1
    if myfork_threat > 1:
        return 3 # grab a fork
    if theirfork_threat > 1:
        return 4 # block enemy fork
    if len(adj) == 4:
        return 5 # grab center space
    if ((space == 1 and b[8] == 'o') or
        (space == 8 and b[1] == 'o') or
        (space == 2 and b[6] == 'o') or
        (space == 6 and b[2] == 'o')):
        return 6 # grab corner if opposite corner is taken
    return 10 - len(adj) # finally, corners are worth more than sides
    

    
