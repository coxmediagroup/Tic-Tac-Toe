import simplejson
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
            return self.board[0][0]
        
        if self.board[0][2] and \
            self.board[0][2] == self.board[1][1] and \
            self.board[1][1] == self.board[2][0]:
            return self.board[0][2]
        
        # Check rows and columns
        for k in range(0, 3):
            # Check row
            if self.board[k][0] and \
                self.board[k][0] == self.board[k][1] and \
                self.board[k][1] == self.board[k][2]:
                return self.board[k][0]
            
            # Check column
            if self.board[0][k] and \
                self.board[0][k] == self.board[1][k] and \
                self.board[1][k] == self.board[2][k]:
                return self.board[0][k]
        return False

    def get_open_moves(self):
        """ Returns all available moves as a list of row, col tuples. """
        openMoves = []
        for i in range(0, 3):
            for k in range(0, 3):
                if not self.board[i][k]:
                    openMoves.append((i, k))
        return openMoves
    
    def check_game_finished(self):
        return self.check_for_winner() or not self.get_open_moves()
    
    def get_json(self):
        if self.check_game_finished():
            winner = self.check_for_winner()
            if winner == "X":
                status = "You Win!"
            elif winner == "O":
                status = "You Lose!"
            else:
                status = "Tie Game!"
        else:
            status = ""
        
        return simplejson.dumps({'board': self.board,
                                 'status': status})