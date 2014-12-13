
import itertools


def other_player(player):
  if player == "x" or player == "X":
    return "O"
  else:
    return "X"


class Board(str):
  def column(self, index):
    return self[index:index+7:3]
  def columns(self):
    for index in range(3):
      yield self.column(index)
  def row(self, index):
    return self[index:index+3]
  def rows(self):
    for index in range(3):
      yield self.row(index)
  def diagL(self):
    return ''.join([self[0], self[4], self[8]])
  def diagR(self):
    return ''.join([self[2], self[4], self[6]])
  def possibilities(self):
    yield from self.columns()
    yield from self.rows()
    yield self.diagL()
    yield self.diagR()
  def is_win_for(self, player):
    win = ''.join([player] * 3)
    for trial in self.possibilities():
      if trial == win:
        return True
  def play_at(board, player, pos):
    if board[pos] != '_':
      raise Exception("%s already played at %d" %(board[pos], pos))
    newboard = Board(board[:pos] + player + board[pos+1:])
    status = "win" if newboard.is_win_for(player) else "open"
    return (status, newboard, player, pos)
  def moves_for(board, player):
    moves = (play_at(board, player, i) for (i, played) in enumerate(board) if played == "_")
    wins, losses = itertools.tee(lambda (s,_,_,_): s=='win', moves)
    moves.sort(key=lambda (s,b,p,x): {'win':0, 'open':10}[s])
    moves


cache = {}

def possible_outcomes(board0="_________", player0="X", desired0='win', history0=tuple()):
  cachekey=(board0,player0)
  if cachekey in cache:
  	return cache[cachekey]
  for move1 in board0.moves_for(player0):
    status1, board1, player1, pos1 = move1
    history1 = history0 + (move1,)
    if status1 == desired0:
      value = (move1, history1)
      cache[cachekey] = value
      yield value
    else:
      for (move2, history2) in possible_outcomes(board1, other_player(player1), 'open', history1):
        status2, board2, player2, pos2 = move2
        yield from possible_outcomes(board2, player1, 'win', history2)

for i in possible_outcomes(): print(i)