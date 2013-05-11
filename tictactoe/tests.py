import unittest
from . import Board, naught_bot

class BoardTests(unittest.TestCase):
    """
    Tests showing the rules of the game are being respected.
    """
    def test_board_raises_when_marking_a_non_empty_cell(self):
        raise NotImplementedError


class NaughtBotTests(unittest.TestCase):
    """
    Tests demonstrating naught_bot's decision-making process.
    """
    def test_knows_if_it_went_first(self):
        raise NotImplementedError

    def test_knows_if_it_went_second(self):
        raise NotImplementedError

    def test_knows_when_to_block(self):
        raise NotImplementedError

    def test_knows_when_to_push_for_a_win(self):
        raise NotImplementedError