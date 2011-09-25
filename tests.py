import unittest

from grid import Grid
from book import Book

class TestGrid(unittest.TestCase):
    
    def setUp(self):
        self.grid = Grid()
        
    def testSquareAvailabe(self):
        ''' Asserts square_taken returns the correct boolean for a free square
        '''
        self.assertFalse(self.grid.square_taken('1'))
        
    def testAvailable(self):
        ''' 
        '''
        self.assertEquals(self.grid.get_available(), ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.grid.fill_square(user='X', square = '7')
        available = self.grid.get_available()
        self.assertFalse(available.__contains__('7'))
        
    def testFillSquare(self):
        self.grid.fill_square(user='X', square='2')
        self.assertTrue(self.grid.printable.__contains__('X'))
        self.assertFalse(self.grid.printable.__contains__('2'))
        
    def testWin(self):
        self.assertFalse(self.grid.test_win())
        
        self.grid.fill_square(user='X', square='1')
        self.grid.fill_square(user='X', square='2')
        self.grid.fill_square(user='X', square='3')
        self.assertEquals(self.grid.test_win(), 'X')
        
class TestBook(unittest.TestCase):
    
    def setUp(self):
        self.grid = Grid()
        self.book = Book('X')
        
    def test_check_win(self):
        self.grid.fill_square(user='X', square='1')
        self.grid.fill_square(user='X', square='2')
        self.grid, win = self.book.check_win(grid=self.grid, player='X')
        self.assertEquals(self.grid.test_win(), 'X')
        
    
        
        
class TestPlayerOneLogic(unittest.TestCase):
    
    def setUp(self):
        self.grid = Grid()
        self.book = Book('X')
        
    def test_first_center_corner(self):
        moves = ['5', '7', '2']
        moves.reverse() # reversing so I can pop them off
        while not self.grid.test_win():
            self.grid = self.book.check_grid(self.grid)
            try:
                self.grid = self.grid.fill_square(user='O', square = moves.pop())
            except:
                break
        self.assertEquals(self.grid.test_win(), 'X')
        
    def test_first_center_edge(self):
        moves = ['5', '8', '3', '4']
        moves.reverse()
        while self.grid.get_available():
            self.grid = self.book.check_grid(self.grid)
            try:
                self.grid = self.grid.fill_square(user='O', square=moves.pop())
            except:
                pass
        self.assertFalse(self.grid.get_available())
        
    def test_first_corner(self):
        moves = ['3', '5', '4']
        moves.reverse()
        while not self.grid.test_win():
            self.grid = self.book.check_grid(self.grid)
            try:
                self.grid = self.grid.fill_square(user='O', square = moves.pop())
            except:
                break
        self.assertEquals(self.grid.test_win(), 'X')
    
    def test_first_edge(self):
        moves = ['4', '9', '7']
        moves.reverse()
        while not self.grid.test_win():
            self.grid = self.book.check_grid(self.grid)
            try:
                self.grid = self.grid.fill_square(user='O', square=moves.pop())
            except:
                break
        self.assertEquals(self.grid.test_win(), 'X')
        
if __name__ == "__main__":
    unittest.main()