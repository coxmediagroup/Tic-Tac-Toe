from django.shortcuts import render_to_response

def index(request):
    output = ""
    title = ""
    game_over = 0
    
    # If we didn't get a board state, or got an invalid board state,
    # then reset the board.
    if "b" in request.GET and len(request.GET["b"]) == 9 and len(request.GET["b"].strip('ox-')) == 0:
        boardstring = request.GET["b"]
        if player_won(boardstring):
            output = "You won."
            title = "You probably cheated."
            game_over = 1
        else:
            ai_choice = determine_ai_move(boardstring)
            if ai_choice is not None:
                ai_move = ai_choice[1]
                boardstring = boardstring[:ai_move] + 'x' + boardstring[ai_move+1:]
                if ai_choice[0] == 1: # a priority 1 move means we won
                    output = "The computer has won."
                    game_over = 1
        if game_over != 1 and '-' not in boardstring:
            output = "It's a draw."
            title = "A strange game.  The only winning move is not to play."
            game_over = 1
    else:
        boardstring = "---------"
        output = "Click on a space to start."
        title = "Shall we play a game?"

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
    return render_to_response('tictactoe.html', {'board': board, 'output_text':output, 'game_over':game_over, 'title':title})

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
    return moves[0]
        

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
    valid_distraction = 0
    for pair in adj:
        if b[pair[0]] == b[pair[1]] == 'x':
            return 1  # victory
        if b[pair[0]] == b[pair[1]] == 'o':
            return 2  # must take this space to block defeat
        if b[pair[0]] == 'x' and b[pair[1]] == '-':
            myfork_threat += 1
            if nonthreatening_space(pair[1],b):
                valid_distraction = 1
        elif b[pair[0]] == '-' and b[pair[1]] == 'x':
            myfork_threat += 1
            if nonthreatening_space(pair[0],b):
                valid_distraction = 1
        if ((b[pair[0]] == 'o' and b[pair[1]] == '-')
         or (b[pair[0]] == '-' and b[pair[1]] == 'o')):
            theirfork_threat += 1
    if myfork_threat > 1:
        return 3 # grab a fork
    if valid_distraction > 0:
        return 4
    if theirfork_threat > 1:
        return 5 # block enemy fork
    if len(adj) == 4:
        return 6 # grab center space
    if ((space == 0 and b[8] == 'o') or
        (space == 8 and b[0] == 'o') or
        (space == 2 and b[6] == 'o') or
        (space == 6 and b[2] == 'o')):
        return 7 # grab corner if opposite corner is taken
    return 11 - len(adj) # finally, corners are worth more than sides
    

def nonthreatening_space(space,b):
    """Determines if an enemy wouldn't threaten us by taking a specific space;
    that is, returns true if it wouldn't win or make a fork for the enemy.
    This lets us know that we can distract the enemy by threatening that space ourselves."""
    adj = adjacent_pairs(space)
    fork_threat = 0
    for pair in adj:
        if b[pair[0]] == b[pair[1]] == 'o':
            return False
        if ((b[pair[0]] == 'o' and b[pair[1]] == '-')
         or (b[pair[0]] == '-' and b[pair[1]] == 'o')):
            fork_threat += 1
    if fork_threat > 1:
        return False
    return True

def player_won(b):
    """Checks if the player has won.  Hopefully this will never be necessary,
    but it's included for completeness (and in case the player cheats.)
    We don't have to check if the AI has won here,
    since it already does that when it calculates its move."""
    lines = (
        (0,1,2),
        (3,4,5),
        (6,7,8),
        (0,3,6),
        (1,4,7),
        (2,5,8),
        (0,4,8),
        (2,4,6),
    )

    for line in lines:
        if b[line[0]] == b[line[1]] == b[line[2]] == 'o':
            return True
    return False
