

class GameBoard:
   def __init__(self, game_state='_________'):
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
      self.board[row][column] = self.get_player()
      
   def get_player(self):
      return 'X' if self.get_state().count('_') % 2 else 'O'
      
   def get_state(self):
      state = ''
      for row in self.board:
         state += ''.join(row)
            
      return state
      
   def validate_board(self):
      state = self.get_state()
      
      x_count = state.count('X')
      o_count = state.count('O')
      if x_count < o_count or x_count - o_count > 1:
         raise ValueError("Invalid play sequence in board: {}".format(state))
      
      for eachSquare in state:
         if eachSquare not in ['X', 'O', '_']:
            raise ValueError("Invalid character {} in state {}".format(eachSquare, state))
      
   def __str__(self):
      return self.get_state()