class Grid:
    ''' This is the class for playing grid. This class is responsible for filling squares,
        printing the current playing grid, and reporting whether a square is filled or not.
    '''
    def __init__(self):
        ''' Sets up the initial grid for the tic-tac-toe game, as well as the conditions for a
                win, and the lists for squares filled by X and O
        '''
        row1 = " 1 | 2 | 3 "
        row2 = " 4 | 5 | 6 "
        row3 = " 7 | 8 | 9 "
        divider = "---+---+---"

        self.printable =  row1 + '\n' + divider + '\n' + row2 + '\n' + divider + '\n' + row3
        
        self.filled = { 'X': [],
                        'O': []}
        
        self.wins = ['123', '456', '789']   # Horizontal wins
        self.wins += ['147', '258', '369']  # Vertical wins
        self.wins += ['159', '357']         # Diagonal wins
        
        self.corners = ['1', '3', '7', '9']
        
    def print_grid(self):
        ''' Prints the playing grid
        '''
        print '\n' + self.printable + '\n'
        
    
            
        
    def square_taken(self, square):
        ''' Tests to see if a square is available or not.
        '''
        if (square not in self.filled['X']) and (square not in self.filled['O']):
            return False
        if square in self.filled['X']:
            return 'X'
        else:
            return 'O'
            
    def fill_square(self, user, square):
        ''' Given a user (X or O) and a square number (as a string),
        '''
        if not self.square_taken(square) and square:
            self.printable = self.printable.replace(square, user)
            self.filled[user].append(square)
            return self
        else:
            print "I'm sorry, but %s isn't available." % square
            return self
            
    def test_win(self):
        for win in self.wins:
            if self.filled['X'].__contains__(win[0]) and self.filled['X'].__contains__(win[1]) and self.filled['X'].__contains__(win[2]):
                return 'X'
            if self.filled['O'].__contains__(win[0]) and self.filled['O'].__contains__(win[1]) and self.filled['O'].__contains__(win[2]):
                return 'O'
            return False
            
    def get_available(self):
        available = []
        for c in self.printable:
            if c.isdigit():
                available.append(c)
        available.sort()
        return available
        
    