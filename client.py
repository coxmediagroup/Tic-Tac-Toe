import re
import requests
import json
import numpy as np

api_version = 'v1'
base_url = 'http://localhost:8000/api/'+api_version+'/'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def print_board(game_dict, state):
  '''
     Prints current status of board to stdout.
  '''
  p1 = 1
  p2 = 8
  matrix = np.zeros((3,3), dtype=np.int)
  text = []
  for item in game_dict['move_set']:
    if item['player']['id'] == state.player_id:
      matrix[item['position_y'], item['position_x']] = p1
    else:
      matrix[item['position_y'], item['position_x']] = p2
  for index, item in enumerate(matrix.ravel().tolist()):
    if index == 3 or index == 6:
      text.append('\n-----------\n')
    if not index % 3 == 0:
      text.append('|')
    if item == p1:
      text.append(' X ')
    elif item == p2:
      text.append(' O ')
    else:
      text.append('   ')
  if game_dict['is_over']:
    if 'winner' in game_dict and game_dict['winner']:
      if game_dict['winner']['is_human']:
        text.append('\n\nWINNER WINNER, CHICKEN DINNER!!!  '+game_dict['winner']['name']+' WINS!!!!!!!!\n')
        text.append("Hope you didn't see this without cheating!")
      else:
        text.append('\n\nOh, so sad, better luck next time!\n')
    else:
      text.append('\n\nTied game.\n')
  print(''.join(text))
  

class GameState():
  name = ''
  #get first computer player, create if doesn't exist
  resp = json.loads(requests.get(base_url+u'player/?is_human=false&format=json').content)
  if int(resp['meta']['total_count']) > 0:
    computer_player_id = resp['objects'][0]['id']
  else:
    player_dict = {'is_human':False, 'name':'Robot'}
    data = json.dumps(player_dict)
    computer_player_id = json.loads(requests.post(base_url+u'player/', data=data, headers=headers).content)['id']
  player_id = 0
  game_in_progress = False
  game_id = 0

def new_game(state):
  '''
     Creates a new game
  '''
  if not len(state.name):
    state.game_in_progress = True
    state.name = raw_input('enter your name: ')
    #for now, just grab the first in db w/ name, or create
    resp = json.loads(requests.get(base_url+u'player/?format=json&is_human=true&name='+state.name).content)
    #store player_id in variable
    if int(resp['meta']['total_count']) > 0:
      state.player_id = resp['objects'][0]['id']
    else:
      player_dict = {'is_human':True, 'name':state.name}
      data = json.dumps(player_dict)
      resp = json.loads(requests.post(base_url+u'player/', data=data, headers=headers).content)
      state.player_id = resp['id']
  #call POST game to create new game w/ players and store game_id in variable
  game_dict = {'player_1':{'id':state.player_id}, 'player_2':{'id':state.computer_player_id}}
  data = json.dumps(game_dict)
  resp = json.loads(requests.post(base_url+u'game/', data=data, headers=headers).content)
  state.game_id = resp['id']

def move_dict(game_id, player_id, x, y):
  return {"game": { "id": game_id }, "player": { "id": player_id }, "position_x": x, "position_y": y}

game_state = GameState()

while (1):
  if (game_state.game_in_progress):
    print_board(json.loads(requests.get(base_url+u'game/'+str(game_state.game_id)+'/?format=json&').content), game_state)
  entered = raw_input(u'n = new game; q = quit; #,# = make move (0 indexed): ')
  if entered.upper() == 'Q':
    break
  if entered.upper() == 'N':
    new_game(game_state)
  m = re.match(r'([0-2]),([0-2])', entered)
  if m:
    move_post = json.dumps(move_dict(game_state.game_id, game_state.player_id, int(m.group(1)), int(m.group(2))))
    resp = requests.post(base_url+u'move/', data=move_post, headers=headers)
