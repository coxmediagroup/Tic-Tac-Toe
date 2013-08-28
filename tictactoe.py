#Authored by: Ronald Braly

import os

PLAYERS = ['X', 'O']
CENTER = (1,1)
CORNERS = [(0,0),(0,2),(2,0),(2,2)]
DIAGONALS = [[(0,0),(1,1),(0,2)],[(2,0),(0,0),(2,2)]]

def init_board():
  board = {(0,0):'-',
           (0,1):'-',
           (0,2):'-',
           (1,0):'-',
           (1,1):'-',
           (1,2):'-',
           (2,0):'-',
           (2,1):'-',
           (2,2):'-'}
  return board

def show_board(board):
  for i in range(3):
    row_str = ''
    for j in range(3):
      row_str = row_str + board[(i,j)]
    print row_str

def get_player_input(board, player):
  try:
    row_coord = raw_input("Player %s, Enter Row (1,2, or 3): " %player)
    row_coord = int(row_coord) - 1
    if row_coord not in range(3):
      print "invalid input"
      return None

    column_coord = raw_input("Player %s, Enter Column (1,2, or 3):" %player)
    column_coord = int(column_coord) - 1
    if column_coord not in range(3):
      print "invalid input"
      return None

    coord = (row_coord, column_coord)

    if board[coord] != '-':
      print "position %s,%s has already been played." %(row_coord + 1, column_coord + 1)
      return None

    return coord

  except:
    print "invalid input"
    return None

def get_computer_input(board, player):
  '''
  return a computer player's move based on applying rules to current board
  '''
  # Rule 1: Play winning move
  # Rule 2: Block other player
  # Rule 3: Play strongest move

  # Rule 1: if player already has 2 spaces in same line and 3rd space is open in that line, use it
  # 1a: check for 2 across
  for i in range(3):
    print "i = " + str(i)
    count = 0
    for j in range(3):
      print "j = " + str(j)
      if board[i,j] != player and board[i,j] != '-':
        # move to next row
        break
      if board[i,j] == player: count = count + 1
    if count == 2:
      row_coord = i
      for j in range(3):
        if board[i,j] == '-':
          column_coord = j
          return (row_coord, column_coord)

  # 1b: check for 2 down
  for i in range(3):
    print "i = " + str(i)
    count = 0
    for j in range(3):
      print "j = " + str(j)
      if board[j,i] != player and board[j,i] != '-':
        # move to next row
        break
      if board[j,i] == player: count = count + 1
    if count == 2:
      row_coord = i
      for j in range(3):
        if board[j,i] == '-':
          column_coord = j
          return (row_coord, column_coord)

  # 1c still punting on diagonals

  # Rule 2: if player already has 2 spaces in same line block them
  # 2a: check for 2 across
  for i in range(3):
    print "i = " + str(i)
    count = 0
    for j in range(3):
      print "j = " + str(j)
      if board[i,j] == player:
        # move to next row
        break
      if board[i,j] != player and board[i,j] != '-': count = count + 1
    if count == 2:
      row_coord = i
      for j in range(3):
        if board[i,j] == '-':
          column_coord = j
          return (row_coord, column_coord)

  # 2b: check for 2 down
  for i in range(3):
    print "i = " + str(i)
    count = 0
    for j in range(3):
      print "j = " + str(j)
      if board[j,i] == player:
        # move to next row
        break
      if board[j,i] != player and board[j,i] != '-': count = count + 1
    if count == 2:
      row_coord = i
      for j in range(3):
        if board[j,i] == '-':
          column_coord = j
          return (row_coord, column_coord)

  # 2c still punting on diagonals

  #Rule 3
  # 3a take center
  if board[CENTER] == '-':
    return CENTER

  # 3b take corner
  for corner in CORNERS:
    if board[corner] == '-':
      return corner

  # 3c take anything
  for coord in board.keys():
    if coord not in CORNERS + [CENTER]:
      if board[coord] != '-':
        return coord

  #should not get here

  return None      
  

def update_board(board, player, move_coord):
  board[move_coord] = player

def is_game_over(board):
  has_won, winning_player = player_has_won(board)
  if has_won:
    return (True, winning_player)
  if no_more_moves(board):
    return (True, "tie")
  return (False, None)

def player_has_won(board):

  #check for three across
  for i in range(3):
    if (board[(i,0)] != '-'
        and board[(i,0)] == board[(i,1)]
        and board[(i,1)] == board[(i,2)]):
      return True, board[(i,0)]

  #check for three down
  for i in range(3):
    if (board[(0,i)] != '-'
        and board[(0,i)] == board[(1,i)]
        and board[(1,i)] == board[(2,i)]):
      return True, board[(0,i)]

  #check for three diagonal
    if (board[(0,0)] != '-'
        and board[(0,0)] == board[(1,1)]
        and board[(1,1)] == board[(2,2)]):
      return True, board[(0,0)]

    if (board[(0,2)] != '-'
        and board[(0,2)] == board[(1,1)]
        and board[(1,1)] == board[(2,0)]):
      return True, board[(0,2)] 

  return False, ''

def no_more_moves(board):
  if '-' in board.values():
    return False
  return True
  

def run():

  os.system('clear')
  computer_player = raw_input("Enter which player is computer, 'X' or 'O' (any other selection will exit):  ")
  computer_player = computer_player.upper()
  if computer_player not in ['X', 'O']:
    print "exiting"
    return

  move_coord = None
  board = init_board()
  show_board(board)
  curr_turn = 0
  curr_player = PLAYERS[curr_turn%2]
  game_is_over = False

  while not game_is_over:
    
    os.system('clear')
    show_board(board)
    print ''
    while not move_coord:
      if curr_player == computer_player:
        move_coord = get_computer_input(board, curr_player)
      else:
        move_coord = get_player_input(board, curr_player)
    update_board(board, curr_player, move_coord)
    (game_is_over, winning_player) = is_game_over(board)
    print str((game_is_over, winning_player))
    if game_is_over:
      break
    curr_turn += 1
    curr_player = PLAYERS[curr_turn%2]
    move_coord = None

  os.system('clear')
  show_board(board)
  print ''
  print "Game Over. Winner is:  " + winning_player

if __name__=="__main__":
  run()
