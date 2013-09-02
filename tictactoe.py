from ai import TicTacToe, zorgAI

def playZorg():

    zorg = zorgAI()
    zorg.newGame()

    while True:
        zorg.makeMove()
        zorg.drawBoard()
        if zorg.isGameOver:
            break
        zorg.humanMove('O')

    if zorg.winner:
        print zorg.winner + ' has won!'
    else:
        print 'Tie game!'

def playMultiplayer():
    ttt = TicTacToe()
    ttt.newGame()

    while True:
        print 'Player X may move'
        ttt.humanMove('X')
        if ttt.isGameOver:
            break

        print 'Player O may move'
        ttt.humanMove('O')
        if ttt.isGameOver:
            break

    if ttt.winner:
        print ttt.winner + ' has won!'
    else:
        print 'Tie game!'

def main():
    print """Welcome to Tic-Tac-Toe!"""

    while True:
        action = raw_input("Play (Z)org AI, Play (M)ultiplayer, (Q)uit:\n")
        if action is 'Z' or action is 'z':
            # playNewGame()
            playZorg()
        elif action is 'M' or action is 'm':
            playMultiplayer()
        elif action is 'Q' or action is 'q':
            print 'Goodbye'
            break
        else:
            print 'Invalid Command'

if __name__ == "__main__":
    main()






