from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import random

EMPTY_CELL = 0
PLAYER1_CELL = 1
PLAYER2_CELL = 2

def home(request):
	'The site home page'
	context = {'name':request.session.get("playerName", ""), 'first':("on" if request.session.get("playerFirst") else "") }
	request.session['start'] = True
	return render(request, 'home.html', context)

def reset(request):
	'Kill the session and start over'
	request.session.flush()
	request.session.clear()
	request.session.delete()
	return redirect("home")

def play(request):
	'Play the game'

	request.session['playerName'] = request.GET.get('player-name', request.session.get('playerName', ""))
	first = request.session['playerFirst'] = request.GET.get('player-first', request.session.get('playerFirst', "on"))

	human_data    = PLAYER1_CELL if first else PLAYER2_CELL
	computer_data = PLAYER2_CELL if first else PLAYER1_CELL

	# board cells are numbered 1 - 9 in the logic 
	request.session['tictactoe'] = {
		"data": [
			# board layout in array
			0,0,0,
			0,0,0,
			0,0,0],
		"moves": []}

	context = {
		'name':          request.session.get("playerName"), 
		'first':         "on" if first else "",
		'human_data':    PLAYER1_CELL if first else PLAYER2_CELL,
		'computer_data': PLAYER2_CELL if first else PLAYER1_CELL
	}

	if not first:
		move = _computer_first_move(request.session['tictactoe'], computer_data)

		request.session['tictactoe']['data'][move-1] = computer_data
		request.session['tictactoe']['moves'].append(move)
		context['move'] = move

	request.session['start'] = True
	return render(request, 'play.html', context)

def move(request):
	resp_data = {}

	data  = request.session['tictactoe']
	cell  = int(request.GET.get('cell'))
	first = request.session.get('playerFirst')

	human_data    = PLAYER1_CELL if first else PLAYER2_CELL
	computer_data = PLAYER2_CELL if first else PLAYER1_CELL

	if cell > 0 and cell <= len(data['data']):
		if data['data'][cell -1]:
			resp_data['error'] = {
				message: "Server out of synch and thinks that cell is in use.",
				critical: True}
		else:
			data['data'][cell -1] = human_data
			data['moves'].append(cell)

			player = _get_move_won(data)
			if player is not None:
				print "player %s won %s" % (player, human_data)
				resp_data['status'] = "human win" if player == human_data else "computer win"
			else:
				if not first:
					move = _computer_first_move(data, computer_data)
				else:
					move = _human_first_move(data, computer_data)

				print "got move "+str(move)

				# for i in range(0, 9):
				# 	if data[i] == 0:
				if move is not None:
					data['data'][move-1] = computer_data
					data['moves'].append(move)
					resp_data['move'] = {'cell': move}

				player = _get_move_won(data)
				if player is not None:
					resp_data['status'] = "human win" if player == human_data else "computer win"
				else:
					found = False
					for j in range(0, 9):
						if data['data'][j] == 0:
							found = True

					if not found:
						resp_data['status'] = "cat win"
						print data

	request.session['tictactoe'] = data

	return HttpResponse(json.dumps(resp_data), content_type="application/json")

