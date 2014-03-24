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
	playersMove = raw_input("Player, please enter your move:")
	validMove = checkPlayerInput(playersMove , validMoves)
	while validMove == False:
		print "Invalid move, the following are valid entries: ", validMoves
		playersMove = raw_input("Player, please enter your move:")
		validMove = checkPlayerInput(playersMove , validMoves)
		
	##if we make it to here, the move is valid, update the gameboard.
	gameBoard.update_board_data(playersMove , "X" )
	gameBoard.draw_board()

##This method handles the computer's move
def cpuMove(gameBoard):	
##Overview of cpu move logic
##Check if the computer can win, if so move to spot needed
	canComputerWin = gameBoard.is_game_winnable("O")
##Check if player can win, if so block players winning move
	canPlayerWin = gameBoard.is_game_winnable("X")
	if canComputerWin != False:
		print "winning"
		gameBoard.update_board_data(canComputerWin, "O")
		gameBoard.draw_board()
	elif canPlayerWin != False:
		print "about to lose"
		gameBoard.update_board_data(canPlayerWin, "O")
		gameBoard.draw_board()
	elif gameBoard.board_data[4] != "X" and gameBoard.board_data[4] != "O": ##If nothing else select a spot based on value
		##The center (5) is the highest valued spot
		print "Why am I here"
		gameBoard.update_board_data("5", "O")
		gameBoard.draw_board()
##The corners (1, 3, 7, 9) are the next highest valued spot
	elif len(gameBoard.get_open_corners()) != 0:
		print "Corner Check"
		gameBoard.update_board_data(gameBoard.get_corner_move(), "O")
		gameBoard.draw_board()
	else:
		print "Something is wrong"
		return 0
		
##If all of these are taken, move to an empty space on one of the sides (2, 4, 6, 8)	

	
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
gameBoard.draw_board()


##if the first move is the player get their move then we can start regular play
##if the first move is the computer determine the best move then start regular play
if firstMove == "you":
	winner = False
	while winner == False:
		##check for a winner
		winner = gameBoard.check_for_winner()
		##TODO check for a tie
		if winner == "player wins":
			print "Congratulations, you win!"
			winner = True
		elif winner == "computer wins":
			print "Sorry, you lost, better luck next time."
			winner = True
		else:
			getPlayersMove(gameBoard)
			cpuMove(gameBoard)
else:
	winner = False
	while winner == False:
		##check for a winner
		winner = gameBoard.check_for_winner()
		##TODO check for a tie
		if winner == "player wins":
			print "Congratulations, you win!"
			winner = True
		elif winner == "computer wins":
			print "Sorry, you lost, better luck next time."
			winner = True
		elif gameBoard.check_for_ties() == 0:
			print "Looks like we have a tie, great game!"
			winner = True
		else:
			cpuMove(gameBoard)
			getPlayersMove(gameBoard)
	





