#!/usr/bin/python

import sys
import Tkinter
import random

class TicTacToe(Tkinter.Frame):
    """A class that implements a Tic-Tac-Toe game with a TK-based GUI interface. Use it as:

    app = TicTacToe()
    app.mainloop()
    """
    
    # Various game state flags
    GAMESTATE_START = 0
    GAMESTATE_PLAYER = 2
    GAMESTATE_COMPUTER = 4
    GAMESTATE_WIN = 8

    # This array describes the 8 winning line combinations in
    # tic-tac-toe. Instead of writing some complex algorithm
    # to trace rays through the edges of adjoining marked squares,
    # we'll just check the state of the board against these lines.
    
    winLines = [
        [ [0, 0], [0, 1], [0, 2] ], # \
        [ [1, 0], [1, 1], [1, 2] ], #  >-- horizontal lines
        [ [2, 0], [2, 1], [2, 2] ], # /
        
        [ [0, 0], [1, 0], [2, 0] ], # \
        [ [0, 1], [1, 1], [2, 1] ], #  >-- vertical lines
        [ [0, 2], [1, 2], [2, 2] ], # /

        [ [0, 0], [1, 1], [2, 2] ],  # .
        [ [0, 2], [1, 1], [2, 0] ] ] #  >--- diagonal lines

    # This dictionary determines the marks placed on the squares
    # in the btnClicked() function depending on the current state
    # of the game
    
    MARKS_BY_PLAYER = {
        GAMESTATE_START : "  ",
        GAMESTATE_WIN : "  ",
        GAMESTATE_PLAYER : "X",
        GAMESTATE_COMPUTER : "O"}
    
    def __init__(self, master = None):
        self.gameState = TicTacToe.GAMESTATE_PLAYER
        self.buttonGrid = []
        self.quitButton = None
        self.newButton = None
        self.turnLabel = None
        self.lineWeights = [] # used by the AI to see which line needs to be defeated the most
        self.lineStates = [] # holds the current state of each of the winning line arrangements
        for i in range(0, 8):
            self.lineStates.append([0, 0, 0])
            self.lineWeights.append(0)

        Tkinter.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def markDraw(self):
        """Announce a draw in the game and mark the board appropriately"""
        for btnrow in self.buttonGrid:
            for btn in btnrow:
                btn.config(foreground = "red", background = "black")
        self.gameState = TicTacToe.GAMESTATE_WIN
        self.turnLabel.config(text = "It's a Draw!")
        return

    def markWinLine(self, idx):
        """Announce that the line described by TicTacToe.winLines[idx] has been completed,
        thus winning the game."""
        if ( self.gameState == TicTacToe.GAMESTATE_PLAYER ):
            self.turnLabel.config(text = "Player wins!")
        elif ( self.gameState == TicTacToe.GAMESTATE_COMPUTER ):
            self.turnLabel.config(text = "Computer wins!")
        for pair in TicTacToe.winLines[idx]:
            self.buttonGrid[pair[0]][pair[1]].config(
                foreground = "red", background = "black")
        self.gameState = TicTacToe.GAMESTATE_WIN
        return

    def computerPlayer(self):
        """Run the computer's AI to defeat the player's attempts (sometimes it even wins, if the player is really bad)"""
        buttonsByPlayerWeight = {}
        # try to populate the center FIRST if we can, so rearrange the way we
        # iterate through the list of winning lines, instead of just taking
        # it in sequential order. This will make sure we hit the center square on
        # all of the winning lines first.
        for idx in [1, 4, 6, 7, 0, 2, 3, 5]:
            playerweight = 0
            for pidx in [1, 0, 2]:
                pair = TicTacToe.winLines[idx][pidx]
                lsidx = TicTacToe.winLines[idx].index(pair)
                if ( self.lineStates[idx][lsidx] == 1 ):
                    playerweight += 1
            if ( playerweight > 0 ):
                for pidx in range(0, 3):
                    pair = TicTacToe.winLines[idx][pidx]
                    lsidx = TicTacToe.winLines[idx].index(pair)
                    if ( self.lineStates[idx][lsidx] == 0 ):
                        if ( not playerweight in buttonsByPlayerWeight.keys() ):
                            buttonsByPlayerWeight[playerweight] = []
                        buttonsByPlayerWeight[playerweight].append(self.buttonGrid[pair[0]][pair[1]])
        keylist = buttonsByPlayerWeight.keys()
        keylist.sort()
        keylist.reverse()
        btn = buttonsByPlayerWeight[keylist[0]][0].invoke()
        return        

    def checkLines(self):
        """Check the current status of the game board and inspect it for a Win or Draw condition"""
        canDraw = 0 # used to track the number of lines which contribute to a draw condition; when this reaches 8, it's a draw.
        for idx in range(0, 8):
            if ( self.lineWeights[idx] == 3 ):
                playerweight = 0
                for pair in TicTacToe.winLines[idx]:
                    lsidx = TicTacToe.winLines[idx].index(pair)
                    if ( self.lineStates[idx][lsidx] == 1 ):
                        playerweight += 1
                if ( playerweight in [3, 0] ):
                    self.markWinLine(idx)
                    return
                canDraw += 1
        if ( canDraw == 8 ):
            self.markDraw()
        return
                            
    def newGame(self):
        """Reset the gameboard to the initial state, to start a new game."""
        self.gameState = TicTacToe.GAMESTATE_START
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
                btn.config(text = TicTacToe.MARKS_BY_PLAYER[self.gameState], foreground = "black", background = "white")
        self.lineStates = []
        for i in range(0, 8):
            self.lineStates.append([0, 0, 0])
            self.lineWeights[i] = 0            
        self.gameState = TicTacToe.GAMESTATE_PLAYER
        self.turnLabel.config(text = "Player's Turn".ljust(15))

    def updateState(self, row, col):
        """Update the state of all lines to mark that the square at this position has been checked.
        It will store 1 in the position for a Player check, 2 for a Computer check."""
        for idx in range(0, 8):
            winline = TicTacToe.winLines[idx]
            linestate = self.lineStates[idx]
            if ( [row, col] in winline ):
                lsidx = winline.index([row, col])
                if ( self.gameState == TicTacToe.GAMESTATE_PLAYER ):
                    linestate[lsidx] = 1
                else:
                    linestate[lsidx] = 2
                self.lineWeights[idx] += 1
        return
        
    def btnClicked(self, row, col):
        """Called to indicate that the button at (row,col) position on the game board has been clicked,
        either by the player or by the computer."""
        
        if (  (self.gameState != TicTacToe.GAMESTATE_PLAYER and self.gameState != TicTacToe.GAMESTATE_COMPUTER) ):
            return
        if ( (row < len(self.buttonGrid) and col < len(self.buttonGrid[row])) ):
            self.buttonGrid[row][col].config(text = TicTacToe.MARKS_BY_PLAYER[self.gameState])
            # have to do this because setting config of 'command' doesn't actually seem to
            # remove its method (otherwise I'd just set its command to None). Set it to a dummy
            # function. (again, looks hackish, but that's Tkinter for you - reliably portal but
            # quirky.)
            def donothing():
                pass
            self.buttonGrid[row][col].config(command = donothing)
            self.updateState(row, col)
            
        self.checkLines()

        # Update gamestate
        if ( self.gameState != TicTacToe.GAMESTATE_WIN ):
            if ( self.gameState == TicTacToe.GAMESTATE_PLAYER ):
                self.gameState = TicTacToe.GAMESTATE_COMPUTER
                self.turnLabel.config(text = "Computer's Turn".ljust(15))
                self.computerPlayer()
            else:
                self.gameState = TicTacToe.GAMESTATE_PLAYER
                self.turnLabel.config(text = "Player's Turn".ljust(15))
            
    def createWidgets(self):
        """Do initial GUI setup"""
        self.master.title("Tic-Tac-Toe")
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

def main(argc, argv):
    app = TicTacToe()
    app.mainloop()
    return 0

if ( __name__ == "__main__" ):
    sys.exit(main(len(sys.argv[1:]), sys.argv[1:]))
