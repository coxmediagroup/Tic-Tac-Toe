import re
import sys

from gameboard import GameBoard

MOVE_PATTERN = "^(q|\(?(?P<x>[0-2]),?(?P<y>[0-2])\)?)$"

def collect_player_symbol():
    print "Before we start, Would you like to be X's or O's? (x/o)"

    player_symbol = None
    while player_symbol is None:
        player_symbol = raw_input().upper().strip()
        if player_symbol not in ('X', 'O'):
            print "'{0}' is not a valid decision.  Please enter 'x' or 'o'.".format(player_symbol)
            player_symbol = None

    print 'Great!'
    return player_symbol

def collect_player_move():
    print "It's your turn! To make a move, enter the x,y coordinates of space you want (ex. 0,2), or enter 'q' to quit at any time."

    move = None
    while not move:
        move_input = raw_input().lower().strip()
        move = re.match(MOVE_PATTERN, move_input)
        if not move:
            print "'{0}' is not a valid move. Please use x,y coordinates. For example: 0,2".format(move_input)

    return move

def collect_yes_or_no(question):
    print '{0} (y/n)'.format(question)

    answer = None
    while answer is None:
        player_input = raw_input().lower().strip()
        if player_input in ('y', 'ye', 'yes'):
            answer = True
        elif player_input in ('n', 'no'):
            answer = False
        else:
            print "'{0}' is not a valid decision. Please enter 'y' or 'n'.".format(player_input)

    print 'OK!'
    return answer

def start_game():
    print 'Welcome to Tic-Tac-Toe!'
    
    board = None
    while True:
        if not board or not board.moves_available:
            player_symbol = collect_player_symbol()
            player_turn = collect_yes_or_no('Would you like to have the first turn?')
            board = GameBoard('X' if player_symbol == 'O' else 'O')
            print ("Let's begin!\n"
                   "The image below is a view of the initial gameboard.  "
                   "As you can see, there are no X's or O's yet.")
            print board.display_str

        if player_turn:
            move = collect_player_move()
            if move.string == 'q':
                print "Thanks for playing!"
                sys.exit(0)

            board.make_move(int(move.group('x')), 
                            int(move.group('y')), 
                            player_symbol)
        else:
            board.move()
        
        print board.display_str
        
        if not board.moves_available:
            if board.winner:
                print 'Aww looks like you lost!'
            else:
                print 'Wow the game is a draw!'

            if not collect_yes_or_no('Would you like to play again?'):
                print "Thanks for playing!"
                sys.exit(0)

        player_turn = not player_turn

if __name__ == '__main__':
    start_game()
