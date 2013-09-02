from ai import computerTurn, TicTacToe, zorgAI

def playNewGame():
    ttt = TicTacToe()
    ttt.newGame()

    while True:
        ttt.board = computerTurn(ttt.board, ttt.turn)
        ttt.drawBoard()
        if ttt.isGameOver():
            break
        ttt.humanMove()
        ttt.turn += 1


def playZorg():
    ttt = TicTacToe()
    ttt.newGame()

    zorg = zorgAI(ttt)

    while True:
        zorg.makeMove()
        ttt.drawBoard()
        if ttt.isGameOver:
            break
        ttt.humanMove('O')
        ttt.turn += 1

    if ttt.winner:
        print ttt.winner + ' has won!'

    else:
        print 'Tie game!'


def main():
    print """Welcome to Tic-Tac-Toe!"""

    while True:
        action = raw_input("(N)ew Game, (Q)uit:\n")
        if action is 'N' or action is 'n':
            # playNewGame()
            playZorg()
        elif action is 'Q' or action is 'q':
            print 'Goodbye'
            break
        else:
            print 'Invalid Command'

if __name__ == "__main__":
    main()






