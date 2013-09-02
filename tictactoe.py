from ai import computerTurn, TicTacToe

def playNewGame():
    ttt = TicTacToe()
    
    while True:
        ttt.board = computerTurn(ttt.board, ttt.turn)
        ttt.printBoard()
        if ttt.isGameOver():
            break
        ttt.humanMove()
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






