class TicTacToe:
  """An unbeatable Tic Tac Toe game.  Human always starts. """
  def __init__(self):
    self.board = [[None, None, None]] * 3
    self.winner = None

  def human_move(self):
    """Accepts / validates the input for a human move.
       
       Returns True on a valid move.
       Otherwise False."""
  
  def computer_move(self):
    """The logic for the computer move. From wikipedia:

       Attempt to move in this order
       1. Win
       2. Block win
       3. Fork
       4. Block Fork
       5. Center
       6. Opposite corner
       7. Empty corner
       8. Empty side
       """

  def win(self):
    """Finds a position that will win the game.

       Returns the position or None"""
  
  def block_win(self):
    """Finds a position that will block an opponent win.

       Returns the position or None"""

  def fork(self):
    """Finds a position that will fork (a move that creates two 
       possible following winning moves).
       
       Returns the position or None"""

  def block_fork(self):
    """Finds a position that will bock an oponent fork."""

  def center(self):
    """Checkes if the center position is empty.
       
       Returns the position or None"""
  def opposite_corner(self):
    """Detects if the opponent has selected a corner and if  
       the opposite corner is available.

       Returns the position or None
       """

  def empty_corner(self):
    """Detects if any corners are empty.  
       
       Returns the position or None"""
  def empty_side(self):
    """Detects if any of the side positions are empty.
       
       Returns the position or None"""
  def tic_tac_toe(self):
    """Examines the board to determine if a tic tac toe
       has occured.

       Returns True or False
       if True, also sets self.winner to "Human", "Computer", or "Cat"
      """

  def __str__(self):
    """Represents the board as a string."""
 
  def main(self):
    """This function drives the game."""

if __name__=='__main__':
  game = TicTacToe()
  game.main()
