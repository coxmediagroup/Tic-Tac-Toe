import random
import GameBoard
from GameBoard import *

def getFirstMove():
	if (random.randint(1,2) == 1):
		return "you"
	else:
		return "the computer"
		
##gets the players input and handles validation of the input
def getPlayersMove(game_board):
	##while the input is not the numbers 1-9 we let the user know their input is not correct
	validMoves = getValidMoves(game_board.get_board_data())
	playersMove = raw_input("Player, please enter your move:")
	validMove = checkPlayerInput(playersMove , validMoves)
	while validMove == False:
		print "Invalid move, the following are valid entries: ", validMoves
		playersMove = raw_input("Player, please enter your move:")
		validMove = checkPlayerInput(playersMove , validMoves)

def getValidMoves(board_data):
	valid_spaces = []
	for entry in board_data:
		if entry != "X" or entry !="O":
			valid_spaces.append(entry)
	return valid_spaces
	
def checkPlayerInput(playersMove, validMoves):
	valid = False
	for entry in validMoves:
		if playersMove == entry:
			valid = True
	return valid
	

gameBoard= GameBoard()

print "Let's play a game of tic-tac-toe"
firstMove = getFirstMove()
print "We randomly chose who gets to go first, and %s goes first" % firstMove

##if the first move is the player get their move then we can start regular play
##if the first move is the computer determine the best move then start regular play
if firstMove == "you":
	getPlayersMove(gameBoard)
else:
	getPlayersMove(gameBoard)
	





