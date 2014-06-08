import random

class PlayerRandom:
   def choose_move(board):
      possible_moves = board.get_valid_moves()
      return random.choice(possible_moves)
      