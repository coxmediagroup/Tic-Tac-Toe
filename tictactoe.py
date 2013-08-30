import time

def printStatus(status):
    print '\n {} | {} | {}\n-----------\n {} | {} | {}\n-----------\n {} | {} | {}'.format(
        status[0], status[1], status[2],
        status[3], status[4], status[5],
        status[6], status[7], status[8])

def computerTurn(status, turn):
    print "Computer's Turn"
    if turn is 1:
        return status.replace('0', 'X')

    elif turn is 2:
        if status[2] is 'O':
            return status.replace('6', 'X')
        elif status[4] is 'O':
            return status.replace('8', 'X')
        elif status[6] is 'O' or status[8] is 'O':
            return status.replace('2', 'X')
        else:
            return status.replace('4', 'X')

    elif turn is 3:
        if status[2] is 'X':
            if status[1] is 'O':
                if status[6] is 'O':
                    return status.replace('8', 'X')
                else:
                    return status.replace('6', 'X')
            else:
                return status.replace('1', 'X') + 'V'
        elif status[4] is 'X':
            if status[8] is 'O':
                if status[1] is 'O' or status[7] is 'O':
                    return status.replace('6', 'X')
                elif status[3] is 'O' or status[5] is 'O':
                    return status.replace('2', 'X')
            else:
                return status.replace('8', 'X') + 'V'
        elif status[6] is 'X':
            if status[3] is 'O':
                return status.replace('8', 'X')
            else:
                return status.replace('3', 'X') + 'V'
        else:
            if status[1] is 'O':
                return status.replace('7', 'X')
            elif status[2] is 'O':
                return status.replace('6', 'X')
            elif status[3] is 'O':
                return status.replace('5', 'X')
            elif status[5] is 'O':
                return status.replace('3', 'X')
            elif status[6] is 'O':
                return status.replace('2', 'X')
            else:
                return status.replace('1', 'X')

    elif turn is 4:
        if status[1] is 'X' and status[8] is 'X':
            if status[2] is 'O':
                return status.replace('6', 'X')
            else:
                return status.replace('2', 'X') + 'V'
        elif status[2] is 'X' and status[4] is 'X':
            if status[1] is 'O':
                return status.replace('6', 'X') + 'V'
            else:
                return status.replace('1', 'X') + 'V'
        elif status[2] is 'X' and status[6] is 'X':
            if status[3] is 'O':
                return status.replace('4', 'X') + 'V'
            else:
                return status.replace('3', 'X') + 'V'
        elif status[2] is 'X' and status[8] is 'X':
            if status[4] is 'O':
                if status[1] is 'O':
                    return status.replace('5', 'X') + 'V'
                else:
                    return status.replace('1', 'X') + 'V'
            else:
                if status[5] is 'O':
                    return status.replace('4', 'X') + 'V'
                else:
                    return status.replace('5', 'X') + 'V'
        elif status[3] is 'X' and status[8] is 'X':
            if status[6] is 'O':
                return status.replace('2', 'X')
            else:
                return status.replace('6', 'X') + 'V'
        elif status[4] is 'X' and status[6] is 'X':
            if status[3] is 'O':
                return status.replace('2', 'X') + 'V'
            else:
                return status.replace('3', 'X') + 'V'
        elif status[5] is 'X' and status[8] is 'X':
            if status[2] is 'O':
                return status.replace('6', 'X')
            else:
                return status.replace('2', 'X') + 'V'
        elif status[6] is 'X' and status[8] is 'X':
            if status[4] is 'O':
                if status[3] is 'O':
                    return status.replace('7', 'X') + 'V'
                else:
                    return status.replace('3', 'X') + 'V'
            else:
                if status[7] is 'O':
                    return status.replace('4', 'X') + 'V'
                else:
                    return status.replace('7', 'X') + 'V'
        elif status[7] is 'X' and status[8] is 'X':
            if status[6] is 'O':
                return status.replace('2', 'X')
            else:
                return status.replace('6', 'X') + 'V'

    else:
        if status[1] is '1':
            status = status.replace('1', 'X')
            if status[0] is 'X' and status[2] is 'X':
                return status + 'V'
            else:
                return status + 'T'
        elif status[3] is '3':
            status = status.replace('3', 'X')
            if status[0] is 'X' and status[6] is 'X':
                return status + 'V'
            else:
                return status + 'T'
        elif status[5] is '5':
            status = status.replace('5', 'X')
            if status[2] is 'X' and status[8] is 'X':
                return status + 'V'
            else:
                return status + 'T'
        elif status[7] is '7':
            status = status.replace('7', 'X')
            if status[6] is 'X' and status[8] is 'X':
                return status + 'V'
            else:
                return status + 'T'

def userTurn(status):
    move = '?'
    while True:
        move = raw_input("Select Move:\n")
        if move not in status or len(move) is not 1:
            print "Invalid Move"
        else:
            break

    return status.replace(move, 'O')

def testWinner(status):
    if len(status) is 10:
        if status[9] is 'V':
            print 'The computer is victorious!'
        else:
            print 'You managed to tie.'
        return True
    return False

def main():
    status = '012345678'
    turn = 1

    print """Welcome to Unfair Tic-Tac-Toe!
Where the computer always wins!

The rules are simple; simply type in the number of the
availible space you wish to place your marker."""
    while True:
        action = raw_input("(N)ew Game, (Q)uit:\n")
        if action is 'N' or action is 'n':
            printStatus(status)
            while True:
                status = computerTurn(status, turn)
                time.sleep(0.5)
                printStatus(status)
                if testWinner(status):
                    break

                status = userTurn(status)
                printStatus(status)
                turn += 1
        elif action is 'Q' or action is 'q':
            print 'Goodbye'
            break
        else:
            print 'Invalid Command'

if __name__ == "__main__":
    main()
