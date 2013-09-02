from ai import TicTacToe, zorgAI

def playZorg(player1=True):

    ''' play a game against the Zorg TicTacToe engine. '''
    ''' We'll assume we get to move first, as player1 '''

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
        print 'Zorg has not lost the game!'


def playMultiplayer():

    ''' Let the humans duke it out against each other. '''

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

        action = raw_input("Who would you like to play? \n (Z)org AI,\n (H)uman Player, or \n (Q)uit: \n")
        
        if action.lower() == 'z':
            action = raw_input("Do you want to Move 1st (y/n)? ")
            
            if action.lower()[:1] == 'y':
                playZorg(False)
            else:
                playZorg()

        elif action.lower() == 'h':
            playMultiplayer()

        elif action.lower() == 'q':
            print 'Goodbye'
            break

        else:
            print 'I don\'t understand what you\'re trying to say. Options are Z, M, Q.'

if __name__ == "__main__":
    main()






