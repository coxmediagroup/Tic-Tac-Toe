#!/opt/python-2.7/bin/python2.7

#	Original game by....who knows.
#	Python implementation on 3/28/14 by Josh "Nodoka" Johnson.
#	"WarGames" (c) Warner Bros. Pictures

toCheck = {1: [[2, 3], [4, 7], [5, 9]],
	2: [[1, 3], [5, 8]],
	3: [[1, 2], [6, 9], [5, 7]],
	4: [[5, 6], [1, 7]],
	5: [[4, 6], [2, 8], [1, 9], [3, 7]],
	6: [[4, 5], [3, 9]],
	7: [[1, 4], [8, 9], [3, 5]],
	8: [[2, 5], [7, 9]],
	9: [[7, 8], [3, 6], [1, 5]]}
tab = " " * 34
blank = "   |   |"
cross = "---+---+---"
plies = "123456789"
turn = 1
gameOver = False

def hasWon(data):
	if ((data[0] == data[1] == data[2]) or
		(data[0] == data[3] == data[6])):
		return (data[0])
	elif ((data[6] == data[7] == data[8]) or
		(data[2] == data[5] == data[8])):
		return (data[8])
	elif ((data[0] == data[4] == data[8]) or
		(data[1] == data[4] == data[7]) or
		(data[3] == data[4] == data[5]) or
		(data[2] == data[4] == data[6])):
		return (data[4])
	else:	return False

def makeMove(board, play, piece):
	return board.replace(str(play), piece)

def isLegal(board, move):
	return (board[move - 1] not in ["X", "O"])

def ifBetter(move1, move2):
	print "Testing %s vs. %s." % (move1, move2)
	if ((move2 == move1) and (move1[1] == 1)):
		return (move1[0], move1[1] + 1)
	if (move2[1] > move1[1]):	return move2
	else:	return move1

def makeBestMove(board):
	best = [5, 0]
	for focus in range(1, 10):
		for check in toCheck[focus]:
			# Test for win
			if ((board[check[0] - 1] == board[check[1] - 1] == "X") and isLegal(board, focus)):
				best = ifBetter(best, [focus, 10])
			# Test for block
			if ((board[check[0] - 1] == board[check[1] - 1] == "O") and isLegal(board, focus)):
				best = ifBetter(best, [focus, 5])
			# Test for next-move wins (accumulate scores)
			if ((isLegal(board, check[0]) and board[check[1] - 1] == "X") or
				(isLegal(board, check[1]) and board[check[0] - 1] == "X") and isLegal(board, focus)):
				best = ifBetter(best, [focus, 1])
			# Fallback
			best = ifBetter(best, [focus, 0])
	return makeMove(board, best[0], "X")

while (not gameOver):
	gameOver = hasWon(plies)
	print "\n"
	print "TIC-TAC-TOE".center(80)
	print "by Josh Johnson".center(80)
	print "-" * 80
	for x in range(3):
		print tab + blank
		print tab + " %s | %s | %s" % (plies[3 * x], plies[3 * x + 1], plies[3 * x + 2])
		print tab + blank
		if (x < 2):	print tab + cross
	print " " * 80
	if (gameOver == "X"):
		print "I'm sorry, but the computer was the victor.  Better luck next time."
	elif (gameOver == "O"):
		print "Congratulations, you bested the computer!  You would make Dr. Falken proud."
	elif (turn == 10):
		print "It was a tie.  The only way to win is not to play."
		gameOver = True
	else:
		if (turn % 2 == 1):
			plies = makeBestMove(plies)
		else:
			valid = False
			while (not valid):
				print "PLAY #" + str(turn)
				try:	play = int(raw_input("Your move?  "))
				except ValueError:	pass
				if (play in range(1, 10)):
					if (isLegal(plies, play)):	valid = True
				if (not valid):	print "Please choose an empty square from 1 through 9."
			plies = makeMove(plies, play, "O")
		turn += 1
print "\nThank you for playing Tic-Tac-Toe with me!"
