class TicTacToe:
  """An unbeatable Tic Tac Toe game.  Human always starts. """
  def __init__(self):
    self.board = [None] *9
    self.winner = None

  def human_move(self):
    """Accepts / validates the input for a human move.
       
       Returns True on a valid move.
       Otherwise False."""
  
  def computer_move(self):
    """The logic for the computer move.
       Rules: If TTT next, prevent
              First move, human:response
                center:topLeft
                edge:adjacent corner
                corner:center
              
              If human in corners
                if center == None, occupy
                otherwise, threaten with edge"""

  def ttt_next(self):
    """Examines the board to determine if the opponent
       can win on the next turn. 

       Returns the position to prevent TTT
       Otherwise None
      """

  def ttt(self):
    """Examines the board to determine if a tic tac toe
       has occured.

       Returns True or False
       if True, also sets self.winner to "Human", "Computer", or "Cat"
      """
  
  def __str__(self):
    """Represents the board as a string."""
 
  def main(self):
    while (not self.ttt()):
      print(str(self))
      while not self.human_move()
        pass
      self.computer_move()
    print ("The {winner} won!".format(winner=self.winner))

if __name__=='__main__':
  game = TicTacToe()
  game.main()
