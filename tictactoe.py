__author__ = 'ali'


def start_game():
    player_symbol = who_goes_first()
    print 'The player is ' + player_symbol + '.'
    if player_symbol == 'X':
        print 'Great!  You go first.'
    elif player_symbol == 'O':
        print 'No problem.  I\'ll go first.'
    draw_board()
    pass


def draw_board():
    """Function for drawing the game board"""
    print "----------------"
    print "|    |    |    |"
    print "----------------"
    print "|    |    |    |"
    print "----------------"
    print "|    |    |    |"
    print "----------------"
    pass


def who_goes_first():
    valid_player_symbols = ['X', 'O']
    player_symbol = ''
    while player_symbol not in valid_player_symbols:
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