import unittest

import sys
sys.path.append('.')

from grid import Grid
from book import Book

class TestGrid(unittest.TestCase):
    
    def setUp(self):
        self.grid = Grid()
        
    def testSquareAvailabe(self):
        ''' Asserts square_available returns the correct boolean for a free and for
            a non-existant square
        '''
        self.assertTrue(self.grid.square_available('1'))
        self.assertTrue(self.grid.square_available('0'))
        
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
        
    def testWin(self):
        self.grid.fill_square(user='X', square='1')
        self.grid.fill_square(user='X', square='2')
        self.grid = self.book.check_win(self.grid)
        result = self.grid.test_win()
        self.assertEquals(result, 'X')
        
    def testBlock(self):
        self.grid.fill_square(user='O', square='4')
        self.grid.fill_square(user='O', square='5')
        self.grid = self.book.check_win(self.grid)
        self.assertTrue(self.grid.filled['X'].__contains__('6'))


if __name__ == "__main__":
    unittest.main()