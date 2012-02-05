from copy import deepcopy

def get_pos(l, pos):
  """l - a 2d list
     pos - a tuple of (level 1 index, level 2 index)"""
  return l[pos[0]][pos[1]]

class TicTacToe:
  """An unbeatable Tic Tac Toe game.  Human always starts. """
  def __init__(self):
    self.board = [list(range(3)), list(range(3, 6)), list(range(6,9))]
    self.winner = None
    self.human = 'x'
    self.computer = 'o'

  def human_move(self):
    """Accepts / validates the input for a human move.
       
       Returns True on a valid move.
       Otherwise False."""
    move = raw_input("Your turn: ")
    if ord(move) > ord('0') and ord(move) <= ord('9'):
      move = int(move)
      if isinstance(self.board[move//3][move%3], int):
        self.board[move//3][move%3]
        return True
      else:
        print("This position has already been played. Try again!")
    else:
      print("Input must be between 1 and 9 inclusive!")
    return False
  
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
    (row, col) = (self.win(self.board, self.computer) or
                  self.win(self.board, self.human) or
                  self.fork(self.computer) or
                  self.fork(self.human) or
                  self.center() or
                  self.opposite_corner() or
                  self.empty_corner() or
                  self.empty_side())
    self.board[row][col] = self.computer

  def win(self, board, mark):
    """Finds a position that will win the game for a given board with a given mark.

       Returns the row, col of or None"""
    # FIXME naive approach
    for row in range(3):
      for col in range(3):
        if isinstance(board[row][col], int):
          new_board = deepcopy(board)
          new_board[row][col] = mark
          if self.tic_tac_toe(new_board):
            return row, col

  
  def fork(self, mark):
    """Finds a position that will fork (a move that creates two 
       possible following winning moves).
       
       Returns the position or None"""
    for row in range(3):
      for col in range(3):
        if isinstance(self.board[row][col], int):
          board = deepcopy(self.board)
          board[row][col] = mark
          win = self.win(board, mark)
          if win:
            board[win[0]][win[1]] = 'i'
            second_win = self.win(board, mark)
            if second_win:
              return row, col
    return None

  def center(self):
    """Checkes if the center position is empty.
       
       Returns the position or None"""
    if isinstance(self.board[1][1], int):
      return 1,1

  def opposite_corner(self):
    """Detects if the opponent has selected a corner and if  
       the opposite corner is available.

       Returns the position or None
    """
    corners = (((0,0),(2,2)), ((0,2),(2,0)))
    for pair in corners:
      if (get_pos(self.board, pair[0]) == self.human and 
          isinstance(get_pos(self.board, pair[1]), int)):
        return pair[1]
      if (get_pos(self.board, pair[1]) == self.human and 
          isinstance(get_pos(self.board, pair[0]), int)):
        return pair[0]

  def empty_pos(self, positions): 
       for row, col in positions:
         if isinstance(self.board[row][col], int):
           return row, col

  def empty_corner(self):
    """Detects if any corners are empty.  
       
       Returns the position or None
    """
    return self.empty_pos(((0,0), (0,2), (2, 0), (2, 2)))

  def empty_side(self):
    """Detects if any of the side positions are empty.
       
       Returns the position or None"""
    return self.empty_pos(((0,1), (1, 0), (1, 2), (2, 1)))
      
  def tic_tac_toe(self, board):
    """Examines the board to determine if a tic tac toe
       has occured.

       Returns True or False
       if True, also sets self.winner to "Human", "Computer", or "Cat"
    """
    def all_same(l):
      """Check if all members of the list are the same value, 
         if so, return that value"""
      if len(set(l)) == 1:
        return l[0]
      return None

    return filter(all_same, self.win_combinations(board))
    
  def win_combinations(self, board):
    return (board[0], board[1], board[2],  # Horizontal
                                 tuple(row[0] for row in board),  # Verticals
                                 tuple(row[1] for row in board),
                                 tuple(row[2] for row in board),
                                 (board[0][0], board[1][1], board[2][2]),  # Diagonals
                                 (board[0][2], board[1][1], board[2][0]))


  def __str__(self):
    """Represents the board as a string."""
    s = (" {0[0][0]} | {0[0][1]} | {0[0][2]}\n"
         "-----------\n"
         " {0[1][0]} | {0[1][1]} | {0[1][2]}\n"
         "-----------\n"
         " {0[2][0]} | {0[2][1]} | {0[2][2]}\n")  # FIXME: move to __init__ or global
    return s.format(self.board)
 
  def main(self):
    """This function drives the game."""

if __name__=='__main__':
  game = TicTacToe()
  game.main()
