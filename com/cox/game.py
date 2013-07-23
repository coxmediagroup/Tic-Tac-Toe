from com.cox import board

class game(object):
    """
    game class that drives players
    """
    def __init__(self, *args, **kwargs):
        self.board = None
    
    def select_letters(self):
        selection = input("choose your letter: O or X ?").upper()
        choices = ['O','X']
        if selection in choices:
            self.board = board.board(human=selection, computer= choices.remove(selection))