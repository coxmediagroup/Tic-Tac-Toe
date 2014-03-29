#!/usr/bin/python
import Tkinter
import time

#Class to handle the actual board display
class tic_tac_toe_board(object, Tkinter.Tk):
  
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        root = Tkinter.Tk
        self.player_turn = True
        self.board_grid =[[None] *3 for x in range(3)]
        self.board_selections=[[None] *3 for x in range(3)]
        self.comp = ComputerPlayer()
        self.initialize()
        self.after(1000, self.call_ai_player)

    #Layout of the actual tic-tac-toe board in grid format
    def initialize(self):
        self.grid()
        self.labelVariable = Tkinter.StringVar()
        
        for x in range(3):
            for y in range(3):
                self.board_selections[x][y] = " "
                self.board_grid[x][y] = Tkinter.Button(self, height=5, width=5, text=str(x) + str(y), command=lambda x=x, y=y: self.OnButtonClick(x, y))
                self.board_grid[x][y].grid(column=x, row=y, sticky='NSEW')
        #self.update()

    def OnButtonClick(self, x, y):
        if self.player_turn == True:
            allowed = self.check_board(x, y)
            if allowed:
                self.board_selections[x][y] = "o"
                self.update_board('o')
                print self.board_selections

                won = self.gamewon(self.board_selections, 'o', x, y)
                if won == True:
                    print "won"
                    return
            
            self.player_turn = False
            
            
        """
                won = self.gamewon(self.board_selections, 'o', x, y)
                if won == True:
                    print("won")
                    return
                else:
                    board  = self.comp.computer_turn(self.board_selections)
                    self.update_board(x, y, 'x')
                    print(self.board_selections)
                    won = self.gamewon(self.board_selections, 'x', x, y)
                    if won == True:
                        print("comp won")
        """
    def call_ai_player(self):
        print("abc")
        if self.player_turn == False:
            time.sleep(2)
            self.board_selections = self.comp.computer_turn(self.board_selections)
            self.update_board("x")
            self.player_turn = True   
        self.after(1000, self.call_ai_player)

    def update_board(self, mark):

        #self.board_selections[x][y] = mark
        #print self.board_selections[x][y]

        for x in range(3):
            for y in range(3):
                if self.board_selections[x][y] == "o":
                    self.board_grid[x][y].config(text="O")
                if self.board_selections[x][y] == "x":
                    self.board_grid[x][y].config(text="X")

    #When a user selects a grid, make sure that it hasn't already been selected
    def check_board(self, x, y):
        if self.board_selections[x][y] == " ":
            return True
        else:
            return False

    def gamewon(self, board, mark, x, y):
        if board[x][0] == (mark) and board[x][1] == (mark) and board [x][2] == (mark):
            return True

        if board[0][y] == (mark) and board[1][y] == (mark) and board [2][y] == (mark):
            return True    

        #Check diagonals
        if board[0][0] == (mark) and board[1][1] == (mark) and board [2][2] == (mark):
            return True

        if board[0][2] == (mark) and board[1][1] == (mark) and board [2][0] == (mark):
            return True
 
        else:
            return False

#Create a computer_player object that will never lose
class ComputerPlayer(object):

    def __init__(self):
        pass

    def comp_move(self, board):
        board = self.computer_turn(board)             
        return board

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
                return board, 

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
            board[path[opengrid][0]][path[opengrid][1]] = 'x'
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
            board[path[opengrid][0]][path[opengrid][1]] = 'x'
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
            board[path[opengrid][0]][path[opengrid][1]] = 'x'
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
            board[path[opengrid][0]][path[opengrid][1]] = 'x'
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


class gameplay(object):

    def __init__(self):
        self.gameboard = tic_tac_toe_board(None)
        self.gameboard.title("TicTacToe")
        self.comp = ComputerPlayer()
        self.player_turn = False
        self.game_won = False
 #Pass in the board, player, and computer objects to start the actual game.
    def play(self):
        board = self.comp.computer_turn(self.gameboard.board_selections)
        # Pass computer player the gameboard, and let them choose
        # Update gameboard
        # Have player make selection
        # Check for win
        self.gameboard.mainloop()

#Start the game session
if __name__ == "__main__":
    gameboard = tic_tac_toe_board(None)
    gameboard.mainloop()