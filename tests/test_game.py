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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()