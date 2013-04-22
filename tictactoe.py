#Authored by: Ronald Braly

def init_board():
  board = {(0,0):'X',
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

def get_input(board):
  print "line 22"
  try:
    row_coord = input("Enter Row (1,2, or 3)")
    row_coord = int(row_coord) - 1
    if row_coord not in range(3):
      print "invalid input"
      return None

    column_coord = input("Enter Column (1,2, or 3)")
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
  

def run():

  board = init_board()
  show_board(board)
  valid_input = True
  while valid_input:
    valid_input = get_input(board)
    print valid_input


if __name__=="__main__":
  run()
