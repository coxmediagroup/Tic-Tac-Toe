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

if __name__ == '__main__':
  unittest.main()
