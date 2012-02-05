import random

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
        
    def print_board(self):
        """Print a representation of the board, and available moves, on the screen"""
        board = ""
        moves = ""
        for i in range(len(self.board)):
            board += self.board[i]
            if self.board[i] == ".":
                moves += str(i)
            else:
                moves += "."
            if (i % 3 == 2):
                print board, "   ", moves
                board = ""
                moves = ""
        print "\n"
        
    def play(self):
        self.print_board()
        while self.game_over == False:
            if self.board_control == self.HUMAN:
                self.do_human_turn()
            else:
                self.do_computer_turn()
            self.print_board()
            game_over, winner = self.check_game_over(self.squares)
            if game_over:
                self.game_over = True
                print "Game over.  You Lose!!"
        
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
        
    def check_game_over(self, squares):
        """Check to see if the game is over and identify the winner
        
        Args:
            squares -- list containing lists of squares held by each player
        Returns:
            a boolean value for whether the game is over, and a score:
                -1: human wins
                 1: computer wins
                 0: tie game (board full)
        
        """
        for victory in self.victories:
            if set(victory).issubset(squares[self.COMPUTER]):
                return True, 1
            elif set(victory).issubset(squares[self.HUMAN]):
                return True, -1
        if self.turns == 9:
            return True, 0
        return False, None
        
    def do_human_turn(self):
        turn_done = False
        while not turn_done:
            pos = raw_input("Make your move: ")
            if pos in ["0","1","2","3","4","5","6","7","8"]:
                pos = int(pos)
                turn_done = self.make_move(self.HUMAN, pos)
        self.board_control = self.COMPUTER

    def do_computer_turn(self):
        """Make an optimal move for the computer."""
        #For the computer's first move, always take the center or a corner.
        if self.turns < 2:
            if not self.make_move(self.COMPUTER, 4):
                self.make_move(self.COMPUTER, 0)

        else:
            score, pos = self.find_good_move(self.COMPUTER)
            self.make_move(self.COMPUTER, pos)
        self.board_control = self.HUMAN
        
    def find_good_move(self, player):
        """Find the optimal move for the computer player."""
        #not implemented yet.  return a random free position
        return 1, random.choice(self.free_squares)
        #if game over, return score
        #if computer turn:
        #   for each available move:
        #       make a move
        #       call find_good_move with new board
        #       undo move
        #       evaluate whether the move gave us a good result
        #   return best score and position
        #else human turn:
        #   for each available move:
        #       make a move
        #       call find_good_move with new board
        #       undo move
        #       evaluate whether the move gave human a good result
        #   return best score and position
        
        
if __name__ == '__main__':
    game = TicTacToe()
    game.play()