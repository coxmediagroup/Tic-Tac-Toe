#	Tic Tac Toe
#	Danny Burrows
#
#	Implement a version of tic-tac-toe where a player plays against an AI bot where the AI never loses.

# possible wins:
#	x, x + 1, x + 2 | y = i (0 to 2)
#	y, y + 1, y + 2 | x = i (0 to 2)
#	z, z+1, z+2 | z = (x, y)
#	z, z-1, z-2 | z = (x, y) from x=2,y=0

def checkWin(board):
	# check wins on board	
	for i in range(3):
		# check rows
		if (board[i][0] == board[i][1] and board[i][1] == board[i][2]):
			return True
		# check columns
		elif (board[0][i] == board[1][i] and board[1][i] == board[2][i]):
			return True
		# check both cross conditions
		elif (board[0][0] == board[1][1] and board[1][1] == board[2][2]):
			return True
		elif (board[2][0] == board[1][1] and board[1][1] == board[0][2]):
			return True
	return False


#	draw board
board = [ [0,1,2],[3,4,5],[6,7,8] ]

print "%s | %s | %s" % (board[0][0], board[0][1], board[0][2])
print "--+---+--"
print "%s | %s | %s" % (board[1][0], board[1][1], board[1][2])
print "--+---+--"
print "%s | %s | %s" % (board[2][0], board[2][1], board[2][2])

print checkWin(board)

#	get user move
#	-test valid user move
#	-mark move

#	computer move
#	-find best move
#	-mark move

#	again?
