from ai import TicTacToe, zorgAI

def playZorg(player1=True):

    zorg = zorgAI()
    zorg.newGame()

    if player1:
        while True:
            zorg.makeMove()
            zorg.drawBoard()
          
            if zorg.isGameOver:
                break
          
            zorg.humanMove('O')
            if zorg.isGameOver:
                break
    else:
        while True:
            zorg.humanMove('O')
            zorg.drawBoard()
          
            if zorg.isGameOver:
                break
          
            zorg.makeMove()
            if zorg.isGameOver:
                break

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
    print chr(27) + "[2J"
    print """Welcome to Tic-Tac-Toe!"""

    while True:
        action = raw_input("Play (Z)org AI, (M)ultiplayer, or (Q)uit: ")
        if action is 'Z' or action is 'z':
            action = raw_input("Do you want to Move (1)st or (2)nd? ")
            # playNewGame()
            if action is '1':
                playZorg(False)
            else:
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






