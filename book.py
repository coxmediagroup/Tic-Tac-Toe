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
        
        self.corner_boarders = {'1': ['2', '4'],
                                '3': ['2', '6'],
                                '7': ['4', '8'],
                                '9': ['8', '6']}
        self.strategy = ""
        
    
    def first(self, grid):
        ''' Strategy if the computer goes first (take the corner)
        '''
        print "mod from first move"
        grid = grid.fill_square(user=self.player, square='1')
        return grid
    
    def first_center(self, grid):
        ''' If the computer is first, and the user takes center, take the opposite corner
            After this, the game is won by the default win threat check.
        ''' 
        grid = grid.fill_square(user=self.player, square='9')
        return grid
    
    def first_corner(self, grid):
        '''
        '''
        pass
    
    def fill_any_corner(self, grid):
        for corner in self.corners.keys():
                        if not grid.square_taken(corner):
                            grid = grid.fill_square(user=self.player, square=corner)
                            return grid

    def first_edge(self, grid):
        ''' If the other player marks an edge, mark a corner not boardered by that corner
        '''
        # What edge has the other player taken?
        for edge in self.edges:
            if edge in grid.filled[self.other]:
                break
        
        for corner in self.corner_boarders.keys():
            if not grid.square_taken(corner) and edge not in self.corner_boarders[corner]:
                grid = grid.fill_square(user=self.player, square=corner)
                return grid
            
        
    def check_grid(self, grid):
        
        print "Checking for a win threat"
        # First, make sure we either win, or block the other player from winning.
        # TODO: I should really try to win before blocking. Assess the whole board.
        grid, changed = self.check_win(grid=grid, player=self.player)
        if grid.test_win():
            return grid
        
        grid, changed = self.check_win(grid=grid, player=self.other)
        if changed:
            return grid
        
        # It's the first move? Fill a corner
        if not grid.filled['X'] and not grid.filled['O']:
            self.strategy = "first"
            grid = self.first(grid)
            return grid
        
        if self.strategy == "first":
            # Did they fill in the center square?
            if grid.filled[self.other][0] == '5':
                self.strategy = "first_center"
                grid = self.first_center(grid)
                return grid
            # Did they play a corner square?
            for corner in self.corners.keys():
                if corner in grid.filled[self.other]:
                    self.strategy = "first_corner"
                    grid = self.fill_any_corner(grid)
                    return grid
            # Did they play an edge?
            if grid.filled[self.other][0] in self.edges:
                self.strategy = "first_edge"
                grid = grid.fill_square(user=self.player, square='5')
                return grid
        
        if self.strategy == "first_edge":
            grid = self.first_edge(grid)
            return grid
        
        # Did they fill a corner? (If they filled in an edge, the game will draw with blocking)
        if self.strategy == "first_center":
            if grid.filled[self.other][0] in self.corners.keys() or grid.filled[self.other][1] in self.corners.keys():
                for corner in self.corners.keys():
                    if not grid.square_taken(corner):
                        grid = grid.fill_square(user=self.player, square = corner)
                        return grid
        
        if not self.strategy:
            # Did they mark an edge or a side?
            if '5' not in grid.filled[self.other]:
                self.strategy = "second_center"
                grid = grid.fill_square(user=self.player, square='5')
                return grid
            # Did they mark the center?
            else:
                pass
        
        if self.strategy == "second_center":
            # Are there more than three marks on the board (Did we already block a threat?)
            
            # Are they in caddy corners?
            
            # Are they in a corner + edge?
            
            # Are they in two edges?
            
            pass
        
        
    def check_win(self, player, grid):
        ''' Checks to see if the one of the players is going to win. If so, either
            win or block!
        '''
        for win in grid.wins:
            squares = 0
            for square in win:
                if square in grid.filled[player]:
                    squares += 1
            if squares == 2:
                for square in win:
                    if not grid.square_taken(square):
                        grid = grid.fill_square(user=self.player, square=square)
                        return grid, True
        return grid, False
        