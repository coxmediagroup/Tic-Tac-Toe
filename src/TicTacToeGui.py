#!/usr/bin/env python
# encoding: utf-8
"""
TicTacToeGui.py

Created by Fredrick Stakem on 2011-02-05.
Copyright (c) 2011 __Stakem Research__. All rights reserved.
"""

from Tkinter import *

def onCanvasClick(event):
    print "Clicked on canvas: " + str(event.x) + " " + str(event.y)
    
def onSquareClick(event):
    print "Clicked on square"
    
def drawCircle(canvas, x, y, rad):
    canvas.create_oval(x-rad, y-rad, x+rad, y+rad, width=3, fill=background_color)
    
def drawX(canvas, x, y, width_height):
    canvas.create_line(x, y, x + width_height, y + width_height, width=marker_line_width, fill=marker_color)
    canvas.create_line(x + width_height, y, x, y + width_height, width=marker_line_width, fill=marker_color)


# GUI elements
#root = Tk()
#root.title('Tic Tac Toe')

# Menu    
#menubar = Menu(root)
#mainmenu = Menu(menubar, tearoff=0)
#mainmenu.add_command(label="New Game", command=newGame)
#mainmenu.add_checkbutton(label="Move First", command=setStartingPlayer)
#mainmenu.add_command(label="Exit", command=root.quit)
#menubar.add_cascade(label="Game", menu=mainmenu)

# Canvas
#game_canvas = Canvas(width=canvas_width, height=canvas_height, bg=background_color)
#game_canvas.bind('<Button-1>', onCanvasClick)
#game_canvas.pack(expand=YES, fill=BOTH)
#circ1 = drawCircle(game_canvas,100,100,20)
#line1 = drawX(game_canvas, 200, 200, 50)

#game_canvas.create_line(upper_left_x + width_of_square, upper_left_y, upper_left_x + width_of_square, upper_left_y + height, width=board_line_width)
#game_canvas.create_line(upper_left_x + 2 * width_of_square + board_line_width, upper_left_y, upper_left_x + 2 * width_of_square + board_line_width, upper_left_y + height, width=board_line_width)
#game_canvas.create_line(upper_left_x, upper_left_y + width_of_square, upper_left_x + width, upper_left_y + width_of_square, width=board_line_width)
#game_canvas.create_line(upper_left_x, upper_left_y + 2 * width_of_square + board_line_width, upper_left_x + width, upper_left_y + + 2 * width_of_square + board_line_width, width=board_line_width)

#for coords in marker_positions:
    #drawX(game_canvas, coords[0], coords[1], coords[2])
    #game_canvas.create_oval(coords[0], coords[1], coords[0]+coords[2], coords[1]+coords[2], width=marker_line_width, fill=background_color, outline=marker_color)



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
    
    def __init__(self, root):
        self.root = root
        self.computer_goes_first = True
        self.marker_positions = []
        
        self.root.title('Tic Tac Toe')
        self.setupMenu()
        self.canvas = Canvas(width=TicTacToeGui.canvas_init_width, height=TicTacToeGui.canvas_init_height, bg=TicTacToeGui.background_color)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.bind('<Configure>', self.resize)
        self.drawCanvas()
        
    def setupMenu(self):
        menubar = Menu(self.root)
        mainmenu = Menu(menubar, tearoff=0)
        mainmenu.add_command(label="New Game", command=self.newGame)
        mainmenu.add_checkbutton(label="Move First", command=self.setStartingPlayer)
        mainmenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Game", menu=mainmenu)
        self.root.config(menu=menubar)
        
    def resize(self, event):
        print str(event.width) + ":" + str(event.height)
        self.canvas.delete(ALL)
        self.canvas.width = event.width
        self.canvas.height = event.height
        self.drawCanvas()
        
    def drawCanvas(self):
        self.recalculateCanvas()
        self.canvas.create_oval(100, 100, 200, 200, width=TicTacToeGui.marker_line_width, fill=TicTacToeGui.background_color, outline=TicTacToeGui.marker_color)
    
    def recalculateCanvas(self):
        width = canvas_width - 2 * board_margins
        height = canvas_height - 2 * board_margins
        upper_left_x = board_margins
        upper_left_y = board_margins
        width_of_square = ( width - 2 * board_line_width - 2 * marker_line_width) / 3
        height_of_square = ( height - 2 * board_line_width - 2 * marker_line_width ) / 3

        for i in range(9):
            coords = []
            column = i % 3
            row = i / 3

            coords.append( board_margins + square_margins + column * width_of_square + column * board_line_width )
            coords.append( board_margins + square_margins + row * height_of_square + row * board_line_width )
            coords.append( width_of_square - 2 * square_margins )
            print str(coords)
            marker_positions.append( coords )
             
    def drawX(self):
        pass
        
    def newGame(self):
        print "New game."
    
    def setStartingPlayer(self):
        print "Set start player."
        
    def foo(self):

        
        

#root.config(menu=menubar)
#mainloop()

root = Tk()
gui = TicTacToeGui(root)
root.mainloop()



