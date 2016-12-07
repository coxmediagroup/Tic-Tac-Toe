from django.test import TestCase
from minimax.minimax import Board, play_turn

class MinimaxTests(TestCase):

    def setUp(self):
        pass
    
    def test_minimax_always_ties_itself(self):
        for unused in range(10):
            board = [0] * 9
            status = 0
            while status == 0:
                status, board = play_turn(board=board, curplayer=Board.X)
                status, board = play_turn(board=board, curplayer=Board.O)
            self.assertEqual(status, 3)
