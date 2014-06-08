
EMPTY = '_'

class GameBoard:
   """ This class contains all logic pertaining to the rules of tic-tac-toe.
   Each square in the game board is referenced by its (row, column) coordinates:
    (0,0) | (0,1) | (0,2)
    ------+-------+------
    (1,0) | (1,1) | (1,2)
    ------+-------+------
    (2,0) | (2,1) | (2,2)
    
    "XOO_X___X" corresponsed to the board:
    X | O | O
   ---+---+---
      | X |
   ---+---+---
      |   | X
   """
   
   def __init__(self, game_state=9 * EMPTY):
      """Game state is input as a 9-character string which each character representing the contents of a square.
      Game state is stored as a 2-D list so it is mutable.
      """
   
      if len(game_state) != 9:
         raise ValueError("Invalid game state {}".format(game_state))

      self.board = self.create_board(game_state)
      
      self.validate_board()
      
   def create_board(self, board_string):
      "Convert a 9-character string to a 2-D grid of rows and columns"
      board = []
      board.append([list(board_string)[i] for i in range(3)])
      board.append([list(board_string)[i] for i in range(3, 6)])
      board.append([list(board_string)[i] for i in range(6, 9)])
      return board
      
   def move(self, row, column):
      if row not in range(3) or column not in range(3):
         raise IndexError("Move location ({}, {}) out of bounds".format(row, column))
         
      if self.board[row][column] != EMPTY:
         raise ValueError("Space ({}, {}) already occupied on board {}".format(row, column, self.get_state()))
         
      self.board[row][column] = self.get_player()
      
   def get_player(self):
      "The next player to move is derived from the game state."
      return 'X' if self.get_state().count(EMPTY) % 2 else 'O'
      
   def get_rows(self):
      "Get a concatenated string for each row"
      return [''.join(row) for row in self.board]
      
   def get_columns(self):
      "Get a concatenated string for each row"
      columns = []
      for col in range(3):
         columns.append(''.join([row[col] for row in self.board]))
         
      return columns
      
   def get_diags(self):
      "Get a concatenated string for the two diagonals"
      board = self.board
      return [''.join([board[0][0], board[1][1], board[2][2]]),
              ''.join([board[0][2], board[1][1], board[2][0]])]
      
   def get_state(self):
      "Convert game state back to a string representation, compatible with the GameBoard constructor."
      return ''.join(self.get_rows())
      
   def is_game_over(self):
      return not self.get_valid_moves() or (self.get_winner() is not None)
      
   def get_winner(self):
      winning_states = self.get_rows()
      winning_states.extend(self.get_columns())
      winning_states.extend(self.get_diags())
      
      if 'XXX' in winning_states:
         return 'X'
         
      if 'OOO' in winning_states:
         return 'O'
         
      return None
      
   def get_valid_moves(self):
      "A list of tuples in (row, column) format. It will be populated even if a player was won."
      valid_moves = []
      for row in range(3):
         for col in range(3):
            if self.board[row][col] == EMPTY:
               valid_moves.append((row, col))
      return valid_moves
      
   def validate_board(self):
      state = self.get_state()
      
      x_count = state.count('X')
      o_count = state.count('O')
      if x_count < o_count or x_count - o_count > 1:
         raise ValueError("Invalid play sequence in board: {}".format(state))
      
      for eachSquare in state:
         if eachSquare not in ['X', 'O', EMPTY]:
            raise ValueError("Invalid character {} in state {}".format(eachSquare, state))
      
   def __str__(self):
      return self.get_state()
      
   def __repr__(self):
      return '\n'.join(self.get_rows())