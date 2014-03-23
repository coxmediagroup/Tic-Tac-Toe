import unittest

import game


class TestMoves(unittest.TestCase):

    def test_ai_move_one(self):
        actual = game.ai_move_one()
        expected = ['cell-0:0', 'cell-0:2', 'cell-1:1', 'cell-2:0', 'cell-2:2']
        self.assertIn(actual, expected)


class TestAIFirstCornerTurn3(unittest.TestCase):

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
        # | |X
        #-----
        # | |
        #-----
        # |P|A
        actual = game.calc_ai_move(['cell-2:1'], ['cell-2:2'])
        self.assertEqual('cell-0:2', actual)

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


class TestAIFirstCornerTurn5(unittest.TestCase):

    def test_player_block(self):
        #P| |X
        #-----
        # | |
        #-----
        #A|P|A
        actual = game.calc_ai_move(['cell-0:0', 'cell-2:1'], ['cell-2:0', 'cell-2:2'])
        self.assertEqual('cell-0:2', actual)
        #X| |A
        #-----
        # | |P
        #-----
        # |P|A
        actual = game.calc_ai_move(['cell-2:1', 'cell-1:2'], ['cell-2:2', 'cell-0:2'])
        self.assertEqual('cell-0:0', actual)

    @unittest.skip('unfinished')
    def test_player_no_block(self):
        #P| |P
        #-----
        # | |
        #-----
        #A|X|A
        actual = game.calc_ai_move(['cell-0:0', 'cell-0:2'], ['cell-2:0', 'cell-2:2'])
        expected = dict(
            cell='cell-2:1',
            victor='ai',
            row=('cell-2:0', 'cell-2:1', 'cell-2:2'),
        )
        self.assertEqual(expected, actual)
        #A| |P
        #-----
        #X| |
        #-----
        #A| |P
        actual = game.calc_ai_move(['cell-2:2', 'cell-0:2'], ['cell-2:0', 'cell-0:0'])
        expected = dict(
            cell='cell-1:0',
            victor='ai',
            row=('cell-0:0', 'cell-1:0', 'cell-2:0'),
        )
        self.assertEqual(expected, actual)
