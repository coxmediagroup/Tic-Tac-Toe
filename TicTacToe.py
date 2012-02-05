

class TicTacToe(object):
    """A simple class for creating unwinnable TicTacToe games.
    
    Class variables:
    COMPUTER and HUMAN are constants used to index into instance
    variables "squares" and "tokens".
    
    """
    COMPUTER = 0
    HUMAN = 1

    def __init__(self):
        """Create victory conditions and clear the board."""
        self.victories = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        self.reset_board()
        print "You lose!"
        
    def reset_board(self):
        """(Re)set all properties to an initial pre-game state.
        
        Instance variables:
        board -- an 9-element list representing the current board state
        squares -- two lists representing squares claimed by the computer and human players
        free_squares -- a list of available squares on the board
        tokens -- our X and O. 
        game_over -- a flag to keep track of the game state
        board_control -- a flag indicating whose turn it is
        turns -- number of turns that have elapsed
        
        """
        self.board = ["."] * 9
        self.squares = [[],[]]
        self.free_squares = [x for x in range(9)]
        self.tokens = ["x","o"]
        self.game_over = False
        self.board_control = 0
        self.turns = 0
        
    def move_possible(self, pos):
        """Determine if a particular square is free and return a boolean.
        
        Arguments:
        pos -- the board position to check for vacancy
        
        """
        return self.board[pos] == "."
        
    def make_move(self, player, pos):
        """Make a move at pos for player.  Return True on success.
        
        Arguments:
        player -- which player is moving.  Either self.COMPUTER or self.HUMAN
        pos -- the board position player is attempting to move to
        
        """
        if self.move_possible(pos):
            self.board[pos] = self.tokens[player]
            self.squares[player].append(pos)
            self.free_squares.remove(pos)
            self.turns = self.turns + 1
            return True
        return False
        
    def undo_move(self, player, pos):
        """Undo a move at pos for player.  Return True on success.
        
        Arguments:
        player -- which player's move to undo.  Either self.COMPUTER or self.HUMAN
        pos -- board position to free
        
        """
        if self.board[pos] == self.tokens[player]:
            self.board[pos] = "."
            self.squares[player].remove(pos)
            
            #free_squares will likely not be in the same order it was before a move.  be careful
            self.free_squares.append(pos)
            self.turns = self.turns - 1
            return True
        return False

if __name__ == '__main__':
    game = TicTacToe()