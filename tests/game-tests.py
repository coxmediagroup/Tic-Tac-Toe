import unittest

import game


class TestMoves(unittest.TestCase):

    def test_ai_move_one(self):
        actual = game.ai_move_one()
        expected = ['cell-0:0', 'cell-0:2', 'cell-1:1', 'cell-2:0', 'cell-2:2']
        self.assertIn(actual, expected)


class TestAIFirstCornerTurn3(unittest.TestCase):

    def setUp(self):
        pass

    def test_player_edge(self):
        # | |
        #-----
        #P| |
        #-----
        #A| |X
        actual = game.calc_ai_move(['cell-1:0'], ['cell-2:0'])
        self.assertEqual('cell-2:2', actual)
        #X|P|
        #-----
        # | |
        #-----
        #A| |X
        actual = game.calc_ai_move(['cell-0:1'], ['cell-2:0'])
        self.assertIn(actual, ['cell-2:2', 'cell-0:0'])
        #X| |
        #-----
        # | |P
        #-----
        #A| |X
        actual = game.calc_ai_move(['cell-1:2'], ['cell-2:0'])
        self.assertIn(actual, ['cell-2:2', 'cell-0:0'])
        #X| |
        #-----
        # | |
        #-----
        #A|P|
        actual = game.calc_ai_move(['cell-2:1'], ['cell-2:0'])
        self.assertEqual('cell-0:0', actual)

    def test_player_corner(self):
        #X| |
        #-----
        # | |
        #-----
        #A| |P
        actual = game.calc_ai_move(['cell-2:2'], ['cell-2:0'])
        self.assertEqual('cell-0:0', actual)
        #P| |
        #-----
        # | |
        #-----
        #A| |X
        actual = game.calc_ai_move(['cell-0:0'], ['cell-2:0'])
        self.assertEqual('cell-2:2', actual)
