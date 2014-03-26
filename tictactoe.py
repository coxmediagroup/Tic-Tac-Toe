class TicTacToe:

    wins = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

    def __init__(self):
        self.our_squares = []
        self.player_squares = []
        self.player_symbol = ''
        self.our_symbol = ''
        self.board_values = self.initialize_board()


    def start_game(self):
        player_symbol = self.who_goes_first()
        print 'The player is ' + player_symbol + '.'
        if player_symbol == 'X':
            our_symbol = 'O'
            print 'Great!  You go first.'
            self.prompt_player()
        elif player_symbol == 'O':
            our_symbol = 'X'
            print 'No problem.  I\'ll go first.'
            self.we_move()

    def we_move(self):
        """The program makes a move"""
        if self.player_squares.__len__() == 0:
            print "This is the first move!"
            self.our_squares.append(5)
            self.board_values[5] = self.our_symbol
        board = self.draw_board(self.board_values)
        print board

    def prompt_player(self):
        """Prompt the player for a move"""
        board = self.draw_board(self.board_values)
        print board
        self.player_moves(self.board_values)

    def is_player_symbol(self, symbol):
        valid_player_symbols = ['X', 'O']
        if symbol in valid_player_symbols:
            return True
        elif symbol not in valid_player_symbols:
            return False
        else:
            print "Oops."

    def player_moves(self, board_values):
        open_squares = []
        for key, value in board_values.iteritems():
            if not self.is_player_symbol(value):
                open_squares.append(key)
        move = raw_input('Which square do you want to move to? %s' % open_squares)

    def initialize_board(self):
        """Create the board_values dictionary with no X's and O's"""
        board_values = {x:x for x in(range(1,10))}
        return board_values

    def draw_board(self, board_values):
        """Function for drawing the game board"""
        board = "-------------------\n"
        board += "|  %s  |  %s  |  %s  |\n" % (board_values[1], board_values[2], board_values[3])
        board += "-------------------\n"
        board += "|  %s  |  %s  |  %s  |\n" % (board_values[4], board_values[5], board_values[6])
        board += "-------------------\n"
        board += "|  %s  |  %s  |  %s  |\n" % (board_values[7], board_values[8], board_values[9])
        board += "-------------------\n"
        return board

    def who_goes_first(self):
        player_symbol = ''
        while self.is_player_symbol(player_symbol) is False:
            player_goes_first = raw_input('Want to go first? [y/n]')
            if player_goes_first == 'y':
                player_symbol = 'X'
            elif player_goes_first == 'n':
                player_symbol = 'O'
            else:
                print "Sorry.  I didn't catch that."
        return player_symbol


if __name__ == "__main__":
    t = TicTacToe()
    t.start_game()
