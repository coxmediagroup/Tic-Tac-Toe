import operator, sys, random, time

class Grid:
    #class to hold the game state
    def __init__(self):
        #create a dictionary with 9 members
        self.squares = [' ']*9
        self.moves = [0,1,2,3,4,5,6,7,8]
        self.moved = False
        
    #obtain all available moves left  
    def getAvailableMoves(self):
        for index, value in enumerate(self.squares):
            if value != ' ':
                try:
                    self.moves.remove(index);
                except ValueError:
                    continue
        
    def ShowBoard(self):
        print self.squares[0:3]
        print self.squares[3:6]
        print self.squares[6:9]
        
    def PresentMoves(self):
        self.getAvailableMoves()
        move = raw_input("Enter your move: (available: %s)" % (self.moves))
        selection = int(move)
        self.squares[selection] = 'X';
        self.moved = False
        self.AnalyzeBoard()
        self.ShowBoard()
        self.PresentMoves()
        
    #count number of items in row
    def CheckRow(self, row):
        count = {'bot':0, 'player':0}
        for item in row:
            #print 'current item is %s' % self.squares[item]
            if self.squares[item] == 'X':
                #print 'i found an x'
                count['player'] += 1
            if self.squares[item] == 'O':
                count['bot'] += 1
        return count 
    
    #prevent player from winning by blocking off nearly completed row
    def FillRow(self, row):
        for item in row:
            #print 'item is %s' % item
            if self.squares[item] == ' ':
                self.squares[item] = 'O' 
                print 'computer made a strategy move on square %s ' % item
                self.moved = True
                #print 'filled item %s' % item 
            
                
    #basic randomly generated bot move
    def BotMove(self):
        index = random.choice(self.moves)
        print 'computer made a random move on square %s ' % index
        self.squares[index] = 'O'       
        
    def AnalyzeBoard(self):
        #update available moves 
        self.getAvailableMoves()
        rows = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        computer_moved = False
        for row in rows:
            count = self.CheckRow(row)
            #print count['player']
            if(count['player'] == 3):
                self.ShowBoard();
                print 'You have won!'
                sys.exit()
            #if computer is about to win, finish the game
            if count['bot'] == 2 and self.moved == False:
                self.FillRow(row)
                print 'computer wins!'
                sys.exit()
            if count['player'] == 2 and self.moved == False:
                print 'found 2 x\'s in this row %s ' % row
                #prevent player from winning the row only if turn hasn't been taken
                self.FillRow(row)
        #if computer still hasn't gone, make a move
        #print 'computer still hasnt moved yet??? %s ' % self.moved
        if self.moved == False:
            self.BotMove()  
                           
game = Grid()
game.PresentMoves()