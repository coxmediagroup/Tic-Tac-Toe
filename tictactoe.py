import re

from gameboard import GameBoard

MOVE_PATTERN = "^(q|\(?(?P<x>[0-2]),?(?P<y>[0-2])\)?)$"

def collect_initial_game_data():
    print "Before we start, Would you like to be X's or O's? (x/o)"
    player_symbol = None
    while player_symbol is None:
        player_symbol = raw_input().upper().strip()
        if player_symbol not in ('X', 'O'):
            print "'{0}' is not a valid decision.  Please enter 'x' or 'o'.".format(player_symbol)
            player_symbol = None

    print 'Great! Would you like to have the first turn? (y/n)'

    player_turn = None
    while player_turn is None:
        player_input = raw_input().lower().strip()
        if player_input in ('y', 'ye', 'yes'):
            player_turn = True
        elif player_input in ('n', 'no'):
            player_turn = False
        else:
            print "'{0}' is not a valid decision. Please enter 'y' or 'n'.".format(player_input)
    
    print "OK! Let's begin!"
    return player_symbol, player_turn

def start_game():
    print 'Welcome to Tic-Tac-Toe!'
    
    board = None
    while True:
        if not board or not board.moves_available:
            player_symbol, player_turn = collect_initial_game_data()
            board = GameBoard('X' if player_symbol == 'O' else 'O')

        if player_turn:
            print "It's your turn! To make a move, enter the x,y coordinates of space you want (ex. 0,2), or enter 'q' to quit at any time."
            move = None
            while not move:
                move_input = raw_input().lower().strip()
                move = re.match(MOVE_PATTERN, move_input)
                if not move:
                    print "'{0}' is not a valid move. Please use x,y coordinates. For example: 0,2".format(move_input)
            if move.string == 'q':
                print "Thanks for playing!"
                sys.exit(0)

            board.make_move(move.group('x'), 
                            move.group('y'), 
                            player_symbol)
        else:
            board.move()

        player_turn = not player_turn

if __name__ == '__main__':
    start_game()
