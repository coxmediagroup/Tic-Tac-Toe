"""
Functions and classes for playing the game. The UI classes can be found in
run.py
"""
import random


WINNING_MOVES = (0x2a000, 0x20202, 0x20028, 0x08082,  
                 0x02a00, 0x02022, 0x0080a, 0x002a0)

# a cache to minimize calculation, populated with some default starting values.
#
# Ideally for opening moves the computer should always take a corner or the
# center, and if the human player is going first, the computer should take
# whichever the player didn't take.
#
# This could be set so the computer always makes the same move in response to
# a human move, but it seems more interesting and challenging to the player if
# the computer has multiple possibilities of equal cost to choose from
# when possible.
PLAYBOOK = {(0x00000, 2): {8: -100, 6: -100, 4: -100, 2: -100},
            (0x20000, 2): {0: -100},
            (0x02000, 2): {0: -100},
            (0x00200, 2): {0: -100},
            (0x00020, 2): {0: -100},
            (0x00002, 2): {8: -100, 6: -100, 4: -100, 2: -100},
            (0x08000, 2): {8: -100, 6: -100},
            (0x00800, 2): {6: -100, 4: -100},
            (0x00080, 2): {4: -100, 2: -100},
            (0x00008, 2): {8: -100, 2: -100}}


# values used when calculating the best move for the computer
WIN_VALUE = 10
LOSS_VALUE = -10
TIE_VALUE = 0

HUMAN = 1
COMPUTER = 2

PLAYER1 = 'X'
PLAYER2 = 'O'


class InvalidStateException(Exception):
    pass


