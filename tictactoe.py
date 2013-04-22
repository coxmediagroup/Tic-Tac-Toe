#Authored by: Ronald Braly

PLAYER = ['X', 'O']

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

def get_input(board, player):
  print "line 22"
  try:
    row_coord = input("Player %s: Enter Row (1,2, or 3)" %player)
    row_coord = int(row_coord) - 1
    if row_coord not in range(3):
      print "invalid input"
      return None

    column_coord = input("Player %s: Enter Column (1,2, or 3)" %player)
    column_coord = int(column_coord) - 1
    if column_coord not in range(3):
      print "invalid input"
      return None

    coord = (row_coord, column_coord)

    if board[coord] != '-':
      print "position %s has already been played." %str(coord)
      return None

    return coord

  except:
    print "invalid input"
    return None

def update_board(board, player, move_coord):
  board[move_coord] = player  

def run():

  move_coord = True
  board = init_board()
  show_board(board)
  curr_turn = 0
  curr_player = PLAYER[curr_turn%2]

  while move_coord:
    move_coord = get_input(board, curr_player)
    print ''
    update_board(board, curr_player, move_coord)
    show_board(board)
    curr_turn += 1
    curr_player = PLAYER[curr_turn%2]

if __name__=="__main__":
  run()
