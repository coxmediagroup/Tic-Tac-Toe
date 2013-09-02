import sys

''' Originally derrived from https://github.com/mindbane/Tic-Tac-Toe '''
''' Snippets borrowed from https://github.com/jmichalicek/Tic-Tac-Toe '''
''' Refactoring performed by Wade Williams '''

class TicTacToe(object):
    
    # wins tuple is an efficient way to check and search for wins.
    # original by jmichalicek
    wins = ((0, 1, 2), # rows
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6), # columns
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8), # diagonals
            (2, 4, 6))


    def newGame(self):
        ''' Set up All Of The Things '''
        self.board = [None, None, None,
                      None, None, None,
                      None, None, None]

        self.winner = None
        self.turn = 1
        self.isGameOver = False
        self.drawBoard()


    def newMove(self, player, position):
        self.board[position] = player
        self.drawBoard()
        self.checkForWin(player)


    def checkForWin(self, player):
        ''' Read the board and check to see if the game is over. '''
        # original by jmichalicek
        for group in self.wins:
            if self.board[group[0]] == player \
                    and self.board[group[1]] == player \
                    and self.board[group[2]] == player:
                
                self.winner = player
                
                self.isGameOver = True
                break

        # If there's no moves left and no winner, its a tie.
        if None not in self.board and self.winner is None:
            self.winner = False
            self.isGameOver = True



    def humanMove(self, player):
        # original by mindbane
        move = '?'
        while True:
            move = raw_input("Select Move:\n")

            try:
                move = int(move)
            except ValueError:
                print "Please enter the position number you wish to move to."
            else:
                if self.board[move] is not None:
                    print "That position is already occupied."
                else:
                    break

        self.newMove(player, move)


    def drawBoard(self):
        # original by jmichalicek
        
        """Draw the game board on screen"""
        # ANSI code to clear the screen
        print chr(27) + "[2J"
        for position, value in enumerate(self.board):
            if value is None:
                sys.stdout.write(str(position))
            else:
                sys.stdout.write(str(value))

            if (position + 1) % 3 != 0:
                sys.stdout.write('|')
            else:
                print ''

            if position == 2 or position == 5:
                print '-' * 5



class zorgAI():

    def __init__(self, ttt):
        self.ttt = ttt

    def lookForWin(self, player):
        # Original by jmichalicek
        """Find a space which allows a win for the given player"""

        win_spot = None
        
        for group in self.ttt.wins:
            # creates a list of just the elements of the board which are
            # part of a specific win group and and not already owned by the player
            # and creates a list of tuples of the element and its value.
            not_mine = [(i, val) for i, val in enumerate(self.ttt.board)
                        if i in group
                        and val != player]

            # If there's only one not owned by the ai player and not owned by
            # the other player then select it and we've won
            if len(not_mine) == 1 and not_mine[0][1] is None:
                # Maybe this should return the selection rather than
                # modifying the board in here.  Decide later.
                win_spot = not_mine[0][0]
                break

        return win_spot

    def makeMove(self):

        if self.ttt.turn is 1:
            self.ttt.newMove('X', 0)
            return self.ttt.board

        else:

            # Check to see if we can win, right now.
            winningMove = self.lookForWin('X')

            if winningMove is not None:
                self.ttt.newMove('X', winningMove)
                return self.ttt.board


            # Don't let the oponent win, ever.
            blockMove = self.lookForWin('O')
            
            if blockMove is not None:
                self.ttt.newMove('X', blockMove)
                return self.ttt.board


            # Otherwise we're free to play a strategy.
            if self.ttt.board[4] is None:
                self.ttt.newMove('X', 4)
            elif self.ttt.board[8] is None:
                self.ttt.newMove('X', 8)

            else: # Just go anywhere, we're here to stop them from winning.
                for move, value in enumerate(self.ttt.board):
                    if move is None:
                        self.ttt.newMove('X', value)



