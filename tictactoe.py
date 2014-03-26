class TicTacToe:

    wins = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    valid_player_symbols = ['X', 'O']

    def __init__(self):
        self.our_squares = []
        self.player_squares = []
        self.player_symbol = ''
        self.our_symbol = ''
        self.board_values = {}
        self.initialize_board()
        self.players_last_move = ''

    def start_game(self):
        self.who_goes_first()
        print 'The player is ' + self.player_symbol + '.'
        if self.player_symbol == 'X':
            self.our_symbol = 'O'
            print 'Great!  You go first.'
            self.prompt_player()
        elif self.player_symbol == 'O':
            self.our_symbol = 'X'
            print 'No problem.  I\'ll go first.'
            self.we_move()

    def we_move(self):
        """The program makes a move"""
        if self.player_squares.__len__() == 0:
            print "This is the first move!"
            self.record_move(self.our_squares, self.our_symbol, 5)
            self.finish_move(self.our_symbol, self.our_squares)
        else:
            print "This is not the first move."
            # See where we should move next
            # Take square 5 if it's open
            if self.is_square_free(5):
                print "Taking square 5."
                self.record_move(self.our_squares, self.our_symbol, 5)
                self.finish_move(self.our_symbol, self.our_squares)
            else:
                # See if the player is about to win
                print "Square 5 is gone.  Picking another."
                for win in TicTacToe.wins:
                    print "Testing winning combos for player."
                    win_count = 0
                    win_matches = []
                    win_misses = []
                    for i in win:
                        if i in self.player_squares:
                            print "square %d is in win" % i
                            win_count += 1
                            win_matches.append(i)
                        elif i not in self.our_squares:
                            win_misses.append(i)
                    print "win_count is %s" % win_count
                    if win_count == 2 and win_misses.__len__() > 0:
                        print "Uh-oh!  Looks like the player might win soon."
                        print "win is %s" % win
                        print "win_matches is %s" % win_matches
                        print "win_misses is %s" % win_misses[0]
                        self.record_move(self.our_squares, self.our_symbol, win_misses[0])
                        self.finish_move(self.our_symbol, self.our_squares)
                        return
                # Try to block based on the player's last move
                if self.players_last_move == 1:
                    if self.is_square_free(2):
                        self.record_move(self.our_squares, self.our_symbol, 2)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(4):
                        self.record_move(self.our_squares, self.our_symbol, 4)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(3):
                        self.record_move(self.our_squares, self.our_symbol, 3)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(7):
                        self.record_move(self.our_squares, self.our_symbol, 7)
                        self.finish_move(self.our_symbol, self.our_squares)
                elif self.players_last_move == 3:
                    if self.is_square_free(2):
                        self.record_move(self.our_squares, self.our_symbol, 2)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(6):
                        self.record_move(self.our_squares, self.our_symbol, 6)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(9):
                        self.record_move(self.our_squares, self.our_symbol, 9)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(1):
                        self.record_move(self.our_squares, self.our_symbol, 1)
                        self.finish_move(self.our_symbol, self.our_squares)
                elif self.players_last_move == 9:
                    if self.is_square_free(6):
                        self.record_move(self.our_squares, self.our_symbol, 6)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(8):
                        self.record_move(self.our_squares, self.our_symbol, 8)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(3):
                        self.record_move(self.our_squares, self.our_symbol, 3)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(7):
                        self.record_move(self.our_squares, self.our_symbol, 7)
                        self.finish_move(self.our_symbol, self.our_squares)
                elif self.players_last_move == 7:
                    if self.is_square_free(8):
                        self.record_move(self.our_squares, self.our_symbol, 8)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(4):
                        self.record_move(self.our_squares, self.our_symbol, 4)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(9):
                        self.record_move(self.our_squares, self.our_symbol, 9)
                        self.finish_move(self.our_symbol, self.our_squares)
                    elif self.is_square_free(1):
                        self.record_move(self.our_squares, self.our_symbol, 1)
                        self.finish_move(self.our_symbol, self.our_squares)
                # No fancy logic here!
                elif self.is_square_free(1):
                    self.record_move(self.our_squares, self.our_symbol, 1)
                    self.finish_move(self.our_symbol, self.our_squares)
                elif self.is_square_free(3):
                    self.record_move(self.our_squares, self.our_symbol, 3)
                    self.finish_move(self.our_symbol, self.our_squares)
                elif self.is_square_free(9):
                    self.record_move(self.our_squares, self.our_symbol, 9)
                    self.finish_move(self.our_symbol, self.our_squares)
                elif self.is_square_free(7):
                    self.record_move(self.our_squares, self.our_symbol, 7)
                    self.finish_move(self.our_symbol, self.our_squares)
                elif self.is_square_free(2):
                    self.record_move(self.our_squares, self.our_symbol, 2)
                    self.finish_move(self.our_symbol, self.our_squares)
                elif self.is_square_free(6):
                    self.record_move(self.our_squares, self.our_symbol, 6)
                    self.finish_move(self.our_symbol, self.our_squares)
                elif self.is_square_free(8):
                    self.record_move(self.our_squares, self.our_symbol, 8)
                    self.finish_move(self.our_symbol, self.our_squares)
                elif self.is_square_free(4):
                    self.record_move(self.our_squares, self.our_symbol, 4)
                    self.finish_move(self.our_symbol, self.our_squares)

    def is_square_free(self, square):
        if self.board_values[square] in range(9):
            return True

    def record_move(self, squares, symbol, square):
        squares.append(square)
        self.board_values[square] = symbol

    def finish_move(self, symbol, squares):
        self.draw_board()
        self.check_for_winner(symbol, squares)

    def check_for_winner(self, symbol, squares):
        """Check to see if someone won"""
        print 'Checking for winner: %s, %s' % (symbol, squares)
        for win in self.wins:
            # Check winning combination for matches
            if all(x in squares for x in win):
                print "%s wins!!!" % symbol
                print self.draw_board()
                exit()
        if not self.any_moves_left():
            print 'Game over!  Looks like a draw.'
            print self.draw_board()
            exit()
        else:
            print "%s didn't win." % symbol
            if symbol == self.our_symbol:
                self.prompt_player()
            elif symbol == self.player_symbol:
                self.we_move()
            else:
                print "Oops."

    def any_moves_left(self):
        squares_free = 0
        for key in self.board_values:
            if not self.is_player_symbol(self.board_values[key]):
                squares_free += 1
        if squares_free > 0:
            return True

    def prompt_player(self):
        """Prompt the player for a move"""
        board = self.draw_board()
        print board
        self.player_moves(self.board_values)

    def is_player_symbol(self, symbol):
        if symbol in TicTacToe.valid_player_symbols:
            return True
        elif symbol not in TicTacToe.valid_player_symbols:
            return False
        else:
            print "Oops."

    def player_moves(self, board_values):
        open_squares = []
        for key, value in board_values.iteritems():
            if not self.is_player_symbol(value):
                open_squares.append(key)
        move = int(raw_input('Which square do you want to move to? %s' % open_squares))
        self.players_last_move = move
        self.player_squares.append(move)
        print self.player_squares

        self.board_values[move] = self.player_symbol
        print self.board_values
        self.check_for_winner(self.player_symbol, self.player_squares)

    def initialize_board(self):
        """Create the board_values dictionary with no X's and O's"""
        self.board_values = {x:x for x in(range(1,10))}

    def draw_board(self):
        """Function for drawing the game board"""
        board = "-------------------\n"
        board += "|  %s  |  %s  |  %s  |\n" % (self.board_values[1], self.board_values[2], self.board_values[3])
        board += "-------------------\n"
        board += "|  %s  |  %s  |  %s  |\n" % (self.board_values[4], self.board_values[5], self.board_values[6])
        board += "-------------------\n"
        board += "|  %s  |  %s  |  %s  |\n" % (self.board_values[7], self.board_values[8], self.board_values[9])
        board += "-------------------\n"
        return board

    def who_goes_first(self):
        while self.player_symbol not in TicTacToe.valid_player_symbols:
            player_goes_first = raw_input('Want to go first? [y/n]')
            if player_goes_first == 'y':
                self.player_symbol = 'X'
            elif player_goes_first == 'n':
                self.player_symbol = 'O'
            else:
                print "Sorry.  I didn't catch that."

if __name__ == "__main__":
    t = TicTacToe()
    t.start_game()
