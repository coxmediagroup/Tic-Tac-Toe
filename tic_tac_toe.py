#!/usr/bin/python
import Tkinter
#Do stuff down here

#Class to handle the actual board display
class tic_tac_toe_board(Tkinter.Tk):
  
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.player = "X"
        self.computer = "O"
        
        self.initialize()

    #Layout of the actual tic-tac-toe board in grid format
    def initialize(self):
        self.grid()
        board_grid = [[None] *3 for x in range(3)]
        self.labelVariable = Tkinter.StringVar()

        for x in range(3):
            for y in range(3):
                board_grid[x][y] = Tkinter.Button(self, height=5, width=5, text=u"Click me!", command=self.OnButtonClick)
                board_grid[x][y].grid(column=x, row=y, sticky='NSEW')
        self.update()

        self.labelVariable.set(u"Test!")
#        self.labelVariable = Tkinter.StringVar()
#        label = Tkinter.Label(self, textvariable=self.labelVariable, anchor="w", fg="white", bg="blue")
#        self.labelVariable.set(u"Hello!")
#        label.grid(column=0, row=1, columnspan=2, sticky='EW')

#Create a player object to handle the human player

    def OnButtonClick(self):
        pass

class player:

    def __init__(self):
        pass

    def turn(self):
        pass

#Create a computer_player object that will never lose
class computer_player:

    def __init__(self):
        pass

    def turn(self):
        pass


class gameplay:

    def __init__(self):
        pass

    #Pass in the board, player, and computer objects to start the actual game.
    def play(self, board, player, computer):
        pass

#Start the game session
if __name__ == "__main__":
    gameboard = tic_tac_toe_board(None)
    gameboard.title('Tic Tac Toe')
    gameboard.mainloop()