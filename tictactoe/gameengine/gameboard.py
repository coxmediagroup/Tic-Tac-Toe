from math import floor
from random import random

# The board for a tic-tac-toe game in this class is defined by a nine character string.
# The mapping for a tic-tac-toe board to this string is very straight forward; starting from
# the top-left and reading left to right, write an x for every X played, an o for every O played,
# and a - for every empty square.
#
# For example, the board:
#
# X - X
# O - -
# 0 - -
# 
# Would be represented as a string as 'x-xo--o--'
#
# Another example:
#
# - - O
# - X X
# X O -
# 
# Would be '--o-xxxo-'

class Board:
	# Checks to see if the game is in a winning state. If so, returns the player that has won.
	# Otherwise, returns None
	def isWinningState(self, board):
		winner = None
		if winner is None:
			winner = self.checkColumns(board)
		if winner is None:
			winner = self.checkRows(board)
		if winner is None:
			winner = self.checkDiagonals(board)
		return winner
		
	# Checks the columns for a winner; return 'x', 'o', or None
	def checkColumns(self, board):
		if board[:1] != "-" and board[:1] == board[3:4] and board[3:4] == board[6:7]:
			return board[:1]
		if board[1:2] != "-" and board[1:2] == board[4:5] and board[4:5] == board[7:8]:
			return board[1:2]
		if board[2:3] != "-" and board[2:3] == board[5:6] and board[5:6] == board[8:]:
			return board[2:3]
		return None
		
	# Checks the rows for a winner; return 'x', 'o', or None
	def checkRows(self, board):
		if board[:1] != "-" and board[:1] == board[1:2] and board[1:2] == board[2:3]:
			return board[:1]
		if board[3:4] != "-" and board[3:4] == board[4:5] and board[4:5] == board[5:6]:
			return board[3:4]
		if board[6:7] != "-" and board[6:7] == board[7:8] and board[7:8] == board[8:]:
			return board[6:7]
		return None
			
	# Checks the diagonals for a winner; return 'x', 'o', or None
	def checkDiagonals(self, board):
		if board[:1] != "-" and board[:1] == board[4:5] and board[4:5] == board[8:]:
			return board[:1]
		if board[2:3] != "-" and board[2:3] == board[4:5] and board[4:5] == board[6:7]:
			return board[2:3]
		return None
		
	# Checks to see if a square is available for a move
	def isValidMove(self, board, index):
		if board[index:index + 1] == '-':
			return True
		return False
		
	# Checks to see if the current state is a "split" condition for the passed player
	# A split condition means that no matter what move the non-passed player makes, the
	# passed player will win in the subsequent move
	def isSplit(self, board, player):
		totalWins = 0
		for i in range(9):
			if self.isValidMove(board, i):
				nextMoveState = board[:i] + player + board[i + 1:]
				if self.isWinningState(nextMoveState) == player:
					totalWins = totalWins + 1
		if totalWins >= 2:
			return True
		return False
	
	# Returns the coords for a winning move for the AI
	def makeWinningMove(self, board):
		for i in range(9):
			if self.isValidMove(board, i):
				nextMoveState = board[:i] + 'o' + board[i + 1:]
				if self.isWinningState(nextMoveState) == 'o':
					x = floor(i / 3)
					y = i % 3
					return str(x) + str(y)
		return None
		
	# Blocks a potential win condition for the player
	def blockNextPlayerMove(self, board):
		for i in range(9):
			if self.isValidMove(board, i):
				nextMoveState = board[:i] + 'x' + board[i + 1:]
				if self.isWinningState(nextMoveState) == 'x':
					x = floor(i / 3)
					y = i % 3
					return str(x) + str(y)
		return None
		
	# Creates a split situation, if possible
	def canSplit(self, board):
		for i in range(9):
			if self.isValidMove(board, i):
				nextMoveState = board[:i] + 'o' + board[i + 1:]
				if self.isSplit(nextMoveState, 'o'):
					x = floor(i / 3)
					y = i % 3
					return str(x) + str(y)
		return None
		
	# Detects if the player can split in the next move
	def playerCanSplit(self, board):
		# first, make sure the player doesn't need to prevent losing the game
		for i in range(9):
			if self.isValidMove(board, i):
				aiNextMove = board[:i] + 'o' + board[i + 1:]
				playerNextMove = board[:i] + 'x' + board[i + 1:]
				# If this spot is a winning spot for the AI, player needs to block
				# But there's still a possibility that blocking also results in a split
				if self.isWinningState(aiNextMove) == 'o' and not self.isSplit(playerNextMove, 'x'):
					return None
		# not in danger of losing; find a viable split
		for i in range(9):
			if self.isValidMove(board, i):
				nextMoveState = board[:i] + 'x' + board[i + 1:]
				if self.isSplit(nextMoveState, 'x'):
					x = floor(i / 3)
					y = i % 3
					return str(x) + str(y)
		return None
	
	# Forces a situation in which the player must block, or else they lose the next turn
	def forceBlock(self, board):
		possibleSolutions = []
		for i in range(9):
			if self.isValidMove(board, i):
				nextMoveState = board[:i] + 'o' + board[i + 1:]
				# If we're capable of making a winning move after this play AND it doesn't allow
				# the player to split while blocking it, add it to our contenders
				if self.makeWinningMove(nextMoveState) is not None and not self.playerCanSplit(nextMoveState):
					possibleSolutions.append(i)
		if len(possibleSolutions) > 0:
			solution = possibleSolutions[floor(random() * len(possibleSolutions))]
			x = floor(solution / 3)
			y = solution % 3
			return str(x) + str(y)
		return None
	
	# If a corner is avaiable, claim it
	# If multiple corners are available, we pick one of them randomly
	def selectCorner(self, board):
		possibleMoves = []
		if board[:1] == '-':
			possibleMoves.append('00')
		if board[2:3] == '-':
			possibleMoves.append('02')
		if board[6:7] == '-':
			possibleMoves.append('20')
		if board[8:] == '-':
			possibleMoves.append('22')
		
		if len(possibleMoves) > 0:
			return possibleMoves[floor(random() * len(possibleMoves))]
			
		return None
			
	# As a last ditch effort, if only sides are available, claim one
	# If multiple sides are available, we pick one of them randomly
	def selectSide(self, board):
		possibleMoves = []
		if board[1:2] == '-':
			possibleMoves.append('01')
		if board[3:4] == '-':
			possibleMoves.append('10')
		if board[5:6] == '-':
			possibleMoves.append('12')
		if board[7:8] == '-':
			possibleMoves.append('21')
				
		if len(possibleMoves) > 0:
			return possibleMoves[floor(random() * len(possibleMoves))]
				
		return None
	
	# Returns the coordinate for the most optimal play, given a board condition
	# Thanks to wikipedia (http://en.wikipedia.org/wiki/Tic_tac_toe#Strategy), we
	# have a basic outline for this optimal play
	def optimalPlay(self, board):
		# Make the winning move
		coords = self.makeWinningMove(board)
		
		# Block a potential winning move
		if coords is None:
			coords = self.blockNextPlayerMove(board)
			if coords is not None:
				coords = coords + " block win"
		
		# If this move results in a split, take it
		if coords is None:
			coords = self.canSplit(board)
			if coords is not None:
				coords = coords + " canSplit"
			
		# Try to get two in a row, forcing the player to block (or getting us to win!)
		if coords is None:
			coords = self.forceBlock(board)
			if coords is not None:
				coords = coords + " forceblock"
			
		# If the center spot is open, take it
		if coords is None and board[4:5] == '-':
			coords = '11 center'
			
		# If a corner is open, take it
		if coords is None:
			coords = self.selectCorner(board)
			if coords is not None:
				coords = coords + " corner"
		
		# If a side if open, take it
		if coords is None:
			coords = self.selectSide(board)
			if coords is not None:
				coords = coords + " side"
			
		return coords