class TicTacToeBoard(object):
    """
    Primary class for tracking and playing the game.  
    
    Each of the nine squares on the board is represented by a number, like so:
                    ___________
                   | 8 | 7 | 6 |
                    -----------
                   | 1 | 0 | 5 |
                    -----------
                   | 2 | 3 | 4 |
                    -----------
    
    These numbers directly correspond to positions in the binary representation
    of the board. An empty board would be represented in binary as:
    
             [8]  [7]  [6]  [5]  [4]  [3]  [2]  [1]  [0]
             0 0  0 0  0 0  0 0  0 0  0 0  0 0  0 0  0 0
             
    The first bit of the two-bit representation of a square indicates whether
    or not the position is filled. The second bit represents player 1 (1 0) or
    player 2 (1 1). For example, if player 2 is X:
                    ___________
                   | X |   |   |
                    -----------
                   |   | O | O |
                    -----------
                   |   | X |   |
                    -----------
    
    This board can be represented in binary as:
       
             [8]  [7]  [6]  [5]  [4]  [3]  [2]  [1]  [0]
             1 1  0 0  0 0  1 0  0 0  1 1  0 0  0 0  1 0
             
    This value is stored as a hex value to make it shorter, so this board would 
    be represented as 0x3080c2. Please also note that the X and O settings can 
    be changed by setting the global 'PLAYER1' and 'PLAYER2' constants above.
    
    Public methods:
        computer_move
        get_square_label
        human_move
        is_computer_turn
        player_stats
        reset_board
    
    """
    def __init__(self):
        """
        Sets the default attributes for the class. No parameters are accepted.
        
        :attr board: an integer representation of the board. Defaults to 0.
        :attr turn: an integer representation of which player is moving. Can be
                    be 0 or 1. Defaults to 0.
        :attr player_wins: integer count of how many times the player has won
                    against the computer. Defaults to 0.
        :attr player_losses: integer count of how many times the player has
                    lost to the computer. Defaults to 0.
        :attr ties: integer count of tied games between player and computer.
                    Defaults to 0.
        """
        super(TicTacToeBoard, self).__init__()
        self.board = 0x00000
        self.turn = 0
        self.player_wins = 0
        self.player_losses = 0
        self.ties = 0
        self.game_over = False      
    
    def _apply_move(self, square, board, player):
        """
        Checks the validity of a given move and applies it to the game board. 
        Returns True if the move was applied; False otherwise.
        
        :param square: integer between 0 and 8
        :param board: integer representing board
        :return: boolean
        :raises: AssertionError
        """
        self._assert_valid_player(player)
        
        if not self.game_over:
            move = self._convert_move(square, player)
            if self._is_valid_move(move, board):
                board += move
                return square, board
        return None, board
    
    def _assert_valid_player(self, player):
        """
        Verifies that a player integer passed is a valid player integer (1 or 2)
        
        :param player: integer representing a player
        :raises: AssertionError
        """
        # this shouldn't fail if the non-public methods are respected
        assert player in (HUMAN, COMPUTER)
    
    def _best_move(self, potential_moves, player):
        """
        Selects the best move from a list of potential moves.
        Returns the best move, and the cost for that move.
        
        :param potential_moves: dictionary of integers representing squares, 
            0 to 8, paired with a calculated cost for making that move
        :return: integer, integer
        :raises: AssertionError
        """
        self._assert_valid_player(player)
        
        # we'll just return None and let self.computer_move handle it as an
        # InvalidStateException. Shouldn't happen if non-public methods are
        # respected
        if not potential_moves:
            return None
        
        # we want to introduce a little bit of randomness for equal values
        if player is COMPUTER:
            return max(potential_moves.items(), 
                       key=lambda x: x[1] + .01 * random.randint(0, 99))
        return min(potential_moves.items(), 
                   key=lambda x: x[1] + .01 * random.randint(0, 99))
    
    def _board_for_player(self, player, board):
        """
        Converts current board to one with only the indicated player's pieces.
        Returns an integer representation of a board.
        
        :param player: integer for the player, either 1 or 2 (human or
                computer, respectively)
        :param board: integer representing a board
        :return: integer
        :raises: AssertionError
        """
        self._assert_valid_player(player) 
        
        mod = player + 1
        player_board = 0
        i = 0
        while board:
            last_two_digits = board & 3
            if last_two_digits and not last_two_digits % mod:
                player_board += (0b10 << i)
            board = board >> 2
            i += 2

        return player_board
    
    def _calculate_board_costs(self, board):
        """
        Calculates the cost for the next play for specific boards from a list.
        Returns a dictionary in the same format as PLAYBOOK.
        
        :param boards: list of tuples in the format 
                (<board integer>, <current cost>, <current player>, <next move>)
        :return: dictionary
        :raises: AssertionError
        """
        board_dict = {}
        revisit_list = []
        
        boards = [(board, 2)]
        while boards:
            board, player = boards.pop(0)
            if (board, player) not in board_dict:
                new_boards, board_costs, revisit = self._calculate_board_variations(
                                                                board, player)
                boards.extend(new_boards)
                revisit_list.extend(revisit)
                board_dict[(board, player)] = board_costs
        
        while revisit_list:
            # starting at the end, where there are more complete boards (and 
            # more likely to be fully calculated)
            board, player, square, new_board = revisit_list.pop()
            
            board_values = board_dict[(board, player)]
            if None in board_values.values():
                try:
                    new_player = ~player & 0x3
                    next_move = board_dict[(new_board, new_player)]
                    best_move = self._best_move(next_move, new_player)[1]
                    if best_move:
                        # we want wins to happen sooner, and losses to happen
                        # later
                        best_move += [-1, 1][best_move < 0]
                    board_dict[(board, player)][square] = best_move
                except TypeError:
                    # the next move still has to be calculated
                    revisit_list.insert(0, (board, player, square, new_board))
        
        return board_dict
    
    def _calculate_board_variations(self, board, player):
        """
        Finds all possible next moves for the specified board.
        Returns a list of boards that still need to be investigated, a 
        dictionary of calculated costs for the current board, and board
        moves that need to be calculated later after its sub-moves have been
        calculated.
        
        :param board: integer representing a board
        :param current_cost: integer cost of making moves up to this point
        :param player: integer representing a player (1 or 2)
        :return: (list, dict, list)
        """
        board_list = []
        board_dict = {}
        revisit_list = []
        
        valid_moves = self._get_valid_moves(board)
        for square in valid_moves:
            new_board = self._apply_move(square, board, player)[1]
            if self._has_won(player, new_board):
                if player is HUMAN:
                    board_dict[square] = LOSS_VALUE
                else:
                    board_dict[square] = WIN_VALUE
            elif self._is_board_full(new_board):
                board_dict[square] = TIE_VALUE
            else:
                other_player = ~player & 0x3
                board_list.append((new_board, other_player))
                
                # we'll calculate this later
                board_dict[square] = None
                revisit_list.append((board, player, square, new_board))
        
        return board_list, board_dict, revisit_list
            
    def _choose_square(self, board):
        """
        Picks a square for the computer to make its move.
        
        The method iterates through possible outcomes (wins, losses, ties)
        and picks the path with the lowest cost. Outcomes that take longer to
        achieve will cost more; losses will cost significantly more and wins
        will cost significantly less.
        
        Cost calculations are stored in the PLAYBOOK dictionary to minimize
        repetition of calculations if they're needed again.
        
        :param board: integer representing a board
        :return: integer
        :raises: InvalidStateException
        """
        if (board, COMPUTER) not in PLAYBOOK:
            new_moves = self._calculate_board_costs(board)
            if not new_moves:
                # let the UI handle it
                raise InvalidStateException("No valid moves for the computer")             
            PLAYBOOK.update(new_moves)
            
        potential_moves = PLAYBOOK[(board, COMPUTER)]
        return self._best_move(potential_moves, COMPUTER)[0]
    
    def _convert_move(self, square, player):
        """
        Converts the number of a square into its integer representation for player.
        
        :param square: integer between 0 and 8
        :param player: integer representing player (1 or 2)
        :return: integer
        """
        try:
            move = int(square)
        except (ValueError, TypeError):
            return None
        
        if not 0 <= move <= 8:
            return None
        
        # player 1 is represented by '1 0' on the board and player 2 is '1 1',
        # so we add 1 to the player number to get the binary representation
        return (player + 1) << (2 * move)
    
    def _game_over_validation(self, board):
        """
        Determines if the game is over based on the state of the board.
        Returns a tuple in the format (<is game over>, <who won>).
        
        Possible Values:
            (True, 1) - human player won
            (True, 2) - computer won
            (True, None) - there was a tie
            (False, None) - the game is still going
        
        :param board: integer representing a board
        :return: (boolean, integer)
        """
        winner = (self._has_won(HUMAN, board) or self._has_won(COMPUTER, board))
        if winner:
            self._set_win(winner)
            return (True, winner)
        
        if self._is_board_full(board):
            self._set_win(winner)
            return (True, None)
        
        return (False, None)
    
    def _get_valid_moves(self, board):
        """
        Returns a list of open spaces on the board.
        
        :param board: integer representation of a board
        :return: list of integers between 0 and 8
        """
        i = 0
        moves = []
        tmp_board = ~board & 0x3ffff
        while tmp_board:
            if (tmp_board & 0x3) == 3:
                moves.append(i)
            tmp_board = tmp_board >> 2
            i += 1
        return moves
    
    def _has_won(self, player, board):
        """
        Checks to see if the indicated player has won the game.
        Returns True if the player has won; False otherwise
        
        :param player: the player number, either 1 or 2, human or computer, 
                    respectively
        :param board: integer representing a board
        :return: boolean
        """
        player_board = self._board_for_player(player, board)
        for combo in WINNING_MOVES:
            if self._is_win(player_board, combo):
                return player
        return None
    
    def _is_board_full(self, board):
        """
        Determines if there are no open squares left on the board.
        Returns False if there are no open squares; True otherwise.
        
        :param board: integer representing a board
        :return: boolean
        """
        full_board = 0x2aaaa  # all squares filled, ignoring which player
        return full_board == full_board & board
    
    def _is_valid_move(self, move, board):
        """
        Checks if a current move is going to an empty square on the board.
        Returns True if the square is empty, and False if the square is filled
        or if move is None (i.e., self._convert_move decided that move was
        originally invalid input).
        
        :param move: an integer that has been generated using self._convert_move
        :param board: integer representing a board
        :return: boolean
        """
        if move is None:
            return False
        # if the move doesn't match up with anything on the board, we should
        # have a zero value if we try to `and` them
        return not (move & board)
    
    def _is_win(self, player_board, winning_combo):
        """
        Checks if a given player board contains a winning combination.
        Returns True if the combination is in the board; otherwise False.
        
        :param player_board: a integer that has been generated using 
                self._board_for_player
        :param winning_combo: an integer representing a board from WINNING_MOVES
        :return: boolean
        """
        return winning_combo == player_board & winning_combo
    
    def _set_turn(self):
        """Alternates the current self.turn between 0 and 1."""
        self.turn = ~self.turn & 0x1
    
    def _set_win(self, player):
        """
        Increments self.player_wins, self.player_losses, and self.ties for player.
        
        :param player: integer representing which player won the game
        """
        if player is None:
            self.ties += 1
        else:
            self.player_wins += int(player is HUMAN)
            self.player_losses += int(player is COMPUTER)
    
    def computer_move(self):
        """
        Autogenerates a move for the computer.
        Returns a tuple indicating (<move successful>, <game over>, <winner>).
        
        May throw an Exception of the game board is not in a valid state or t
        
        :return: (boolean, boolean, int or None)
        :raises: InvalidStateException
        """
        if not self.is_computer_turn():
            return (None, False, None)
        
        square = self._choose_square(self.board)
        square, self.board = self._apply_move(square, self.board, self.turn+1)
        if square is None:
            raise InvalidStateException("Illegal move by computer") # let the UI handle it
        self._set_turn()
        self.game_over, winner = self._game_over_validation(self.board)
        return (square, self.game_over, winner)   
    
    def get_square_label(self, square):
        """
        Finds the appropriate 'X' or 'O' label for a given square
        
        :param square: integer representing the desired square
        :return: string
        """
        player = (self.board >> (square*2)) & 0x3
        if not player:
            return ''
        return [PLAYER1, PLAYER2][(player - 1) is COMPUTER]
    
    def human_move(self, square):
        """
        Completes a move that the human has made.
        Returns a tuple indicating (<move successful>, <game over>, <winner>).
        
        :param square: integer from 0 to 8 indicating which square to play in
        :return: (boolean, boolean, integer or None)
        """
        if self.is_computer_turn():
            return (None, False, None)
        
        square, self.board = self._apply_move(square, self.board, self.turn+1)
        winner = None
        if square is not None:
            self._set_turn()
            self.game_over, winner = self._game_over_validation(self.board)
        return (square, self.game_over, winner)
    
    def is_computer_turn(self):
        """
        Determines whether it's the computer's turn to make a move. 
        The human player always goes when self.turn=0, and the computer goes 
        when self.turn=1
        
        :return: boolean
        """
        return bool(self.turn)
    
    def player_stats(self, player):
        """
        Generates a string showing player wins, losses, and ties
        
        :param player: integer representing the player, either 1 or 2
        :return: string
        """
        plyr = [PLAYER1, PLAYER2][player is COMPUTER]
        wins = self.player_wins if player is HUMAN else self.player_losses
        losses = self.player_losses if player is HUMAN else self.player_wins
        ties = self.ties
        
        return "(Player %s)\n\nWins: %s\nLosses: %s\nTies: %s" % (plyr, wins,
                                                                  losses, ties)
    
    def reset_board(self):
        """
        Sets self.board back to 0.
        Does not reset turns, wins, losses, or ties, because for the purposes
        of this game the player will have to exit the game in order to reset
        their scores.
        """
        self.board = 0
        self.game_over = False
 