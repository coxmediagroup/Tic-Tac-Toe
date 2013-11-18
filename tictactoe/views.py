from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

from tictactoe.models import Board

def game_view(request):
	""" Renders the Game Board """

	# Get or Create a new Game Board
	board_id = request.session.get('board_id', None)
	if board_id:
		board = Board.objects.get(id=board_id)
	else:
		board = Board.objects.create()
		request.session['board_id'] = board.id
		messages.success(request, 'Started a New Game. Your turn!')

	# Check for Victory
	if board.victory_status() == -1:
		messages.warning(request, 'The Computer has won the Game')
	elif board.victory_status() == 1:
		messages.success(request, 'You have miraculously won the Game!')

	return render(request, 'app.html', { 'board': board })

def select_piece(request):
	"""
	Accepts a Piece Selection from a User, executes the Computer Player's next 
	move, and redirects the User back to the `game_view`.
	"""

	# Get or Create a new Game Board
	board_id = request.session.get('board_id', None)
	if board_id:
		board = Board.objects.get(id=board_id)
	else:
		board = Board.objects.create()
		request.session['board_id'] = board.id
		messages.success(request, 'Started a New Game. Your Turn!')

	# Check for Victory
	if board.victory_status() == -1:
		messages.warning(request, 'The Computer has won the Game')
		return redirect('home')
	elif board.victory_status() == 1:
		return redirect('home')

	# Set the User's Selection
	if request.method == 'POST':
		if 'selection' in request.POST:
			selection = request.POST['selection']
			if getattr(board, selection) == 0:
				piece = setattr(board, selection, 1)
				board.save()
			else:
				messages.warning(request, "Cannot place a Game Piece here")

	return redirect('home')

def end_game(request):
	""" Ends the current game and redirects the User to play a new Game. """

	# Get and delete the current Game Board if it exists.
	board_id = request.session.get('board_id', None)
	if board_id:
		request.session.pop('board_id')
		board = Board.objects.get(id=board_id)
		board.delete()

	# Redirect the User to play the Game.
	return redirect('home')
