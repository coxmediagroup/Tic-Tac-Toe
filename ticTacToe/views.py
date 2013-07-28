from django.http import HttpResponse
from django.template import Context, loader

def index(request):
	'''Default page'''
	t = loader.get_template('index.html')
	c = Context({})
	return HttpResponse(t.render(c))

def newGame(request):
	'''Creates and redirects to new game instance'''
	return HttpResponse('New game created.')

def game(request, gameId):
	'''Loads a game and displays to user'''
	t = loader.get_template('game.html')
	c = Context({
		'gameId': gameId
	})
	return HttpResponse(t.render(c))

def move(request, gameId, positionX, positionY):
	'''Applies player move to game'''
	return HttpResponse('not yet defined')

