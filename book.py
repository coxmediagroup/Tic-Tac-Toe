from grid import Grid

class Book:
    '''This is the 'book' for the Tic Tac To
    '''
    def __init__(self, player):
        self.player=player
        
    def check_board(self, grid):
        if not grid.x_filled and not grid.o_filled:
            # It's the first move!
            grid.fill_square(user='X', square='5')
            return
        
    
    def check_win(self, grid):
        ''' Checks to see if anyone is going to win. 
        '''
        for win in grid.wins:
            x = 0
            o = 0
            for square in win:
                if square in grid.x_filled:
                    x += 1
                    win = win.replace(square, '')
                if square in grid.o_filled:
                    o += 1
                    win = win.replace(square, '')
                if o == 2 or x == 2:
                    grid.fill_square(user=self.player, square=win)
