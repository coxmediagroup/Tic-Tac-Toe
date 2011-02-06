#!/usr/bin/env python
# encoding: utf-8
"""
TicTacToeGui.py

Created by Fredrick Stakem on 2011-02-05.
Copyright (c) 2011 __Stakem Research__. All rights reserved.
"""

from Tkinter import *

# Game parameters
computer_goes_first = True
background_color = 'white'
highlight_color = 'red'
canvas_height = 400
canvas_width = 400
board_margins = 40
square_margins = 3
marker_positions = []
board_line_width = 5

# Automatically set up the board game
width = canvas_width - 2 * board_margins
height = canvas_height - 2 * board_margins
upper_left_x = board_margins
upper_left_y = board_margins
width_of_square = ( width - 2 * board_line_width ) / 3

# GUI elements
root = Tk()
root.title('Tic Tac Toe')

def newGame():
    print "hello!"
    
def setStartingPlayer():
    pass

def calculateCoord(position):
    # x, y, radius, width/height
    coords = [None, None, None, None]
    column = position % 3
    row = position / 3
    
    if column == 0:
        coords[0] = 1
    elif column == 1:
        coords[0] = 1
    elif column == 2:
        coords[0] = 1
        
    if row == 0:
        coords[1] = 1
    elif row == 1:
        coords[1] = 1
    elif row == 2:
        coords[1] = 1
    
    return coords
    
def drawCircle(canvas, x, y, rad):
    canvas.create_oval(x-rad, y-rad, x+rad, y+rad, width=3, fill=background_color)
    
def drawX(canvas, x, y, width_height):
    canvas.create_line(x, y, x + width_height, y + width_height, width=3)
    canvas.create_line(x + width_height, y, x, y + width_height, width=3)

# Menu    
menubar = Menu(root)
mainmenu = Menu(menubar, tearoff=0)
mainmenu.add_command(label="New Game", command=newGame)
mainmenu.add_checkbutton(label="Move First", command=setStartingPlayer)
mainmenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Game", menu=mainmenu)

# Canvas
game_canvas = Canvas(width=canvas_width, height=canvas_height, bg=background_color)
game_canvas.pack(expand=YES, fill=BOTH)
circ1 = drawCircle(game_canvas,100,100,20)
#line1 = drawX(game_canvas, 200, 200, 50)

game_canvas.create_line(upper_left_x + width_of_square, upper_left_y, upper_left_x + width_of_square, upper_left_y + height, width=board_line_width)
game_canvas.create_line(upper_left_x + 2 * width_of_square + board_line_width, upper_left_y, upper_left_x + 2 * width_of_square + board_line_width, upper_left_y + height, width=board_line_width)
game_canvas.create_line(upper_left_x, upper_left_y + width_of_square, upper_left_x + width, upper_left_y + width_of_square, width=board_line_width)
game_canvas.create_line(upper_left_x, upper_left_y + 2 * width_of_square + board_line_width, upper_left_x + width, upper_left_y + + 2 * width_of_square + board_line_width, width=board_line_width)


root.config(menu=menubar)
mainloop()


if __name__ == '__main__':
    pass

