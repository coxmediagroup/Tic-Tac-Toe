
board = [[None] * 3] * 3

def print_board():
    pass

def collect_initial_game_data():
    print "Welcome to Tic-Tac-Toe! Before we start, would you like to be X's or O's? (x/o)"

    player_symbol = None
    while player_symbol is None:
        player_symbol = raw_input().upper()
        if player_symbol not in ('X', 'O'):
            print "'{0}' is not a valid decision.  Please enter 'x' or 'o'.".format(player_symbol)
            player_symbol = None

    print 'Great! Would you like to have the first turn? (y/n)'

    player_turn = None
    while player_turn is None:
        player_input = raw_input().lower()
        if player_input in ('y', 'ye', 'yes'):
            player_turn = True
        elif player_input in ('n', 'no'):
            player_turn = False
        else:
            print "'{0}' is not a valid decision. Please enter 'y' or 'n'.".format(player_input)
    
    print "OK! Let's begin!"
    return player_symbol, player_turn

if __name__ == '__main__':
    collect_initial_game_data()
    print_board()
