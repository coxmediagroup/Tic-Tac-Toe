from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

from tictactoe.models import Board

def game_view(request):
	""" Renders the Game Board """

	# Get or Create a new Game Board
	board_id = request.session.get('board_id', None)
	if board_id:
		print "Getting current board"
		board = Board.objects.get(id=board_id)
	else:
		print "Creating a new Board"
		board = Board.objects.create()
		request.session['board_id'] = board.id
		messages.success(request, 'Started a New Game')

	return render(request, 'app.html', { 'board': board })

def select_piece(request):
	"""
	Accepts a Piece Selection from a User, executes the Computer Player's next 
	move, and redirects the User back to the `game_view`.
	"""

	# Get and Print the User's Piece Selection
	if 'selection' in request.POST:
		selection = request.POST['selection']
		print selection
		messages.success(request, 'Started a New Game')

def end_game(request):
	""" Ends the current game and redirects the User to play a new Game. """

	board_id = request.session.get('board_id', None)
	if board_id:
		request.session.pop('board_id')
		board = Board.objects.get(id=board_id)
		board.delete()
		messages.success(request, 'Game ended successfully.')

	# Redirect the User to play the Game.
	return redirect('home')
