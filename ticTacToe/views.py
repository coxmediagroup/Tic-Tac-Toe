from django.http import HttpResponse

def index(request):
	'''Default page'''
	return HttpResponse('Start a new game?')

def newGame(request):
	'''Creates and redirects to new game instance'''
	return HttpResponse('New game created.')

def game(request, gameId):
	'''Loads a game and displays to user'''
	return HttpResponse('not yet defined')

def move(request, gameId, positionX, positionY):
	'''Applies player move to game'''
	return HttpResponse('not yet defined')

