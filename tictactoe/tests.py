from django.core.urlresolvers import reverse
from django.test import SimpleTestCase, TestCase
from rest_framework.test import APITestCase
import mock

from .board import Board
from .models import Game
from .strategy import RandomStrategy, MinimaxStrategy


class BoardTest(SimpleTestCase):
    def test_new_game(self):
        b = Board()
        expected = (
            ' | | \n'
            '-+-+-\n'
            ' | | \n'
            '-+-+-\n'
            ' | | ')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(0, b.state())
        self.assertEqual(Board.X_NEXT, b.next_mark())
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8], b.next_moves())
        self.assertIsNone(b.winner())

    def test_one_move(self):
        b = Board(state=1)
        expected = (
            'X| | \n'
            '-+-+-\n'
            ' | | \n'
            '-+-+-\n'
            ' | | ')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(1, b.state())
        self.assertEqual(Board.O_NEXT, b.next_mark())
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], b.next_moves())
        self.assertIsNone(b.winner())

    def test_row1_winner(self):
        b = Board(state=14755)
        expected = (
            'X|X|X\n'
            '-+-+-\n'
            ' |O| \n'
            '-+-+-\n'
            'O| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.X_WINS, b.winner())
        self.assertEqual([(0, 1, 2)], b.winning_positions())
        self.assertIsNone(b.next_mark())
        self.assertEqual([], b.next_moves())

    def test_row2_winner(self):
        b = Board(state=9453)
        expected = (
            ' |X| \n'
            '-+-+-\n'
            'O|O|O\n'
            '-+-+-\n'
            ' |X|X')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.O_WINS, b.winner())
        self.assertEqual([(3, 4, 5)], b.winning_positions())

    def test_row3_winner(self):
        b = Board(state=9695)
        expected = (
            'O| | \n'
            '-+-+-\n'
            'O|O| \n'
            '-+-+-\n'
            'X|X|X')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.X_WINS, b.winner())
        self.assertEqual([(6, 7, 8)], b.winning_positions())

    def test_col1_winner(self):
        b = Board(state=10343)
        expected = (
            'O| | \n'
            '-+-+-\n'
            'O|X| \n'
            '-+-+-\n'
            'O|X|X')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.O_WINS, b.winner())
        self.assertEqual([(0, 3, 6)], b.winning_positions())

    def test_col2_winner(self):
        b = Board(state=3783)
        expected = (
            ' |X| \n'
            '-+-+-\n'
            'O|X| \n'
            '-+-+-\n'
            'O|X| ')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.X_WINS, b.winner())
        self.assertEqual([(1, 4, 7)], b.winning_positions())

    def test_col3_winner(self):
        b = Board(state=14439)
        expected = (
            ' |X|O\n'
            '-+-+-\n'
            ' |X|O\n'
            '-+-+-\n'
            'X| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.O_WINS, b.winner())
        self.assertEqual([(2, 5, 8)], b.winning_positions())

    def test_rising_slash_winner(self):
        b = Board(state=14427)
        expected = (
            ' | |X\n'
            '-+-+-\n'
            ' |X|O\n'
            '-+-+-\n'
            'X| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.X_WINS, b.winner())
        self.assertEqual([(2, 4, 6)], b.winning_positions())

    def test_falling_slash_winner(self):
        b = Board(state=14267)
        expected = (
            'O| |X\n'
            '-+-+-\n'
            ' |O|X\n'
            '-+-+-\n'
            'X| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.O_WINS, b.winner())
        self.assertEqual([(0, 4, 8)], b.winning_positions())

    def test_two_way_winner(self):
        self.assertRaises(ValueError, Board, state=715)
        b = Board(state=18859)
        expected = (
            'X|X|X\n'
            '-+-+-\n'
            'O|X|O\n'
            '-+-+-\n'
            'X|O|O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.X_WINS, b.winner())
        self.assertEqual([(0, 1, 2), (2, 4, 6)], b.winning_positions())

    def test_tie(self):
        b = Board(state=12119)
        expected = (
            'O|X|O\n'
            '-+-+-\n'
            'X|O|X\n'
            '-+-+-\n'
            'X|O|X')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.TIE, b.winner())
        self.assertEqual([], b.winning_positions())

    def test_two_winners_raises(self):
        self.assertRaises(ValueError, Board, state=715)
        # This corresponds to this board:
        # X|X|X #
        # -+-+- #
        # O|O|O #
        # -+-+- #
        #  | |  #

    def test_large_state_raises(self):
        self.assertRaises(ValueError, Board, state=pow(3, 9))

    def test_O_first_raises(self):
        self.assertRaises(ValueError, Board, state=2)

    def test_too_many_X_raises(self):
        self.assertRaises(ValueError, Board, state=4)

    def test_valid_move(self):
        b = Board()
        b.move(0)
        expected = (
            'X| | \n'
            '-+-+-\n'
            ' | | \n'
            '-+-+-\n'
            ' | | ')
        self.assertEqual(expected, str(b))
        self.assertEqual(1, b.state())
        self.assertIsNone(b.winner())

    def test_winning_move(self):
        b = Board(state=228)
        expected = (
            ' |X|X\n'
            '-+-+-\n'
            'O|O| \n'
            '-+-+-\n'
            ' | | ')
        self.assertEqual(expected, str(b))
        b.move(0)
        expected = (
            'X|X|X\n'
            '-+-+-\n'
            'O|O| \n'
            '-+-+-\n'
            ' | | ')
        self.assertEqual(expected, str(b))
        self.assertEqual(Board.X_WINS, b.winner())
        self.assertIsNone(b.next_mark())
        self.assertEqual([], b.next_moves())

    def test_invalid_move_raises(self):
        b = Board(state=1)
        self.assertRaises(ValueError, b.move, 0)


class GameAPITest(APITestCase):
    '''Test the Game API'''

    def setUp(self):
        patcher = mock.patch('tictactoe.strategy.random_choice')
        self.addCleanup(patcher.stop)
        self.mock_choice = patcher.start()

    def test_list_no_games(self):
        response = self.client.get(
            reverse('game-list'), format='json')
        self.assertEqual(200, response.status_code, response.content)
        expected = {'count': 0, 'next': None, 'previous': None, 'results': []}
        self.assertEqual(expected, response.data)

    def test_create_game_server_is_first(self):
        self.mock_choice.return_value = 0
        response = self.client.post(
            reverse('game-list'), {'server_player': Game.PLAYER_X})
        self.assertEqual(201, response.status_code, response.content)
        game = Game.objects.latest('id')
        expected_url = (
            'http://testserver' +
            reverse('game-detail', kwargs={'pk': game.id}))
        self.assertEqual(expected_url, response['location'])
        expected = {
            'id': game.id,
            'url': expected_url,
            'board': [1, 0, 0, 0, 0, 0, 0, 0, 0],
            'next_moves': [1, 2, 3, 4, 5, 6, 7, 8],
            'move_url': expected_url + 'move/',
            'server_player': Game.PLAYER_X,
            'winner': 0,
            'winning_positions': [],
        }
        self.assertEqual(expected, response.data)
        self.mock_choice.assert_called_once_with(range(9))

    def test_create_game_server_is_second(self):
        self.mock_choice.side_effect = Exception('Not called')
        response = self.client.post(
            reverse('game-list'), {'server_player': Game.PLAYER_O})
        self.assertEqual(201, response.status_code, response.content)
        game = Game.objects.latest('id')
        expected_url = (
            'http://testserver' +
            reverse('game-detail', kwargs={'pk': game.id}))
        self.assertEqual(expected_url, response['location'])
        expected = {
            'id': game.id,
            'url': expected_url,
            'board': [0, 0, 0, 0, 0, 0, 0, 0, 0],
            'next_moves': [0, 1, 2, 3, 4, 5, 6, 7, 8],
            'move_url': expected_url + 'move/',
            'server_player': Game.PLAYER_O,
            'winner': 0,
            'winning_positions': [],
        }
        self.assertEqual(expected, response.data)

    def test_retrieve_game(self):
        game = Game.objects.create(server_player=Game.PLAYER_O)
        path = reverse('game-detail', kwargs={'pk': game.id})
        response = self.client.get(path)
        self.assertEqual(200, response.status_code, response.content)
        expected_url = 'http://testserver' + path
        expected = {
            'id': game.id,
            'url': expected_url,
            'board': [0, 0, 0, 0, 0, 0, 0, 0, 0],
            'next_moves': [0, 1, 2, 3, 4, 5, 6, 7, 8],
            'move_url': expected_url + 'move/',
            'server_player': Game.PLAYER_O,
            'winner': 0,
            'winning_positions': [],
        }
        self.assertEqual(expected, response.data)

    def test_retrieve_game_as_html(self):
        game = Game.objects.create(server_player=Game.PLAYER_O)
        path = reverse('game-detail', kwargs={'pk': game.id})
        response = self.client.get(path, {'format': 'html'})
        self.assertEqual(200, response.status_code, response.content)
        self.assertContains(response, 'ttt_data')
        expected_url = 'http://testserver' + path
        expected = {
            'id': game.id,
            'url': expected_url,
            'board': [0, 0, 0, 0, 0, 0, 0, 0, 0],
            'next_moves': [0, 1, 2, 3, 4, 5, 6, 7, 8],
            'move_url': expected_url + 'move/',
            'server_player': Game.PLAYER_O,
            'winner': 0,
            'winning_positions': [],
        }
        self.assertEqual(expected, response.data)

    def test_make_move(self):
        self.mock_choice.return_value = 2
        game = Game.objects.create(server_player=Game.PLAYER_O)
        path = reverse('game-move', kwargs={'pk': game.id})
        response = self.client.post(path, {'position': 0}, follow=True)
        expected_url = reverse('game-detail', kwargs={'pk': game.id})
        self.assertRedirects(response, expected_url)
        game = Game.objects.get(id=game.id)
        expected = (
            'X| |O\n'
            '-+-+-\n'
            ' | | \n'
            '-+-+-\n'
            ' | | ')
        self.assertEqual(expected, str(game.board))

    def test_make_winning_move(self):
        self.mock_choice.side_effect = Exception('Not called')
        game = Game.objects.create(server_player=Game.PLAYER_X, state=861)
        expected_board = (
            ' |O|O\n'
            '-+-+-\n'
            'X|X| \n'
            '-+-+-\n'
            'X| | ')
        self.assertEqual(expected_board, str(game.board))
        path = reverse('game-move', kwargs={'pk': game.id})
        response = self.client.post(path, {'position': 0}, follow=True)
        expected_url = reverse('game-detail', kwargs={'pk': game.id})
        self.assertRedirects(response, expected_url)
        game = Game.objects.get(id=game.id)
        self.assertEqual(game.state, 863)
        expected_board = (
            'O|O|O\n'
            '-+-+-\n'
            'X|X| \n'
            '-+-+-\n'
            'X| | ')
        self.assertEqual(expected_board, str(game.board))

    def test_make_duplicate_move(self):
        self.mock_choice.side_effect = Exception('Not called')
        game = Game.objects.create(server_player=Game.PLAYER_X, state=88)
        expected_board = (
            'X|O| \n'
            '-+-+-\n'
            ' |X| \n'
            '-+-+-\n'
            ' | | ')
        self.assertEqual(expected_board, str(game.board))
        path = reverse('game-move', kwargs={'pk': game.id})
        response = self.client.post(path, {'position': 1})
        self.assertEqual(400, response.status_code, response.content)
        expected = {'position': '1 is an invalid move'}
        self.assertEqual(expected, response.data)

    def test_make_invalid_move(self):
        self.mock_choice.side_effect = Exception('Not called')
        game = Game.objects.create(server_player=Game.PLAYER_O)
        path = reverse('game-move', kwargs={'pk': game.id})
        response = self.client.post(path, {'position': 'foo'})
        self.assertEqual(400, response.status_code, response.content)
        expected = {
            'position': "invalid literal for int() with base 10: 'foo'"}
        self.assertEqual(expected, response.data)

    def test_make_move_complete_game(self):
        self.mock_choice.side_effect = Exception('Not called')
        game = Game.objects.create(server_player=Game.PLAYER_X, state=863)
        path = reverse('game-move', kwargs={'pk': game.id})
        response = self.client.post(path, {'position': 5})
        self.assertEqual(400, response.status_code, response.content)
        expected = {'position': '5 is an invalid move'}
        self.assertEqual(expected, response.data)

    def test_make_move_without_position(self):
        self.mock_choice.side_effect = Exception('Not called')
        game = Game.objects.create(server_player=Game.PLAYER_X, state=863)
        path = reverse('game-move', kwargs={'pk': game.id})
        response = self.client.post(path)
        self.assertEqual(400, response.status_code, response.content)
        expected = {'position': 'must be a valid next move'}
        self.assertEqual(expected, response.data)


class GameModelTest(SimpleTestCase):
    '''Game tests that do not require a database'''

    def test_other_player_O(self):
        game = Game(server_player=Game.PLAYER_X)
        self.assertEqual(Game.PLAYER_O, game.other_player)

    def test_other_player_X(self):
        game = Game(server_player=Game.PLAYER_O)
        self.assertEqual(Game.PLAYER_X, game.other_player)

    def test_get_board(self):
        game = Game(state=220)
        board = game.board
        expected = (
            'X|X| \n'
            '-+-+-\n'
            'O|O| \n'
            '-+-+-\n'
            ' | | ')
        self.assertEqual(expected, str(board))
        self.assertEqual(220, board.state())

    def test_set_board_in_progress(self):
        board = Board(state=220)
        game = Game()
        game.board = board
        self.assertEqual(220, game.state)
        self.assertEqual(Game.IN_PROGRESS, game.winner)

    def test_set_board_winner(self):
        board = Board(state=18859)
        game = Game()
        game.board = board
        self.assertEqual(18859, game.state)
        self.assertEqual(Game.X_WINS, game.winner)

    def test_random_strategy(self):
        game = Game(strategy_type=Game.RANDOM_STRATEGY)
        strategy = game.strategy
        self.assertTrue(isinstance(strategy, RandomStrategy))


class GameViewTest(TestCase):
    '''User's game interface'''
    def test_start_game(self):
        url = reverse('start-game')
        response = self.client.post(
            url, data={'server_player': 1}, follow=True)
        game = Game.objects.latest('id')
        game_url = reverse('play-game', kwargs={'game_id': game.id})
        self.assertRedirects(response, game_url)
        self.assertContains(response, url)

    def test_start_game_bad_args(self):
        url = reverse('start-game')
        response = self.client.post(
            url, data={'server_player': 4}, follow=True)
        self.assertFalse(Game.objects.exists())
        self.assertContains(response, 'Start over?', status_code=400)


class RandomStrategyTest(SimpleTestCase):
    @mock.patch('tictactoe.strategy.random_choice')
    def test_random_move(self, mock_choice):
        board = Board(state=220)
        expected = (
            'X|X| \n'
            '-+-+-\n'
            'O|O| \n'
            '-+-+-\n'
            ' | | ')
        self.assertEqual(expected, str(board))
        strategy = RandomStrategy()
        mock_choice.return_value = 7

        move = strategy.next_move(board)
        self.assertEqual(7, move)
        mock_choice.assert_called_once_with([2, 5, 6, 7, 8])


class MinimaxStrategyTest(SimpleTestCase):
    def setUp(self):
        self.strategy = MinimaxStrategy()

    def test_one_move_left(self):
        board = Board(state=17230)
        expected = (
            'X|X| \n'
            '-+-+-\n'
            'O|O|X\n'
            '-+-+-\n'
            'O|X|O')
        self.assertMultiLineEqual(expected, str(board))
        res = self.strategy.score_moves(board)
        self.assertEqual(res, {2: 2})
        self.assertEqual(2, self.strategy.next_move(board))

    def test_o_wins_next_move(self):
        board = Board(state=10426)
        expected = (
            'X|X| \n'
            '-+-+-\n'
            'O|O| \n'
            '-+-+-\n'
            'O|X|X')
        self.assertMultiLineEqual(expected, str(board))
        res = self.strategy.score_moves(board)
        self.assertEqual(res, {2: -3, 5: -3})
        self.assertTrue(self.strategy.next_move(board) in [2, 5])

    def test_o_can_win_next_move(self):
        board = Board(state=4108)
        expected = (
            'X|X| \n'
            '-+-+-\n'
            'O|O|X\n'
            '-+-+-\n'
            'O|X| ')
        self.assertMultiLineEqual(expected, str(board))
        res = self.strategy.score_moves(board)
        self.assertEqual(res, {2: -3, 8: 2})
        self.assertEqual(2, self.strategy.next_move(board))

    def test_x_can_win_on_next_move(self):
        board = Board(state=3865)
        expected = (
            'X|X| \n'
            '-+-+-\n'
            'O|O| \n'
            '-+-+-\n'
            'O|X| ')
        self.assertMultiLineEqual(expected, str(board))
        res = self.strategy.score_moves(board)
        self.assertEqual(res, {2: 4, 5: -3, 8: -3})
        self.assertEqual(2, self.strategy.next_move(board))
