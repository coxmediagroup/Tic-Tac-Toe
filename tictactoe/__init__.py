import string
from board import Board, BadMoveError
from ai import AI, ABAI


def play(ai_type=0):
    """ would you like to play a game of Tic-Tac-Toe? """
    humanx = True
    humany = True
    tempp = None
    while True:
        tempp =  raw_input('is X human?(y/n): ')
        if tempp == 'n':
            humanx = False
            break
        if tempp == 'y':
            break
        print """please answer with 'y' or 'n'"""

    tempp = None
    while True:
        tempp = raw_input('is O human?(y/n): ')
        if tempp == 'n':
            humany = False
            break
        if tempp == 'y':
            break
        print """please answer with 'y' or 'n'"""

    ai = None
    if (not humanx) or (not humany):
        if ai_type == 0:
            ai = AI()
        else:
            ai = ABAI()

    board = Board()

    while not board.win_check() and board.legal_moves():
        if board.next_move == 1:
            player = 'X'
            human = humanx 
        else:
            player = 'O'
            human = humany

        if human:
            while True:
                try:
                    xstr, ystr = string.split(raw_input('What is your move?(coordinates seperated by a space): '))
                    move = (int(xstr),int(ystr))
                    board.move(move[0],move[1])
                    break
                except BadMoveError:
                    print "please make a valid move"
                except ValueError:
                    print "please enter two coordinates"
            
        else:
            move = ai.find_move(board)
            board.move(move[0],move[1])

        print board
        print player + ' moved ' + str(move)

    winner =  board.win_check()
    if winner == 1:
        print "X won the game"
    if winner is None:
        print "The game was a tie"
    else:
        print "O won the game"
    


