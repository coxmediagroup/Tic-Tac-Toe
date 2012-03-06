import copy
import random
import sys

"""
TicTacToeBoard
By: Will Riley
"""

def main():
  # create empty tic-tac-toe game board
  board = TicTacToeBoard()
  
  # randomly pick whether the user will be the first or second player
  userPlayerId = random.choice([1,2])
  computerPlayerId = board.get_other_player_num(userPlayerId)
  
  # welcome the user to the game
  print "Welcome to Tic-Tac-Toe"

  # beginning with the first player,
  # alternate turns between players until the game ends
  currentPlayerId = 1 # the id of the current player
  cmd = '' # the command entered by the user
  while(cmd != 'q' and board.is_game_over() is False):
    if currentPlayerId == computerPlayerId:      
      board.take_best_move(computerPlayerId)
      # end turn and allow the user to take a turn
      currentPlayerId = userPlayerId
    else:
      # display the board
      board.display()
      
      # remind the user whether they are X's or O's
      if userPlayerId == 1:
        print "You are X's"
      else:
        print "You are O's"
      
      # ask user to input the coordinates of her mark, or to press q to quit
      cmd = raw_input('<enter "{rowNum}, {columnNum}" or "q" to quit>: ')
      
      # make sure the user has entered valid coordinates for her mark
      # and if so, mark the board for the user
      parts = cmd.split(',')
      if len(parts) == 2:
        row = int(parts[0].strip())
        col = int(parts[1].strip())
        validRowRange = validColRange = [1,2,3]
        if row in validRowRange and col in validColRange:
          # make sure a mark does not already exist at the coordinates 
          if  board.d[row - 1][col - 1] == board.CELL_NO_PLAYER:
            # mark the board at the coordinate for the player
            board.d[row - 1][col - 1] = userPlayerId
            # end turn and allow the computer player to take a turn
            currentPlayerId = computerPlayerId
  
  # display final board  
  board.display()

  # display final game results
  winnerId = board.get_winner()
  if winnerId == userPlayerId:
    print "You won!"
  elif winnerId == computerPlayerId:
    print "You lost!"
  elif winnerId == board.GAME_WINNER_TIED:
    print "You tied!"
        
