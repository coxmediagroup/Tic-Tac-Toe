from django.db import models

# Create your models here.


class Move(models.Model):
  session_id = models.CharField(max_length=36)
  insert_id = models.AutoField(primary_key=True)
  player = models.CharField(max_length=1)
  position = models.IntegerField()


import tictactoe.SudhagarS_minmax_tictactoe as minmax

class GameState:
  """Records tic-tac-toe state and validates moves against the model."""
  def __init__(self, game_id):
    self.game_id = game_id
    self.board = list("---------") # "X", "O", or "-"
    self.movelist = [] # list of (player, position) tuples

  def last_player(self):
    return None if not self.movelist else self.movelist[-1][0]

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

  def validate_next(self, player, position):
    "Report whether the supplied move makes sense"
    if self.isWon():
      return (False, "The game has already been won.")
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
      }


class PersistentGameState(GameState):
  "A GameState with extra methods that allow us to persist via saving and loading Moves"
  def save_move(self, player, position):
    "save a move to the database and then tally it"
    m = Move(session_id=self.game_id, player=player, position=position)
    m.save()
    self.tally_move(player, position)

  @classmethod
  def load(PGS, game_id):
    "find all moves for this game_id and return a new Game with them tallied up"
    gameState = PGS(game_id)
    recordedMoves = Move.objects.filter(session_id=game_id).order_by('insert_id')
    for recordedMove in recordedMoves:
      gameState.tally_move(recordedMove.player, recordedMove.position)
    return gameState

  @staticmethod
  def getAllGameIds():
    firstMoves = Move.objects.filter(insert_id=1)
    for m in firstMoves:
      yield m.session_id


