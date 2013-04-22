# Authored by: Ronald Braly

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

def run():

 board = init_board()
 show_board(board)

if __name__=="__main__":
  run()
