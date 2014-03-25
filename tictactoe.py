__author__ = 'Ali Nabavi'


def start_game():
    player_symbol = who_goes_first()
    print 'The player is ' + player_symbol + '.'
    if player_symbol == 'X':
        print 'Great!  You go first.'
        prompt_player()
    elif player_symbol == 'O':
        print 'No problem.  I\'ll go first.'
        we_move()


def we_move():
    pass


def prompt_player():
    board_values = initialize_board()
    board = draw_board(board_values)
    print board
    player_moves(board_values)



def is_player_symbol(symbol):
    valid_player_symbols = ['X', 'O']
    if symbol in valid_player_symbols:
        return True
    elif symbol not in valid_player_symbols:
        return False
    else:
        print "Oops."


def player_moves(board_values):
    open_squares = []
    for key, value in board_values.iteritems():
        if is_player_symbol(value) == False:
            open_squares.append(key)
    move = raw_input('Which square do you want to move to? %s' % open_squares)


def initialize_board():
    board_values = {x:x for x in(range(1,10))}
    return board_values


def draw_board(board_values):
    """Function for drawing the game board"""
    board = "-------------------\n"
    board += "|  %s  |  %s  |  %s  |\n" % (board_values[1], board_values[2], board_values[3])
    board += "-------------------\n"
    board += "|  %s  |  %s  |  %s  |\n" % (board_values[4], board_values[5], board_values[6])
    board += "-------------------\n"
    board += "|  %s  |  %s  |  %s  |\n" % (board_values[7], board_values[8], board_values[9])
    board += "-------------------\n"
    return board


def who_goes_first():
    player_symbol = ''
    while is_player_symbol(player_symbol) is False:
        player_goes_first = raw_input('Want to go first? [y/n]')
        if player_goes_first == 'y':
            player_symbol = 'X'
        elif player_goes_first == 'n':
            player_symbol = 'O'
        else:
            print "Sorry.  I didn't catch that."
    return player_symbol

if __name__ == "__main__":
    start_game()