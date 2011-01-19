#!/usr/bin/python

import sys
import Tkinter
import random

class GameApp(Tkinter.Frame):
    GAMESTATE_START = 0
    GAMESTATE_PLAYER = 2
    GAMESTATE_COMPUTER = 4

    buttonGrid = []
    gameState = 0
    MARKS_BY_PLAYER = {
        GAMESTATE_START : "  ",
        GAMESTATE_PLAYER : "X",
        GAMESTATE_COMPUTER : "O"}
    
    def __init__(self, master = None):
        self.gameState = GameApp.GAMESTATE_PLAYER
        self.buttonGrid = []
        self.quitButton = None
        self.newButton = None
        self.turnLabel = None
        Tkinter.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def newGame(self):
        self.gameState = GameApp.GAMESTATE_START
        for i in range(0, 3):
            for j in range(0, 3):
                btn = self.buttonGrid[i][j]
                # So the button callbacks need to know which button they're being fired off for.
                # This is a bit of a hack but since we can't make the Tkinter button callbacks
                # accept an argument, we'll just define a new function for each button. It'll all
                # scope out fine, though I admit it looks a bit funky. All the functions do is
                # call self.btnClicked with the row and column of the button, is all, so you shouldn't
                # have to worry too much about maintenance on this particular bit.
                def func(obj = self, x = i, y = j):
                    obj.btnClicked(x, y)
                btn.config(command = func)
                btn.config(text = GameApp.MARKS_BY_PLAYER[self.gameState])
        self.gameState = GameApp.GAMESTATE_PLAYER
        self.turnLabel.config(text = "Player's Turn".ljust(15))
        
    def btnClicked(self, row, col):
        if ( len(self.buttonGrid) > row and len(self.buttonGrid[row]) > col ):
            self.buttonGrid[row][col].config(text = GameApp.MARKS_BY_PLAYER[self.gameState])
            # have to do this because setting config of 'command' doesn't actually seem to
            # remove its method (otherwise I'd just set its command to None). Set it to a dummy
            # function. (again, looks hackish, but that's Tkinter for you - reliably portal but
            # quirky.)
            def donothing():
                pass
            self.buttonGrid[row][col].config(command = donothing)
            if ( self.gameState == GameApp.GAMESTATE_PLAYER ):
                self.gameState = GameApp.GAMESTATE_COMPUTER
                self.turnLabel.config(text = "Computer's Turn".ljust(15))
            else:
                self.gameState = GameApp.GAMESTATE_PLAYER
                self.turnLabel.config(text = "Player's Turn".ljust(15))
            
    def createWidgets(self):
        self.turnLabel = Tkinter.Label(self, text="Whose turn is it?")
        self.turnLabel.grid(row=0, column=1 )
        for i in range(0, 3):
            row = []
            for j in range(0, 3):
                tmpbtn = Tkinter.Button(self, text="  ")
                tmpbtn.grid(row=i+1, column=j)
                row.append(tmpbtn)
            self.buttonGrid.append(row)
        self.quitButton = Tkinter.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(row=4, column=2)
        self.newButton = Tkinter.Button(self, text="Restart", command=self.newGame)
        self.newButton.grid(row=4, column=0)
        self.newGame()
        print self.buttonGrid

def main(argc, argv):
    app = GameApp()
    app.master.title("Tic-Tac-Toe")
    app.mainloop()
    return 0

if ( __name__ == "__main__" ):
    sys.exit(main(len(sys.argv[1:]), sys.argv[1:]))
