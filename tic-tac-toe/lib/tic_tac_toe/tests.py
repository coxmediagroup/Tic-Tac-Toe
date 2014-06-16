import unittest

from core import TicTacToeGame, ComputerPlayer


class TestTicTacToeGame(unittest.TestCase):
    
    def test_board_when_game_created_is_empty(self):
        game = TicTacToeGame()
        self.assertSequenceEqual(game._board, [None] * 9)
    
    def test_game_winner_is_none_after_creation(self):
        game = TicTacToeGame()
        self.assertIsNone(game.winner)
    
    def test_available_positions(self):
        game = TicTacToeGame()
        self.assertSequenceEqual(game.available_positions(), range(9))
        
        game = TicTacToeGame(board='X O X O'.split() + [None] * 5)
        self.assertSequenceEqual(game.available_positions(), [4, 5, 6, 7, 8])
    
    def test_game_is_over_by_x_player_wins(self):
        board_configs = (
            'X X X O X O X O O',
            'X X O O X X O O X',
            'O X O X X X O O X',
        )
        board_configs = [b.split() for b in board_configs]
        board_configs.append([None, 'X', 'X', None, 'O', 'X', 'O', 'O', 'X'])
        
        for board in board_configs:
            game = TicTacToeGame(board=board)
            self.assertEquals(game.winner, 'X')
    
    def test_game_is_a_draw(self):
        game = TicTacToeGame(board='O X O X X O O O X'.split())
        self.assertTrue(game.is_over and game.winner is None)
    
    def test_computer_plays_best_winning_move(self):
        board_configs = (
            (4, ['O', None, 'X', 'X', None, None, 'X', 'O', 'O']),
            (4, [None, 'X', 'O', None, None, 'X', 'O', 'O', 'X']),
            (3, ['O', 'X', 'O', None, 'X', 'X', 'O', 'O', 'X']),
            (2, [None, 'X', None, None, 'O', 'X', 'O', 'O', 'X']),
            (0, [None, 'X', 'O', 'O', 'X', 'X', 'O', 'O', 'X']),
        )
        computer_player = ComputerPlayer()
        
        for best_move, board in board_configs:
            game = TicTacToeGame(board=board)
            computer_player.do_move(game)
            self.assertEquals(game._board[best_move], 'X')

    def test_game_cannot_be_created_with_odd_chars(self):
        tampered_board = 'X X X O X O X O Y'.split()
        self.assertRaises(Exception, TicTacToeGame.from_game, game=tampered_board)
    
    def test_game_cannot_be_created_with_wrong_size(self):
        wrong_sized_board = 'X X X O'.split()
        self.assertRaises(Exception, TicTacToeGame.from_game, game=wrong_sized_board)