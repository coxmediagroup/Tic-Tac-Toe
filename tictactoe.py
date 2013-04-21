'''
Interactive script to play a single-player game of Tic-Tac-Toe
against an AI opponent.

To begin, run::

    $ python tictactoe.py

'''
import re
import sys

from gameboard import GameBoard

def collect_player_symbol():
    print "Before we start, Would you like to be X's or O's? (x/o)"

    player_symbol = None
    while player_symbol is None:
        player_symbol = raw_input().upper().strip()
        if player_symbol not in ('X', 'O'):
            print ("'{0}' is not a valid decision.  "
                   "Please enter 'x' or 'o'.".format(player_symbol))
            player_symbol = None

    print 'Great!'
    return player_symbol

def collect_player_move(player_symbol):
    print ("It's your turn! You are {0}'s.  To make a move, enter "
           "the id/index of the space you want (ex. 5), or "
           "enter 'q' to quit at any time.".format(player_symbol))

    move = None
    while not move:
        move_input = raw_input().lower().strip()
        move = re.match("^(q|[0-8])$", move_input)
        if not move:
            print ("'{0}' is not a valid move.  Please use a single integer. "
                   "For example: 5".format(move_input))

    return move.string

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
            print ("'{0}' is not a valid decision.  "
                   "Please enter 'y' or 'n'.".format(player_input))

    print 'OK!'
    return answer

def start_game():
    print 'Welcome to Tic-Tac-Toe!'
    
    board = None
    while True:
        if not board:
            player_symbol = collect_player_symbol()
            player_turn = collect_yes_or_no('Would you like the first move?')
            board = GameBoard('X' if player_symbol == 'O' else 'O')
            print ("Let's begin!\n"
                   "The image below is a view of the initial gameboard.  "
                   "As you can see, there are no X's or O's yet.")
            print board.display

        if player_turn:
            move = collect_player_move(player_symbol)
            if move == 'q':
                print "Thanks for playing!"
                sys.exit(0)

            board.make_move_by_index(int(move), player_symbol)
            print 'Nice move! Here is what the game board looks like now:'
        else:
            board.move()
            print "Here is what the game board looks like after your opponent's move:"

        print board.display
        
        if not board.moves_available:
            if board.winner:
                print 'Aww looks like you lost!'
            else:
                print 'Wow the game is a draw!'

            if not collect_yes_or_no('Would you like to play again?'):
                print "Thanks for playing!"
                sys.exit(0)

            board = None

        player_turn = not player_turn

if __name__ == '__main__':
    start_game()
