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
    assert self.T.tic_tac_toe(self.T.board)

  def test_winner_1(self):
    """The correct winner is recorded"""
    self.T.board[0] = ['x']*3
    assert self.T.tic_tac_toe(self.T.board)[0][0] == 'x'
  #  7 move of these?

  def sim(self,prep, win):
    for move in prep:
      self.T.board[move[0]][move[1]] = 'x'
    assert win == self.T.win(self.T.board, 'x')
    
  # test win possibilities
  def test_win_top_row(self):
    self.sim(((0,1), (0,2)),(0,0))
  def test_win_mid_row(self):
    self.sim(((1,0), (1,2)),(1,1))
  def test_win_bottom_row(self):
    self.sim(((2,0),(2,1)),(2,2))
  def test_win_left_col(self):
    self.sim(((0,1),(0,2)),(0,0))
  def test_win_mid_col(self):
    self.sim(((1,0),(1,2)),(1,1))
  def test_win_right_col(self):
    self.sim(((2,0),(2,1)),(2,2))
  def test_win_first_diag(self):
    self.sim(((0,0),(1,1)),(2,2))
  def test_win_second_diag(self):
    self.sim(((0,2),(2,0)),(1,1))
 
  #TODO test fork possibilities
  def test_fork(self):
    self.T.board[0][1] = 'x'
    self.T.board[1][0] = 'x'
    self.T.board[0][0] = 'o'
    assert self.T.fork('x') == (1,1)

  def test_center(self):
    assert self.T.center() == (1,1)

  def test_opposite_corner_1(self):
    self.T.board[0][0] = 'x'
    assert self.T.opposite_corner() == (2,2)
  def test_opposite_corner_2(self):
    self.T.board[2][0] = 'x'
    assert self.T.opposite_corner() == (0,2)

  def test_empty_corner_1(self):
    assert self.T.empty_corner() == (0,0)
  def test_empty_corner_2(self):
    self.T.board[0][0] = 'x'
    self.T.board[0][2] = 'x'
    assert self.T.empty_corner() == (2, 0)

  def test_empty_side_1(self):
    self.T.board[0][1] = 'x'
    assert self.T.empty_side() == (1,0)


  def test_human_input(self):
    """Humans are not allowed to make invalid moves."""

if __name__ == '__main__':
  unittest.main()
