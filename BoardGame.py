#!/usr/bin/env python

import random
import itertools
import os, sys



class TicTacToeGame():
    """Base class for Tic Tac Toe game.     """
     

    def __init__(self):
        """Initializes class attributes for Tic Tac Toe game. 
    
          
            @type moves: List
            @param moves: List of X and O positions marked on the Tic Tac Toe Board
            @type cpu: List
            @param cpu: List of moves made by the computer player                      
            @type human: List
            @param human: List of moves made by the human player
            @type count: int
            @param count: flags set when the computer player makes its first move
            @type player: int
            @param player: The position marked on the board corresponding the numbered grid
            @type cpu_mark: string
            @param cpu_mark: The letter assigned to the computer player, X or O
            @type human_mark= string
            @param human_mark: The letter assigned to the human player, X or O
            @type availableChoices: List 
            @param availableChoices: A list of available positions on the board that a given player can mark
            @type first: string
            @param first: Holds the value of the player who marks the board first, cpu or human
        """
        self.moves=[' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.cpu=[]
        self.human=[]
        self.count=None
        self.player=None
        self.cpu_mark=''
        self.human_mark=''
        self.availableChoices=[0,1,2,3,4,5,6,7,8]
        self.first = ''
       
            
            
    def RedrawBoard(self, restart=None, first=None):
        """draws the board on the start of the game and redraws tic tac toe board after every move
        
            @type moves: List
            @param moves: List of X and O positions marked on the Tic Tac Toe Board
            
            based on the numbered position selected a mark is set to the given index within the self.moves list
        
        
        """
        
        if restart and first == 'cpu':
            self.PlayCPUMove()
            
        elif restart and first == 'human':
            pass
       
            
        
        
        print "\n" 
        print "  0  |  1  |  2  ", "\t", "  " + self.moves[0] + "  |  " + self.moves[1] + "  |  " + self.moves[2] + "  "
        print "_____|_____|_____", "\t","_____|_____|_____"
        print "  3  |  4  |  5  ", "\t","  " + self.moves[3] + "  |  " + self.moves[4] + "  |  " + self.moves[5] + "  "
        print "_____|_____|_____", "\t","_____|_____|_____"
        print "  6  |  7  |  8  ", "\t","  " + self.moves[6] + "  |  " + self.moves[7] + "  |  " + self.moves[8] + "  "
        print "     |     |     ", "\t","     |     |     "
        print "\n"
        
        
        who,win=self.CheckForWin('X')
        if win:
            print who, ' has won the game, game over.'
            return win
                
        who,win=self.CheckForWin('O')
        if win:
            print who, ' has won the game, game over.'
            return win
        if len(self.availableChoices)==0:
            return 'draw'
            
        
                 
    def CheckForWin(self,mark): 
        """winning combinations
         (0,1,2) (3,4,5) (6,7,8) (0,3,6) (1,4,7) (2,5,8) (0,4,8) (2,4,6)
         
            @type moves: List
            @param moves: List of X and O positions marked on the Tic Tac Toe Board
            @type mark: string
            @param mark: Either X or O
            
            Based on the winning combinations, the grid is check for marks in the indexes 
         
         """
        win=0
        if self.moves[0]== mark and self.moves[1]==mark and self.moves[2]==mark:
            win=1
            print mark, " wins!"
        elif self.moves[0]== mark and self.moves[3]==mark and self.moves[6]==mark:
            win=1
            print mark, " wins!"
        elif self.moves[0]== mark and self.moves[4]==mark and self.moves[8]==mark:
            win=1
            print mark, " wins!"
        elif self.moves[3]== mark and self.moves[4]==mark and self.moves[5]==mark:
            win=1
            print mark, " wins!"
        elif self.moves[6]== mark and self.moves[7]==mark and self.moves[8]==mark:
            win=1
            print mark, " wins!"
        elif self.moves[1]== mark and self.moves[4]==mark and self.moves[7]==mark:
            win=1
            print mark, " wins!"
        elif self.moves[2]== mark and self.moves[5]==mark and self.moves[8]==mark:
            win=1
            print mark, " wins!"
        elif self.moves[2]== mark and self.moves[4]==mark and self.moves[6]==mark:
            win=1
            print mark, " wins!"                
              
        return mark, win
        
    
    def FindWin(self):        
        
        """winning combinations
        
         (0,1,2) (3,4,5) (6,7,8) (0,3,6) (1,4,7) (2,5,8) (0,4,8) (2,4,6)
         
            @type availableChoices: List 
            @param availableChoices: A list of available positions on the board that a given player can mark
            @type cpu: List
            @param cpu: List of moves made by the computer player      
            
            Based on the winning combinations the computer player compares currently marked positions against winning combinations.
            It selects the next move base on that, else selects from the available choices.              
         
         
         """      
        
            
        if 3 in self.availableChoices:
            cpu_m=3
        if 3 in self.cpu and 4 in self.cpu and 5 in self.availableChoices:
            cpu_m=5
        if 2 in self.availableChoices:
            cpu_m=2
        if 2 in self.cpu and 4 in self.cpu and 6 in self.availableChoices:
            cpu_m=6        
        if 5 in self.availableChoices:
            cpu_m=5
        if 5 in self.cpu and 4 in self.cpu and 3 in self.availableChoices:
            cpu_m=3
            
        if 8 in self.availableChoices:
            cpu_m=8
        if 8 in self.cpu and 4 in self.cpu and 0 in self.availableChoices:
            cpu_m=0            
        if 0 in self.availableChoices:
            cpu_m=0
        if 0 in self.cpu and 4 in self.cpu and 8 in self.availableChoices:
            cpu_m=8
        if 7 in self.availableChoices:
            cpu_m=7
        if 7 in self.cpu and 4 in self.cpu and 1 in self.availableChoices:
            cpu_m=1            
        if 6 in self.availableChoices:
            cpu_m=6
        if 6 in self.cpu and 4 in self.cpu and 2 in self.availableChoices:
            cpu_m=2
        #print cpu_m
        if cpu_m:  
            self.pencilMark(cpu_m, 'cpu')
        elif len(self.availableChoices) > 1:
            cpu_m = random.choice(self.availableChoices)                             
            self.pencilMark(cpu_m, 'cpu')
            
    def GoForWin(self):        
        
        """winning combinations
        
         (0,1,2) (3,4,5) (6,7,8) (0,3,6) (1,4,7) (2,5,8) (0,4,8) (2,4,6)
         
            @type availableChoices: List 
            @param availableChoices: A list of available positions on the board that a given player can mark
            @type cpu: List
            @param cpu: List of moves made by the computer player      
            
            Based on the winning combinations the computer player compares based on the current two previous moves selects the next move for the win.
        
         
         """
        wins=[(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for w in wins:
            
            cw = list(set(w) - set(self.cpu))
           
            if len(cw) == 1 and cw[0] in self.availableChoices:               
                return cw[0]
    
    def GoForBlock(self,mark):        
        
        """winning combinations
        
         (0,1,2) (3,4,5) (6,7,8) (0,3,6) (1,4,7) (2,5,8) (0,4,8) (2,4,6)
         
            @type availableChoices: List 
            @param availableChoices: A list of available positions on the board that a given player can mark
            @type human: List
            @param human: List of moves made by the human player      
            
            Based on the winning combinations the computer player compares based on the current two previous moves
            made by the human player and selects the next move to block their win.
        
         
         """
        blocks=[(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for hb in blocks:
            
            b = list(set(hb) - set(self.human))            
            if len(b) == 1 and b[0] in self.availableChoices: 
                return b[0]
            
       

    def CheckCorners(self):
        """
         
            @type availableChoices: List 
            @param availableChoices: A list of available positions on the board that a given player can mark
            
            The computer player selects the best positions with the center (4) being priority else it selects the available corners
            
        """
        best=[4,0,2,6,8]
        for c in best:
            if c in self.availableChoices:
               
                return [c]
            
    def pencilMark(self, mark, player):  
        """
         
            @type availableChoices: List 
            @param availableChoices: A list of available positions on the board that a given player can mark
            @type cpu: List
            @param cpu: List of moves made by the computer player                      
            @type human: List
            @param human: List of moves made by the human player           
            @type player: int
            @param player: The position marked on the board corresponding the numbered grid
            @type cpu_mark: string
            @param cpu_mark: The letter assigned to the computer player, X or O
            @type human_mark= string
            @param human_mark: The letter assigned to the human player, X or O         
            @type moves: List
            @param moves: List of X and O positions marked on the Tic Tac Toe Board
            @type mark: string
            @param mark: Either X or O
            
            Places the players mark in the selected position and then removes that position from the available choices list
            
            
        """
        
        i = self.availableChoices.index(mark)                
        del self.availableChoices[i] 
        if player == 'cpu': 
            self.cpu.append(mark)  
            self.moves[mark]=self.cpu_mark         
        elif player == 'human':  
            self.human.append(mark)         
            self.moves[mark]=self.human_mark     
            
               
       
    def PlayCPUMove(self): 
        """
            @type cpu_m: int
            @param cpu_m: numbered position
            @type next_m: int
            @param next_: numbered position for the block
            @type for_the_win: int
            @param for_the_win: numbered position for win
            @type corner: int
            @param corner: numbered corner position
            @type availableChoices: List 
            @param availableChoices: A list of available positions on the board that a given player can mark
            @type cpu: List
            @param cpu: List of moves made by the computer player  
            @type count: int
            @param count: flags set when the computer player makes its first move
            @type first: string
            @param first: Holds the value of the player who marks the board first, cpu or human
            
           Determines the computer player's moves based on Tic Tac Toe probability strategies 
        """
     
        cpu_m=None
        next_m=None
        for_the_win = None
        corner = None
        
        if len(self.availableChoices) == 0:
            print 'No more moves its a draw'   
            
            
        elif len(self.availableChoices) == 1:
            cpu_m = self.availableChoices[0]  
            self.pencilMark(cpu_m, 'cpu')          
            print 'No more moves its a draw'   
           
           
        next_m=self.GoForBlock(self.human_mark)
        #'cpu should play this move'
        for_the_win = self.GoForWin()
        #'cpu should play this to win'
        corner = self.CheckCorners()
        #'cpu should play this'
        if self.count != 1:
            if self.first=='cpu' and 4 in self.availableChoices:
                cpu_m=4 
                self.pencilMark(cpu_m, 'cpu')
                self.count=1 
                
            elif self.first=='human' and 4 in self.availableChoices:
                cpu_m=4 
                self.pencilMark(cpu_m, 'cpu')
                self.count=1
                
            elif self.first=='human' and 4 not in self.availableChoices:
                cpu_m = self.CheckCorners()
                 
                self.pencilMark(cpu_m[0], 'cpu')
                self.count=1
         
        
        elif for_the_win and next_m:
            if for_the_win in self.availableChoices:                  
                self.pencilMark(for_the_win, 'cpu')   
            
        elif next_m and for_the_win == None:
            cpu_m=next_m            
            self.pencilMark(cpu_m, 'cpu')
            
        elif for_the_win and next_m == None:
            if for_the_win in self.availableChoices:         
                self.pencilMark(for_the_win, 'cpu')
        elif corner:             
            #cpu_m = self.CheckCorners()
            self.pencilMark(corner[0], 'cpu') 
             
        elif len(self.availableChoices) != 0:    
            self.FindWin()                   
         
     
                    
        
    def placement(self):  
        """
          
            @type availableChoices: List 
            @param availableChoices: A list of available positions on the board that a given player can mark
            @type mark: int
            @param mark: numbered position
            @type first: string
            @param first: Holds the value of the player who marks the board first, cpu or human
            
           Handles the selection of positions from the human player based on available choices
        """
     
         
         
          
            
        if len(self.availableChoices) != 0:  
            
            mark = raw_input('Select your place using numbers 0 to 8. \n')  
            mark = int(mark)
            self.player=mark
            self.pencilMark(mark, 'human')
            return
        else:
            print "No more moves available" 
            return
                
    def Refresh(self):
        """Refreshes/restarts class variables after a completed game               
        
        """
        
        self.moves=[' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.cpu=[]
        self.human=[]
        self.count=None
        self.player=None
        self.cpu_mark=''
        self.human_mark=''
        self.availableChoices=[0,1,2,3,4,5,6,7,8]
        self.first = ''  
            
   
    

    def selectMark(self):
        """Starts game, determines letter assignments and who makes the first move.  
            
            @type first: string
            @param first: Will the human or computer go first Y(yes) of N(no)
            @type letter: string
            @param letter: The letter selected X or O
            @type cpu_mark: string
            @param cpu_mark: The letter assigned to the computer player, X or O
            @type human_mark= string
            @param human_mark: The letter assigned to the human player, X or O           
            @type self.first: string
            @param self.first: Holds the value of the player who marks the board first, cpu or human
        """
        
        first = raw_input('Do you want to go first? Y or N \n').upper()
        if first == 'Y':
            self.first='human'
            letter = raw_input('Do you want to be X or O? \n').upper()
            
            if letter == 'X':
                self.human_mark = letter
                self.cpu_mark = 'O'            
            elif letter == 'O':            
                self.human_mark = letter
                self.cpu_mark = 'X'
            else:    
                print ('That is not a valid choice. Please try again \n')
                self.counter +=1 
                if self.counter > 4:
                    print 'Really? that is very mature of you.'
                return TicTacToeGame.selectMark(self)
        else:
            self.first='cpu'
            self.cpu_mark = 'X'
            self.human_mark = 'O'
            print 'CPU is has chosen ' + self.cpu_mark + '.\n'
        
        print
        
       
        
        print 'Your choice is ' + self.human_mark + ' the cpu will be ' + self.cpu_mark + ' have fun!'
        return self.first, self.human_mark
    
if __name__ == "__main__":
    
    print \
         """
            This is my tic tac toe game for the Cox Media Challenge game.  In this challenge the 
            computer player is to always win.  Technically the computer cannot always win unless a 'draw'
            will be counted as a win for the computer similar to a 'bust' in blackjack.\n  
            
        """        
    print \
            """
            
            Please select the placing of your move according to the layout of the below tic tac toe board.
            Your mark will be placed by entering a number from 0 to 8. The number
            will correspond to the board position:

                                         0 | 1 | 2
                                        -----------
                                         3 | 4 | 5
                                         -----------
                                         6 | 7 | 8

             \n\r
            """
    print 'Go!'        
    game = TicTacToeGame()
    game.RedrawBoard()
    first,mark = game.selectMark()
   
    win = None
   
    i=0
    if first == 'human': 
        while 1:
            if i == 8:
                break
                       
            
            game.placement()             
            win=game.RedrawBoard()
            if win:
                game.Refresh()
                restart = raw_input('Do you want to play again? Y or N \n').upper()
                if restart == 'Y': 
                    game = TicTacToeGame()
                    game.RedrawBoard(restart=1,first=first)
                    first,mark = game.selectMark()
                     
                elif restart == 'N':
                    print 'This concludes our game goodbye!'
                    sys.exit()
                else:
                    print 'Game Over!'       
                    break

            game.PlayCPUMove() 
            win=game.RedrawBoard()
            if win:
                game.Refresh()
                restart = raw_input('Do you want to play again? Y or N \n').upper()
                if restart == 'Y': 
                    game = TicTacToeGame()
                    first,mark = game.selectMark()
                    game.RedrawBoard(restart=1,first=first)
                     
                elif restart == 'N':
                    print 'This concludes our game goodbye!'
                    sys.exit()
                else:
                    print 'Game Over!'       
                    break
        
        i+=1
           
    if first == 'cpu': 
        while 1:
            if i == 8:
                break
                        
            game.PlayCPUMove()            
            win=game.RedrawBoard()
            if win:
                
                game.Refresh()
                restart = raw_input('Do you want to play again? Y or N \n').upper()
                if restart == 'Y': 
                    game = TicTacToeGame()
                    first,mark = game.selectMark()
                    game.RedrawBoard(restart=1,first=first)
                     
                elif restart == 'N':
                    print 'This concludes our game goodbye!'
                    sys.exit()
                else:
                    print 'Game Over!'       
                    break
                #break
            game.placement()
            win=game.RedrawBoard()
            if win:
                
                game.Refresh()
                restart = raw_input('Do you want to play again? Y or N \n').upper()
                if restart == 'Y': 
                    game = TicTacToeGame()
                    first,mark = game.selectMark()
                    game.RedrawBoard(restart=1,first=first)
                     
                elif restart == 'N':
                    print 'This concludes our game goodbye!'
                    sys.exit()
                else:
                    print 'Game Over!'       
                    break
        
        i+=1
                        
