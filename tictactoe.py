from ai import computerTurn, TicTacToe

def userTurn(status):
    move = '?'
    while True:
        move = raw_input("Select Move:\n")
        if move not in status or len(move) is not 1:
            print "Invalid Move"
        else:
            break

    return status.replace(move, 'O')


def playNewGame():
    ttt = TicTacToe()
    ttt.printBoard()
    while True:
        ttt.board = computerTurn(ttt.board, ttt.turn)
        ttt.printBoard()
        if ttt.isGameOver():
            break
        ttt.board = userTurn(ttt.board)
        ttt.printBoard()
        ttt.turn += 1


def main():
    print """Welcome to Tic-Tac-Toe!"""

    while True:
        action = raw_input("(N)ew Game, (Q)uit:\n")
        if action is 'N' or action is 'n':
            playNewGame()
        elif action is 'Q' or action is 'q':
            print 'Goodbye'
            break
        else:
            print 'Invalid Command'


if __name__ == "__main__":
    main()






