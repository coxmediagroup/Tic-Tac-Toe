import pyjd # this is dummy in pyjs.
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui.Grid import Grid
from pyjamas import Window

import pygwt

class GameBoard(Grid):
    def __init__(self, grid_size):
        Grid.__init__(self)

        # populate the grid with some stuff
        #
        self.resize(grid_size, grid_size)

        self.setBorderWidth(2)
        self.setCellPadding(4)
        self.setCellSpacing(1)

        self.setStyleName("gameboard") # just doesn't work

        # Set up game board 
        #
        # Note that must iterate over indices, rather than Cell
        # instances, until the table positions are set up here
        #
        index = 0   # debug
        for i in range(grid_size):
            for j in range(grid_size):
                cell = HTML("&nbsp;")
#                cell.setVisible(False)  # causes to ignore click events
                cell.position = (i, j)  # might be handy at some point
                index+=1; cell.index = index    # debug
#                cell.setStyleName("cell_O")
                cell.addClickListener(getattr(self, "onCellClicked"))
                self.setWidget(i, j, cell)

    def rows(self):
        """
        Build an array of Cell arrays
        """
        rows = []
        for i in range(self.getRowCount()):
            row = []
            for j in range(self.getCellCount(i)):
                widget = self.getWidget(i, j)
                row.append(widget)
            rows.append(row)
        return rows

    def setMark(self, mark="Z"):
        """
        Make all of the positions have the specified mark
        For debugging purposes, mainly
        """
        for row in self.rows():
            for cell in row:
                cell.setHTML(mark)

    def onCellClicked(self, sender):
        # to do: verify that sender still free
        sender.setHTML("X")
        sender.setStyleName("cell_X")

        perms = self.getRowPermutations()

        # debug
        for perm in perms:
            print [cell.index for cell in perm]
        return

        move_cell = None     # unless set below

        move_cell = self.getWinningMove(perms)  # sets game status to WIN

        if not move_cell:
            move_cell = self.getBlockingMovie(perms)

        if not move_cell:
            move_cell = self.getAnyMove()

        if not move_cell:
            # It's a draw, since the poor human never wins.
            #
            self.setGameStatus(GAME_DRAW)
            endGame()
        else:
            move_cell.setHTML('O')

        if not self.getAnyMove():
            # we took the last avail position
            #
            self.setGameStatus(GAME_DRAW)
            endGame()

    def getRowPermutations(self):
        """
        Use a matrix transformation to get every
        winning permutation.
        """
        board = self.rows()
        perms = []

        # build the diagonal from the element of this row which
        # matches its row index (row == col)
        #
        diag1 = []
        for i in range(len(board)):
            perms.append(board[i])  # add a "horizontal" row
            diag1.append(board[i][i])
        perms.append(diag1)

        # We've now gotten the (3) rows and (1) diagonal.
        # now invert self and get the other ones
        #
        board = rotateMatrix(board)

        diag2 = []
        for i in range(len(board)):
            perms.append(board[i])
            diag2.append(board[i][i])
        perms.append(diag2)

        return perms

    def __repr__(self):
        return self.rows()

def rotateMatrix(board):
    """
    Return a list of lists that represents a 90-degree
    rotation of the input 2-dimensional array.

    The original array elements, ordered differently, are returned.
    Note that we get no standard library 'copy' module here (a
    peculiarity of Pyjamas, presumably). So a shallow copy must
    be made manually.

    The "board[j][(size - 1) - i]" expression was arrived at almost
    empirically, after I discovered to my chagrin that my original
    transformation was actually an inversion over the down-right
    diagonal, thus depriving us of our needed 2nd diagonal as it doesn't
    get modified by the transform.

    Here is the mapping of row/col tuples from the original to the
    desired (rotated) matrix:
    0,0 -> 0,2
    0,1 -> 1,2
    0,2 -> 2,2
    1,0 -> 0,1
    1,1 -> 1,1
    ...

    """
    board_copy = []

    # make our copy
    #
    for row in board:
        row_copy = []
        for col in row:
            row_copy.append(col)
        board_copy.append(row_copy)

    # populate our copy
    #
    size = len(board)
    for i in range(size):
        for j in range(size):
            board_copy[i][j] = board[j][(size - 1) - i]

    # return our copy
    #
    return board_copy

class TicTacToe(HorizontalPanel):
    def __init__(self, grid_size):
        HorizontalPanel.__init__(self)
        board = GameBoard(grid_size)
        self.add(board)
        self.setStyleName("hpanel")

        # debug
#       board = self.getChildren()[0]
#       board.setMark()

def testInvert(board):
    board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    board = invertMatrix(board)
    print board

if __name__ == '__main__':
#    testInvert(board)   # debug
    game = TicTacToe(12)
    RootPanel().add(game)

    pyjd.run()
