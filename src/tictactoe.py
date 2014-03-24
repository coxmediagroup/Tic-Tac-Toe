'''
@author: Corey Hutton
'''
from math import sqrt
from random import random, randrange
from Tkinter import Button, Canvas

class TicTacToe(object):
    '''
    A simple Tic-Tac-Toe game in which the computer cannot lose.
    '''
    # Range of values in milliseconds used to generate a random length of time
    # to delay computer play to simulate "thinking".
    CP_WAIT_MIN = 250
    CP_WAIT_MAX = 850

    # UI default settings. Set width to equal height to ensure a square board.
    BOARD_DEFAULTS = {'bd': 2,
                      'bg': 'white',
                      'cursor': 'dot',
                      'height': 515,
                      'highlightcolor': 'yellow'}
    BOARD_DEFAULTS['width'] = BOARD_DEFAULTS['height']
    LINE_DEFAULTS = {'width': 4}
    O_DEFAULTS = {'fill': 'blue',
                  'tags': 'O'}
    X_DEFAULTS = {'fill': 'red',
                  'tags': 'X'}

    # An empty array representation of the state of the board.
    DEFAULT_STATE = [[None, None, None], [None, None, None], [None, None, None]]
    state = [x[:] for x in DEFAULT_STATE]

    board = None # The game board UI object.
    player = None # The human player's symbol: "X" or "O".
    playerTurn = None # Whether it is the human player's turn.

    def __init__(self, *args, **kwargs):
        '''
        Initializes the game by drawing the game board and "resetting" it.

        NB: A keyword argument 'master' should be provided that identifies
            the master Tkinter UI object.
        '''
        self.drawBoard(kwargs['master'])
        self.reset()

    def canWin(self, value):
        '''
        Searches the game board for two in a row of a given symbol (e.g.: 'X',
        'X', None) and returns the coordinates of the empty space.

        @param value: A string containing the player symbol to search for.
        @return: A tuple pair of indices for the empty space if the search
                 succeeds; False if it does not.
        '''
        for x in xrange(3):
            # Check rows.
            if self.state[x][0] == value:
                if self.state[x][1] == value and self.state[x][2] is None:
                    return (x, 2)
                elif self.state[x][2] == value and self.state[x][1] is None:
                    return (x, 1)
            elif self.state[x][0] is None and self.state[x][1] == value \
                                          and self.state[x][2] == value:
                return (x, 0)
            # Check columns.
            if self.state[0][x] == value:
                if self.state[1][x] == value and self.state[2][x] is None:
                    return (2, x)
                elif self.state[2][x] == value and self.state[1][x] is None:
                    return (1, x)
            elif self.state[0][x] is None and self.state[1][x] == value \
                                          and self.state[2][x] == value:
                return (0, x)

        # Check diagonals.
        if self.state[0][0] == value:
            if self.state[1][1] == value and self.state[2][2] is None:
                return (2, 2)
            elif self.state[2][2] == value and self.state[1][1] is None:
                return (1, 1)
        elif self.state[0][0] is None and self.state[1][1] == value \
                                      and self.state[2][2] == value:
            return (0, 0)
        elif self.state[2][0] == value:
            if self.state[1][1] == value and self.state[0][2] is None:
                return (0, 2)
            elif self.state[0][2] == value and self.state[1][1] is None:
                return (1, 1)
        elif self.state[2][0] is None and self.state[1][1] == value \
                                      and self.state[0][2] == value:
            return (2, 0)

        return False

    def checkWin(self, value):
        '''
        Checks the game board for three in a row of a given symbol and returns
        the identifier of the row (e.g., 'r1' for the middle row).

        @param value: A string containing the player symbol to search for.
        @return: A string specifying in which row ('r'), column ('c'), or
                 diagonal ('d') three matching symbols are found.
        '''
        for x in xrange(3):
            if self.state[x][0] == value and self.state[x][1] == value \
                                         and self.state[x][2]  == value:
                return 'r%d' % x
            elif self.state[0][x] == value and self.state[1][x] == value \
                                           and self.state[2][x]  == value:
                return 'c%d' % x

        if self.state[0][0] == value and self.state[1][1] == value and \
                                         self.state[2][2] == value:
                return 'd1'
        elif self.state[2][0] == value and self.state[1][1] == value and \
                                           self.state[0][2] == value:
                return 'd2'

        return False

    def computerTurn(self):
        '''
        Performs a turn for the computer player.
        '''
        # Win
        canWin = self.canWin(self.computer)
        if canWin:
            self.makeMove(self.computer, canWin[0], canWin[1])
            return

        # Block Win
        canBlock = self.canWin(self.player)
        if canBlock:
            self.makeMove(self.computer, canBlock[0], canBlock[1])
            return

        # Make Fork

        # Block Fork

        # Play Center
        if self.state[1][1] is None:
            self.makeMove(self.computer, 1, 1)
            return

        # Play Opposite Corner

        # Play Corner
        CORNER_SPACES = ((0, 0), (0, 2), (2, 0), (2, 2))
        for x, y in CORNER_SPACES:
            if self.state[0][0] is None:
                self.makeMove(self.computer, 0, 0)
                return

        # Play Side
        SIDE_SPACES = ((0, 1), (1, 0), (1, 2), (2, 1))
        for x, y in SIDE_SPACES:
            if self.state[x][y] is None:
                self.makeMove(self.computer, x, y)
                return

    def doClick(self, event):
        '''
        Callback method for the game board's click event.

        @param event: The Tkinter-supplied click event object.
        '''
        if self.playerTurn:
            width = self.BOARD_DEFAULTS['width'] / 3
            height = self.BOARD_DEFAULTS['height'] / 3

            x = 0 if event.x < width else (1 if event.x < 2 * width else 2)
            y = 0 if event.y < height else (1 if event.y < 2 * height else 2)

            self.makeMove(self.player, x, y)

    def drawBoard(self, master):
        '''
        Draws the game board and related UI elements.

        @param master: The master Tkinter UI object.
        '''
        x1 = self.BOARD_DEFAULTS['width'] / 3
        x2 = 2 * x1
        y1 = self.BOARD_DEFAULTS['height'] / 3
        y2 = 2 * y1

        self.board = Canvas(master, self.BOARD_DEFAULTS)
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
        '''
        Draws an "O" symbol on the game board.

        @param x1: An integer specifying where along the x-axis to begin the box
                   bounding the O.
        @param y1: An integer specifying where along the y-axis to begin the box
                   bounding the O.
        @param x2: An integer specifying where along the x-axis to end the box
                   bounding the O.
        @param y2: An integer specifying where along the y-axis to end the box
                   bounding the O.
        '''
        oWidth = self.BOARD_DEFAULTS['width'] / 12

        self.board.create_oval(x1, y1, x2, y2, self.O_DEFAULTS)
        self.board.create_oval(x1 + oWidth, y1 + oWidth,
                               x2 - oWidth, y2 - oWidth,
                               fill=self.BOARD_DEFAULTS['bg'],
                               tags=self.O_DEFAULTS['tags'])

    def drawSymbol(self, symbol, column, row):
        '''
        Draws an X or O in a space on the game board.

        @param symbol: A string containing the player symbol to draw.
        @param column: An integer index of the column being played on.
        @param row: An integer index of the row being played on.
        '''
        padding = 10

        side = self.BOARD_DEFAULTS['width'] / 3
        startX = column * side + padding
        startY = row * side + padding

        if symbol == 'O':
            self.drawO(startX, startY, (column + 1) * side - padding,
                                       (row + 1) * side - padding)
        elif symbol == 'X':
            self.drawX(side - 2 * padding, startX, startY)

    def drawWin(self, row):
        '''
        Draws a line through a row, column, or diagonal on the game board.

        @param row: A string specifying over which row ('r'), column ('c'), or
                    diagonal ('d') to draw a line.
        '''
        length = self.BOARD_DEFAULTS['width']
        sixth = length / 6

        for x in xrange(3):
            strx = str(x)
            if row[1] == strx:
                if row[0] == 'r':
                    r = (sixth, 0, sixth, (2 * x + 1) * length)
                    tags = self.state[x][0]
                elif row[0] == 'c':
                    r = (0, sixth, (2 * x + 1) * length, sixth)
                    tags = self.state[0][x]
                elif row[0] == 'd':
                    d = {'1': (0, 0, length, length),
                         '2': (length, length, 0, 0)}
                    r = d[strx]
                    tags = self.state[1][1]

                self.board.create_line(r, self.LINE_DEFAULTS, tags=tags)

    def drawX(self, side, x, y):
        '''
        Draws an "X" symbol on the game board.

        @param side: An integer specifying the length of one side of the box
                     bounding the X.
        @param x: An integer specifying where along the x-axis to begin the box
                  bounding the X.
        @param y: An integer specifying where along the y-axis to begin the box
                  bounding the X.
        '''
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

    def makeMove(self, symbol, column, row):
        '''
        Validates (i.e., checks if the desired space is empty) and executes a
        move by either player, then checks the game board for a win.

        @param symbol: A string containing the player symbol to draw.
        @param column: An integer index of the column being played on.
        @param row: An integer index of the row being played on.
        '''
        # Check that this is a valid move: the space's value should be None.
        if not bool(self.state[column][row]):
            self.drawSymbol(symbol, column, row)
            self.state[column][row] = symbol
            self.playerTurn = not self.playerTurn

            checkWin = self.checkWin(symbol)
            if checkWin:
                self.player = None
                self.playerTurn = False
                self.drawWin(checkWin)
            elif symbol == self.player:
                # The computer playing instantly is disconcerting.
                self.board.after(randrange(self.CP_WAIT_MIN, self.CP_WAIT_MAX),
                                 self.computerTurn)

    def reset(self):
        '''
        Resets the players, game board, and game state. Initiates the first
        turn if the computer is X.
        '''
        self.player = None
        self.board.delete('O')
        self.board.delete('X')
        self.state = [x[:] for x in self.DEFAULT_STATE]

        # Choose players randomly. X goes first.
        if random() > 0.5:
            self.player = 'X'
            self.computer = 'O'
            self.playerTurn = True
        else:
            self.player = 'O'
            self.computer = 'X'
            self.playerTurn = False
            self.computerTurn()
