from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from tictactoe import TicTacToe

def home(request):
	'The site home page'

	ttt = request.session.get("ttt")
	if not ttt:
		ttt = TicTacToe("")
	else:
		ttt = TicTacToe.from_json(ttt)

	request.session['ttt'] = ttt.to_json()

	context = {'name':ttt.player_name, 'first':("on" if ttt.human_first else "") }
	return render(request, 'home.html', context)

def reset(request):
	'Kill the session and start over'

	request.session.flush()
	request.session.clear()
	request.session.delete()
	return redirect("home")

def play(request):
	'Play the game'

	ttt = request.session.get("ttt")
	if not ttt:
		ttt = TicTacToe()
	else:
		ttt = TicTacToe.from_json(ttt)

	name  = request.GET.get('player-name', ttt.player_name)
	first = request.GET.get('player-first', "on" if ttt.human_first else "" )

	ttt.reset(name, first == "on")

	context = {
		'name':          ttt.player_name, 
		'first':         ttt.human_first,
		'human_data':    ttt.human_data,
		'computer_data': ttt.computer_data
	}

	move = ttt.do_first_move()
	context['move'] = move

	request.session['ttt'] = ttt.to_json()

	return render(request, 'play.html', context)

def move(request):
	"""
	record player move and determine our own move and scoring

	json response contains {
		error : {                  # [optional] if error occurred
			message: ""                         # what happened
			critical: Boolean                   # [optional] True if critical / unrecoverable error
		},
		status: ""                 # [optional] status of the game
		                              "cat win" - a tie occurred
		                              "computer win" - the computer won
		                              "human win" - the human won
		move: {                    # [optional] what move the computer has taken
			cell: int                           # the cell the computer chose
		}
	}
	"""

	ttt = request.session.get("ttt")
	if not ttt:
		return redirect("home")
	ttt = TicTacToe.from_json(ttt)

	resp_data = {}

	cell  = int(request.GET.get('cell'))

	if cell > 0 and cell <= 9:
		if ttt.occupied(cell):
			resp_data['error'] = {
				message: "Server out of synch and thinks that cell is in use.",
				critical: True}
		else:
			ttt.record_human_move(cell)

			player = ttt.did_player_win()
			if player is not None:
				print "player %s won %s" % (player, ttt.human_data)
				resp_data['status'] = "human win" if player == ttt.human_data else "computer win"
			else:
				move = ttt.do_move()

				print "got move "+str(move)

				# for i in range(0, 9):
				# 	if data[i] == 0:
				if move is not None:
					resp_data['move'] = {'cell': move}

				player = ttt.did_player_win()
				if player is not None:
					resp_data['status'] = "human win" if player == ttt.human_data else "computer win"
				else:
					if ttt.did_tie() :
						resp_data['status'] = "cat win"

	request.session['ttt'] = ttt.to_json()

	return HttpResponse(json.dumps(resp_data), content_type="application/json")
