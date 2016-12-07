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
        print "Board   Available moves\n"
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
        coin_toss = random.randint(0,1)
        self.tokens[coin_toss] = "x"
        self.tokens[(coin_toss + 1) & 1] = "o"
        if self.tokens[self.COMPUTER] == "x":
            self.board_control = self.COMPUTER
            print "You are Os.  Computer goes first.\n"
        else:
            self.board_control = self.HUMAN
            print "You are Xs.  You go first!\n"
        
        self.print_board()
        while self.game_over == False:
            if self.board_control == self.HUMAN:
                self.do_human_turn()
            else:
                self.do_computer_turn()
            self.print_board()
            game_over, winner = self.check_game_over()
            if game_over:
                self.game_over = True
                if winner == 1:
                    print "Game over.  You Lose!!"
                elif winner == 0:
                    print "Tie game.  You don't win!!"
                else:
                    print "You win.  This shouldn't be possible."
        
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
        
    def check_game_over(self):
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
            if set(victory).issubset(self.squares[self.COMPUTER]):
                return True, 1
            elif set(victory).issubset(self.squares[self.HUMAN]):
                return True, -1
        if self.turns == 9:
            return True, 0
        return False, None
        
    def do_human_turn(self):
        """Prompt the user for a board position and make the move if possible."""
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
        """Find the optimal move for the computer player.
        
        This is a recursive minimax algorithm.  A good description can be found here:
            http://www.ocf.berkeley.edu/~yosenl/extras/alphabeta/alphabeta.html
        
        The computer will try every possible move, and simulate the human's responses.
        The computer will then choose an advantageous move.
        
        Args:
            player -- which player to try moves for
            
        Returns:
            (score, pos).
            score is used internally by the algorithm to evalute a move's worth to the player.
            pos is discarded internally, but on final return contains a safe move.
        
        """
        game_over, score = self.check_game_over()
        if game_over:
            return score, None
        
        if player == self.COMPUTER:
            #initialize best_score to a value worse than the worst score (-1)
            best_score = -5
            best_pos = -1
            #use set() here to avoid repeat moves, as undo_move() doesn't preserve the order of the original list.
            for pos in set(self.free_squares):
                self.make_move(player, pos)
                score, dummy = self.find_good_move(self.HUMAN)
                self.undo_move(player, pos)
                if score == 1:
                    return score, pos
                if score > best_score:
                    best_score = score
                    best_pos = pos
            return best_score, best_pos
            
        else: #HUMAN turn
            best_score = 5
            best_pos = -1
            for pos in set(self.free_squares):
                self.make_move(player, pos)
                score, dummy = self.find_good_move(self.COMPUTER)
                self.undo_move(player, pos)
                if score == -1:
                    return score, pos
                if score < best_score:
                    best_score = score
                    best_pos = pos
            return best_score, best_pos
        
        
if __name__ == '__main__':
    game = TicTacToe()
    lets_play = True
    while lets_play:
        game.play()
        
        while True:
            answer = raw_input("Play again? (y or n):").upper()
            if answer == "Y":
                game.reset_board()
                break
            elif answer == "N":
                lets_play = False
                break
            else:
                print "Invalid input."