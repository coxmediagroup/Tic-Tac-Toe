from grid import Grid

class Book:
    ''' This is the 'book' for the Tic Tac Toe game. A 'book' for a game is a compilation 
        of all possible moves for any game. Tic Tac Toe is a solved game because its book is
        complete, encompassing every possible game.
        
    '''
    def __init__(self, player):
        self.player=player
        if player == 'X':
            self.other = 'O'
        else:
            self.other = 'X'
        self.edges = ['2', '4', '6', '8']
        self.corners = {'1': '9',
                        '9': '1',
                        '3': '7',
                        '7': '3'}
        self.edge_opp_corner = {'2': ['7', '9'],
                                '4': ['3', '9'],
                                '6': ['1', '7'],
                                '8': ['1', '3']}
        self.strategy = ""
        
    
    def first(self, grid):
        print "mod from first move"
        grid = grid.fill_square(user=self.player, square='1')
        return grid
    
    def first_1(self, grid):
        grid = grid.fill_square(user=self.player, square='9')
    
    def first_1_1(self, grid):
        pass
    
    def first_1_1_1(self, grid):
        pass

        
    def check_grid(self, grid):
        
        print "Checking for a win threat"
        # First, make sure we either win, or block the other player from winning.
        for win in grid.wins:
            x = 0
            o = 0
            for square in win:
                if square in grid.filled['X']:
                    x = x + 1
                if square in grid.filled['O']:
                    o = o + 1
                if x == 2 or o == 2:
                    for square in win:
                        if not grid.square_taken():
                            grid = grid.fill_square(user=self.player, square=square)
                            return grid
        
        print "Checking for first move"
        # It's the first move? Fill a corner
        if not grid.filled['X'] and not grid.filled['O']:
            self.strategy = "first"
            grid = self.first(grid)
            return grid
        
        if self.strategy == "first":
            if grid.filled[self.other][0] == '5':
                self.strategy = "first_1"
                grid = self.first_1(grid)
                return grid
            
            
        
        print "Checking for player filling the center"
        # Did the other player fill in the center? Get the opposite corner, if possible
        if grid.filled[self.other].__contains__('5'):
            if grid.square_taken('9'):
                print "mod from center"
                grid = grid.fill_square(user=self.player, square='9')
                
                return grid
        
        print "Checking for player filling a corner"    
        # Did the other player fill a corner? Fill any other corner!
        for corner in self.corners.keys():
            owner = grid.square_taken(corner)
            if owner == self.other and grid.square_taken(self.corners[corner]):
                print "Mod from corner"
                grid = grid.fill_square(user=self.player, square=self.corners[corner])
                
                return grid
        
        print "Checking for player filling an edge"    
        # Did the other player fill an edge? Fill an opposite corner!
        for edge in self.edge_opp_corner.keys():
            if grid.square_taken(edge) == self.other:
                for corner in edge_opp_corner[edge]:
                    if grid.square_taken(corner):
                        print "mod from edge"
                        grid = grid.fill_square(user=self.player, square=corner)
                        return grid

        
                
            
    
            
       
    
    def check_win(self, grid):
        ''' Checks to see if anyone is going to win. 
            If so, either block the other player or play the winning move.
        '''
        no_win = True
        for win in grid.wins:
            x = 0
            o = 0
            print win
            
            for square in win:
                if square in grid.filled['X']:
                    x += 1
                    win = win.replace(square, '')
                if square in grid.filled['O']:
                    o += 1
                    win = win.replace(square, '')
                if (o == 2 or x == 2) and grid.square_taken(square):
                    print "Filling %s for a win or a block!" % square
                    grid = grid.fill_square(user=self.player, square=win)      # This will either win the game, 
                    no_win = False                                              # or block the other player from winning. 
                    return grid                                                    # No need to check which we're doing, as the 
                                                                        # grid will test for a win.
            
                    
        
        print "Sending a no win from check_win"
        return grid
        