class TicTacToeBoard:  
  def __init__(self):
    # create a 3 by 3 matrix representing the tic-tac-toe board
    # each cell will have the player number 
    # 0 = no player, 1 = player 1, 2 = player 2    
    self.CELL_NO_PLAYER = 0
    self.d = [[self.CELL_NO_PLAYER for i in xrange(3)] for j in xrange(3)]
    
    self.GAME_WINNER_GAME_NOT_OVER = 0
    self.GAME_WINNER_TIED = 3
    
  def is_game_over(self):
    return self.get_winner() != self.GAME_WINNER_GAME_NOT_OVER
  
  def is_tied(self):
    return self.get_winner() == self.GAME_WINNER_TIED
    
  def has_won(self, playerNum):
    return self.get_winner() == playerNum
    
  def take_best_move(self, playerNum):
    # if player can win, mark spot so the player can win 
    for r in xrange(3):
      for c in xrange(3):
        if self.d[r][c] == self.CELL_NO_PLAYER:
          nB = copy.deepcopy(self)
          nB.d[r][c] = str(playerNum)
          if nB._can_win(playerNum):
            self.d[r][c] = playerNum
            return
    
    # if player cannot win but the player can tie, 
    # mark spot so the player can tie     
    for r in xrange(3):
      for c in xrange(3):
        if self.d[r][c] == self.CELL_NO_PLAYER:
          nB = copy.deepcopy(self)
          nB.d[r][c] = str(playerNum)
          if nB._can_tie(playerNum):
            self.d[r][c] = playerNum
            return
            
    # if player can neither win nor tie, mark any spot
    for r in xrange(3):
      for c in xrange(3):
        if self.d[r][c] == self.CELL_NO_PLAYER:
          self.d[r][c] = playerNum
          return
  
  def display(self):
    # display board such that 
    # player 1 has X's and player 2 has O's 
    # and other spots have dashes
    # also include axes with row and column coordinates 
    print '  123'
    no_player_symbol = '-'
    player_1_symbol = 'X'
    player_2_symbol = 'O'
    for i in xrange(3):
        print str(i+1) + ' ' + ''.join(map(str, self.d[i])).replace('1', player_1_symbol).replace('2', player_2_symbol).replace('0', no_player_symbol)
    pass
  
  def get_winner(self):
    # return 0 if the game is not over
    # return 1 if player 1 is the winner
    # return 2 if player 2 is the winner
    # return 3 if player 1 and player 2 tied
    gameOver = True
    for line in self._get_lines():
      if line == '111':
        return 1 # player 1 won
      elif line == '222':
        return 2 # player 2 won
      if '0' in line:
        gameOver = False
    if gameOver:
      return self.GAME_WINNER_TIED # tied
    else:
      return self.GAME_WINNER_GAME_NOT_OVER # game is not over yet
  
  def get_other_player_num(self, playerNum):
    if playerNum == 1:
      return 2
    else:
      return 1
  
  def _get_lines(self):
    # return all horizontal, vertical, and diagnol lines on the tic-tac-toe board
    # where each line is represented by a string of player numbers
    # it will use zeros to represent empty cells where no player is present
    lines = []
    
    # add horizontal row lines
    for i in xrange(3):
      lines.append(''.join(map(str, self.d[i])))
    
    # add vertical column lines
    for i in xrange(3):
      lines.append(str(self.d[0][i]) + str(self.d[1][i]) + str(self.d[2][i]))
    
    # add diagnol lines
    lines.append(str(self.d[0][0]) + str(self.d[1][1]) + str(self.d[2][2]))
    lines.append(str(self.d[0][2]) + str(self.d[1][1]) + str(self.d[2][0]))
    return lines
    
  def _get_next_move_boards(self, playerNum):
    nextBoards = []
    for r in xrange(3):
      for c in xrange(3):
        if self.d[r][c] == self.CELL_NO_PLAYER:
          nB = copy.deepcopy(self)
          nB.d[r][c] = str(playerNum)
          nextBoards.append(nB)
    return nextBoards

  def _can_win(self, playerNum):
    # assume player playerNum has just moved and
    # it is the other player's turn
    # return whether player playerNum can still win

    # determine the other player
    otherPlayerNum = self.get_other_player_num(playerNum)

    # make sure the player has not already lost or tied
    winner = self.get_winner()
    if winner == playerNum:
      return True
    elif winner == otherPlayerNum or winner == self.GAME_WINNER_TIED:
      return False

    # make sure the player can win indepedent of the other player's next move  
    for nextMoveBoard in self._get_next_move_boards(otherPlayerNum):
      nextWinner = nextMoveBoard.get_winner()
      if nextWinner == otherPlayerNum or nextWinner == self.GAME_WINNER_TIED:
        return False
      cW = False
      for nextMoveBoard2 in nextMoveBoard._get_next_move_boards(playerNum): 
        if nextMoveBoard2._can_win(playerNum):
          cW = True
          break
      if cW is False:
        return False
    return True

  def _can_tie(self, playerNum):
    # assume player playerNum has just moved and
    # it is the other player's turn
    # return whether player playerNum can still tie
    
    # determine the other player
    otherPlayerNum = self.get_other_player_num(playerNum)
    
    # make sure the player has not lost
    winner = self.get_winner()
    if winner == playerNum or winner == self.GAME_WINNER_TIED:
      return True
    elif winner == otherPlayerNum:
      return False
    
    # make sure the player can tie indepedent of the other player's next move  
    for nextMoveBoard in self._get_next_move_boards(otherPlayerNum):
      if nextMoveBoard.get_winner() == otherPlayerNum:
        return False
      if nextMoveBoard.get_winner() == self.GAME_WINNER_TIED:
        continue
      cT = False
      for nextMoveBoard2 in nextMoveBoard._get_next_move_boards(playerNum): 
        if nextMoveBoard2._can_tie(playerNum):
          cT = True
          break
      if cT is False:
        return False
    return True

if __name__ == "__main__":
  sys.exit(main())