
class GameBoard(object):
    def __init__(self, symbol):
        self._symbol = symbol
        self._spaces = [[None] * 3] * 3
    
    @property
    def moves_available(self):
        return True
    
    def make_move(self, x, y, symbol):
        pass
    
    def move(self):
        pass
    
    def display(self):
        print 'TODO'
    
    def __str__(self):
        return '{0}(symbol={1}, spaces={2})'.format(self.__class__.__name__,
                                                    self._symbol,
                                                    self._spaces)

    __repr__ = __str__
