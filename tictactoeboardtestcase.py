import copy
import random
import unittest
from tictactoeboard import TicTacToeBoard

"""A Tic-Tac-Toe board test case class.

Exported Classes:

TicTacToeBoardTestCase -- A tic-tac-toe board test case class.

"""

class TicTacToeBoardTestCase(unittest.TestCase):
  def test_initial_board(self):
    """Test whether the default constructor generates an empty 3x3 board."""
    board = TicTacToeBoard()
    # make sure the board is the traditional 3x3 board with no marks
    self.assertEqual(board.column_count, 3)
    self.assertEqual(board.row_count, 3)
    self.assertEqual(len(board.matrix), board.row_count)
    self.assertEqual(len(board.matrix[0]), board.column_count)
    # make sure board has no initial marks
    self.assertEqual(board.CELL_NO_PLAYER, 0)
    for row in xrange(board.row_count):
      for col in xrange(board.column_count):
        self.assertEqual(board.matrix[row][col], board.CELL_NO_PLAYER)
  
  def test_get_other_player_function(self):
    """Test whether the get_other_player_id function provides the id of the other player."""
    board = TicTacToeBoard()
    self.assertEqual(board.get_other_player_id(1), 2)
    self.assertEqual(board.get_other_player_id(2), 1)
    
  def test_get_lines_on_empty_square_board(self):
    """Test whether the _get_lines function provides the correct lines for an empty square board."""
    board = TicTacToeBoard()
    lines = board._get_lines()
    # make sure there are the correct number of lines
    self.assertEqual(len(lines), board.column_count + board.row_count + 2)
    # make sure all lines are empty
    emptyLine = [board.CELL_NO_PLAYER for i in xrange(board.column_count)]
    for line in lines:
      self.assertEqual(line, emptyLine)
  
  def test_get_lines_on_board(self):
    """Test whether the _get_lines function provides the correct lines for a non empty square board."""
    # create non-empty square tic-tac-toe game board    
    board = TicTacToeBoard()
    board.matrix[0] = [1, 2, 0]
    board.matrix[1] = [0, 1, 0]
    board.matrix[2] = [0, 2, 0]
    lines = board._get_lines()
    # make sure there are the correct number of lines
    self.assertEqual(board.column_count + board.row_count + 2, 8)
    self.assertEqual(len(lines), 8)
    # make sure the lines are correct
    self.assertEqual(lines.count([0,0,0]), 1)
    self.assertEqual(lines.count([1,0,0]), 1)
    self.assertEqual(lines.count([1,2,0]), 1)
    self.assertEqual(lines.count([0,1,0]), 2)
    self.assertEqual(lines.count([1,1,0]), 1)
    self.assertEqual(lines.count([0,2,0]), 1)
    self.assertEqual(lines.count([2,1,2]), 1)
    
  def test_get_winner_on_empty_square_board(self):
    """Test whether get_winner function provides game not over status for an empty square board."""
    board = TicTacToeBoard()
    # make sure that the game is not over when it begins with an empty board
    winner = board.get_winner()
    self.assertEqual(winner, board.GAME_WINNER_GAME_NOT_OVER)
    
  def test_get_winner_on_non_empty_game_not_over_square_board(self):
    """Test whether get_winner function provides game not over status for a non-empty square board."""
    # create non-empty game-not-over tic-tac-toe game board
    board = TicTacToeBoard()
    board.matrix[0] = [1, 2, 0]
    board.matrix[1] = [0, 1, 0]
    board.matrix[2] = [0, 2, 0]
    winner = board.get_winner()
    # make sure that the game is not over
    self.assertEqual(winner, board.GAME_WINNER_GAME_NOT_OVER)
  
  def test_get_winner_on_non_empty_tied_game_square_board(self):
    """Test whether get_winner function provides game tied status for a non-empty square board."""
    # create non-empty tied tic-tac-toe game board
    board = TicTacToeBoard()
    board.matrix[0] = [1, 2, 1]
    board.matrix[1] = [1, 2, 1]
    board.matrix[2] = [2, 1, 2]
    winner = board.get_winner()
    self.assertEqual(board.GAME_WINNER_TIED, -1)
    self.assertEqual(winner, board.GAME_WINNER_TIED)
    
  def test_get_winner_on_non_empty_player_1_wins_square_board(self):
    """Test whether get_winner function provides player 1 wins for a non-empty square board that player 1 won."""
    # create non-empty tic-tac-toe game board that player 1 has won
    board = TicTacToeBoard()
    board.matrix[0] = [1, 0, 0]
    board.matrix[1] = [2, 1, 0]
    board.matrix[2] = [0, 2, 1]
    winner = board.get_winner()
    self.assertEqual(winner, 1)

  def test_get_winner_on_non_empty_player_2_wins_square_board(self):
    """Test whether get_winner function provides player 2 wins for a non-empty square board that player 2 won."""
    # create non-empty tic-tac-toe game board that player 2 has won
    board = TicTacToeBoard()
    board.matrix[0] = [2, 0, 0]
    board.matrix[1] = [1, 2, 0]
    board.matrix[2] = [1, 1, 2]
    winner = board.get_winner()
    self.assertEqual(winner, 2)
    
  def test_get_next_move_boards_on_non_empty_game_not_over_square_board(self):
    """Test whether _get_next_move_boards function provides all next move boards for a non-empty game-not-over square board."""
    # create non-empty game-not-over tic-tac-toe game board
    board = TicTacToeBoard()
    board.matrix[0] = [2, 0, 0]
    board.matrix[1] = [1, 2, 0]
    board.matrix[2] = [1, 1, 2]
    next_boards = board._get_next_move_boards(1)
    # initialize valid next boards
    valid_next_boards = []
    # add valid next board 1 to list
    valid_next_board = TicTacToeBoard()
    valid_next_board.matrix = copy.deepcopy(board.matrix)
    valid_next_board.matrix[0][1] = 1
    valid_next_boards.append(valid_next_board)
    # add valid next board 2 to list
    valid_next_board = TicTacToeBoard()
    valid_next_board.matrix = copy.deepcopy(board.matrix)
    valid_next_board.matrix[0][2] = 1
    valid_next_boards.append(valid_next_board)
    # add valid next board 3 to list
    valid_next_board = TicTacToeBoard()
    valid_next_board.matrix = copy.deepcopy(board.matrix)
    valid_next_board.matrix[1][2] = 1
    valid_next_boards.append(valid_next_board)
    # Make sure there are the correct number of next boards for player 1
    next_board_matrices = [next_board.matrix for next_board in next_boards]
    self.assertEqual(len(next_board_matrices), 3)
    # Make sure that each valid next board for player 1 was found 
    for valid_next_board in valid_next_boards:
      self.assertTrue(valid_next_board.matrix in next_board_matrices)

  def test_can_win_on_non_empty_square_board_that_you_won(self):
    """Test whether _can_win function returns that a player can win a non-empty square board that they have won."""
    # create non-empty tic-tac-toe game board that player 1 has won
    board = TicTacToeBoard()
    board.matrix[0] = [1, 0, 0]
    board.matrix[1] = [2, 1, 0]
    board.matrix[2] = [0, 2, 1]
    self.assertTrue(board._can_win(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [1, 0, 0]
    board.matrix[1] = [1, 2, 0]
    board.matrix[2] = [1, 2, 0]
    self.assertTrue(board._can_win(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [1, 1, 1]
    board.matrix[1] = [0, 2, 0]
    board.matrix[2] = [0, 2, 0]
    self.assertTrue(board._can_win(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [0, 2, 1]
    board.matrix[1] = [0, 1, 0]
    board.matrix[2] = [1, 2, 0]
    self.assertTrue(board._can_win(1))    
    # create non-empty tic-tac-toe game board that player 2 has won
    board = TicTacToeBoard()
    board.matrix[0] = [2, 0, 0]
    board.matrix[1] = [1, 2, 0]
    board.matrix[2] = [0, 1, 2]
    self.assertTrue(board._can_win(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [2, 0, 0]
    board.matrix[1] = [2, 1, 0]
    board.matrix[2] = [2, 1, 0]
    self.assertTrue(board._can_win(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [2, 2, 2]
    board.matrix[1] = [0, 1, 0]
    board.matrix[2] = [0, 1, 0]
    self.assertTrue(board._can_win(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [0, 1, 2]
    board.matrix[1] = [0, 2, 0]
    board.matrix[2] = [2, 1, 0]
    self.assertTrue(board._can_win(2))

  def test_can_win_on_non_empty_square_board_you_lost(self):
    """Test whether _can_win function returns that a player cannot win a non-empty square board that they lost."""
    # create non-empty tic-tac-toe game board that player 1 has won
    board = TicTacToeBoard()
    board.matrix[0] = [1, 0, 0]
    board.matrix[1] = [2, 1, 0]
    board.matrix[2] = [0, 2, 1]
    self.assertFalse(board._can_win(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [1, 0, 0]
    board.matrix[1] = [1, 2, 0]
    board.matrix[2] = [1, 2, 0]
    self.assertFalse(board._can_win(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [1, 1, 1]
    board.matrix[1] = [0, 2, 0]
    board.matrix[2] = [0, 2, 0]
    self.assertFalse(board._can_win(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [0, 2, 1]
    board.matrix[1] = [0, 1, 0]
    board.matrix[2] = [1, 2, 0]
    self.assertFalse(board._can_win(2))
    # create non-empty tic-tac-toe game board that player 2 has won
    board = TicTacToeBoard()
    board.matrix[0] = [2, 0, 0]
    board.matrix[1] = [1, 2, 0]
    board.matrix[2] = [0, 1, 2]
    self.assertFalse(board._can_win(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [2, 0, 0]
    board.matrix[1] = [2, 1, 0]
    board.matrix[2] = [2, 1, 0]
    self.assertFalse(board._can_win(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [2, 2, 2]
    board.matrix[1] = [0, 1, 0]
    board.matrix[2] = [0, 1, 0]
    self.assertFalse(board._can_win(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [0, 1, 2]
    board.matrix[1] = [0, 2, 0]
    board.matrix[2] = [2, 1, 0]
    self.assertFalse(board._can_win(1))
    
  def test_can_tie_on_non_empty_square_board_that_you_won(self):
    """Test whether _can_tie function returns that a player can tie a non-empty square board that they have won."""
    # create non-empty tic-tac-toe game board that player 1 has won
    board = TicTacToeBoard()
    board.matrix[0] = [1, 0, 0]
    board.matrix[1] = [2, 1, 0]
    board.matrix[2] = [0, 2, 1]
    self.assertTrue(board._can_tie(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [1, 0, 0]
    board.matrix[1] = [1, 2, 0]
    board.matrix[2] = [1, 2, 0]
    self.assertTrue(board._can_tie(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [1, 1, 1]
    board.matrix[1] = [0, 2, 0]
    board.matrix[2] = [0, 2, 0]
    self.assertTrue(board._can_tie(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [0, 2, 1]
    board.matrix[1] = [0, 1, 0]
    board.matrix[2] = [1, 2, 0]
    self.assertTrue(board._can_tie(1))    
    # create non-empty tic-tac-toe game board that player 2 has won
    board = TicTacToeBoard()
    board.matrix[0] = [2, 0, 0]
    board.matrix[1] = [1, 2, 0]
    board.matrix[2] = [0, 1, 2]
    self.assertTrue(board._can_tie(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [2, 0, 0]
    board.matrix[1] = [2, 1, 0]
    board.matrix[2] = [2, 1, 0]
    self.assertTrue(board._can_tie(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [2, 2, 2]
    board.matrix[1] = [0, 1, 0]
    board.matrix[2] = [0, 1, 0]
    self.assertTrue(board._can_tie(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [0, 1, 2]
    board.matrix[1] = [0, 2, 0]
    board.matrix[2] = [2, 1, 0]
    self.assertTrue(board._can_tie(2))

  def test_can_tie_on_non_empty_square_board_you_lost(self):
    """Test whether _can_tie function returns that a player cannot tie a non-empty square board that they lost."""
    # create non-empty tic-tac-toe game board that player 1 has won
    board = TicTacToeBoard()
    board.matrix[0] = [1, 0, 0]
    board.matrix[1] = [2, 1, 0]
    board.matrix[2] = [0, 2, 1]
    self.assertFalse(board._can_tie(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [1, 0, 0]
    board.matrix[1] = [1, 2, 0]
    board.matrix[2] = [1, 2, 0]
    self.assertFalse(board._can_tie(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [1, 1, 1]
    board.matrix[1] = [0, 2, 0]
    board.matrix[2] = [0, 2, 0]
    self.assertFalse(board._can_tie(2))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [0, 2, 1]
    board.matrix[1] = [0, 1, 0]
    board.matrix[2] = [1, 2, 0]
    self.assertFalse(board._can_tie(2))
    # create non-empty tic-tac-toe game board that player 2 has won
    board = TicTacToeBoard()
    board.matrix[0] = [2, 0, 0]
    board.matrix[1] = [1, 2, 0]
    board.matrix[2] = [0, 1, 2]
    self.assertFalse(board._can_tie(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [2, 0, 0]
    board.matrix[1] = [2, 1, 0]
    board.matrix[2] = [2, 1, 0]
    self.assertFalse(board._can_tie(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [2, 2, 2]
    board.matrix[1] = [0, 1, 0]
    board.matrix[2] = [0, 1, 0]
    self.assertFalse(board._can_tie(1))
    # test another similar board
    board = TicTacToeBoard()
    board.matrix[0] = [0, 1, 2]
    board.matrix[1] = [0, 2, 0]
    board.matrix[2] = [2, 1, 0]
    self.assertFalse(board._can_tie(1))

  def test_can_win_on_empty_square_board(self):
    """Test whether _can_win function returns that a player can always win on an empty square board."""
    # create empty tic-tac-toe game board
    board = TicTacToeBoard()
    # a perfect player is not garunteed to win on an empty board
    self.assertFalse(board._can_win(1))
    self.assertFalse(board._can_win(2))

  def test_can_tie_on_empty_square_board(self):
    """Test whether _can_tie function returns that a player can tie on an empty square board."""
    # create empty tic-tac-toe game board
    board = TicTacToeBoard()
    # a perfect player is garunteed to tie on an empty board
    self.assertTrue(board._can_tie(1))
    self.assertTrue(board._can_tie(2))

  def test_can_win_on_non_empty_square_board_they_cannot_win(self):
    """Test whether _can_win function returns that a player can win on a non-empty square board they cannot win."""
    # create non-empty tic-tac-toe game board that player 2 cannot win
    board = TicTacToeBoard()
    board.matrix[0] = [1, 2, 1]
    board.matrix[1] = [2, 1, 0]
    board.matrix[2] = [0, 0, 2]
    self.assertFalse(board._can_win(2))
    # create non-empty tic-tac-toe game board that player 1 cannot win
    board = TicTacToeBoard()
    board.matrix[0] = [2, 1, 2]
    board.matrix[1] = [1, 2, 0]
    board.matrix[2] = [0, 0, 1]
    self.assertFalse(board._can_win(1))

if __name__ == '__main__':
    unittest.main()