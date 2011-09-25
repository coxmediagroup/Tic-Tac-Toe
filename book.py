from grid import Grid

class Book:
    ''' This is the 'book' for the Tic Tac Toe game. A 'book' for a game is a compilation 
        of all possible moves for any game. Tic Tac Toe is a solved game because its book is
        complete, encompassing every possible game.
        
    '''
    def __init__(self, player):
        ''' Initializes the Book, setting the marker, the marker for the other player,
            and some useful dictionaries for determing which square to fill.
        '''
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
                                '9': ['6', '8']}
        
        self.strategy = ""
        
    
    def first(self, grid):
        ''' Strategy if the computer goes first (take the corner)
        '''
        grid = grid.fill_square(user=self.player, square='1')
        return grid
    
    def first_center(self, grid):
        ''' If the computer is first, and the user takes center, take the opposite corner
            After this, the game is won by the default win threat check.
        ''' 
        grid = grid.fill_square(user=self.player, square='9')
        return grid
    
    def fill_any_corner(self, grid):
        ''' Fills the first available corner
        '''
        for corner in self.corners.keys():
             if not grid.square_taken(corner):
                grid = grid.fill_square(user=self.player, square=corner)
                return grid
    
    def fill_any_edge(self, grid):
        ''' Fills the first available edge
        '''
        for edge in self.edges:
            if not grid.square_taken(edge):
                grid = grid.fill_square(user=self.player, square=edge)
                return grid

    def first_edge(self, grid):
        ''' If the other player marks an edge, mark a corner not boardered by that edge
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
        ''' The main logic for the book. As the game progresses, the book keeps track of what
            the current strategy is by modifying self.strategy.
            
            The most important thing is to either block the other player from winning, or win
            ourselves. That runs before any other test.
            
            Once a strategy has been decided upon, the grid is return to the main game.
        '''
        # If we can win, do it!
        grid, changed = self.check_win(grid=grid, player=self.player)
        if grid.test_win():
            return grid
        
        # If we have to block the other player, do it!
        grid, changed = self.check_win(grid=grid, player=self.other)
        if changed:
            return grid
        
        # It's the first move? Fill a corner. 
        if not grid.filled['X'] and not grid.filled['O']:
            self.strategy = "first"
            grid = self.first(grid)
            return grid
        
        # If we went first, and the other player has made a move...
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
        
        # Did we go first, with the player playing an edge, and us taking center? Mark corner not 
        # boarded by their edge.
        if self.strategy == "first_edge":
            grid = self.first_edge(grid)
            return grid
        
        # Did we go first, and did they take the center?
        if self.strategy == "first_center":
            if grid.filled[self.other][0] in self.corners.keys() or grid.filled[self.other][1] in self.corners.keys():
                for corner in self.corners.keys():
                    if not grid.square_taken(corner):
                        grid = grid.fill_square(user=self.player, square = corner)
                        return grid
        
        # Are we going second?
        if not self.strategy:
            # Did they mark an edge or a side?
            if '5' not in grid.filled[self.other]:
                self.strategy = "second_center"
                grid = grid.fill_square(user=self.player, square='5')
                return grid
            # Did they mark the center?
            else:
                grid = self.fill_any_corner(grid)
                self.strategy = "second_nocenter"
                return grid
        
        # Did they mark the center on their first turn? Grab any corner.
        if self.strategy == "second_nocenter":
            grid = self.fill_any_corner(grid)
            return grid
        
        # Did they mark something besides the center on their first turn?
        if self.strategy == "second_center":
            # Are there more than three marks on the board (Did we already block a threat?)
            if grid.get_available().__len__() <= 4:
                for edge in self.edges:
                    if not grid.square_taken(edge):
                        grid = grid.fill_square(user = self.player, square=edge)
                        return grid
                    
            # Are their marks in caddy corners?
            for corner in self.corners.keys():
                if corner in grid.filled[self.other] and self.corners[corner] in grid.filled[self.other]:
                    grid = self.fill_any_edge(grid)
                    return grid
            
            # Are they in a corner + edge?
            for corner in self.corners.keys():
                if corner in grid.filled[self.other]:
                    for edge in self.edges:
                        if edge in grid.filled[self.other]:
                            grid = grid.fill_square(user=self.player, square=self.corners[corner])
                            return grid
            
            # Are they in two edges?
            edges = []
            for edge in self.edges:
                if edge in grid.filled[self.other]:
                    edges.append(edge)
            
            if edges.__len__() == 2:
                edges.sort()
                # Do they both boarder a corner?
                for corner in self.corner_boarders.keys():
                    if self.corner_boarders[corner] == edges:
                        grid.fill_square(user=self.player, square=corner)
                        self.strategy = "second_center_any"
                        return grid
                grid = self.fill_any_edge(grid)
                self.strategy = "second_center_boarder"
                return grid
        
        # Are they in the center and boarder an edge?    
        if self.strategy == "second_center_boarder":
            for corner in self.corners.keys():
                if not grid.square_taken(corner):
                    # One of these has to be open. The other has to have an X
                    if not grid.square_taken(self.corner_boarders[corner][0]) or grid.square_taken(self.corner_boarders[corner][1]):
                        if grid.square_taken(self.corner_boarders[corner][0]) == 'X' or grid.square_taken(self.corner_boarders[corner][1]) == 'X':
                            grid = grid.fill_square(user=self.player, square=grid.get_available()[0])
                            return grid
                        
        # This turn, we can mark any square   
        if self.strategy == "second_center_any":
            grid = grid.fill_square(user=self.player, square=grid.get_available()[0])
            return grid
            
        
        
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
        