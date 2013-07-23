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