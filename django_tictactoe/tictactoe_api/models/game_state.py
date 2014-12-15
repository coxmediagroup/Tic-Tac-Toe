from . import SudhagarS_minmax_tictactoe as minmax
import uuid

class GameState:
  """Records tic-tac-toe state and validates moves.
     
     After creating a GameState, validate new moves with validate_next
     and commit the result with tally_move.
  """
  def __init__(self, game_id):
    self.game_id = game_id
    self.board = list("---------") # "X", "O", or "-"
    self.movelist = [] # list of (player, position) tuples

  def last_player(self):
    return None if not self.movelist else self.movelist[-1][0]

  def next_player(self):
    return 'O' if self.last_player() == 'X' else 'X'

  def validate_next_player(self, player):
    "Any player can play first, but then they must alternate"
    if not self.movelist:
      return True
    return self.last_player() != player
  
  def tally_move(self, player, position):
    "Update our history of the game to include a move"
    self.board[position] = player
    self.movelist.append((player, position),)

  def isWon(self):
    return minmax.isWin(self.board)

  def isDrawn(self):
    "Drawn if the game isn't won and there is nowhere to play"
    return (not self.isWon()) and ("-" not in self.board)

  def isFinished(self):
    return self.isDrawn() or self.isWon()

  def validate_next(self, player, position):
    "Report whether the supplied move makes sense"
    if self.isWon():
      return (False, "The game has already been won.")
    if self.isDrawn():
      return (False, "The game is drawn.")
    if not self.validate_next_player(player):
      return (False, "It's not your turn!")
    if self.board[position] == player:
      return (False, "You've already played there!")
    if self.board[position] != "-":
      return (False, "Opponent has already played there!")
     # otherwise a valid move
    return (True, (player, position))

  def suggest_next(self, player):
    "Use the minmax algorithm to suggest a next move"
    whoWillWin, whereToPlay = minmax.nextMove(self.board, player)
    return whoWillWin, whereToPlay

  def summarize(self):
    "return a dictionary suitable for jsonifying"
    return {
      "board": self.board, 
      "moves": self.movelist,
      "lastPlayer": self.last_player(),
      "gameId": self.game_id,
      "isWon": self.isWon(),
      "isDrawn": self.isDrawn()
      }

