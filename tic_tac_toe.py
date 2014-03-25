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
        self.empty = "."
        self.size = 3
        self.fields = {}
        for y in range(self.size):
            for x in range(self.size):
                self.fields[x,y] = self.empty
        
        self.initialize()

    #Layout of the actual tic-tac-toe board
    def initialize(self):
        self.grid()

#Create a player object to handle the human player
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