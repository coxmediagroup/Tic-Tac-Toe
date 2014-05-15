'''
	Name: ai.py
	Author: Matthew Reinbold
	Purpose: Series of services for making Tic-Tac-Toe decisions
'''
import json

# define all winning sets
winningSets = [
	[0,1,2],
	[3,4,5],
	[6,7,8],
	[0,3,6],
	[1,4,7],
	[2,5,8],
	[0,4,8],
	[2,4,6],
]

def echoGameState( state ):
	# simply returns a json representation of the passed gamestate
	return json.dumps( state )

def makeRandomMove( state ):
	# given state, make a random move
	# find the available cells
	possibleMoves = getAvailableMoves( state )
	currentMove = randomPicker( possibleMoves )

	state[currentMove] = 'C'

	return json.dumps(state)

def randomPicker( moves ):
	# pick an available move at random
	from random import choice
	currentMove = choice( moves )

	return currentMove	

def getAvailableMoves( state ):
	# using list comprehension
	lMoves = [i for i,x in enumerate(state) if x == '-']

	return lMoves

def checkForPendingWin( gameState, player ):
	# return a -1 if there is not a possible win
	winIndex = -1

	# get list of indexes for the player
	playerMoves = [i for i,x in enumerate(gameState) if x == player]

	# loop through sets
	for set in winningSets:
		itemsFound = []
		#loop through player moves, see if they exist in sets
		for move in playerMoves:
			if move in set:
				itemsFound.append( move )

			if len(itemsFound) == 2:
				# need to find which item needs to be made
				for i in set:
					# not enough to have winning set item, also must be empty
					if i not in itemsFound and gameState[i] == '-':
						winIndex = i
						break 
	return winIndex

def playToWin( state ):
	possibleMoves = getAvailableMoves( state )

	# narrowing initial move is vital for narrowing decision tree
	if len(possibleMoves) == 9:
		# first move; offensively play the edges
		possibleMoves = [0,2,6,8]
		currentMove = randomPicker( possibleMoves )
	elif len(possibleMoves) == 8:
		if 4 not in possibleMoves:
			# opponent has played the center, pursue the edge
			possibleMoves = [0,2,6,8]
			currentMove = randomPicker( possibleMoves )
		else:
			#edge is taken, take center and go on offense
			currentMove = 4
	else:
		# first, see if we can win with another move
		playerPendingWin = checkForPendingWin( state, 'C')

		if playerPendingWin != -1:
			currentMove = playerPendingWin
		else:
			# we can't play move to win, make sure neither can the opponent
			playerPendingWin = checkForPendingWin( state, 'P')
		
			if playerPendingWin == -1:
				# there is no pending win
				if len(possibleMoves) == 6:
					# check if player has been playing the edges, force draw
					cornerCheck = [i for i,x in enumerate(state) if x == 'P' and (i==0 or i==2 or i==6 or i==8)]
					if len(cornerCheck) > 1:
						possibleMoves = [1,3,5,7]
						currentMove = randomPicker( possibleMoves )
						while state[ currentMove ] != '-':
							currentMove = randomPicker( possibleMoves )
					else:
						currentMove = randomPicker( possibleMoves )
				else:
					currentMove = randomPicker( possibleMoves )
			else:
				# there is a pending player win, move to block
				currentMove = playerPendingWin



	state[currentMove] = 'C'

	return json.dumps(state)