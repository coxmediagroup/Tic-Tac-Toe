import copy

board_outline = {"1": (0, 0), "2": (0, 1), "3": (0, 2),
                 "4": (1, 0), "5": (1, 1), "6": (1, 2),
                 "7": (2, 0), "8": (2, 1), "9": (2, 2)}


class TicTacToeBoard:
    def __init__(self, board_clone=None):
        self.current_play = 'X'
        self.opponent_play = 'O'
        self.width = 3
        self.height = 3
        self.positions = {}
        for k, v in board_outline.iteritems():
            self.positions[v[0], v[1]] = k
        if board_clone:
            self.__dict__ = copy.deepcopy(board_clone.__dict__)

    def _is_empty(self, position):
        """Simple 'is it empty' checker'
        """
        return position != "X" and position != "O"

    def checker(self, player):
        """Returns the optimal minimized or maximized value for the player. This algorithm is
        based on the minimax algo: http://en.wikipedia.org/wiki/Minimax

        Values returned are in the format (minimizing|maximizing) value, (position_x, position_y)
        tuple. The returning position is what the AI will use for placement.
        """
        if self.check_win():
            if player:
                return -1, None     # minimizing player
            else:
                return 1, None      # maximizing player
        elif self.check_draw():
            return 0, None
        elif player:    # check the minimizing player
            test_check = (-2, None)
            for pos_x, pos_y in self.positions:
                if self._is_empty(self.positions[pos_x, pos_y]):
                    # A cloned version of the board for evaluating possible moves
                    test_board = self.move(pos_x, pos_y)
                    value = test_board.checker(not player)[0]
                    if value > test_check[0]:
                        test_check = value, (pos_x, pos_y)
            return test_check
        else:    # check the maximizing player
            test_check = (+2, None)
            for pos_x, pos_y in self.positions:
                if self._is_empty(self.positions[pos_x, pos_y]):
                    # A cloned version of the board for evaluating possible moves
                    test_board = self.move(pos_x, pos_y)
                    value = test_board.checker(not player)[0]
                    if value < test_check[0]:
                        test_check = value, (pos_x, pos_y)
            return test_check

    def move(self, pos_x, pos_y):
        """Make the move then swap the players
        """
        if not self._is_empty(self.positions[pos_x, pos_y]):
            raise Exception("Obviously you're not a golfer.")
        new_board = TicTacToeBoard(self)    # get a cloned version of the current board
        new_board.positions[pos_x, pos_y] = new_board.current_play
        (new_board.current_play, new_board.opponent_play) = (new_board.opponent_play, new_board.current_play)
        return new_board

    def optimal(self):
        """Return the optimal placement from the checker
        """
        optimal_check = self.checker(True)
        return optimal_check

    def check_draw(self):
        """Check if the board is in a 'draw' state
        """
        for pos_x, pos_y in self.positions:
            if self._is_empty(self.positions[pos_x, pos_y]):
                return False
        return True

    def check_win(self):
        """Check if the board is in a 'win' state (one player is a winner)
        """
        # check diags
        # l to r
        win_list = []
        for pos_y in range(self.height):
            pos_x = pos_y   # corners or middle
            if self.positions[pos_x, pos_y] == self.opponent_play:
                win_list.append((pos_x, pos_y))
            if len(win_list) == self.height:
                return win_list

        # r to l
        win_list = []
        for pos_y in range(self.height):

            pos_x = self.height - pos_y - 1      # opposite end
            if self.positions[pos_x, pos_y] == self.opponent_play:
                win_list.append((pos_x, pos_y))
            if len(win_list) == self.height:
                return win_list

        # check cols
        for pos_x in range(self.width):
            win_list = []
            for pos_y in range(self.height):
                if self.positions[pos_x, pos_y] == self.opponent_play:
                    win_list.append((pos_x, pos_y))
            if len(win_list) == self.height:
                return win_list

        # check rows
        for pos_y in range(self.height):
            win_list = []
            for pos_x in range(self.width):
                if self.positions[pos_x, pos_y] == self.opponent_play:
                    win_list.append((pos_x, pos_y))
            if len(win_list) == self.width:
                return win_list

        # no winner
        return None

    def print_board(self):
        """Print out the board
        """
        str = "\n"
        str += "   %s | %s | %s\n" % (self.positions[0, 0], self.positions[0, 1], self.positions[0, 2])
        str += "   ---------\n"
        str += "   %s | %s | %s\n" % (self.positions[1, 0], self.positions[1, 1], self.positions[1, 2])
        str += "   ---------\n"
        str += "   %s | %s | %s\n" % (self.positions[2, 0], self.positions[2, 1], self.positions[2, 2])
        str += "\n"
        return str


def print_header():
    print " ------------ ---- ----------  ------------ --------- ----------  ------------ --------- ----------"
    print " |          | |  | |        |  |          | |  ---  | |        |  |          | |  ---  | |        |"
    print " ----    ---- |  | |  -------  ----    ---- |  | |  | |  -------  ----    ---- |  | |  | |  -------"
    print "     |  |     |  | |  |            |  |     |  ---  | |  |            |  |     |  | |  | |        |"
    print "     |  |     |  | |  -------      |  |     |  | |  | |  -------      |  |     |  | |  | |  -------"
    print "     |  |     |  | |        |      |  |     |  | |  | |        |      |  |     |  ---  | |        |"
    print "     ----     ---- ----------      ----     ---- ---- ----------      ----     --------- ----------"
    print "                                                                                                   "
    print "(or naughts and crosses as those Irish folk like to call it)                                       "
    print "                                                                                                   "
    print "                                                                                                   "
    print "Rules:"
    print " * You are 'X' and the computer is 'O'"
    print " * If you attempt to use an occupied position, you will forfeit the game"
    print " * You will not win"
    print ""
    print "Begin!"
    print ""
    print "Pick a position (available positions are numbered)"


def print_winner(winner, plays):
    print "%s won in %d moves. The game is over." % (winner, plays)
    print ""

if __name__ == "__main__":
    game_over, plays = False, 0
    print_header()
    board = TicTacToeBoard()
    print board.print_board()
    while not game_over:
        player_position = raw_input("Your position: ")
        x, y = board_outline[player_position]
        board = board.move(x, y)
        plays += 1
        winner_check = board.check_win()
        if winner_check:
            print_winner("X", plays)
            game_over = True
        print board.print_board()
        print "The AI will now move."
        print ""
        optimal = board.optimal()       # is there an optimal move?
        if optimal:
            board = board.move(*optimal[1])
        plays += 1
        winner_check = board.check_win()
        if winner_check:
            print_winner("O", plays)
            game_over = True
        print board.print_board()