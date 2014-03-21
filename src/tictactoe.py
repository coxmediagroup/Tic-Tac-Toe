'''
@author: Corey Hutton
'''
import Tkinter
from math import sqrt

class TicTacToe(object):
    '''
    A simple Tic-Tac-Toe game in which the computer cannot lose.
    '''
    BOARD_DEFAULTS = {'bd': 2,
                      'bg': 'white',
                      'cursor': 'dot',
                      'height': 515,
                      'highlightcolor': 'yellow',
                      'width': 515}
    O_DEFAULTS = {'fill': 'blue'}
    X_DEFAULTS = {'fill': 'red'}

    def __init__(self, *args, **kwargs):
        '''
        '''
        self.drawBoard(kwargs['master'])

    def drawBoard(self, master):
        board = Tkinter.Canvas(master, self.BOARD_DEFAULTS)

        x1 = self.BOARD_DEFAULTS['width'] / 3
        x2 = 2 * x1
        y1 = self.BOARD_DEFAULTS['height'] / 3
        y2 = 2 * y1
        board.create_line(x1, 0, x1, self.BOARD_DEFAULTS['height'])
        board.create_line(x2, 0, x2, self.BOARD_DEFAULTS['height'])
        board.create_line(0, y1, self.BOARD_DEFAULTS['width'], y1)
        board.create_line(0, y2, self.BOARD_DEFAULTS['width'], y2)

        resetButton = Tkinter.Button(master, text="Reset", command=self.reset())

        exitButton = Tkinter.Button(master, text ="Exit",
                                    command=master.destroy)

        board.grid(row=0, column=0, columnspan=2)
        resetButton.grid(row=1, column=0)
        exitButton.grid(row=1, column=1)

    def drawO(self, board, x1, y1, x2, y2):
        oWidth = self.BOARD_DEFAULTS['width'] / 12
        board.create_oval(x1, y1, x2, y2, self.O_DEFAULTS)
        board.create_oval(x1 + oWidth, y1 + oWidth, x2 - oWidth, y2 - oWidth,
                          fill=self.BOARD_DEFAULTS['bg'])

    def drawShape(self, board, shape, column, row):
        padding = 10

        side = (self.BOARD_DEFAULTS['width'] / 3)
        startX = (column - 1) * side + padding
        startY = (row - 1) * side + padding

        if shape == "O":
            self.drawO(board, startX, startY,
                       column * side - padding, row * side - padding)
        elif shape == "X":
            self.drawX(board, side - (2 * padding), startX, startY)

    def drawX(self, board, side, x, y):
        sqrt2 = sqrt(2) / 2
        board.create_polygon(side / 5 + x, y,
                             side / 2 + x, side / 2 - (side / 5 * sqrt2) + y,
                             4 * side / 5 + x, y,
                             side + x, side / 5 + y,
                             side / 2 + (side / 5 * sqrt2) + x, side / 2 + y,
                             side + x, 4 * side / 5 + y,
                             4 * side / 5 + x, side + y,
                             side / 2 + x, side / 2 + (side / 5 * sqrt2) + y,
                             side / 5 + x, side + y,
                             x, 4 * side / 5 + y,
                             side / 2 - (side / 5 * sqrt2) + x, side / 2 + y,
                             x, side / 5 + y,
                             self.X_DEFAULTS)

    def reset(self):
        pass
