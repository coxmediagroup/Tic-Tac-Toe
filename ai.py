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
        self.turn += 1
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
            move = raw_input("Choose your move:\n")

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

        print '\n'



class zorgAI(TicTacToe):

    def lookForWin(self, player):

        # Original by jmichalicek
        """Find a space which allows a win for the given player"""

        win_spot = None
        
        for group in self.wins:
            # creates a list of just the elements of the board which are
            # part of a specific win group and and not already owned by the player
            # and creates a list of tuples of the element and its value.
            not_mine = [(i, val) for i, val in enumerate(self.board)
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

        ''' Make the first move, top left corner. '''
        if self.turn is 1:
            self.newMove('X', 0)
            return self.board

        else:

            # Check to see if we can win, right now.
            winningMove = self.lookForWin('X')

            if winningMove is not None:
                self.newMove('X', winningMove)
                return self.board

            # Don't let the oponent win, ever.
            blockMove = self.lookForWin('O')
            
            if blockMove is not None:
                self.newMove('X', blockMove)
                return self.board

            # Otherwise we're free to play a more interesting strategy.
            return self.reallySimpleStrategy()
            

    def reallySimpleStrategy(self):

        if self.turn == 4:
            # The meatbag must have moved first.
            # Check to make sure they're not going to beat us with sneaky tricks.
            if (self.board[0] == 'O' and self.board[8] == 'O') or (self.board[2] == 'O' and self.board[6] == 'O'): 
                self.newMove('X', 1)
                return self.board

        elif self.board[4] is None:
            self.newMove('X', 4)
            return self.board

        elif self.board[8] is None:
            self.newMove('X', 8)
            return self.board

        else: # Just go anywhere, we're here to stop them from winning, remember?
            for key, value in enumerate(self.board):
                if value is None:
                    self.newMove('X', key)
                    return self.board

