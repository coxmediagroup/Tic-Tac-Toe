#!/usr/bin/python
import Tkinter
#Do stuff down here

#Class to handle the actual board display
class tic_tac_toe_board(Tkinter.Tk):
  
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.player_turn = True
        self.unavailable_buttons = []
        human = Player()
        comp = Computer_player()
        self.initialize()

    #Layout of the actual tic-tac-toe board in grid format
    def initialize(self):
        self.grid()
        board_grid = [[None] *3 for x in range(3)]
        self.labelVariable = Tkinter.StringVar()

        for x in range(3):
            for y in range(3):
                board_grid[x][y] = Tkinter.Button(self, height=5, width=5, text=str(x) + str(y), command=lambda x=x, y=y: self.OnButtonClick(board_grid[x][y]))
                board_grid[x][y].grid(column=x, row=y, sticky='NSEW')
        self.update()

        self.labelVariable.set(u"Test!")

#Create a player object to handle the human player

    def OnButtonClick(self, board_grid):
        #Make sure button hasn't already been clicked.
        #Call check_board
        allowed = self.check_board(board_grid)
        #if allowed:
        print(board_grid)
        if board_grid in self.unavailable.buttons:
            print("Not allowed")
        if self.player_turn == True:
            board_grid.config(text="X")
            self.unavailable_buttons.append(board_grid)
            print(self.unavailable_buttons)
            self.player_turn = False
        else:
            board_grid.config(text="O")
            self.player_turn = True
        #Update the list of available buttons


    def check_board(self, board_grid):
        pass


class Player:

    def __init__(self):
        self.marker = "abc"
        self.player_turn = True
    def turn(self):
        pass

#Create a computer_player object that will never lose
class Computer_player:

    def __init__(self):
        pass

    def turn(self):
        pass
        #Read in an array of available moves, and choose the best move accordingly

class gameplay:

    def __init__(self):
        self.player = "X"
        self.computer = "O"
    #Pass in the board, player, and computer objects to start the actual game.
    def play(self):
        gameboard = tic_tac_toe_board(None)
        gameboard.title('Tic Tac Toe')
        gameboard.mainloop()

#Start the game session
if __name__ == "__main__":
   # gameboard = tic_tac_toe_board(None)
   # gameboard.title('Tic Tac Toe')
   # gameboard.mainloop()
    start = gameplay()
    start.play()