from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse
from ticTacToe.models import Games, Moves

def index(request):
	'''Default page'''
	template = loader.get_template('index.html')
	context = Context({})
	return HttpResponse(template.render(context))

def newGame(request):
	'''Creates and redirects to new game instance'''
	newOne = Games(startTime = datetime.now())
	newOne.save()
	return HttpResponseRedirect(reverse('ticTacToe.views.game',
		args = (newOne.id,)
	))

def game(request, gameId):
	'''Loads a game and displays to user'''
	try:
		currentGame = Games.objects.get(id = gameId)
	except:
		return HttpResponse('There was an error loading game ' + gameId)

	#load game spaces
	gameSpaces = loadGameSpaces(gameId)

	#check game state
	#import pdb; pdb.set_trace()
	winner = checkForWinner(gameSpaces)
	if winner == 'X':
		currentGame.status = 'X Wins'
	elif winner == 'O':
		currentGame.status = 'O Wins'
	elif winner == 'draw':
		currentGame.status = 'The game was a draw'
	else:
		currentGame.status = 'incomplete'
	currentGame.save()

	template = loader.get_template('game.html')
	context = Context({
		'gameId': gameId,
		'status': currentGame.status,
		'gameSpaces': gameSpaces
	})
	return HttpResponse(template.render(context))

def move(request, gameId, xPosition, yPosition, playerMark):
	'''Applies player move to game'''

	#check to see if gameId is valid
	currentGame = Games.objects.filter(id = gameId)
	if currentGame.exists() == False or	currentGame[0].status != 'incomplete':
		return HttpResponse('Invalid game specified')

	#check to make sure position has not already been claimed
	oldMove = Moves.objects.filter(
		game = gameId,
		positionX = xPosition,
		positionY = yPosition
	)
	if oldMove.exists():
		return HttpResponse('That position has already been claimed')

	#add a move record to the table
	newMove = Moves(
		game = currentGame[0],
		player = (playerMark == 'x'),
		positionX = xPosition,
		positionY = yPosition,
		timestamp = datetime.now()
	)
	newMove.save()

	#reload the game page
	return HttpResponseRedirect(reverse('ticTacToe.views.game', args = (gameId,)))

def loadGameSpaces(gameId):
	'''Creates list of game spaces'''

	spaceList = []

	for x in range(0, 3):
		for y in range(0, 3):
			try:
				currentMove = Moves.objects.get(
					game = gameId,
					positionX = x,
					positionY = y
				)

				if currentMove.player:
					mark = 'X'
				else:
					mark = 'O'
			except:
				mark = 'blank'

			newSpace = Space(mark, x, y)
			spaceList.append(newSpace)

		newSpace = Space('newline', 0, 0)
		spaceList.append(newSpace)

	return spaceList

def checkForWinner(gameSpaces):
	'''Checks game state for a winner'''

	lineCombos = [
		[0, 1, 2],
		[4, 5, 6],
		[8, 9, 10],
		[0, 4, 8],
		[1, 5, 9],
		[2, 6, 10],
		[0, 5, 10],
		[2, 5, 8]
	]

	#check for a winning line
	for combo in lineCombos:
		if gameSpaces[combo[0]].mark == gameSpaces[combo[1]].mark == gameSpaces[combo[2]].mark:
			mark = gameSpaces[combo[0]].mark
			if mark != 'blank':
				return mark

	#check for a draw
	draw = True
	for space in gameSpaces:
		if space.mark == 'blank':
			draw = False
	if draw:
		return 'draw'
	else:
		return 'incomplete'

class Space:
	'''Represents a space on the game board'''

	def __init__(self, markType, xValue, yValue):
		self.x = xValue
		self.y = yValue
		self.mark = markType

