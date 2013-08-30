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
                pass
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
                pass
            else:
                return status.replace('3', 'X') + 'V'
        elif status[8] is 'X':
            pass

    elif turn is 4:
        if status[4] is 'X' and status[6] is 'X':
            if status[3] is 'O':
                return status.replace('2', 'X') + 'V'
            else:
                return status.replace('3', 'X') + 'V'
        elif status[4] is 'X' and status[2] is 'X':
            if status[1] is 'O':
                return status.replace('6', 'X') + 'V'
            else:
                return status.replace('1', 'X') + 'V'

    return status

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
    return len(status) is 10

def main():
    status = '012345678'
    turn = 1

    print """Welcome to Unfair Tic-Tac-Toe!
Where the computer always wins!

The rules are simple; simply type in the number of the
availible space you wish to place your marker."""
    printStatus(status)
    while True:
        status = computerTurn(status, turn)
        printStatus(status)
        if testWinner(status):
            print 'The computer is Victorious'
            break

        status = userTurn(status)
        printStatus(status)
        turn += 1

if __name__ == "__main__":
    main()
