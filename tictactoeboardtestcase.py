import random
import unittest
from tictactoeboard import TicTacToeBoard

class TicTacToeBoardTestCase(unittest.TestCase):
  def setUp(self):
    pass

  def test_initial_board(self):
    emptyBoard = TicTacToeBoard()
    
    # make sure the board is the traditional 3x3 board with no marks
    self.assertEqual(emptyBoard.COLUMN_COUNT, 3)
    self.assertEqual(emptyBoard.ROW_COUNT, 3)
    self.assertEqual(len(emptyBoard.matrix), emptyBoard.ROW_COUNT)
    self.assertEqual(len(emptyBoard.matrix[0]), emptyBoard.COLUMN_COUNT)

    # make sure board has no initial marks
    self.assertEqual(emptyBoard.CELL_NO_PLAYER, 0)
    for row in xrange(emptyBoard.ROW_COUNT):
      for col in xrange(emptyBoard.COLUMN_COUNT):
        self.assertEqual(emptyBoard.matrix[row][col], emptyBoard.CELL_NO_PLAYER)
  
  def test_get_other_player_num(self):
    emptyBoard = TicTacToeBoard()
    self.assertEqual(emptyBoard.get_other_player_num(1), 2)
    self.assertEqual(emptyBoard.get_other_player_num(2), 1)
    
  def test_get_lines_on_empty_square_board(self):
    emptyBoard = TicTacToeBoard()
    
    lines = emptyBoard._get_lines()
    
    # make sure there are the correct number of lines
    self.assertEqual(len(lines), emptyBoard.COLUMN_COUNT + emptyBoard.ROW_COUNT + 2)
    
    # make sure all lines are empty
    emptyLine = [emptyBoard.CELL_NO_PLAYER for i in xrange(emptyBoard.COLUMN_COUNT)]
    for line in lines:
      self.assertEqual(line, emptyLine)
  
  def test_get_lines_on_non_empty_square_board(self):
  
    # create non-empty square tic-tac-toe game board    
    nonEmptySquareBoard = TicTacToeBoard()
    nonEmptySquareBoard.matrix[0] = [1, 2, 0]
    nonEmptySquareBoard.matrix[1] = [0, 1, 0]
    nonEmptySquareBoard.matrix[2] = [0, 2, 0]
  
    lines = nonEmptySquareBoard._get_lines()
    
    # make sure there are the correct number of lines
    self.assertEqual(nonEmptySquareBoard.COLUMN_COUNT + nonEmptySquareBoard.ROW_COUNT + 2, 8)
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
    emptyBoard = TicTacToeBoard()
    # make sure that the game is not over when it begins with an empty board
    winner = emptyBoard.get_winner()
    self.assertEqual(winner, emptyBoard.GAME_WINNER_GAME_NOT_OVER)
    
  def test_get_winner_on_non_empty_game_not_over_square_board(self):
    
    # create non-empty game-not-over tic-tac-toe game board
    nonEmptyGameNotOverBoard = TicTacToeBoard()
    nonEmptyGameNotOverBoard.matrix[0] = [1, 2, 0]
    nonEmptyGameNotOverBoard.matrix[1] = [0, 1, 0]
    nonEmptyGameNotOverBoard.matrix[2] = [0, 2, 0]
    
    winner = nonEmptyGameNotOverBoard.get_winner()
    # make sure that the game is not over
    self.assertEqual(winner, nonEmptyGameNotOverBoard.GAME_WINNER_GAME_NOT_OVER)
    
  def test_get_winner_on_non_empty_game_not_over_square_board(self):

    # create non-empty game-not-over tic-tac-toe game board
    nonEmptyGameNotOverBoard = TicTacToeBoard()
    nonEmptyGameNotOverBoard.matrix[0] = [1, 2, 0]
    nonEmptyGameNotOverBoard.matrix[1] = [0, 1, 0]
    nonEmptyGameNotOverBoard.matrix[2] = [0, 2, 0]

    winner = nonEmptyGameNotOverBoard.get_winner()
    self.assertEqual(winner, nonEmptyGameNotOverBoard.GAME_WINNER_GAME_NOT_OVER)
  
  def test_get_winner_on_non_empty_tied_game_square_board(self):

    # create non-empty game-not-over tic-tac-toe game board
    nonEmptyGameNotOverBoard = TicTacToeBoard()
    nonEmptyGameNotOverBoard.matrix[0] = [1, 2, 1]
    nonEmptyGameNotOverBoard.matrix[1] = [1, 2, 1]
    nonEmptyGameNotOverBoard.matrix[2] = [2, 1, 2]

    winner = nonEmptyGameNotOverBoard.get_winner()
    self.assertEqual(nonEmptyGameNotOverBoard.GAME_WINNER_TIED, -1)
    self.assertEqual(winner, nonEmptyGameNotOverBoard.GAME_WINNER_TIED)
    
    
  def test_get_winner_on_non_empty_player_1_wins_square_board(self):

    # create non-empty game-not-over tic-tac-toe game board
    nonEmptyGameNotOverBoard = TicTacToeBoard()
    nonEmptyGameNotOverBoard.matrix[0] = [1, 0, 0]
    nonEmptyGameNotOverBoard.matrix[1] = [2, 1, 0]
    nonEmptyGameNotOverBoard.matrix[2] = [0, 2, 1]

    winner = nonEmptyGameNotOverBoard.get_winner()
    self.assertEqual(winner, 1)

  def test_get_winner_on_non_empty_player_2_wins_square_board(self):

    # create non-empty game-not-over tic-tac-toe game board
    nonEmptyGameNotOverBoard = TicTacToeBoard()
    nonEmptyGameNotOverBoard.matrix[0] = [2, 0, 0]
    nonEmptyGameNotOverBoard.matrix[1] = [1, 2, 0]
    nonEmptyGameNotOverBoard.matrix[2] = [1, 1, 2]

    winner = nonEmptyGameNotOverBoard.get_winner()
    self.assertEqual(winner, 2)

if __name__ == '__main__':
    unittest.main()