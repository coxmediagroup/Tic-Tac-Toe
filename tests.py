import unittest

from grid import Grid
from book import Book

class TestGrid(unittest.TestCase):
    ''' Unittest for the grid class
    '''
    def setUp(self):
        self.grid = Grid()
        
    def testSquareAvailabe(self):
        ''' Asserts square_taken returns the correct boolean for a free square
        '''
        self.assertFalse(self.grid.square_taken('1'))
        
    def testAvailable(self):
        ''' Asserts that the get_available function is altered by filling squares
        '''
        self.assertEquals(self.grid.get_available(), ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.grid.fill_square(user='X', square = '7')
        available = self.grid.get_available()
        self.assertFalse(available.__contains__('7'))
        
    def testFillSquare(self):
        ''' Asserts that filling a square works
        '''
        self.grid.fill_square(user='X', square='2')
        self.assertTrue(self.grid.printable.__contains__('X'))
        self.assertFalse(self.grid.printable.__contains__('2'))
        
    def testWin(self):
        ''' Asserts that the grid can detect wins
        '''
        self.assertFalse(self.grid.test_win())
        
        self.grid.fill_square(user='X', square='1')
        self.grid.fill_square(user='X', square='2')
        self.grid.fill_square(user='X', square='3')
        self.assertEquals(self.grid.test_win(), 'X')
        
class TestBook(unittest.TestCase):
    ''' Unittest for the book class (just the non-logic functions. Logic is tested elsewhere)
    '''
    def setUp(self):
        self.grid = Grid()
        self.book = Book('X')
        
    def test_check_win(self):
        ''' Book can detect a threat
        '''
        self.grid.fill_square(user='X', square='1')
        self.grid.fill_square(user='X', square='2')
        self.grid, win = self.book.check_win(grid=self.grid, player='X')
        self.assertEquals(self.grid.test_win(), 'X')
        
    
        
        
class TestPlayerOneLogic(unittest.TestCase):
    ''' Unittests for the logic patterns if the book is the first player
    '''
    def setUp(self):
        self.grid = Grid()
        self.book = Book('X')
        
    def test_first_center_corner(self):
        ''' Game for the second player taking the center, then a corner
        '''
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
        ''' Game for the second player taking the center, then an edge
        '''
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
        ''' Game for the second player taking a corner
        '''
        moves = ['3', '5', '4']
        moves.reverse()
        while not self.grid.test_win():
            self.grid = self.book.check_grid(self.grid)
            try:
                self.grid = self.grid.fill_square(user='O', square = moves.pop())
            except:
                break
        self.assertEquals(self.grid.test_win(), 'X')
    
    def test_first_edge_nothreat(self):
        ''' Game where the second player takes an edge, followed by a non-threat move
        '''
        moves = ['4', '9', '7']
        moves.reverse()
        while not self.grid.test_win():
            self.grid = self.book.check_grid(self.grid)
            try:
                self.grid = self.grid.fill_square(user='O', square=moves.pop())
            except:
                break
        self.assertEquals(self.grid.test_win(), 'X')
        
    def test_first_edge_threat(self):
        ''' Game where the second player takes an edge, followed by a threat
        '''
        moves = ['6', '9', '7']
        moves.reverse()
        while not self.grid.test_win():
            self.grid = self.book.check_grid(self.grid)
            try:
                self.grid = self.grid.fill_square(user='O', square=moves.pop())
            except:
                break
        self.assertEquals(self.grid.test_win(), 'X')
        
class TestPlayerTwoLogic(unittest.TestCase):
    ''' Unittests for when the book goes second
    '''
    
    def setUp(self):
        self.grid = Grid()
        self.book = Book('O')
        
    def run_game(self, moves):
        while not self.grid.test_win() and self.grid.get_available():
            try:
                self.grid = self.grid.fill_square(user='O', square=moves.pop())
            except:
                break
            self.grid = self.book.check_grid(self.grid)
        
    def test_noncenter_threat_threat(self):
        moves = ['1', '4', '3', '8', '9']
        moves.reverse()
        self.run_game(moves)
        self.assertEquals(self.grid.test_win(), 'O')
            
    def test_noncenter_threat_nothreat(self):
        moves = ['7', '9', '2', '6', '1']
        moves .reverse()
        self.run_game(moves)
        self.assertEquals(self.grid.test_win(), 'O')
        
    
        
        
if __name__ == "__main__":
    unittest.main()