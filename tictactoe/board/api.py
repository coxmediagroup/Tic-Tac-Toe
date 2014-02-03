from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from django.http import Http404
from board.models import Player, Move, Game
import numpy as np

def generate_matrix(game, p1, p2):
  '''
     Generates and returns a numpy matrix for game passed in using the moves associated with that game and values for players (p1 & p2).
     Free coordinates have the value of zero.
     Numpy matrix stores values in row major order.
  '''
  matrix = np.zeros((3,3), dtype=np.int)
  for item in Move.objects.filter(game=game):
    if game.player_1 == item.player:
      matrix[item.position_y, item.position_x] = p1
    else:
      matrix[item.position_y, item.position_x] = p2
  print(matrix)
  print(matrix.ravel())
  return matrix

def determine_winner(game):
  '''
     Determines the winner of the game passed as argument.
     Returns a Player model object or None.
     Different values per player are used in turn positions and summed.  If the expected sum for victory is found, the winner is the corresponding player.
  '''
  winner = None
  p1_token = 1
  p2_token = 9
  p1_win_sum = p1_token * 3
  p2_win_sum = p2_token * 3
  
  matrix = generate_matrix(game, p1_token, p2_token)
  sums = []
  #diagonals
  sums.append(np.trace(matrix))
  sums.append(np.trace(np.rot90(matrix)))
  #columns
  sums += np.sum(matrix, axis=0).ravel().tolist()
  #rows
  sums += np.sum(matrix, axis=1).ravel().tolist()
  
  if p1_win_sum in sums:
    return game.player_1
  elif p2_win_sum in sums:
    return game.player_2
  else:
    return None

def update_game_status(game):
  '''
     Accepts a Game model object and updates it in persistence if game is over and/or there is winner.
     Returns True if updated.
  '''
  if not game:
    return
  existing_moves = Move.objects.filter(game=game.id)
  winner = determine_winner(game)
  if winner:
    game.winner = winner
    game.save(update_fields=['winner'])

  if winner or len(existing_moves) == 9:
    game.is_over = True
    game.save(update_fields=['is_over'])
    return True

def make_computer_move(game):
  '''
     Accepts Game model object, pulls the moves, if next player is non-human, creates and saves new move for computer player.
     Does nothing if game is None or is_over.
     Currently, it simply takes the first available coordinate (row major order)
  '''
  if not game or game.is_over:
    return
  player1 = game.player_1
  player2 = game.player_2
  #If no moves and player1 is computer, make move.
  if len(game.move_set.all()) < 1:
    current_player = player1
    #We can be confident next to last move is current player due to restriction on the database level (models.py)
  elif len(game.move_set.all()) > 1:
    current_player = game.move_set.all().order_by('-time')[1].player
  else:
    last_player = game.move_set.all().order_by('-time')[0].player
    current_player = player2 if last_player == player1 else player1
  if current_player.is_human:
    pass
  else:
    matrix = generate_matrix(game, 1, 9)
    #default for ravel is row major order, so y is the first order of the array
    first_zed = matrix.ravel().tolist().index(0)
    x = first_zed % 3
    y = first_zed / 3
    Move(game=game, player=current_player, position_x=x, position_y=y).save()
   
    

class PlayerResource(ModelResource):
  '''
     Standard Resource for Player model
  '''

  class Meta:
    queryset = Player.objects.all()
    resource_name = 'player'
    authorization = Authorization()

class GameResource(ModelResource):
  '''
     Standard Resource for Game model with players/winner added via Foreign Key
  '''
  player_1 = fields.ForeignKey(__name__ + '.PlayerResource', 'player_1', full=True, null=True)
  player_2 = fields.ForeignKey(__name__ + '.PlayerResource', 'player_2', full=True, null=True)
  winner = fields.ForeignKey(__name__ + '.PlayerResource', 'winner', full=True, null=True)
  class Meta:
    queryset = Game.objects.all()
    resource_name = 'game'
    authorization = Authorization()

class MoveResource(ModelResource):
  '''
     Resource for Move with player and game added via Foreign Key
     Customized functionality post-save located in overridden obj_create()
  '''
  player = fields.ForeignKey(__name__ + '.PlayerResource', 'player', full=True, null=True)
  game = fields.ForeignKey(__name__ + '.GameResource', 'game', full=True, null=True)
  class Meta:
    queryset = Move.objects.all()
    resource_name = 'move'
    authorization = Authorization()

  def obj_create(self, bundle, **kwargs):
    '''
       Occurs after saved to persistence.
       If a game has exhausted all positions, or if there is a winner, that is set on the game object here.
    '''
    bundle = super(MoveResource, self).obj_create(bundle, **kwargs)
    game = Game.objects.get(id=bundle.data['game']['id'])
    if not update_game_status(game):
      #TODO: call to method for computer's turn if next turn is for computer
      make_computer_move(game)
      #also call update_game_status
      game = Game.objects.get(id=game.id)
      update_game_status(game)

    return bundle
    

api = Api(api_name='v1')
api.register(PlayerResource())
api.register(MoveResource())
api.register(GameResource())
