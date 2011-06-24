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
        for i in range(grid_size):
            for j in range(grid_size):
                cell = HTML("&nbsp;")
#                cell.setVisible(False)  # causes to ignore click events
                cell.position = (i, j)  # might be handy at some point
                cell.setStyleName("cell_O")
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
        sender.setHTML("X")
        sender.setStyleName("cell_X")

class TicTacToe(HorizontalPanel):
    def __init__(self, grid_size):
        HorizontalPanel.__init__(self)
        board = GameBoard(grid_size)
        self.add(board)
        self.setStyleName("hpanel")

        # debug
#        board = self.getChildren()[0]
#        board.setMark()

if __name__ == '__main__':
    game = TicTacToe(3)
    RootPanel().add(game)

    pyjd.run()
