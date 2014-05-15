import random
import sys
from tictactoeboard import TicTacToeBoard

"""A Tic-Tac-Toe game class.

Exported Classes:

TicTacToeGame -- A tic-tac-toe game class that allows a single user to play 
against a perfect computer opponent that always wins or ties.

"""

def main():
  """Starts the game."""
  # Create a tic-tac-toe game
  game = TicTacToeGame()
  # Start the tic-tac-toe game.
  game.start()

class TicTacToeGame:  
  """A tic-tac-toe game class that allows a single user to play 
  against a perfect computer opponent that always wins or ties.
  
  Public functions:
  start -- Starts the game.
  
  """
  def start(self, row_count=3, column_count=3):
    """Starts the game.
    
    Arguments:
    row_count -- Number of rows in tic-tac-toe board
    column_count -- Number of columns in tic-tac-toe board
    
    Side-Effects:
    Creates a tic-tac-toe game board with the specified number of rows and columns.
    Decides the order in which the players will take turns.
    Displays the game board to standard output and then alternates turns between
    the user and the computer player.
    During the user's turn, it prompts the user to input
    the coordinates with which to mark the game board.
    The user can also input 'q' to quit the game.
    If the game continues until competion, it indicates whether the player won, lost, or tied the game.
    The user should never win.
    
    """
    # Initialize game board
    self.board = TicTacToeBoard(row_count, column_count)
    # Initialize players
    self._initialize_players()
    # Welcome the user to the game
    self._display_welcome()
    # Let the players turns marking the game board
    self._take_turns()    
    # Display the game results
    self._display_results()

  def _take_turns(self):
    """Alternate between players, allowing each player to mark the game board until the game ends, or the user quits.
    
    During the user's turn, prompt the user for coordinates with which to mark the board.
    Allow the user to quit the game by entering 'q'
    """
    # Beginning with the first player,
    # alternate turns between players until the game ends
    self.current_player_id = 1 # the id of the current player
    user_command = '' # the command entered by the user
    while(self.board.is_game_over() is False):
      if self.current_player_id == self.computer_player_id:      
        self.board.take_best_move(self.computer_player_id)
        # End turn and allow the user to take a turn
        self.current_player_id = self.user_player_id
      else:
        # Display the board
        self.board.display()
        # Remind the user whether they are X's or O's
        if self.user_player_id == 1:
          print "You are X's"
        else:
          print "You are O's"
        # Ask user to input the coordinates of her mark, or to press q to quit
        user_command = raw_input('<enter "{rowNum}, {columnNum}" or "q" to quit>: ')
        print ""
        # Process the user command
        if user_command.lower().strip() == 'q':
          # End the game
          break
        else:
          # Mark the board for the user
          self._mark_board_for_user(user_command)
    # Display final board  
    self.board.display()
    # Determine winner
    self.winner_id = self.board.get_winner()   

  def _mark_board_for_user(self, user_command):
    """Mark the board according to the user's command.
    
    Arguments:
    user_command -- a user command that specifies where to mark the board.
    
    Side-Effects:
    If the user command provides valid coordinates for where to mark the board,
    the board is marked at those coordinates by the user.
    
    """
    # Make sure the user has entered valid coordinates for her mark
    # and if so, mark the board for the user
    user_command_parts = user_command.split(',')
    if len(user_command_parts) == 2:
      row = int(user_command_parts[0].strip()) - 1
      col = int(user_command_parts[1].strip()) - 1
      valid_row_range = xrange(self.board.row_count)
      valid_col_range = xrange(self.board.column_count)
      if row in valid_row_range and col in valid_col_range:
        # Make sure a mark does not already exist at the coordinates 
        if  self.board.matrix[row][col] == self.board.CELL_NO_PLAYER:
          # Mark the board at the coordinate for the player
          self.board.matrix[row][col] = self.user_player_id
          # End turn and allow the computer player to take a turn
          self.current_player_id = self.computer_player_id

  def _display_welcome(self):
    """ Display text that welcomes the user to the game."""
    print ""
    print "Welcome to Tic-Tac-Toe"
    print ""
    
  def _display_results(self):
    """Display final game results"""
    print ""
    if self.winner_id == self.user_player_id:
      print "You won!"
    elif self.winner_id == self.computer_player_id:
      print "You lost!"
    elif self.winner_id == self.board.GAME_WINNER_TIED:
      print "You tied!"
    print ""
    
  def _initialize_players(self):
    """Randomly pick whether the user will be the first or second player."""
    self.user_player_id = random.choice([1,2])
    self.computer_player_id = self.board.get_other_player_id(self.user_player_id)

if __name__ == "__main__":
  sys.exit(main())