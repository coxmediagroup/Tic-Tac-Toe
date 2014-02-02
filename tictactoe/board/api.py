from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from django.http import Http404
from board.models import Player, Move, Game
import numpy as np

class PlayerResource(ModelResource):
  class Meta:
    queryset = Player.objects.all()
    resource_name = 'player'
    authorization = Authorization()

class GameResource(ModelResource):
  player_1 = fields.ForeignKey(__name__ + '.PlayerResource', 'player_1', full=True, null=True)
  player_2 = fields.ForeignKey(__name__ + '.PlayerResource', 'player_2', full=True, null=True)
  winner = fields.ForeignKey(__name__ + '.PlayerResource', 'winner', full=True, null=True)
  class Meta:
    queryset = Game.objects.all()
    resource_name = 'game'
    authorization = Authorization()

def determine_winner(game):
  winner = None
  p1_token = 1
  p2_token = 9
  p1_win_sum = p1_token * 3
  p2_win_sum = p2_token * 3
  
  matrix = np.zeros((3,3), dtype=np.int)
  for item in Move.objects.filter(game=game).select_related():
    if game.player_1 == item.player:
      matrix[item.position_x, item.position_y] = p1_token
    else:
      matrix[item.position_x, item.position_y] = p2_token
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


class MoveResource(ModelResource):
  player = fields.ForeignKey(__name__ + '.PlayerResource', 'player', full=True, null=True)
  game = fields.ForeignKey(__name__ + '.GameResource', 'game', full=True, null=True)
  class Meta:
    queryset = Move.objects.all()
    resource_name = 'move'
    authorization = Authorization()

  def obj_create(self, bundle, **kwargs):
    bundle = super(MoveResource, self).obj_create(bundle, **kwargs)
    game = Game.objects.get(id=bundle.data['game']['id'])
    existing_moves = Move.objects.filter(game=game.id)
    # TODO: remove this print statement (left commented in case for debugging)
    '''
    for move in existing_moves:
      print('HEY HEY HEY,,, move: %s - %s vs %s | player: %s marked position %s,%s' % (move.time, move.game.player_1.name, move.game.player_2.name, move.player.name, move.position_x, move.position_y))
    '''
    winner = determine_winner(game)
    if winner:
      game.winner = winner
      game.save(update_fields=['winner'])

    if winner or len(existing_moves) == 9:
      game.is_over = True
      game.save(update_fields=['is_over'])
    else:
      #TODO: call to method for computer's turn if next turn is for computer
      pass


    return bundle
    

api = Api(api_name='v1')
api.register(PlayerResource())
api.register(MoveResource())
api.register(GameResource())
