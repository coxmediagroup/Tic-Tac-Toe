import random
import GameBoard
from GameBoard import *

##Randomly determines who goes first
def getFirstMove():
	if ( random.randint(1 , 2) == 1 ):
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

	if ( canComputerWin != False ):
		gameBoard.update_board_data(canComputerWin, "O")
		gameBoard.draw_board()
	elif ( canPlayerWin != False ):
		gameBoard.update_board_data(canPlayerWin, "O")
		gameBoard.draw_board()
	elif ( len(gameBoard.get_open_corners()) != 0 ):
		##The corners (1, 3, 7, 9) are the highest valued spot
		gameBoard.update_board_data(gameBoard.get_move("corner"), "O")
		gameBoard.draw_board()
	elif ( gameBoard.board_data[4] != "X" and gameBoard.board_data[4] != "O" ): 
		##The center (5) is the highest valued spot
		gameBoard.update_board_data("5", "O")
		gameBoard.draw_board()
	else:
		##If all of these are taken, move to an empty space on one of the sides (2, 4, 6, 8)	
		##This wont happen very often, but is needed when only a side is left and noone can win ---> leads to a tie
		gameBoard.update_board_data(gameBoard.get_move("side"), "O")
		gameBoard.draw_board()

##Validates player input
##validMoves contains a list of moves that are open	
def checkPlayerInput(playersMove, validMoves):
	valid = False
	for entry in validMoves:
		if ( playersMove == entry ):
			valid = True
	return valid

##Prints the winner of the game or a tie
##The player should never win, either the computer will win or the game will end in a tie.
def printWinner(winner):
	if ( winner == "player wins" ):
		print "Congratulations, you win!"
	elif ( winner == "computer wins" ):
		print "Sorry, you lost, better luck next time."
		print "\n" + "\n"
	else:
		print "Looks like we have a tie, great game!"
		print "\n" + "\n"
	
##Handles the start of the game
##firstPlayer is randomly determined	
def playGame():
	gameBoard= GameBoard()
	firstMove = getFirstMove()
	print "\n" + "\n"
	print "Let's play a game of tic-tac-toe"
	print "We randomly chose who gets to go first, and %s goes first" % firstMove
	##if the first move is the player get their move then we can start regular play
	##if the first move is the computer determine the best move then start regular play
	
	##Winner is used to keep track of win/lose/tie
	winner = False
	if firstMove == "you":
		while winner == False:
			##check for a winner
			game_over = gameBoard.check_for_winner()
			
			if ( game_over != False ):
				##Print the winner out
				printWinner(game_over)
				winner = True
			else:
				##We need to make sure the game isnt over before any more is made
				if ( gameBoard.check_for_winner() == False ):
					gameBoard.draw_board()
					getPlayersMove(gameBoard)
				if ( gameBoard.check_for_winner() == False ):
					cpuMove(gameBoard)
	else:
		while winner == False:
			##check for a winner
			game_over = gameBoard.check_for_winner()
			
			##TODO check for a tie
			if game_over == "player wins":
				##Print the winner out
				printWinner(game_over)
				winner = True
			else:
				##We need to make sure the game isnt over before any more is made
				if ( gameBoard.check_for_winner() == False ):
					cpuMove(gameBoard)
				if ( gameBoard.check_for_winner() == False ):
					getPlayersMove(gameBoard)
	
##Call playGame to start the game
playGame()