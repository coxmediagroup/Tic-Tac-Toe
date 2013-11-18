from django.shortcuts import render_to_response

from tictactoe.models import Board

def game_view(request):
	"""
	This View is responsible for providing the HTML5 code along with
	instantiating or loading a Game Board for the current browser session.
	"""

	# Get or Create a new Game Board
	board_id = request.session.get('board_id')
	if board_id:
		print "Getting current board"
		board = Board.objects.get(id=board_id)
	else:
		print "Creating a new Board"
		board = Board.objects.create()
		request.session['board_id'] = board.id

	return render_to_response('app.html', { 'board': board })