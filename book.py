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
                        if not grid.square_available():
                            grid = grid.fill_square(user=self.player, square=square)
                            return grid
        
        print "Checking for first move"
        if not grid.filled['X'] and not grid.filled['O']:
            # It's the first move!
            print "mod from first move"
            grid = grid.fill_square(user=self.player, square='1')
            
            return grid
        

        print "At the end of my logic! Halp!"
                
            
    
            
       
    
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
                if (o == 2 or x == 2) and grid.square_available(square):
                    print "Filling %s for a win or a block!" % square
                    grid = grid.fill_square(user=self.player, square=win)      # This will either win the game, 
                    no_win = False                                              # or block the other player from winning. 
                    return grid                                                    # No need to check which we're doing, as the 
                                                                        # grid will test for a win.
            
                    
        
        print "Sending a no win from check_win"
        return grid
        