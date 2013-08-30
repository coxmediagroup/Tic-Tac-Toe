def printStatus(status):
    print ' {} | {} | {}\n-----------\n {} | {} | {}\n-----------\n {} | {} | {}'.format(
        status[0], status[1], status[2],
        status[3], status[4], status[5],
        status[6], status[7], status[8])

def computerTurn(status):
    print "Computer's Turn"
    if status == '123456789':
        return 'X23456789'
    elif status == 'XO3456789':
        return 'XO34X6789'
    elif status == 'XOO4X6789':
        return 'XOO4X678XV'
    else:
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

def main():
    status = '123456789'

    print """Welcome to Unfair Tic-Tac-Toe!
Where the computer always wins!

The rules are simple; simply type in the number of the
availible space you wish to place your marker."""
    printStatus(status)
    while True:
        status = computerTurn(status)
        printStatus(status)
        if len(status) is 10:
            print 'The computer is Victorious'
            break

        status = userTurn(status)
        printStatus(status)

if __name__ == "__main__":
    main()
