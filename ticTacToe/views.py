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
	g = Games(startTime = datetime.now())
	g.save()
	return HttpResponseRedirect(reverse('ticTacToe.views.game', args = (g.id,)))

def game(request, gameId):
	'''Loads a game and displays to user'''
	try:
		g = Games.objects.get(id = gameId)
	except:
		return HttpResponse('There was an error loading game ' + gameId)

	template = loader.get_template('game.html')
	context = Context({
		'gameId': gameId,
		'status': g.status
	})
	return HttpResponse(template.render(context))

def move(request, gameId, xPosition, yPosition):
	'''Applies player move to game'''

	#check to see if gameId is valid
	currentGame = Games.objects.filter(id = gameId)
	if currentGame.exists() == False or	currentGame[0].status != 'incomplete':
		return HttpResponse('Invalid game specified')

	#check to make sure position has not already been claimed
	oldMove = Moves.objects.filter(game = gameId,
		positionX = xPosition,
		positionY = yPosition
	)
	if oldMove.exists():
		return HttpResponse('That position has already been claimed')

	#add a move record to the table
	newMove = Moves(game = currentGame[0],
		positionX = xPosition,
		positionY = yPosition,
		timestamp = datetime.now()
	)
	newMove.save()

	#reload the game page
	return HttpResponseRedirect(reverse('ticTacToe.views.game', args = (gameId,)))

