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

def checkWin(board):
	# check wins on board	
	for i in range(3):
		# check rows
		if (board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != 0):
			return True
		# check columns
		elif (board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != 0):
			return True
		# check both cross conditions
		elif (board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != 0):
			return True
		elif (board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[2][0] != 0):
			return True
	return False

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
	moves = generateMoves(board)
	if checkWin(board):
		#print board
		if (player == 1):
			return (1, None)
		else:
			return (2, None)
	elif (player == 1):
		best = (-100, None);
		for move in moves:
			x = move[0]
			y = move[1]
			board[x][y] = player
			# value keeps track of whether the move would be more benificial or harmful to the player
			value = miniMax(board, player)[0]
			if value > best[0]:
				best = (value,(x,y))
			board[x][y] = 0
		return best
	#if (player == 2):
	else:
		best = (+100, None);
		for move in moves:
			x = move[0]
			y = move[1]
			board[x][y] = player
			value = miniMax(board, player)[0]
			if value < best[0]:
				best = (value,(x,y))
			board[x][y] = 0
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
def runTests(board):
	board = [ [1,0,0],[1,2,0],[0,0,0] ]
	testCase(board, (0,2))
	board = [ [1,1,0],[2,2,0],[0,0,0] ]
	testCase(board, (1,2))
	board = [ [0,0,1],[0,2,1],[0,0,0] ]
	testCase(board, (2,2))
	board = [ [1,0,2],[0,1,0],[0,0,0] ]
	testCase(board, (2,2))
	board = [ [0,0,0],[0,2,0],[1,0,1] ]
	testCase(board, (2,1))

#	run test, determine outcome
def testCase(board, expected):
	bestMove = miniMax(board, 2)
	if (bestMove[1] != expected):
		print "FAILED \t Expected " + str(expected) + " Calculated " + str(bestMove[1])
	else:
		print "PASSED \t Expected " + str(expected)

board = [ [1,0,0],[1,2,0],[0,0,0] ]

runTests(board)
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
