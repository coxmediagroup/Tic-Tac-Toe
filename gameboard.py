from itertools import product

class GameBoard(object):
    def __init__(self, symbol):
        self._symbol = symbol
        self._spaces = [[1, 2, 4],
                        [8, 16, 32],
                        [64, 128, 256]]
        self._move_snapshots = {'X': 0, 'O': 0}
        self._wins = [[1, 2, 4],
                      [8, 16, 32],
                      [64, 128, 256],
                      [1, 8, 64],
                      [2, 16, 128],
                      [4, 32, 256],
                      [1, 16, 256],
                      [4, 16, 64]]
        self._moves = []
        self._corners = [1, 4, 64, 256]

    def find_best_move(self):
        '''
        Find an available corner that is farthest
        from
        '''
        last_move_x, last_move_y = self.coords_by_value(self._moves[-1])
        if last_move_x == 0 or last_move_y == 0:
            x = 0 if last_move_x > 0 else 2
            y = 0 if last_move_y > 0 else 2
        else:
            x = 2 if last_move_x < 2 else 0
            y = 2 if last_move_y < 2 else 0
        
        space_value = self._spaces[x][y]
        if space_value not in self._moves:
            return space_value
        
        for corner_value in self._corners:
            if corner_value not in self._moves:
                return corner_value
        
        for x, y in product(range(3), repeat=2):
            if self._spaces[x][y] not in self._moves:
                return self._spaces[x][y]

        return None
    
    def space_taken(self, space, snapshot):
        '''
        Determines whether or not one or more spaces 
        are occupied by a player.
        
        :param space: the numerical value associated with 1 or more spaces
        :type space: int
        
        '''
        if not isinstance(snapshot, int):
            snapshot = self._move_snapshots[snapshot]
        return snapshot & space == space
    
    @property
    def opponent_symbol(self):
        return 'X' if self._symbol == 'O' else 'O'
    
    def check(self, symbol):
        '''
        'Check' is taken from chess. In this context,
        it means that either side of the game can possibly
        have 3 in a row on their next turn.
        
        :param symbol: The symbol to examine for a 'check' situation
        :type symbol: string
        
        :returns: value depicting the spot that requires action
            that will result in a win or a block
        :rtype: int; None if there is no 'check' situations

        '''
        symbol_snapshot = self._move_snapshots[symbol]
        opponent_symbol = 'X' if symbol == 'O' else 'O'
        opponent_snapshot = self._move_snapshots[opponent_symbol]

        for win in self._wins:
            spots_owned_by_symbol = []
            spots_owned_by_opponent = []
            spots_not_owned = []
            for space in win:
                if self.space_taken(space, symbol_snapshot):
                    spots_owned_by_symbol.append(space)
                elif self.space_taken(space, opponent_snapshot):
                    spots_owned_by_opponent.append(space)
                else:
                    spots_not_owned.append(space)
            
            if (len(spots_owned_by_symbol) > 1 and
                spots_not_owned):
                return spots_not_owned[0]

        return None
    
    @property
    def moves_available(self):
        return len(self._moves) < 9

    @property
    def winner(self):
        x = self._move_snapshots['X']
        o = self._move_snapshots['O']
        
        if any([(x & sum(win)) == sum(win) for win in self._wins]):
            return 'X'
        elif any([(o & sum(win)) == sum(win) for win in self._wins]):
            return 'O'
        return None
    
    def make_move(self, x, y, symbol):
        space = self._spaces[x][y]
        if self.space_taken(space, symbol):
            return False

        space_value = self._spaces[x][y]
        self._move_snapshots[symbol] += space_value
        self._moves.append(space_value)
        return True
    
    def coords_by_value(self, value):
        for x, y in product(xrange(3), repeat=2):
            if self._spaces[x][y] == value:
                return x, y
    
    def make_move_by_value(self, value):
        x, y = self.coords_by_value(value)
        self.make_move(x, y, self._symbol)

    def move(self):
        critical_move = self.check(self._symbol) or self.check(self.opponent_symbol)
        if critical_move:
            self.make_move_by_value(critical_move)
        elif not self.center_taken:
            self.make_move(1, 1, self._symbol)
        else:
            move = self.find_best_move()
            self.make_move_by_value(move)

    @property
    def center_taken(self):
        return self._spaces[1][1] in self._moves
    
    @property
    def display_str(self):
        display =  '-' * 25 +'\n'
        for y in xrange(3):
            coordinate_row = '|'
            symbol_row = '|'
            for x in xrange(3):
                coordinate_row += ' ({0},{1}) |'.format(x, y)
                space_value = self._spaces[x][y]
                symbol = ' '
                if self.space_taken(space_value, 'X'):
                    symbol = 'X'
                elif self.space_taken(space_value, 'O'):
                    symbol = 'O'
                symbol_row += '   {0}   |'.format(' ' if symbol is None else symbol)

            display += '|       ' * 3 + '|\n'
            display += '{0}\n{1}\n'.format(coordinate_row, symbol_row)
            display += '|       ' * 3 + '|\n'
            display += '-' * 25 + '\n'

        return display

    def __str__(self):
        return '{0}(symbol={1}, spaces={2})'.format(self.__class__.__name__,
                                                    self._symbol,
                                                    self._spaces)
    __repr__ = __str__
