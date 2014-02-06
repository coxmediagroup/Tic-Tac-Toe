from django.conf.urls import patterns, url, include
from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from django.http import Http404
from board.models import Player, Move, Game
from collections import defaultdict
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

def select_move_for_computer(matrix, user, comp):
  '''
     Selects move for computer using the following criteria in order of precedence (where p2 is computer):
     1) If middle not selected, select it.
     2) Win if possible by selecting empty coordinate where line has sum == p2_token * 2.
     3) Prevent win for other player (line w/ sum == p1_token * 2).
     4) Select first empty coordinate going right to left, top to bottom.
  '''
  def find_empty_in_coordinate_list(coords):
    '''
       First tuple from list comprehension to gather all empty coordinates is returned.
       Will error if there are no empty coordinates in the list!
    '''
    #matrix is in row major order, so y comes first when looking up values
    return [coord for coord in coords if matrix[coord[1], coord[0]] == 0][0]
    
  #1
  if matrix[1][1] == 0:
    return (1,1)
  #2-4
  else:
    corners = [(0,0),(2,0),(0,2),(2,2)]
    sums = defaultdict(list)
    #diagonals
    sums[np.trace(matrix)].append([(0,0),(1,1),(2,2)])
    sums[np.trace(np.rot90(matrix))].append([(2,0),(1,1),(0,2)])
    #columns
    column_sums = np.sum(matrix, axis=0).ravel().tolist()
    for index, column_sum in enumerate(column_sums):
      sums[column_sum].append([(index, 0),(index,1),(index,2)])
    #rows
    row_sums = np.sum(matrix, axis=1).ravel().tolist()
    for index, row_sum in enumerate(row_sums):
      sums[row_sum].append([(0,index),(1,index),(2,index)])
    #2
    if comp*2 in sums:
      return find_empty_in_coordinate_list(sums[comp*2][0])
    #3
    if user*2 in sums:
      return find_empty_in_coordinate_list(sums[user*2][0])
    #4
    first_zed = matrix.ravel().tolist().index(0)
    return (first_zed % 3, first_zed / 3)
    

def make_computer_move(game):
  '''
     Accepts Game model object, pulls the moves, if next player is non-human, creates and saves new move for computer player.
     Does nothing if game is None or is_over.
  '''
  if not game or game.is_over:
    return
  player1 = game.player_1
  player2 = game.player_2
  p1_token = 1
  p2_token = 9
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
    matrix = generate_matrix(game, p1_token, p2_token)
    (x,y) = select_move_for_computer(matrix, p1_token, p2_token)


    Move(game=game, player=current_player, position_x=x, position_y=y).save()

class PlayerResource(ModelResource):
  '''
     Standard Resource for Player model
  '''

  class Meta:
    queryset = Player.objects.all()
    resource_name = 'player'
    authorization = Authorization()
    # bug in django-tastypie-swagger necessitates lists for comparison options
    filtering = { 'name': ['exact', 'icontains',],
                  'is_human': ['exact',],
    }
    always_return_data = True

class GameResource(ModelResource):
  '''
     Standard Resource for Game model with players/winner added via Foreign Key
  '''
  player_1 = fields.ForeignKey(__name__ + '.PlayerResource', 'player_1', full=True, null=True)
  player_2 = fields.ForeignKey(__name__ + '.PlayerResource', 'player_2', full=True, null=True)
  winner = fields.ForeignKey(__name__ + '.PlayerResource', 'winner', full=True, null=True)
  move_set = fields.ToManyField(__name__ + '.MoveResource', 'move_set', full=True, null=True)
  class Meta:
    queryset = Game.objects.all()
    resource_name = 'game'
    authorization = Authorization()
    always_return_data = True

class MoveResource(ModelResource):
  '''
     Resource for Move with player and game added via Foreign Key
     Customized functionality post-save located in overridden obj_create()
  '''
  player = fields.ForeignKey(__name__ + '.PlayerResource', 'player', full=True, null=True)
  game = fields.ForeignKey(__name__ + '.GameResource', 'game', full=False, null=True)
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
      make_computer_move(game)
      game = Game.objects.get(id=game.id)
      update_game_status(game)

    return bundle
    

api = Api(api_name='v1')
api.register(PlayerResource())
api.register(MoveResource())
api.register(GameResource())
