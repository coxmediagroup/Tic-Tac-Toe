

class GameBoard:
   def __init__(self, game_state='_________'):
      if len(game_state) != 9:
         raise ValueError("Invalid game state {}".format(game_state))

      self.board = self.create_board(game_state)
      
   def create_board(self, board_string):
      "Convert a 9-character string to a 2-D grid of rows and columns"
      board = []
      board.append([list(board_string)[i] for i in range(3)])
      board.append([list(board_string)[i] for i in range(3, 6)])
      board.append([list(board_string)[i] for i in range(6, 9)])
      return board
      
   def move(self, row, column):
      player = 'X' if self.get_state().count('_') % 2 else 'O'
      self.board[row][column] = player
      
   def get_state(self):
      state = ''
      for row in self.board:
         for col in row:
            state += col
            
      return state
      
   def __str__(self):
      return self.state