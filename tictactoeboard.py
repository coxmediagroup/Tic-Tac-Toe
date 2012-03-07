import copy

"""A Tic-Tac-Toe board class.

Exported Classes:

TicTacToeBoard -- A tic-tac-toe board class that allows a player to take an optimal move.

"""

class TicTacToeBoard:  
  """A tic-tac-toe board class that allows a player to take an optimal move.
  
  Public functions:
  is_game_over -- Return whether the game is over according to the board.
  is_tied -- Return whether the game is tied according to the board.
  has_won -- Return whether a player has won the game according to the board.
  take_best_move -- Take a best move for a specified player.
  display -- Display the game board and coordinate axes.
  get_winner -- Return the player id of the winner, or a code that indicates the game status.
  get_other_player_id -- Return the id of the other player.
  
  """
  def __init__(self, row_count=3, column_count=3):
    """Initializes the tic-tac-toe game board.
    
    Arguments:
    row_count -- Number of rows in tic-tac-toe board
    column_count -- Number of columns in tic-tac-toe board
    
    Side-Effects:
    The board matrix is initialzed as empty with zeros.
    
    """
    # Create a matrix representing the tic-tac-toe board
    # each cell will have the player number 
    # 0 = no player, 1 = player 1, 2 = player 2
    self.row_count = row_count
    self.column_count = column_count
    self.CELL_NO_PLAYER = 0    
    self.matrix = [[self.CELL_NO_PLAYER for col in xrange(self.column_count)] for row in xrange(self.row_count)]
    # Define winner constants
    self.GAME_WINNER_GAME_NOT_OVER = 0
    self.GAME_WINNER_TIED = -1
        
  def is_game_over(self):
    """Return whether the game is over according to the board."""
    return self.get_winner() != self.GAME_WINNER_GAME_NOT_OVER
  
  def is_tied(self):
    """Return whether the game is tied according to the board."""
    return self.get_winner() == self.GAME_WINNER_TIED
    
  def has_won(self, player_id):
    """Return whether the player won the game according to the board.
    
    Arguments:
    player_id -- id number of player
    
    Returns:
    A boolean, whether the player won the game according to the board.
    
    """
    return self.get_winner() == player_id
    
  def take_best_move(self, player_id):
    """Take a best move for a specified player.
    
    Arguments:
    player_id -- id number of player
    
    Side-Effects:
    Board is marked with the player's id in a best spot.  
    If the player can win, it marks a winnable spot.
    Otherwise, if the player can tie, it marks a tieable spot.
    
    """
    # If player can win, mark spot so the player can win 
    for row in xrange(self.row_count):
      for col in xrange(self.column_count):
        if self.matrix[row][col] == self.CELL_NO_PLAYER:
          next_board = copy.deepcopy(self)
          next_board.matrix[row][col] = player_id
          if next_board._can_win(player_id):
            self.matrix[row][col] = player_id
            return
    # If player cannot win but the player can tie, 
    # mark spot so the player can tie     
    for row in xrange(self.row_count):
      for col in xrange(self.column_count):
        if self.matrix[row][col] == self.CELL_NO_PLAYER:
          next_board = copy.deepcopy(self)
          next_board.matrix[row][col] = player_id
          if next_board._can_tie(player_id):
            self.matrix[row][col] = player_id
            return
    # If player can neither win nor tie, mark any spot
    for row in xrange(self.row_count):
      for col in xrange(self.column_count):
        if self.matrix[row][col] == self.CELL_NO_PLAYER:
          self.matrix[row][col] = player_id
          return
  
  def display(self, player_1_symbol = 'X', player_2_symbol = 'O', no_player_symbol = '-'):
    """Display the game board and coordinate axes.
    
    Arguments:
    player_1_symbol -- The symbol that marks player 1 on the board (e.g. 'X') 
    player_2_symbol -- The symbol that marks player 2 on the board (e.g. 'O')
    no_player_symbol -- The symbol that marks an unused spot on the board (e.g. '-')
    
    Side-Effects:
    Prints a board with coordinate axes to standard output.
    
    """
    # Display board such that 
    # player 1 has X's and player 2 has O's 
    # and other spots have dashes
    # also include axes labels with row and column coordinates 
    # print column axis labels
    print '  ' + ''.join(map(str, xrange(1, self.column_count + 1)))
    # print rows and row axis labels
    for i in xrange(self.row_count):
        print str(i+1) + ' ' + ''.join(map(str, self.matrix[i])).replace('1', player_1_symbol).replace('2', player_2_symbol).replace('0', no_player_symbol)
    pass
  
  def get_winner(self):
    """Return the player id of the winner, or a code that indicates the game status."""
    # Return 1 if player 1 is the winner
    # Return 2 if player 2 is the winner
    # Return self.GAME_WINNER_TIED if player 1 and player 2 tied
    # Return self.GAME_WINNER_GAME_NOT_OVER if the game is not over
    game_over = True
    for line in self._get_lines():
      if line.count(0) > 0:
        game_over = False
      elif line.count(1) > 0 and line.count(2) == 0:
        return 1 # player 1 won
      elif line.count(2) > 0 and line.count(1) == 0:
        return 2 # player 2 won
    if game_over:
      return self.GAME_WINNER_TIED # tied
    else:
      return self.GAME_WINNER_GAME_NOT_OVER # game is not over yet
  
  def get_other_player_id(self, player_id):
    """Return the id of the other player.
    
    Arguments:
    player_id -- id number of player
    
    Returns:
    The id of the other player.
    
    """
    if player_id == 1:
      return 2
    else:
      return 1
  
  def _get_lines(self):
    """"Return all horizontal, vertical, and diagnol lines on the tic-tac-toe board.
    
    Each line is represented by a list of player ids
    and empty cells which no player has marked is represented by zeros.
    
    Returns:
    A list of lines, where each line is a list of player ids or zeros.
    
    """
    lines = []
    # Add horizontal row lines
    for row in xrange(self.row_count):
      lines.append(copy.deepcopy(self.matrix[row]))
    # Add vertical column lines
    for col in xrange(self.column_count):
      line = []
      for row in xrange(self.row_count):
        line.append(self.matrix[row][col])
      lines.append(line)
    # Add diagnol lines if the board matrix is square
    if self.row_count == self.column_count:
      lines.append([self.matrix[i][i] for i in xrange(self.row_count)])
      lines.append([self.matrix[i][self.row_count - i - 1] for i in xrange(self.row_count)])
    return lines
    
  def _get_next_move_boards(self, player_id):
    """"Return a list of boards that represent all possible next moves by a player.
    
    Arguments:
    player_id -- id of player.
    
    Returns:
    A list of boards that represent all possible next moves by a player.
    
    """
    next_boards = []
    for row in xrange(self.row_count):
      for col in xrange(self.column_count):
        if self.matrix[row][col] == self.CELL_NO_PLAYER:
          next_board = copy.deepcopy(self)
          next_board.matrix[row][col] = player_id
          next_boards.append(next_board)
    return next_boards

  def _can_win(self, player_id):
    """"Return whether a player can win, assuming the specified player has just moved and it is the other player's turn.
    
    Arguments:
    player_id -- id of player.
    
    Returns:
    A boolean, indicating whether the player can win,
    assuming the specified player has just moved and it is the other players turn. 
    
    """
    # Determine the other player
    other_player_id = self.get_other_player_id(player_id)
    # Make sure the player has not already lost or tied
    winner = self.get_winner()
    if winner == player_id:
      return True
    elif winner == other_player_id or winner == self.GAME_WINNER_TIED:
      return False
    # Make sure the player can win indepedent of the other player's next move  
    for next_move_board in self._get_next_move_boards(other_player_id):
      next_winner = next_move_board.get_winner()
      if next_winner == other_player_id or next_winner == self.GAME_WINNER_TIED:
        return False
      can_win = False
      for next_move_board_2 in next_move_board._get_next_move_boards(player_id): 
        if next_move_board_2._can_win(player_id):
          can_win = True
          break
      if can_win is False:
        return False
    return True

  def _can_tie(self, player_id):
    """"Return whether a player can tie, assuming the specified player has just moved and it is the other player's turn.
    
    Arguments:
    player_id -- id of player.
    
    Returns:
    A boolean, indicating whether the player can tie,
    assuming the specified player has just moved and it is the other players turn. 
    
    """
    # Determine the other player
    other_player_id = self.get_other_player_id(player_id)
    # Make sure the player has not lost
    winner = self.get_winner()
    if winner == player_id or winner == self.GAME_WINNER_TIED:
      return True
    elif winner == other_player_id:
      return False
    # Make sure the player can tie indepedent of the other player's next move  
    for next_move_board in self._get_next_move_boards(other_player_id):
      if next_move_board.get_winner() == other_player_id:
        return False
      if next_move_board.get_winner() == self.GAME_WINNER_TIED:
        continue
      can_tie = False
      for next_move_board_2 in next_move_board._get_next_move_boards(player_id): 
        if next_move_board_2._can_tie(player_id):
          can_tie = True
          break
      if can_tie is False:
        return False
    return True