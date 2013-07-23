'''
Created on Jul 23, 2013

@author: christie
'''
import unittest
from com.cox import board

class Test(unittest.TestCase):


    def setUp(self):
        self.board = board.board()        
    
    def test_printboard(self):        
        self.board.print_board()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_printboard']
    unittest.main()