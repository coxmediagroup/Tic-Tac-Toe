#!/usr/bin/python
import Tkinter
import time
#Do stuff down here

#Class to handle the actual board display
class tic_tac_toe_board(Tkinter.Tk):
  
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.player_turn = True
        self.game_won = False
        self.board_grid =[[None] *3 for x in range(3)]
        self.board_selections=[[None] *3 for x in range(3)]
        self.comp = Computer_player()
        self.initialize()

    #Layout of the actual tic-tac-toe board in grid format
    def initialize(self):
        self.grid()
        self.labelVariable = Tkinter.StringVar()
        
        for x in range(3):
            for y in range(3):
                self.board_selections[x][y] = " "
                self.board_grid[x][y] = Tkinter.Button(self, height=5, width=5, text=str(x) + str(y), command=lambda x=x, y=y: self.OnButtonClick(self.board_grid[x][y], x, y))
                self.board_grid[x][y].grid(column=x, row=y, sticky='NSEW')
        self.update()

#Create a player object to handle the human player

    def OnButtonClick(self, board_grid, x, y):
        print(self.board_selections)
        allowed = self.check_board(x, y)
        if allowed:
            if self.player_turn == True:
                board_grid.config(text="O")
                self.board_selections[x][y] = "o"
               # self.player_turn = False
                board = self.comp.computer_turn(self.board_selections)               
                print(board)
                print("abc")
                return
            else:
                pass
        else:
            pass

    def update_board(self):
        pass

    def check_board(self, x, y):
        if self.board_selections[x][y] == " ":
            #update title to show that button has already been used
            return True
        else:
            return False

    def startgame(self):
        pass

#Create a computer_player object that will never lose
class Computer_player:

    def __init__(self):
        pass

    #Pass in a 3x3 array of the gameboard, and the computer will make the most intelligent decision based off the following logic.
    def computer_turn(self, board):
    
        #complete horizontal sets of 3
        for row in range(3):
            comp_pieces = 0
            opengrid = None
            for column in range(3):
                if board[row][column] == 'x':
                    comp_pieces += 1
                elif board[row][column] == ' ':
                    opengrid = column
                else: break
            if opengrid != None and comp_pieces == 2:
            #there is an empty slot which would win the game
                board[row][opengrid] = 'x'
                return board

        #complete vertical sets of 3
        for colNum in range(3):
            comp_pieces = 0
            opengrid = None
            for column in range(3):
                if board[column][colNum] == 'x':
                    comp_pieces += 1
                elif board[column][colNum] == ' ':
                    opengrid = column
                else: break
            if opengrid != None and comp_pieces == 2:
                board[opengrid][colNum] = 'x'
                return board

        #complete diagonal sets of 3
        #upper left to lower right
        path = [[0, 0], [1, 1], [2, 2]]
        comp_pieces = 0
        opengrid = None
        for column in range(3):
            if board[path[column][0]][path[column][1]] == 'x':
                comp_pieces += 1
            elif board[path[column][0]][path[column][1]] == ' ':
                opengrid = column
            else: break
        if opengrid != None and comp_pieces == 2:
            board[path[opengrid][0]][path[openSlot][1]] = 'x'
            return board

        #upper right to lower left
        path = [[0, 2], [1, 1], [2, 0]]
        comp_pieces = 0
        opengrid = None
        for column in range(3):
            if board[path[column][0]][path[column][1]] == 'x':
                comp_pieces += 1
            elif board[path[column][0]][path[column][1]] == ' ':
                opengrid = column
            else: break
        if opengrid != None and comp_pieces == 2:
            board[path[opengrid][0]][path[openSlot][1]] = 'x'
            return board


        #Always prevent the player from being able to win.    
        #complete horizontal sets of 3
        for row in range(3):
            player_pieces = 0
            opengrid = None
            for column in range(3):
                if board[row][column] == 'o':
                    player_pieces += 1
                elif board[row][column] == ' ':
                    opengrid = column
                else: break 
            if opengrid != None and player_pieces == 2:
                board[row][opengrid] = 'x'
                return board

        #complete vertical sets of 3
        for colNum in range(3):
            player_pieces = 0
            opengrid = None
            for column in range(3):
                if board[column][colNum] == 'o':
                    player_pieces += 1
                elif board[column][colNum] == ' ':
                    opengrid = column
                else: break
            if opengrid != None and player_pieces == 2:
                board[opengrid][colNum] = 'x'
                return board

        #upper left to lower right
        path = [[0, 0], [1, 1], [2, 2]]
        player_pieces = 0
        opengrid = None
        for column in range(3):
            if board[path[column][0]][path[column][1]] == 'o':
                player_pieces += 1
            elif board[path[column][0]][path[column][1]] == ' ':
                opengrid = column
            else: break
        if opengrid != None and player_pieces == 2:
            board[path[opengrid][0]][path[openSlot][1]] = 'x'
            return board

        #upper right to lower left
        path = [[0, 2], [1, 1], [2, 0]]
        player_pieces = 0
        opengrid = None
        for column in range(3):
            if board[path[column][0]][path[column][1]] == 'o':
                player_pieces += 1
            elif board[path[column][0]][path[column][1]] == ' ':
                opengrid = column
            else: break
        if opengrid != None and player_pieces == 2:
            board[path[opengrid][0]][path[openSlot][1]] = 'x'
            return board

        #ideal starting move
        if board[1][1] == ' ':
            board [1][1] = 'x'
            return board

        #Always attempt to pick a corner first
        path = [[0, 0], [0, 2], [2, 0], [2, 2]]
        for column in range(4):
            if board[path[column][0]][path[column][1]] == ' ':
                board[path[column][0]][path[column][1]] = 'x'
                return board

        #If no corners are available, pick the first move you see
        for row in range(3):
            for column in range(3):
                if board[row][column] == ' ':
                    board[row][column] = 'x'
                    return board

class gameplay:

    def __init__(self):
        pass   
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