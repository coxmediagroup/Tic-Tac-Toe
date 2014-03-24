import random
import GameBoard
from GameBoard import *

def getFirstMove():
	if (random.randint(1 , 2) == 1):
		return "you"
	else:
		return "the computer"
		
##gets the players input and handles validation of the input
def getPlayersMove(gameBoard):
	validMoves = gameBoard.get_board_moves_left()
	gameBoard.draw_board()
	playersMove = raw_input("Player, please enter your move:")
	validMove = checkPlayerInput(playersMove , validMoves)
	while validMove == False:
		print "Invalid move, the following are valid entries: ", validMoves
		playersMove = raw_input("Player, please enter your move:")
		validMove = checkPlayerInput(playersMove , validMoves)
		
	##if we make it to here, the move is valid, update the gameboard.
	gameBoard.update_board_data(playersMove , "X" )
	gameBoard.draw_board()
	

	
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
	





