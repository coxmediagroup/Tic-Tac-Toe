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

# GUI elements
root = Tk()
root.title('Tic Tac Toe')

def newGame():
    print "hello!"
    
def setStartingPlayer():
    pass
    
menubar = Menu(root)
mainmenu = Menu(menubar, tearoff=0)
mainmenu.add_command(label="New Game", command=newGame)
mainmenu.add_checkbutton(label="Move First", command=setStartingPlayer)
mainmenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Game", menu=mainmenu)


root.config(menu=menubar)
mainloop()


if __name__ == '__main__':
    pass

