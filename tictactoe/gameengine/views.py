from math import floor
from random import random

from django.http import HttpResponse

from gameengine.gameboard import Board

def index(request):
	b = Board()
	boardState = request.GET["state"]
	return HttpResponse(b.optimalPlay(boardState))