def _computer_first_move(data, computer_data):
	moveName = ""

	for move in data['moves']:
		moveName += str(move)

	if moveName is "":
		moveName = "-"

	# cells already taken in play
	taken = []
	for i in range(0, 9):
		if data['data'][i] is not 0:
			taken.append(i+1)

	# TODO : Look for blocks
	move = _get_move_win(data, computer_data)
	if move:
		return move

	# TODO : Look for wins
	move = _get_move_block(data, computer_data)
	if move:
		return move

	# With no blocks or immediate wins, try a good move toward a win

	print moveName
	print taken

	bestMoves = {
		# start
		"-": [5,1,3,7,9],

		# center -> corner
		"51": [9],
		"53": [7],
		"57": [3],
		"59": [1],

		"519": [7,3],
		"537": [1,9],
		"573": [1,9],
		"591": [7,3],

		# center -> edge
		"52": [7,9],
		"54": [3,9],
		"56": [1,7],
		"58": [1,3],

		# 5273  [9]
		# 527x  [3]
		# 5291  [7]
		# 529x  [1]

		# corner -> center
		"15": [9],
		"35": [7],
		"75": [3],
		"95": [1],

		"159": [3,7],
		"357": [1,9],
		"753": [1,9],
		"951": [3,7],

		# corner -> edge / corner
		"12": [7,9],
		"13": [7,9],
		"14": [3,9],
		"17": [3,9],
		"16": [3,7,9], # ? too loose
		"18": [3,7,9], # ? too loose
		"19": [3,7],

		"31": [7,9],
		"32": [7,9],
		"34": [1,7,9], # ?
		"36": [1,7],
		"37": [1,9],
		"38": [1,7,9], # ?
		"39": [1,7],

		"71": [3,9],
		"72": [1,3,9], # ?
		"73": [1,9],
		"74": [3,9],
		"76": [1,3,9], # ?
		"78": [1,3],
		"79": [1,3],

		"91": [3,7],
		"92": [1,3,9], # ?
		"93": [1,7],
		"94": [1,3,7], # ?
		"96": [1,7],
		"97": [1,3],
		"98": [1,3],

		"1xx5": [3,7],
		"3xx5": [1,9],
		"7xx5": [1,9],
		"9xx5": [3,7]
	}

	possibleMoves = bestMoves.get(moveName)

	if possibleMoves is None and len(moveName) > 1:
		# try partial
		possibleMoves = bestMoves.get(moveName[:-1])

	if possibleMoves is None and len(moveName) > 2:
		# try partial
		possibleMoves = bestMoves.get(moveName[:-2])

	if possibleMoves is None:
		# was it a late center move?
		if len(moveName) >= 4 and moveName[3] == '5':
			moveName = moveName[0] + "xx5"
			possibleMoves = bestMoves.get(moveName)

	if possibleMoves is not None:
		print "best = "
		print possibleMoves

		possibleMoves = list( set(possibleMoves) - set(taken) )

		print "possible not taken = "
		print possibleMoves

		if len(possibleMoves) == 1:
			return possibleMoves[ 0 ];
		if len(possibleMoves) > 1:
			return possibleMoves[ random.randint(0, len(possibleMoves)-1) ];
		# else fall down to brute force

	print "try to brute force"

	# brute force into TIE
	for j in range(0, 9):
		if data['data'][j] == 0:
			return j+1
			# data[i] = computer_data
			# resp_data['move'] = {'cell': i+1}
			# break

	print "no moves left"

	return None

def _human_first_move(data, computer_data):
	moveName = ""

	for move in data['moves']:
		moveName += str(move)

	if moveName is "":
		moveName = "-"

	# cells already taken in play
	taken = []
	for i in range(0, 9):
		if data['data'][i] is not 0:
			taken.append(i+1)

	# TODO : Look for blocks
	move = _get_move_win(data, computer_data)
	if move:
		return move

	# TODO : Look for wins
	move = _get_move_block(data, computer_data)
	if move:
		return move

	# With no blocks or immediate wins, try a good move toward a win

	print moveName
	print taken

	bestMoves = {
		# start
		"-": [],
		"5": [1,3,7,9],

		"1": [5],
		"3": [5],
		"7": [5],
		"9": [5],

		"159": [2,4,6,8],
		"357": [2,4,6,8],
		"753": [2,4,6,8],
		"951": [2,4,6,8],

		"15": [3,7,9],
		"35": [1,7,9],
		"75": [1,3,9],
		"95": [1,3,7]
	}

	possibleMoves = bestMoves.get(moveName)

	if possibleMoves is None and len(moveName) > 1:
		# try partial
		possibleMoves = bestMoves.get(moveName[:-1])

	if possibleMoves is None and len(moveName) > 2:
		# try partial
		possibleMoves = bestMoves.get(moveName[:-2])

	if possibleMoves is None:
		# was it a late center move?
		if len(moveName) >= 4 and moveName[3] == '5':
			moveName = moveName[0] + "xx5"
			possibleMoves = bestMoves.get(moveName)

	if possibleMoves is not None:
		print "best = "
		print possibleMoves

		possibleMoves = list( set(possibleMoves) - set(taken) )

		print "possible not taken = "
		print possibleMoves

		if len(possibleMoves) == 1:
			return possibleMoves[ 0 ];
		if len(possibleMoves) > 1:
			return possibleMoves[ random.randint(0, len(possibleMoves)-1) ];
		# else fall down to brute force

	print "try to brute force"

	# brute force into TIE
	for j in range(0, 9):
		if data['data'][j] == 0:
			return j+1
			# data[i] = computer_data
			# resp_data['move'] = {'cell': i+1}
			# break

	print "no moves left"

	return None

