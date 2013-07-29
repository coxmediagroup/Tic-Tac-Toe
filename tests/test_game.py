'''
Created on Jul 23, 2013

@author: christie
'''
import unittest
from com.cox import game


class Test(unittest.TestCase):


    def setUp(self):
        self.game = game.game()


    def tearDown(self):
        pass


    def test_select_letters(self):
        self.game.select_letters()
        
    def test_toss(self):
        head_tail = self.game.toss()
        assert(head_tail == 'computer')

if __name__ == "__main__":
    unittest.main()