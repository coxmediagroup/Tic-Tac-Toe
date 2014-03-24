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

##This method handles the computer's move
##def cpuMove(gameBoard):	
##Overview of cpu move logic
##Check if the computer can win, if so move to spot needed
##Check if player can win, if so block players winning move
##If nothing else select a spot based on value
##The center (5) is the highest valued spot
##The corners (1, 3, 7, 9) are the next highest valued spot
##If all of these are taken, move to an empty space on one of the sides (2, 4, 6,8)


gameBoard= GameBoard()

print "Let's play a game of tic-tac-toe"
firstMove = getFirstMove()
print "We randomly chose who gets to go first, and %s goes first" % firstMove


##if the first move is the player get their move then we can start regular play
##if the first move is the computer determine the best move then start regular play
if firstMove == "you":
	winner = False
	while gameBoard.count_board_moves_left() > 0 and (winner != "player wins" or winner != "computer wins"):
		##check for a winner
		winner = gameBoard.check_for_winner()
		getPlayersMove(gameBoard)
else:
	winner = False
	while gameBoard.count_board_moves_left() > 0 and (winner != "player wins" or winner != "computer wins"):
		winner = gameBoard.check_for_winner()
		getPlayersMove(gameBoard)
	





