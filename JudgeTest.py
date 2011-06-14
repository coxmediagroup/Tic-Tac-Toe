import unittest
import Judge


class TestJudge(unittest.TestCase):
    
    
    def setUp(self):
        self.board = Board()
        self.judge = Judge()

    def tearDown(self):
        self.board = null
        self.judge = null



