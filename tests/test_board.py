'''
Created on Jul 23, 2013

@author: christie
'''
import unittest
from com.cox import board

class Test(unittest.TestCase):


    def setUp(self):
        self.board = board.board(human='O', computer='X')        
    
    def test_printboard(self):        
        self.board.print_board()
    
    def test_letter_selection(self):
        assert(self.board.players.get('human')=='O')
        assert(self.board.players.get('computer')=='X')


if __name__ == "__main__":
    unittest.main()