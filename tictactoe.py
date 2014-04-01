#!/opt/python-2.7/bin/python2.7
#  (Change the #! line above as needed.  I used Python 2.7 for this code sample.)

#  Python implementation on 3/31/14 by Josh "Nodoka" Johnson.
#  "WarGames" (c) Warner Bros. Pictures

#  For screen-clearing functionality:
import os 
if (os.name == "nt"):	cls = "cls"
else:	cls = "clear"

#  Check other squares in a line for matching symbols.
#  Rather than create a formula for deciding what other squares, I found it easier to verbosely list them.
toCheck = {1: [[2, 3], [4, 7], [5, 9]],
	2: [[1, 3], [5, 8]],
	3: [[1, 2], [6, 9], [5, 7]],
	4: [[5, 6], [1, 7]],
	5: [[4, 6], [2, 8], [1, 9], [3, 7]],
	6: [[4, 5], [3, 9]],
	7: [[1, 4], [8, 9], [3, 5]],
	8: [[2, 5], [7, 9]],
	9: [[7, 8], [3, 6], [1, 5]]}

#  Formatting variables:
tab = " " * 34
blank = "   |   |"
cross = "---+---+---"

#  Empty board, equivalent to:
#  
#   1 | 2 | 3
#  ---+---+---
#   4 | 5 | 6
#  ---+---+---
#   7 | 8 | 9
#
plies = "123456789"

#  Game-related variables:
turn = 1
gameOver = False

#  Check to see if a player has won the game.
#  The board string $plies is labeled 1 ~ 9, but the string itself is 0-indexed.
def hasWon(data):
	if ((data[0] == data[1] == data[2]) or			# Top row
		(data[0] == data[3] == data[6])):			# First column
		return (data[0])
	elif ((data[6] == data[7] == data[8]) or 		# Bottom row
		(data[2] == data[5] == data[8])):			# Third column
		return (data[8])
	elif ((data[0] == data[4] == data[8]) or		# \ Diagonal
		(data[1] == data[4] == data[7]) or			# Middle column
		(data[3] == data[4] == data[5]) or			# Middle row
		(data[2] == data[4] == data[6])):			# / Diagonal
		return (data[4])
	else:	return False

#  Adjust the board with the move made by the player.
def makeMove(board, play, piece):
	return board.replace(str(play), piece)

#  Check the legality of a play, making sure that no X or O is already occupying the desired space.
def isLegal(board, move):
	return (board[move - 1] not in [C, H])

#  Compare the weighted play with the best weighted play so far.
#  If the play (first part of each duet) is the same, add one to the weight.
#  This will favor plays with multiplie next-move-wins possibilities.
def ifBetter(move1, move2):
	if ((move2 == move1) and (move1[1] == 1)):
		return (move1[0], move1[1] + 1)
	if (move2[1] > move1[1]):	return move2
	else:	return move1

#  Make the best move for the computer player.
#  Different weights are given to the types of best moves:
#    Ten (10) points for a winning move;
#    Five (5) for a block, preventing the human player from winning;
#    One (1) for a "next-move-wins" move, putting two X's in the same line (row, column, diagonal).;
#    Zero (0) for any other move.
def makeBestMove(board):
	best = [5, 0]
	for focus in range(1, 10):
		for check in toCheck[focus]:
			# Test for win
			if ((board[check[0] - 1] == board[check[1] - 1] == C) and isLegal(board, focus)):
				best = ifBetter(best, [focus, 10])
			# Test for block
			if ((board[check[0] - 1] == board[check[1] - 1] == H) and isLegal(board, focus)):
				best = ifBetter(best, [focus, 5])
			# Test for next-move wins
			if ((isLegal(board, check[0]) and board[check[1] - 1] == C) or
				(isLegal(board, check[1]) and board[check[0] - 1] == C) and isLegal(board, focus)):
				best = ifBetter(best, [focus, 1])
			# Fallback
			best = ifBetter(best, [focus, 0])
	return makeMove(board, best[0], C)

#  Set up a new game.
#  Originally, it defaulted to Player 1 (X) as Computer and Player 2 (O) as human.
#  This makes it interactive.
try:	os.system(cls)
except OSError:	pass
print "WELCOME TO TIC-TAC-TOE!\n"

#  Check for valid data.  This is used to ameliorate user error.
valid = False
while (not valid):
	try:
		first = raw_input("Would you like to be first (Y/N)?  ")
		valid = first in ["y", "Y", "n", "N"]
		if (not valid):	print "\tPlease enter either 'y' or 'n'.\n"
	except ValueError:	pass
valid = False
while (not valid):
	try:
		xo = raw_input("X or O?  ")
		valid = xo in ["X", "x", "O", "o"]
		if (not valid):	print "\tPlease enter either 'X' or 'O'.\n"
	except ValueError:	pass

#  Assign the computer its turn parity (odds or evens):
if (first in ["n", "N"]):	cturn = 1
else:	cturn = 0

#  Assign X's and O's:
if (xo in ["X", "x"]):
	C = "O"
	H = "X"
else:
	C = "X"
	H = "O"

#  MAIN PROGRAM LOOP
#  Make plays until the winner has been determined, or the game ends in a tie.
while (not gameOver):
	gameOver = hasWon(plies)

	#  Platform-dependant screen clear:
	try:	os.system(cls)
	except OSError:	pass
	print "\n"
	print "TIC-TAC-TOE".center(80)
	print "by Josh Johnson".center(80)
	print "-" * 80
	#  Display the board:
	for x in range(3):
		print tab + blank
		print tab + " %s | %s | %s" % (plies[3 * x], plies[3 * x + 1], plies[3 * x + 2])
		print tab + blank
		if (x < 2):	print tab + cross
	print " " * 80
	
	#  Depending on whether the game has been won, print a message or prompt the player for his/her
	#    next move.
	if (gameOver == C):
		print "I'm sorry, but the computer was the victor.  Better luck next time."
	elif (gameOver == H):
		print "Congratulations, you bested the computer!  You would make Dr. Falken proud."
	elif (turn == 10):		#  After 9 moves, the game is a tie.
		print "It was a tie.  The only way to win is not to play."
		gameOver = True		#  Set this to True, so that the outer WHILE loop is exited.
	else:
		#  The computer plays on odd-numbered, the human, even-numbered, plays.
		if (turn % 2 == cturn):
			plies = makeBestMove(plies)
		else:
			valid = False
			while (not valid):
				print "PLAY #" + str(turn)
				
				#  Allow only legal and valid plays:
				try:	play = int(raw_input("Your move?  "))
				except ValueError:	pass
				if (play in range(1, 10)):
					if (isLegal(plies, play)):	valid = True
				if (not valid):	print "Please choose an empty square from 1 through 9."
			
			#  Change the board for either the computer or human play, whichever was made this turn.
			plies = makeMove(plies, play, H)
		turn += 1

#  Salutation:
print "\nThank you for playing Tic-Tac-Toe with me!"
