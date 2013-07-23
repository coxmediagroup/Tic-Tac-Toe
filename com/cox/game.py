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
            print('choose X or O')
            selection = input().upper()
        self.board = board.board(human=selection, computer= choices.remove(selection))