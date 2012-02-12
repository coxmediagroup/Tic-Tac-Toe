# We don't need a database, but this will at least hold our runtime classes.

class GameState:
    """ An object representing the current board, as 3 rows of 3 columns.
        Open spaces are an empty string.
        Played spaces are the appropriate letter ("X" or "O") """
    
    def __init__(self):
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
    
    def make_move(self, letter, x, y):
        self.board[y][x] = letter
    
    def check_for_winner(self):
        # Check diagonals first
        if self.board[0][0] and \
            self.board[0][0] == self.board[1][1] and \
            self.board[1][1] == self.board[2][2]:
            return True
        
        if self.board[0][2] and \
            self.board[0][2] == self.board[1][1] and \
            self.board[1][1] == self.board[2][0]:
            return True
        
        # Check rows and columns
        for k in range(0, 3):
            # Check row
            if self.board[k][0] and \
                self.board[k][0] == self.board[k][1] and \
                self.board[k][1] == self.board[k][2]:
                return True
            
            # Check column
            if self.board[0][k] and \
                self.board[0][k] == self.board[1][k] and \
                self.board[1][k] == self.board[2][k]:
                return True
        return False
