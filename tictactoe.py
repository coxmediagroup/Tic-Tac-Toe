from ai import computerTurn


def printBoard(status):
    print '\n {} | {} | {}\n - - - - - \n {} | {} | {}\n - - - - - \n {} | {} | {}'.format(
        status[0], status[1], status[2],
        status[3], status[4], status[5],
        status[6], status[7], status[8])

def isGameOver(status):
    if len(status) is 10:
        if status[9] is 'V':
            print 'The computer is victorious!'
        else:
            print 'You managed to tie.'
        return True
    return False


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
    status = '012345678'
    turn = 1
    printBoard(status)
    while True:
        status = computerTurn(status, turn)
        
        printBoard(status)

        if isGameOver(status):
            break

        status = userTurn(status)
        printBoard(status)
        turn += 1


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
