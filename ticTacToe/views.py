from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse
from ticTacToe.models import Games

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
	#check to see if gameId is valid? ...maybe also check to see if still going here too
	#check to make sure position has not already been claimed
	#add a move record to the table
	#reload the game page
	return HttpResponse('received x: ' + xPosition + ', y: ' + yPosition)