def _get_move_block(data, player_data):
	for cell in [1,2,3,4,7]:
		player = _get_cell_data(data['data'][cell-1])
		print "check block cell %d player %s" % (cell, (player))
		if player is not player_data:
			if cell in [1,2,3]: #vertical
				print "vert"
				row = [ 
				  _get_cell_data(data['data'][cell-1 + 0]) , 
				  _get_cell_data(data['data'][cell-1 + 3]) , 
				  _get_cell_data(data['data'][cell-1 + 6]) ]

				tally = [0,0,0] # empty, computer, human

				for i in [0,1,2]:
					if row[i] == 0: 
						tally[0] = cell + (i*3) # ok, ok, empty is not a count but last found empty cell
					elif row[i] == player_data:
						tally[1] += 1
					else:
						tally[2] += 1

				if tally[2] == 2 and tally[1] == 0:
					return tally[0]
			if cell in [1,4,7]: #horizontal
				print "horz"
				row = [ 
				  _get_cell_data(data['data'][cell-1 + 0]) , 
				  _get_cell_data(data['data'][cell-1 + 1]) , 
				  _get_cell_data(data['data'][cell-1 + 2]) ]

				tally = [0,0,0] # empty, computer, human

				for i in [0,1,2]:
					if row[i] == 0: 
						tally[0] = cell + (i) # ok, ok, empty is not a count but last found empty cell
					elif row[i] == player_data:
						tally[1] += 1
					else:
						tally[2] += 1

				if tally[2] == 2 and tally[1] == 0:
					return tally[0]
			if cell is 1: # diagonal
				print "diag 1"
				row = [ 
				  _get_cell_data(data['data'][1-1]) , 
				  _get_cell_data(data['data'][5-1]) , 
				  _get_cell_data(data['data'][9-1]) ]

				tally = [0,0,0] # empty, computer, human

				for i in [0,1,2]:
					if row[i] == 0: 
						tally[0] = {0:1,1:5,2:9}[i] # ok, ok, empty is not a count but last found empty cell
					elif row[i] == player_data:
						tally[1] += 1
					else:
						tally[2] += 1

				if tally[2] == 2 and tally[1] == 0:
					return tally[0]
			if cell is 3: # diagonal
				print "diag 2"
				row = [ 
				  _get_cell_data(data['data'][3-1]) , 
				  _get_cell_data(data['data'][5-1]) , 
				  _get_cell_data(data['data'][7-1]) ]

				tally = [0,0,0] # empty, computer, human

				for i in [0,1,2]:
					if row[i] == 0: 
						tally[0] = {0:3,1:5,2:7}[i] # ok, ok, empty is not a count but last found empty cell
					elif row[i] == player_data:
						tally[1] += 1
					else:
						tally[2] += 1

				if tally[2] == 2 and tally[1] == 0:
					return tally[0]
	return None

