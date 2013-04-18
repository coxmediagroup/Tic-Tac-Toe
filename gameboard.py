
class GameBoard(object):
    def __init__(self, symbol):
        self._symbol = symbol
        self._spaces = [[None] * 3 for i in xrange(3)]
    
    @property
    def moves_available(self):
        return True

    @property
    def winner(self):
        return None
    
    def make_move(self, x, y, symbol):
        if self._spaces[x][y] is not None:
            return False

        self._spaces[x][y] = symbol
        return True
    
    def move(self):
        pass
    
    @property
    def display_str(self):
        display =  '-' * 25 +'\n'
        for y in xrange(3):
            coordinate_row = '|'
            symbol_row = '|'
            for x in xrange(3):
                coordinate_row += ' ({0},{1}) |'.format(x, y)
                symbol = self._spaces[x][y]
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
