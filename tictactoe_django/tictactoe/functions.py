
def reset_gamestate(request):
    request.session['gamestate'] = GameState()
    make_ai_move(request.session['gamestate'])

def make_player_move(gamestate, playermove):
    """ Carries out Player action on gamestate.
        playermove is a string in the form of rXcY where X and Y are Row Col. """
    row = int(playermove[1])
    col = int(playermove[3])
    
    gamestate.board[row][col] = "O"

def make_ai_move(gamestate):
    """ Acts as AI to choose a move based on the current gamestate. """



from models import *