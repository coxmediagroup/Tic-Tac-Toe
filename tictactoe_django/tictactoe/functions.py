
humanLetter = "X"
aiLetter = "O"

def reset_gamestate(request):
    request.session['gamestate'] = GameState()

def make_player_move(gamestate, playermove):
    """ Carries out Player action on gamestate.
        playermove is a string in the form of rXcY where X and Y are Row Col. """
    row = int(playermove[1])
    col = int(playermove[3])
    
    if gamestate.check_game_finished():
        return False
    
    if not gamestate.board[row][col]:
        gamestate.board[row][col] = humanLetter
        return True
    return False

def make_ai_move(gamestate):
    """ Acts as AI to choose a move based on the current gamestate. """
    print "AI"
    board = gamestate.board
    ## Handle first move
    if (board[0].count(humanLetter) + board[1].count(humanLetter)
        + board[2].count(humanLetter)) <= 1:
        if not board[1][1]:
            board[1][1] = aiLetter
        else:
            board[0][2] = aiLetter
        return
    
    ## Look for any moves where we win, and collect open moves
    openMoves = gamestate.get_open_moves()
    for i, k in openMoves:
        board[i][k] = aiLetter
        if gamestate.check_for_winner():
            return
        else:
            board[i][k] = ""
    
    ## If there aren't any open moves, just leave
    if not openMoves:
        return

    ## Look for any moves that need blocking
    for i, k in openMoves:
        board[i][k] = humanLetter
        if gamestate.check_for_winner():
            board[i][k] = aiLetter
            return
        else:
            board[i][k] = ""
    
    ## Pick a move of our own
    # Check corners first
    if not board[0][0]:
        board[0][0] = aiLetter
        return
    if not board[2][2]:
        board[2][2] = aiLetter
        return
    if not board[2][0]:
        board[2][0] = aiLetter
        return
    board[openMoves[0][0]][openMoves[0][1]] = aiLetter
    


from models import *