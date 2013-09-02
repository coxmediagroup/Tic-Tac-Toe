
class TicTacToe(object):
    def __init__(self):
        self.newGame()

    def newGame(self):
        self.board = '012345678'
        self.winner = None
        self.turn = 1

    def newMove(self, player, position):
        self.board.replace(position, player)

    def isGameOver(self):

        # Temp hack to make sure everything's working...
        if len(self.board) is 10:
            self.winner = True

        if self.winner is None:
            return False

        return True


    def printBoard(self):
        print '\n {} | {} | {}\n - - - - - \n {} | {} | {}\n - - - - - \n {} | {} | {}'.format(
            self.board[0], self.board[1], self.board[2],
            self.board[3], self.board[4], self.board[5],
            self.board[6], self.board[7], self.board[8])

    













def computerTurn(status, turn):
    print "Zorg's Turn"


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