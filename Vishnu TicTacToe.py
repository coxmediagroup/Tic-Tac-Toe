import time
board = []
global computer
global opponent
open = " "
previous_moves = []
choice =" "

def drawBoard(board):
# This function prints out the board.
    print('   |   |')
    print(' ' + str(board[1]) + ' | '+ str(board[2]) + ' | '+ str(board[3]))
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + str(board[4]) + ' | ' + str(board[5]) + ' | '+ str(board[6]))
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + str(board[7]) + ' | ' + str(board[8]) + ' | ' + str(board[9]))
    print('   |   |')

def createBoard(board):
# "board" is a list of 10 strings representing the board (ignore index 0)
   board=[0,1,2,3,4,5,6,7,8,9]
   return board

def getChoice():
# This function determines who gets to go first
  choice =raw_input('Do you wish to go First? (Type y or n): ')
  choice = choice.upper()
  return choice

def tie(board, playing): 
# If there is a tie
  print 'Looks like we have a Tie here, Thank you for a good game!!!'
  playing = 'N'
  return playing
  
   
  
def opponent_turn(playing, board, opponent, computer):
#Opponent's choice is executed in this function
  if len(previous_moves) == 9:
    playing = tie(board, playing)
    return playing
  
  opponent_Move = input('Please enter the number of box you would like to select:')
  
  while opponent_Move in previous_moves:
    opponent_Move = input('This slot has already been taken, please select another slot:') 
  
  
  board[opponent_Move] = opponent 
  previous_moves.append(opponent_Move)
  drawBoard(board)
  print 'You selected', opponent_Move, 'Now It\'s my turn' 
  #time.sleep(1)
  return playing

    
def computer_turn(playing, board, opponent, computer):

# Computer's play is determined in this function

  if len(previous_moves) == 9:
  # if all nine boxes are filled without a winner, it's a tie.
    playing = tie(board, playing)
    return playing
    
  best_options = (5,1,3,7,9,2,4,6,8)  
  for move in best_options: 
    if move not in previous_moves:
      board[move]=computer
      if winning_combination(board)==computer:
      #if computer has a winning combination on the board
        previous_moves.append(move)
        drawBoard(board)
        print 'I selected', move, 'and I win, Thank you for a good game.'
        playing = 'N'
        return playing
      else:
        board[move]=move  
  for move in best_options:
    if move not in previous_moves:
    #if there is a chance for opponent to win during next turn, that box is filled by computer now    
      board[move]=opponent
      if winning_combination(board)==opponent:
        board[move]=computer
        previous_moves.append(move)
        print 'I selected', move, 'Now it\'s your turn'
        #time.sleep(1)
        drawBoard(board) 
        return playing
      else:
        board[move]=move
        
  for move in best_options: 
  # Assuming that computer hasn't won and opponent has no chance of winning in next play, best option is selected here
    if move not in previous_moves:
      board[move]=computer
      previous_moves.append(move)
      print 'I selected', move, 'Now it\'s your turn'
      time.sleep(1)
      drawBoard(board)
      return playing     
    
      
    
def winning_combination(board):  # Winner is determined in this function

  victory=((1,2,3),(1,5,9),(2,5,8),(3,6,9),(4,5,6),(7,8,9),(3,5,7),(1,4,7))    
# If board has a row of 'X's or 'O's a winner is determined    
  
  for row in victory:
        if board[row[0]]==board[row[1]]==board[row[2]] != open:
            winner = board[row[0]]
            return winner

    

def main():
  # This program plays TicTacToe game and will never lose
  playing = 'Y'
  global board 
  board = createBoard(board)  #board is created
  choice = getChoice() #Determines who goes first, X is followed by O, always.
  if choice == 'Y':
    opponent = 'X'
    computer = 'O'   
  else:
    computer= 'X'
    opponent= 'O'

  print 'You are', opponent, 'and I am', computer
  global previous_moves
  print('Welcome to Tic Tac Toe!')
  drawBoard(board) # displays board on screen
  while playing == 'Y':
   if opponent == 'X': # if Opponent goes first 
     playing = opponent_turn(playing, board, opponent, computer)
     if playing =='N':
       break
     playing = computer_turn(playing, board, opponent, computer)
   else:  # if Computer goes first
     playing = computer_turn(playing, board, opponent, computer)
     if playing == 'N':
       break
     playing = opponent_turn(playing, board, opponent, computer)
 

  


if __name__ == '__main__':
  main()
