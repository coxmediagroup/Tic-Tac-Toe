import unittest
from tictactoe import TicTacToe

class TestTicTacToe(unittest.TestCase):
  def setUp(self):
    self.T = TicTacToe()

  def tearDown(self):
    self.T = None

  def test_win(self):
    """Test that a winner is detected"""
    self.T.board[0] = ['x']*3
    assert self.T.tic_tac_toe()

  def test_winner_1(self):
    """The correct winner is recorded"""
    self.T.board[0] = ['x']*3
    self.T.tic_tac_toe()
    assert self.T.winner == 'x'
  #  7 move of these?

  def test_human_input(self):
    """Humans are not allowed to make invalid moves."""

if __name__ == '__main__':
  unittest.main()
