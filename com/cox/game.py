import random
from com.cox import board

class game(object):
    """
    game class that drives players
    """
    def __init__(self, *args, **kwargs):
        self.board = None
    
    def select_letters(self):
        selection = ''
        choices = ['O','X']
        while not (selection == 'X' or selection == 'O'):
            selection = raw_input('Choose X OR O').upper()
        self.board = board.board(human=selection, computer= choices.remove(selection))
    
    
    def toss(self):
        # coin flip
        if random.randint(0, 1) == 0:
            return 'computer'
        else:
            return 'computer' #change this to human, to make fair game.
