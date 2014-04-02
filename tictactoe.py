#!/usr/bin python
#	Tic Tac Toe
#	Danny Burrows
#
#	Implement a version of tic-tac-toe where a player plays against an AI bot where the AI never loses.
import copy
# possible wins:
#	x, x + 1, x + 2 | y = i (0 to 2)
#	y, y + 1, y + 2 | x = i (0 to 2)
#	z, z+1, z+2 | z = (x, y)
#	z, z-1, z-2 | z = (x, y) from x=2,y=0

#
def checkWin(board):
	# check wins on board	
	for i in range(3):
		# check rows
		if (board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != 0):
			return board[i][0]
		# check columns
		elif (board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != 0):
			return board[0][i]
		# check both cross conditions
		elif (board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != 0):
			return board[0][0]
		elif (board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[2][0] != 0):
			return board[2][0]
	return False

def checkTie(board):
	for x in board:
		for y in x:
			if not y:
				return False
	return True

#	find the best move for the AI to ensure no lose situation
def generateMoves(board):
	# check all possible open moves
	possMoves = []
	for x in range(3):
		for y in range(3):
			if possibleMove(board, (x,y)):
				possMoves.append((x,y))
	
	return possMoves

def miniMax(board, player):
	# pseudo code for minimax
	# miniMax(node)
	# 	max = -inf, min = +inf
	#	if node.isBlack
	#		foreach(child of node)
	#			max = max(max, minimax(child))
	#		return max
	#	else
	#		foreach(child of node)
	#			min = min(min, minimax(child))
	#		return min
	#printBoard(board)
	#print "\n"
	moves = generateMoves(board)
	if (checkWin(board) == 1):
		return (1, None)
	elif (checkWin(board) == 2):
		return (2, None)
	elif (checkTie(board)):
		return (0, None)

	if player == 1:
		nextPlayer = 2
	elif player == 2:
		nextPlayer = 1
	
	if (player == 1):
		best = (-100, None);
		for move in moves:
			markMove(board, move, player)
			value = miniMax(board, nextPlayer)[0]
			if value > best[0]:
				best = (value,move)
		return best
	elif (player == 2):
		best = (+100, None);
		for move in moves:
			markMove(board, move, player)
			value = miniMax(board, nextPlayer)[0]
			if value < best[0]:
				best = (value,move)
		return best

def markMove(board, position, player):
	x = position[0]
	y = position[1]
	board[x][y] = player

#	check if move is possible
def possibleMove(board, possible):
	x = possible[0]
	y = possible[1]
	if board[x][y] == 0:
		return True
	return False

#	draw board
def printBoard(board):
	print "%s | %s | %s" % (board[0][0], board[0][1], board[0][2])
	print "--+---+--"
	print "%s | %s | %s" % (board[1][0], board[1][1], board[1][2])
	print "--+---+--"
	print "%s | %s | %s" % (board[2][0], board[2][1], board[2][2])

#	some simple test cases
def runTests():
	board = [ [1,0,0],[1,2,0],[0,0,0] ]
	testCase(board, (0,2))

	board = [ [1,1,0],[2,2,0],[0,0,0] ]
	testCase(board, (1,2))

	board = [ [1,2,1],[2,1,2],[2,1,2] ]
	testCase(board, None)

	board = [ [0,0,1],[0,2,1],[0,0,0] ]
	testCase(board, (2,2))

	board = [ [2,2,0],[0,1,1],[0,1,0] ]
	testCase(board, (0,2))
	
	board = [ [1,0,2],[0,1,0],[0,0,0] ]
	testCase(board, (2,2))

	board = [ [0,0,0],[0,2,0],[1,0,1] ]
	testCase(board, (2,1))
#	run test, determine outcome
def testCase(board, expected):
	#printBoard(board)
	bestMove = miniMax(board, 2)
	if (bestMove[1] != expected):
		print "FAILED \t Expected " + str(expected) + " Calculated " + str(bestMove[1])
	else:
		print "PASSED \t Expected " + str(expected)

# game class
# need the following
# -actual board array
# -list of open moves
# -is game over
# -who's turn
# -winner
# -mark a board slot
# -remove a mark
class gameState:
	def __init__(self):
		self.board = [0 for x in range(9)]
		self.winner = None

	def printBoard(self):
		print self.board

	def availMoves(self):
		moves = []
		for i,x in enumerate(self.board):
			if x == 0:
				moves.append(i)
		return moves

	def gameOver(self):
		# 0 1 2
		# 3 4 5
		# 6 7 8
		wins = [ (0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6) ]
		for i,j,k in wins:
			if self.board[i] == self.board[j] == self.board[k] and self.board[i] != 0:
				self.winner = self.board[i]
				return True

		return False

	def makeMove(self, move, player):
		if not self.board[move]:
			self.board[move] = player
			return True
		return False

	def clearMove(self, move):
		self.board[move] = 0

	def setBoard(self, array):
		self.board = self.__boardArray(array)

	def __boardArray(self, input):
		return (map(int,input.split()))

# class for AI moves
# need:
# miniMax function
# -implement via game trees, attempt to maximize AI moves to win, minimize players to lose
# -max and min functions, that work recursively on the current ply
# -evaluation of currently tested ply
class botAI:
	def __init__(self, marker = 2, opponent = 1):
		self.marker = marker
		self.opponent = opponent

	def miniMax(self, gameInstance):
		return maxMove(gameInstance)
	# bestMove location and bestMove value
	# value will be used to determine if the move is a good one or not, from eval game
	def maxMove(self, ply):
		bestMove = None
		bestValue = -10
		# foreach childnode, find min
		# track both the move and the value, will need on upwards travesal
		for move in ply.availMoves():
			# for each move, make the move and test the result
			# if the move is not the best move, based on evaluation of each ply, then undo move
			ply.makeMove(move, self.marker)
			# base case
			if ply.gameOver():
				value = evalGame(ply)
			# recusive case
			else:
				value,move = minMove(ply)
			
			ply.clearMove(move)

			if value > bestValue:
				bestValue = value
				bestMove = move

		return bestValue, bestMove

	# from psuedo, essentially the same, but swaping the logic checks
	def minMove(self, ply):
		bestMove = None
		bestValue = 10
		# foreach childnode, find min
		# track both the move and the value, will need on upwards travesal
		for move in ply.availMoves():
			# for each move, make the move and test the result
			# if the move is not the best move, based on evaluation of each ply, then undo move
			ply.makeMove(move, self.marker)
			# base case
			if ply.gameOver():
				value = evalGame(ply)
			# recusive case
			else:
				value,move = minMove(ply)
			
			ply.clearMove(move)

			if value < bestValue:
				bestValue = value
				bestMove = move

		return bestValue, bestMove

	def evalGame(self, ply):
		# check this ply has reached conclusion
		if ply.gameOver():
			# ai has won
			if ply.winner == self.marker:
				return 10
			# player has won
			elif ply.winner == self.opponent:
				return -10
		return 0 # default case

game = gameState()
game.printBoard()
game.setBoard("1 1 0 2 2 2 0 0 0")
game.printBoard()
print game.makeMove(2, 1)
game.printBoard()
print game.makeMove(1,2)
game.printBoard()
print game.availMoves()
#runTests()
#bestMove = miniMax(board, 2)
#print bestMove
#markMove(board, bestMove[1], 2)

#	get user move
#	-test valid user move
#	-mark move

#	computer move
#	-find best move
#	-mark move

#	again?
