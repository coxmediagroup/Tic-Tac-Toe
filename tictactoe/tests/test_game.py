import mocker
import unittest2 as unittest

from tictactoe import game
from tictactoe.board import Board


class TestGame(mocker.MockerTestCase, unittest.TestCase):
    """Examples of using mocker to test functionality requiring
    input from stdin.

    """

    def test_get_player_choice_for_human_succeeds(self):
        mock_input = self.mocker.replace(raw_input)
        mock_input(mocker.ANY)
        expected_player = 'x'
        self.mocker.result(expected_player.upper())
        self.mocker.replay()

        player = game.get_player_choice_for_human()
        self.assertEqual(player, expected_player, 'Invalid player returned')

    def test_ask_yes_no_question(self):
        mock_input = self.mocker.replace(raw_input)
        mock_input(mocker.ANY)
        expected_choice = ''
        self.mocker.result(expected_choice)
        self.mocker.replay()

        self.assertTrue(game.ask_yes_no_question(''), 'Invalid result')

    def test_human_moves_first_succeeds(self):
        mock_input = self.mocker.replace(raw_input)
        mock_input(mocker.ANY)
        expected_choice = 'n'
        self.mocker.result(expected_choice)
        self.mocker.replay()

        self.assertFalse(game.human_moves_first(), 'Invalid choice returned')

    def test_get_move_position_for_human(self):
        mock_input = self.mocker.replace(raw_input)
        mock_input(mocker.ANY)
        self.mocker.result('1')
        self.mocker.replay()

        position = game.get_move_position_for_human(Board(), 'x')
        self.assertEqual(position, 0, 'Invalid position returned')