def _get_move_win(data, player_data):
	for cell in [1,2,3,4,7]:
		player = _get_cell_data(data['data'][cell-1])
		print "check to win cell %d player %s" % (cell, (player))
		if True:
			if cell in [1,2,3]: #vertical
				print "vert"
				row = [ 
				  _get_cell_data(data['data'][cell-1 + 0]) , 
				  _get_cell_data(data['data'][cell-1 + 3]) , 
				  _get_cell_data(data['data'][cell-1 + 6]) ]

				tally = [0,0,0] # empty, player, other

				for i in [0,1,2]:
					if row[i] == 0: 
						tally[0] = cell + (i*3) # ok, ok, empty is not a count but last found empty cell
					elif row[i] == player_data:
						tally[1] += 1
					else:
						tally[2] += 1

				if tally[1] == 2 and tally[2] == 0:
					return tally[0]
				print tally
			if cell in [1,4,7]: #horizontal
				print "horz"
				row = [ 
				  _get_cell_data(data['data'][cell-1 + 0]) , 
				  _get_cell_data(data['data'][cell-1 + 1]) , 
				  _get_cell_data(data['data'][cell-1 + 2]) ]

				tally = [0,0,0] # empty, computer, human

				for i in [0,1,2]:
					if row[i] == 0: 
						tally[0] = cell + (i) # ok, ok, empty is not a count but last found empty cell
					elif row[i] == player_data:
						tally[1] += 1
					else:
						tally[2] += 1

				if tally[1] == 2 and tally[2] == 0:
					return tally[0]
				print tally
			if cell is 1: # diagonal
				print "diag 1"
				row = [ 
				  _get_cell_data(data['data'][1-1]) , 
				  _get_cell_data(data['data'][5-1]) , 
				  _get_cell_data(data['data'][9-1]) ]

				tally = [0,0,0] # empty, computer, human

				for i in [0,1,2]:
					if row[i] == 0: 
						tally[0] = {0:1,1:5,2:9}[i] # ok, ok, empty is not a count but last found empty cell
					elif row[i] == player_data:
						tally[1] += 1
					else:
						tally[2] += 1

				if tally[1] == 2 and tally[2] == 0:
					return tally[0]
			if cell is 3: # diagonal
				print "diag 2"
				row = [ 
				  _get_cell_data(data['data'][3-1]) , 
				  _get_cell_data(data['data'][5-1]) , 
				  _get_cell_data(data['data'][7-1]) ]

				tally = [0,0,0] # empty, computer, human

				for i in [0,1,2]:
					if row[i] == 0: 
						tally[0] = {0:3,1:5,2:7}[i] # ok, ok, empty is not a count but last found empty cell
					elif row[i] == player_data:
						tally[1] += 1
					else:
						tally[2] += 1

				if tally[1] == 2 and tally[2] == 0:
					return tally[0]
	return None

def _get_cell_data(d):
	if isinstance(d, (int, long)) :
		return d
	if len(d) > 0 :
		return d[0]
	return d[9]
def _get_move_won(data):
	print data['data']
	for cell in [1,2,3,4,7]:
		player = _get_cell_data(data['data'][cell-1])
		print "check cell %d player %s" % (cell, (player))
		if player is not 0:
			if cell in [1,2,3]: #vertical
				print "vert"
				if _get_cell_data(data['data'][cell-1 + 3]) == player and _get_cell_data(data['data'][cell-1 + 6]) == player:
					return player
			if cell in [1,4,7]: #horizontal
				print "horz"
				if _get_cell_data(data['data'][cell-1 + 1]) == player and _get_cell_data(data['data'][cell-1 + 2]) == player:
					return player
			if cell is 1: # diagonal
				print "diag 1"
				if _get_cell_data(data['data'][5-1]) == player and _get_cell_data(data['data'][9-1]) == player:
					return player
			if cell is 3: # diagonal
				print "diag 2"
				if _get_cell_data(data['data'][5-1]) == player and _get_cell_data(data['data'][7-1]) == player:
					return player
	return None
