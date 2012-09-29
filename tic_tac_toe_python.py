__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'
__date__ = '09/26/2012'
__project__ = 'Tic_Tac_Toe Test for Coxmedia'

import random

def drawboard():
	print
	print " %s| %s| %s" % (board[0], board[1], board[2])
	print "__|__|__"
	print " %s| %s| %s" % (board[3], board[4], board[5])
	print "__|__|__"
	print " %s| %s| %s" % (board[6], board[7], board[8])
	print
	return


def iswinner(test):
	if board[0] == test and board[1] == test and board[2] == test:
		return True
	if board[3] == test and board[4] == test and board[5] == test:
		return True
	if board[6] == test and board[7] == test and board[8] == test:
		return True
	if board[0] == test and board[3] == test and board[6] == test:
		return True
	if board[1] == test and board[4] == test and board[7] == test:
		return True
	if board[2] == test and board[5] == test and board[8] == test:
		return True
	if board[0] == test and board[4] == test and board[8] == test:
		return True
	if board[6] == test and board[4] == test and board[2] == test:
		return True
	return False


game = 0
random.seed()
while (game == 0):
	board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
	print "Tic-Tac-Toe (game for CoxMedia test)"
	print
	print "Greetings Professor Falken."
	print
	shell_interface = raw_input("Shall we play a game?")
	if shell_interface.lower() == "let's play global thermonuclear war":
		no_nukes = raw_input("wouldn't you prefer a nice game of Tic-Tac-Toe?")
		if no_nukes.lower() == "no":
			print
			print "You do not have access to that game."
			print
		else:
			print
			print "We will play Tic-Tac-Toe."
			print
	else:
		print
		print "We shall play Tic-Tac-Toe."
		print
	print
	player1 = raw_input("What is your name? ")
	player2 = raw_input("What is your opponents name? (Hint: Type 'joshua' to play the computer) ")
	movesplayed = 0
	playersturn = 1
	gamewon = False
	while (movesplayed < 9):
		drawboard()
		if playersturn == 1:
			nextmove = raw_input("Your Move %s ? " % (player1))
			if board[(int(nextmove) - 1)] == nextmove:
				board[(int(nextmove) - 1)] = "X"
				if iswinner("X"):
					gamewon = True
					winner = player1
					break
				playersturn = 0
				movesplayed = movesplayed + 1
			else:
				print "You have chosen an invalid move."
		else:
			if player2.lower() == "joshua":
				nextmove = str(random.randrange(1, 9))
				print "Joshua's move was %s " % (nextmove)
			else:
				nextmove = raw_input("Your Move %s ? " % (player2))
			if board[(int(nextmove) - 1)] == nextmove:
				board[(int(nextmove) - 1)] = "0"
				if iswinner("0"):
					gamewon = True
					winner = player2
					break
				playersturn = 1
				movesplayed = movesplayed + 1
			else:
				print "You have chosen an invalid move."
	if gamewon:
		print
		print "Congratulation %s you won this game" % winner
		print
else:
	print "The game between %s and %s has no winner" % (player1, player2)
	print
	print "Strange Game."
	print
	print "The only winning move is not to play."
	print
print

if  raw_input("Play again? ( Y or N) ").lower() == 'n':
	game = 1

print "End of line."