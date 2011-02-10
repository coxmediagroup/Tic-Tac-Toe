#!/usr/bin/env python
# encoding: utf-8
"""
TicTacToeGui.py

Created by Fredrick Stakem on 2011-02-05.
Copyright (c) 2011 __Stakem Research__. All rights reserved.
"""

from Tkinter import *
from TicTacToe import *
from ComputerPlayer import *

class TicTacToeGui(object):
    
    # Static variables
    background_color = 'white'
    highlight_color = 'red'
    marker_color = 'blue'
    board_margins = 40
    square_margins = 18
    board_line_width = 5
    marker_line_width = 3
    canvas_init_width = 400
    canvas_init_height = 400
    board_upper_left_x = board_margins
    board_upper_left_y = board_margins
    
    def __init__(self, root):
        self.root = root
        self.computer_goes_first = True
        self.marker_positions = []
        self.board_width = 0
        self.board_height = 0
        self.width_of_square = 0
        self.height_of_square = 0
        self.game = TicTacToe()
        self.computer = ComputerPlayer(TicTacToe.players[0])
        
        self.root.title('Tic Tac Toe')
        self.setupMenu()
        self.canvas = Canvas(width=TicTacToeGui.canvas_init_width, height=TicTacToeGui.canvas_init_height, bg=TicTacToeGui.background_color)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.bind('<Configure>', self.resize)
        self.canvas.bind('<Button-1>', self.onCanvasClick)
        self.newGame()
        
    def setupMenu(self):
        menubar = Menu(self.root)
        mainmenu = Menu(menubar, tearoff=0)
        mainmenu.add_command(label="New Game", command=self.newGame)
        mainmenu.add_checkbutton(label="Move First", command=self.setStartingPlayer)
        mainmenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Game", menu=mainmenu)
        self.root.config(menu=menubar)
        
    def resize(self, event):
        self.canvas.delete(ALL)
        self.canvas.width = event.width
        self.canvas.height = event.height
        self.drawCanvas()
        
    def drawCanvas(self):
        self.recalculateCanvas()
        self.drawBoard()
        state = self.game.getCurrentGameState()
        for i, s in enumerate(state):
            coords = self.marker_positions[i]
            if s == TicTacToe.players[0]:
                self.drawX(coords[0], coords[1], coords[2])
            elif s == TicTacToe.players[1]:
                self.canvas.create_oval(coords[0], coords[1], coords[0] + coords[2], coords[1] + coords[2], width=TicTacToeGui.marker_line_width, fill=TicTacToeGui.background_color, outline=TicTacToeGui.marker_color)
           
    def recalculateCanvas(self):
        self.board_width = self.canvas.width - 2 * TicTacToeGui.board_margins
        self.board_height = self.canvas.height - 2 * TicTacToeGui.board_margins
        
        self.width_of_square = ( self.board_width - 2 * TicTacToeGui.board_line_width - 6 * TicTacToeGui.marker_line_width) / 3
        self.height_of_square = ( self.board_height - 2 * TicTacToeGui.board_line_width - 6 * TicTacToeGui.marker_line_width ) / 3
        self.marker_positions = []
        
        for i in range(9):
            coords = []
            column = i % 3
            row = i / 3

            coords.append( TicTacToeGui.board_margins + TicTacToeGui.square_margins + column * self.width_of_square + column * TicTacToeGui.board_line_width )
            coords.append( TicTacToeGui.board_margins + TicTacToeGui.square_margins + row * self.height_of_square + row * TicTacToeGui.board_line_width )
            coords.append( self.width_of_square - 2 * TicTacToeGui.square_margins )
            self.marker_positions.append( coords )
            
    def drawBoard(self):
        self.canvas.create_line(TicTacToeGui.board_upper_left_x + self.width_of_square, 
                                TicTacToeGui.board_upper_left_y, 
                                TicTacToeGui.board_upper_left_x + self.width_of_square, 
                                TicTacToeGui.board_upper_left_y + self.board_height, 
                                width=TicTacToeGui.board_line_width)
        self.canvas.create_line(TicTacToeGui.board_upper_left_x + 2 * self.width_of_square + TicTacToeGui.board_line_width, 
                                TicTacToeGui.board_upper_left_y, 
                                TicTacToeGui.board_upper_left_x + 2 * self.width_of_square + TicTacToeGui.board_line_width, 
                                TicTacToeGui.board_upper_left_y + self.board_height, 
                                width=TicTacToeGui.board_line_width)
        self.canvas.create_line(TicTacToeGui.board_upper_left_x, 
                                TicTacToeGui.board_upper_left_y + self.height_of_square, 
                                TicTacToeGui.board_upper_left_x + self.board_width, 
                                TicTacToeGui.board_upper_left_y + self.height_of_square, 
                                width=TicTacToeGui.board_line_width)
        self.canvas.create_line(TicTacToeGui.board_upper_left_x, 
                                TicTacToeGui.board_upper_left_y + 2 * self.height_of_square + TicTacToeGui.board_line_width, 
                                TicTacToeGui.board_upper_left_x + self.board_width, 
                                TicTacToeGui.board_upper_left_y + + 2 * self.height_of_square + TicTacToeGui.board_line_width, 
                                width=TicTacToeGui.board_line_width)
                 
    def drawX(self, x, y, width_height):
        self.canvas.create_line(x, y, x + width_height, y + width_height, width=TicTacToeGui.marker_line_width, fill=TicTacToeGui.marker_color)
        self.canvas.create_line(x + width_height, y, x, y + width_height, width=TicTacToeGui.marker_line_width, fill=TicTacToeGui.marker_color)
        
    def newGame(self):
        print "New game."
        self.game.newGame()
        if self.computer_goes_first:
            self.computer.newGame(TicTacToe.players[0])
        else:
            self.computer.newGame(TicTacToe.players[1])
        
    def setStartingPlayer(self):
        print "Set start player."
        
    def onCanvasClick(self, event):
        print "Clicked on canvas: " + str(event.x) + " " + str(event.y)
        
        
root = Tk()
gui = TicTacToeGui(root)
root.mainloop()



