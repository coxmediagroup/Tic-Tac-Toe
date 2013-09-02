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