import unittest

from tickytack.engines import MinMax
from tickytack.engines import ROWS


DEMO_BOARD_1 = ['x', 'o', 'x',
                'o', 'x', ' ',
                ' ', ' ', 'o']

DEMO_BOARD_2 = ['x', ' ', ' ',
                ' ', ' ', ' ',
                ' ', ' ', ' ']

DEMO_BOARD_3 = ['x', 'o', ' ',
                ' ', 'x', 'o',
                ' ', ' ', 'x']

DEMO_BOARD_4 = ['x', 'o', 'o',
                'o', 'x', 'x',
                'x', 'x', 'o']


class TestMinMaxEngine(unittest.TestCase):

    def setUp(self):
        self.engine = MinMax
        self.board = self.engine(DEMO_BOARD_1, 'x')

    def test_get_children(self):
        board = MinMax(DEMO_BOARD_1, 'x')
        # this board has player 'x', children should have player 'o'
        count = 0
        for child, move in board._get_children():
            self.assertEquals(child.player, 'o',
                              'child has wrong player set')
            self.assertTrue(move in [5, 6, 7],
                            'unexpected move: %s' % move)
            count += 1
        self.assertEquals(count, 3,
                          "wrong number of children: %s" % count)

    def test_calculate_line_score(self):
        """ assert that line values are calculated as expected
        """
        scores = []
        expected = [0, 0, -10, 0, 0, 0, 0, 300]
        for row in ROWS:
            line = [self.board.board[cell] for cell in row]
            score = self.board._calculate_line_score(line)
            scores.append(score)

        for actual, expect in zip(scores, expected):
            self.assertEquals(actual, expect,
                              'expected %s, got %s' % (expect, actual))

    def test_calculate_score(self):
        # score should be set at __init__ time
        self.assertEquals(self.board.score, 290)
        # but if we clear it, we can recalculate automatically
        self.board._score = None
        self.assertEquals(self.board.score, 290)

    def test_is_terminal(self):
        for b in [DEMO_BOARD_1, DEMO_BOARD_2]:
            board = MinMax(b, 'x')
            self.assertFalse(board.is_terminal,
                             'this board should not be terminal: %s' % b)
        for b in [DEMO_BOARD_3, DEMO_BOARD_4]:
            board = MinMax(b, 'x')
            self.assertTrue(board.is_terminal,
                            'this board should be terminal: %s' % b)

    def test_get_move(self):
        score, move = self.board.choose(9, -999999, 999999)
        self.assertEqual(score, 1000)
        self.assertEqual(move, 6)
