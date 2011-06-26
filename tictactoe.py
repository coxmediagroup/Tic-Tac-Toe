import pyjd # this is dummy in pyjs.
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui.Grid import Grid
from pyjamas import Window

import pygwt

SPACE = '&nbsp;'    # needed to hold initial col width

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
                cell = HTML(SPACE)
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
        PLAYER_COMPUTER = 'O'
        PLAYER_HUMAN    = 'X'

        # to do: verify that sender still free
        sender.setHTML(PLAYER_HUMAN)
        sender.setStyleName("cell_X")

        perms = self.getRowPermutations()

        move_cell = None     # unless set below

        move_cell = self.getWinningMove(perms, PLAYER_HUMAN)
        if move_cell:   # take the win
            move_cell.setHTML(PLAYER_COMPUTER)
        else:           # prevent a loss
            move_cell = self.getWinningMove(perms, PLAYER_COMPUTER)
            if move_cell:
                move_cell.setHTML(PLAYER_COMPUTER)
            else:       # just move somewhere
                move_cell = self.getAnyMove()
                if move_cell:
                    move_cell.setHTML(PLAYER_COMPUTER)
                """
                else:   # It's a draw, since the poor human never wins.
                    self.setGameStatus(GAME_DRAW)
                    endGame()
                """
        """
        if not self.getAnyMove():
            # we took the last avail position
            #
            self.setGameStatus(GAME_DRAW)
            endGame()
        """

    def getWinningMove(self, perms, player_mark):
        """
        Iterates over the input row permutations
        looking for any which are nearly complete.
        Returns the cell to be marked for the win,
        if such a cell exists (already two in a row).

        player_mark is the mark which, when looking
        for a winning move, terminates the poss for a
        row or, when looking for a "blocking" move,
        rules out the poss of there being one for the
        given row.

        If there is either a) more than one empty position or
        b) an opposing mark, then the retval is None for that row.

        Note: testing indicates too many positives in
        later stage of game or when several winning
        positions exist. We'll just hope this doesn't
        bite us, as the logic looks good.
        """

        """
        # debug/test
        perms = [
            [HTML("X"), HTML("X"), HTML(SPACE)],     # 0
            [HTML("X"), HTML(SPACE), HTML("X")],      # 2

            [HTML("X"), HTML(SPACE), HTML(SPACE)],
            [HTML(SPACE), HTML("X"), HTML(SPACE)],
            [HTML(SPACE), HTML(SPACE), HTML("X")],

            [HTML(SPACE), HTML("X"), HTML("O")],
        ]
        """

        retval = None
        i = 0
        for perm in perms:
            empty_count = 0
            for cell in perm:
                mark = cell.getHTML()
                if mark == SPACE: # possible winner
                    empty_count += 1
                    if empty_count <= 1:
                        retval = cell
                    else:
                        # not nearly complete
                        retval = None
                        break
                elif mark == player_mark:
                    # false hopes shattered
                    retval = None
                    break
            if retval:
                # Window.alert("getWinningMove: " + str(i))
                break   # turn this on after testing
            i += 1
        return retval

    def getAnyMove(self):
        """
        Return the first of
        a) center position
        b) corner position
        c) any position
        """

        retval = None
        cells = []  # holds the center and corner cells
        rows = self.rows()

        # get the center
        #
        grid_size = len(rows) 
        center = int(grid_size / 2)
        #print "getAnyMove: center: ", center

        center = rows[center][center]

        cells.append(center)
        #print "getAnyMove: center: ", center

        # get the corners
        #
        max = grid_size - 1
        corners = [
            rows[0][0],
            rows[0][max],
            rows[max][0],
            rows[max][max]
        ]
        for cell in corners:
            cells.append(cell)

        # get the first empty cell in case
        # neither the center or a corner is
        # available
        #
        for row in rows:
            for cell in row:
                if cell.getHTML() == SPACE:
                    cells.append(cell)

        for cell in cells:
            # cells are ordered in terms of priority:
            # center, corner and first empty
            #
            #print "getAnyMove: cell: ", cell.position
            if cell.getHTML() == SPACE:
                retval = cell
                break
        return retval

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
#       board = self.getChildren()[0]   # yes, this works
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
    game = TicTacToe(3) # supports arbitrary gameboard size
    RootPanel().add(game)

#    pyjd.run()