def computerTurn(status, turn):
    print "Zorg's Turn"


    if turn is 1:
        status[0] = 'X'
        return status

    elif turn is 2:
        if status[2] is 'O':
            status[6] = 'X'
            return status
        elif status[4] is 'O':
            status[8] = 'X'
            return status
        elif status[6] is 'O' or status[8] is 'O':
            status[2] = 'X'
            return status
        else:
            status[4] = 'X'
            return status

    elif turn is 3:
        if status[2] is 'X':
            if status[1] is 'O':
                if status[6] is 'O':
                    status[8] = 'X'
                    return status
                else:
                    status[6] = 'X'
                    return status
            else:
                status[1] = 'X' + 'V'
                return status
        elif status[4] is 'X':
            if status[8] is 'O':
                if status[1] is 'O' or status[7] is 'O':
                    status[6] = 'X'
                    return status
                elif status[3] is 'O' or status[5] is 'O':
                    status[2] = 'X'
                    return status
            else:
                status[8] = 'X' + 'V'
                return status
        elif status[6] is 'X':
            if status[3] is 'O':
                status[8] = 'X'
                return status
            else:
                status[3] = 'X' + 'V'
                return status
        else:
            if status[1] is 'O':
                status[7] = 'X'
                return status
            elif status[2] is 'O':
                status[6] = 'X'
                return status
            elif status[3] is 'O':
                status[5] = 'X'
                return status
            elif status[5] is 'O':
                status[3] = 'X'
                return status
            elif status[6] is 'O':
                status[2] = 'X'
                return status
            else:
                status[1] = 'X'
                return status

    elif turn is 4:
        if status[1] is 'X' and status[8] is 'X':
            if status[2] is 'O':
                status[6] = 'X'
                return status
            else:
                status[2] = 'X' + 'V'
                return status
        elif status[2] is 'X' and status[4] is 'X':
            if status[1] is 'O':
                status[6] = 'X' + 'V'
                return status
            else:
                status[1] = 'X' + 'V'
                return status
        elif status[2] is 'X' and status[6] is 'X':
            if status[3] is 'O':
                status[4] = 'X' + 'V'
                return status
            else:
                status[3] = 'X' + 'V'
                return status
        elif status[2] is 'X' and status[8] is 'X':
            if status[4] is 'O':
                if status[1] is 'O':
                    status[5] = 'X' + 'V'
                    return status
                else:
                    status[1] = 'X' + 'V'
                    return status
            else:
                if status[5] is 'O':
                    status[4] = 'X' + 'V'
                    return status
                else:
                    status[5] = 'X' + 'V'
                    return status
        elif status[3] is 'X' and status[8] is 'X':
            if status[6] is 'O':
                status[2] = 'X'
                return status
            else:
                status[6] = 'X' + 'V'
                return status
        elif status[4] is 'X' and status[6] is 'X':
            if status[3] is 'O':
                status[2] = 'X' + 'V'
                return status
            else:
                status[3] = 'X' + 'V'
                return status
        elif status[5] is 'X' and status[8] is 'X':
            if status[2] is 'O':
                status[6] = 'X'
                return status
            else:
                status[2] = 'X' + 'V'
                return status
        elif status[6] is 'X' and status[8] is 'X':
            if status[4] is 'O':
                if status[3] is 'O':
                    status[7] = 'X' + 'V'
                    return status
                else:
                    status[3] = 'X' + 'V'
                    return status
            else:
                if status[7] is 'O':
                    status[4] = 'X' + 'V'
                    return status
                else:
                    status[7] = 'X' + 'V'
                    return status
        elif status[7] is 'X' and status[8] is 'X':
            if status[6] is 'O':
                status[2] = 'X'
                return status
            else:
                status[6] = 'X' + 'V'
                return status

    else:
        if status[1] is '1':
            atus = status[1] = 'X'
            return status
            if status[0] is 'X' and status[2] is 'X':
                return status + 'V'
            else:
                return status + 'T'
        elif status[3] is '3':
            atus = status[3] = 'X'
            return status
            if status[0] is 'X' and status[6] is 'X':
                return status + 'V'
            else:
                return status + 'T'
        elif status[5] is '5':
            atus = status[5] = 'X'
            return status
            if status[2] is 'X' and status[8] is 'X':
                return status + 'V'
            else:
                return status + 'T'
        elif status[7] is '7':
            atus = status[7] = 'X'
            return status
            if status[6] is 'X' and status[8] is 'X':
                return status + 'V'
            else:
                return status + 'T'