'''
@author: Corey Hutton
'''
from math import sqrt
from Tkinter import Button, Canvas
from tkMessageBox import askyesno

class TicTacToe(object):
    '''
    A simple Tic-Tac-Toe game in which the computer cannot lose.
    '''
    # UI default settings.
    BOARD_DEFAULTS = {'bd': 2,
                      'bg': 'white',
                      'cursor': 'dot',
                      'height': 515,
                      'highlightcolor': 'yellow'}
    BOARD_DEFAULTS['width'] = BOARD_DEFAULTS['height'] # Ensures a square board.
    O_DEFAULTS = {'fill': 'blue',
                  'tags': 'O'}
    X_DEFAULTS = {'fill': 'red',
                  'tags': 'X'}

    # An empty array representation of the state of the board.
    DEFAULT_STATE = [[None, None, None],
                     [None, None, None],
                     [None, None, None]]
    state = list(DEFAULT_STATE)

    board = None # The board UI object.
    player = None # The human player's shape: "X" or "O".
    playerTurn = False # Whether it is the human player's turn.

    def __init__(self, *args, **kwargs):
        self.drawBoard(kwargs['master'])
        self.reset()

    def choosePlayers(self):
        if askyesno('Choose Players', 'Do you want to go first?',
                    parent=self.board.master):
            self.player = 'X'
            self.playerTurn = True
        else:
            self.player = 'O'

    def doClick(self, event):
        if not self.playerTurn:
            return

        width = self.BOARD_DEFAULTS['width'] / 3
        height = self.BOARD_DEFAULTS['height'] / 3

        x = 2
        if event.x < 2 * width:
            if event.x < width:
                x = 0
            else:
                x = 1

        y = 2
        if event.y < 2 * height:
            if event.y < height:
                y = 0
            else:
                y = 1

        self.makeMove(x, y)

    def drawBoard(self, master):
        self.board = Canvas(master, self.BOARD_DEFAULTS)

        x1 = self.BOARD_DEFAULTS['width'] / 3
        x2 = 2 * x1
        y1 = self.BOARD_DEFAULTS['height'] / 3
        y2 = 2 * y1
        self.board.create_line(x1, 0, x1, self.BOARD_DEFAULTS['height'])
        self.board.create_line(x2, 0, x2, self.BOARD_DEFAULTS['height'])
        self.board.create_line(0, y1, self.BOARD_DEFAULTS['width'], y1)
        self.board.create_line(0, y2, self.BOARD_DEFAULTS['width'], y2)

        self.board.bind('<Button-1>', self.doClick)

        resetButton = Button(master, text='Reset', command=self.reset)

        exitButton = Button(master, text ='Exit',
                                    command=master.destroy)

        self.board.grid(row=0, column=0, columnspan=2)
        resetButton.grid(row=1, column=0)
        exitButton.grid(row=1, column=1)

    def drawO(self, x1, y1, x2, y2):
        oWidth = self.BOARD_DEFAULTS['width'] / 12

        self.board.create_oval(x1, y1, x2, y2, self.O_DEFAULTS)
        self.board.create_oval(x1 + oWidth, y1 + oWidth,
                               x2 - oWidth, y2 - oWidth,
                               fill=self.BOARD_DEFAULTS['bg'],
                               tags=self.O_DEFAULTS['tags'])

    def drawShape(self, shape, column, row):
        padding = 10

        side = (self.BOARD_DEFAULTS['width'] / 3)
        startX = column * side + padding
        startY = row * side + padding

        if shape == 'O':
            self.drawO(startX, startY, (column + 1) * side - padding,
                                       (row + 1) * side - padding)
        elif shape == 'X':
            self.drawX(side - (2 * padding), startX, startY)

    def drawX(self, side, x, y):
        sqrt2 = sqrt(2) / 2
        points = (side / 5 + x, y,
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
                  x, side / 5 + y)

        self.board.create_polygon(points, self.X_DEFAULTS)

    def isValidMove(self, column, row):
        return not bool(self.state[column][row])

    def makeMove(self, column, row):
        if self.isValidMove(column, row):
            self.drawShape(self.player, column, row)
            self.state[column][row] = self.player

    def reset(self):
        self.playerTurn = False
        self.player = None
        self.board.delete('O')
        self.board.delete('X')
        self.state = list(self.DEFAULT_STATE)
        self.choosePlayers()
