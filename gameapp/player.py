import random

from .game import GameBoard

class PlayerRandom:
   def choose_move(board):
      possible_moves = board.get_valid_moves()
      return random.choice(possible_moves)
      
class PlayerMinimax:
   def choose_move(board):
      player_value = 1
      if board.get_player() == board.player_o:
         player_value = -1
         
      bestval, choices = minimax(board, 6, player_value)
      return random.choice(choices)
         
def get_value(board):
   if board.get_winner() == board.player_x:
      return 1
   elif board.get_winner() == board.player_o:
      return -1
   else:
      return 0
      
def minimax(board, depth, player_multiplyer):
   """ Basic minimax algorithm, implemented as negamax Reference: http://en.wikipedia.org/wiki/negamax """

   best_choices = []

   if depth == 0 or board.is_game_over():
      return get_value(board) * player_multiplyer, []
   bestValue = -1
   player_multiplyer *= -1
   for choice in board.get_valid_moves():
      new_board = GameBoard(board.get_state())
      new_board.move(*choice)
      nega_val, tmp_choices = minimax(new_board, depth - 1, player_multiplyer)
      value = -nega_val
      bestValue, best_choices = get_max(bestValue, value, best_choices, choice)
      
      #shortcut game logic if we find a winner
      if bestValue == 1:
         return bestValue, [choice]
         
   return bestValue, best_choices
   
def get_max(bestVal, comparisonVal, bestChoices, comparisonChoice):
   if comparisonVal > bestVal:
      return comparisonVal, [comparisonChoice]
   elif comparisonVal == bestVal:
      bestChoices.append(comparisonChoice)
      
   return bestVal, bestChoices
      