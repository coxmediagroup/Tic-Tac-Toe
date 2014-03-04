from django.http import HttpResponse

# Admittedly, defining the board class here in the view MAY NOT go along with
# best Django design practices; however, considering I sat down to learn
# Django to fufill this challenge and my experience with it is non-existant,
# I'll be happy to understand better practices in the future
#
# Represents a class for the tic tac toe board, and also contains the AI to solve
# the game
class Board:
	def hello(self):
		return "12"

def index(request):
	b = Board()
	return HttpResponse(b.hello())