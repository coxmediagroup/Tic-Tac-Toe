import unittest

import mock

import game


class TestMoves(unittest.TestCase):

    def test_ai_move_one(self):
        actual = game.ai_move_one()
        expected = ['cell-0:0', 'cell-0:2', 'cell-2:0', 'cell-2:2']
        self.assertIn(actual, expected)


class TestAIFirstCornerTurn3(unittest.TestCase):

    def test_player_edge(self):
        # | |
        #-----
        #P| |
        #-----
        #A| |X
        actual = game.calc_ai_move(['cell-1:0'], ['cell-2:0'])
        self.assertEqual(dict(cell='cell-2:2'), actual)
        #X|P|
        #-----
        # | |
        #-----
        #A| |X
        actual = game.calc_ai_move(['cell-0:1'], ['cell-2:0'])
        self.assertIn(actual, [dict(cell='cell-2:2'), dict(cell='cell-0:0')])
        #X| |
        #-----
        # | |P
        #-----
        #A| |X
        actual = game.calc_ai_move(['cell-1:2'], ['cell-2:0'])
        self.assertIn(actual, [dict(cell='cell-2:2'), dict(cell='cell-0:0')])
        #X| |
        #-----
        # | |
        #-----
        #A|P|
        actual = game.calc_ai_move(['cell-2:1'], ['cell-2:0'])
        self.assertEqual(dict(cell='cell-0:0'), actual)
        # | |X
        #-----
        # | |
        #-----
        # |P|A
        actual = game.calc_ai_move(['cell-2:1'], ['cell-2:2'])
        self.assertEqual(dict(cell='cell-0:2'), actual)

    def test_player_corner(self):
        #X| |
        #-----
        # | |
        #-----
        #A| |P
        actual = game.calc_ai_move(['cell-2:2'], ['cell-2:0'])
        self.assertEqual(dict(cell='cell-0:0'), actual)
        #P| |
        #-----
        # | |
        #-----
        #A| |X
        actual = game.calc_ai_move(['cell-0:0'], ['cell-2:0'])
        self.assertEqual(dict(cell='cell-2:2'), actual)

    def test_player_center(self):
        #A| |
        #-----
        # |P|
        #-----
        # | |X
        actual = game.calc_ai_move(['cell-1:1'], ['cell-0:0'])
        self.assertEqual(dict(cell='cell-2:2'), actual)


class TestAIFirstCornerTurn5(unittest.TestCase):

    def test_player_block(self):
        #P| |X
        #-----
        # | |
        #-----
        #A|P|A
        actual = game.calc_ai_move(['cell-0:0', 'cell-2:1'], ['cell-2:0', 'cell-2:2'])
        self.assertEqual(dict(cell='cell-0:2'), actual)
        #X| |A
        #-----
        # | |P
        #-----
        # |P|A
        actual = game.calc_ai_move(['cell-2:1', 'cell-1:2'], ['cell-2:2', 'cell-0:2'])
        self.assertEqual(dict(cell='cell-0:0'), actual)

    @mock.patch('game.choice')
    def test_player_no_block(self, _choice):
        _choice.return_value = 'I win!'
        #P| |P
        #-----
        # | |
        #-----
        #A|X|A
        actual = game.calc_ai_move(['cell-0:0', 'cell-0:2'], ['cell-2:0', 'cell-2:2'])
        expected = dict(
            cell='cell-2:1',
            winning_cells=('cell-2:0', 'cell-2:1', 'cell-2:2'),
            message='I win!',
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
            winning_cells=('cell-0:0', 'cell-1:0', 'cell-2:0'),
            message='I win!',
        )
        self.assertEqual(expected, actual)

    def test_player_center(self):
        #A| |P
        #-----
        # |P|
        #-----
        #X| |A
        actual = game.calc_ai_move(['cell-1:1', 'cell-0:2'], ['cell-0:0', 'cell-2:2'])
        self.assertEqual(dict(cell='cell-2:0'), actual)


class TestAIFirstCornerTurn7(unittest.TestCase):

    @mock.patch('game.choice')
    def test_player_block(self, _choice):
        _choice.return_value = 'I win!'
        # At this point there's a trap setup, so it's a meager block attempt

        #A|P|A
        #-----
        # |P|X
        #-----
        #P| |A
        actual = game.calc_ai_move(['cell-2:0', 'cell-0:1', 'cell-1:1'], ['cell-0:0', 'cell-0:2', 'cell-2:2'])
        expected = dict(
            cell='cell-1:2',
            winning_cells=('cell-0:2', 'cell-1:2', 'cell-2:2'),
            message='I win!',
        )
        self.assertEqual(expected, actual)

    def test_draw_handled(self):
        # occurs on this turn if the player chose an edge cell for their second
        # play rather than a corner cell
        #A|A|P
        #-----
        # |P|
        #-----
        # |P|A
        actual = game.calc_ai_move(['cell-1:1', 'cell-2:1', 'cell-0:2'], ['cell-0:0', 'cell-2:2', 'cell-0:1'])
        expected = dict(
            draw_cell='cell-0:2',
            message=("I'm pretty sure you just misclicked. I mean, it's almost as if you want the game "
                     "to end in a draw. I'm going to give you the benefit of the doubt and just assume "
                     "you totally did not intend for this match to be a tie. Lucky you! You get to pick "
                     "again!")
        )
        self.assertEqual(expected, actual)
