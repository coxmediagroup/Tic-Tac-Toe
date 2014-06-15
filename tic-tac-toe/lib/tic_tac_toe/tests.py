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
            '. X X . O X O O X',
        )
        for board in board_configs:
            game = TicTacToeGame(board=board.split())
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
