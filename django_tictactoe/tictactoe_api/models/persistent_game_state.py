import uuid
from django.db.models import Min, F

from .game_state import GameState
from .move import Move


class PersistentGameState(GameState):
  "A GameState with extra methods that allow us to persist via saving and loading Moves"
  " PersistentGameState follows a lightweight event-sourced approach with moves being events. "
  " The GameState is the ephemeral domain model that is 'hydrated' on every request with the "
  " events recorded to that point."

  def save_move(self, player, position):
    "save a move to the database and then tally it"
    m = Move(session_id=self.game_id, player=player, position=position)
    m.save()
    self.tally_move(player, position)

  def execute_move(self, player, pos, onValid, onInvalid):
    "Perform the move validation and commit it if it's valid. Return one of the two callbacks depending on validity."
    "onValid should take the resulting game as an argument, onInvalid takes the reason string"
    valid, data = self.validate_next(player, pos)
    if not valid:
      return onInvalid(data)
    else:
      self.save_move(*data)
      return onValid(self)

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
    firstMoves = Move.objects.values("session_id").annotate(min_session_id=Min('session_id'))
    for m in firstMoves:
      yield m['session_id']

  @staticmethod
  def generate_id():
    return str(uuid.uuid4())
