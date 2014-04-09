from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

def home(request):
	'The site home page'
	context = {'name':request.session.get("playerName"), 'first':("on" if request.session.get("playerFirst") else "") }
	request.session['start'] = True
	return render(request, 'home.html', context)

def reset(request):
	'Kill the session and start over'
	request.session.flush()
	return request.redirect(home)

def play(request):
	'Play the game'
	request.session['playerName'] = request.GET.get('player-name')
	first = request.session['playerFirst'] = request.GET.get('player-first')

	human_data    = ("X" if first else "O"),
	computer_data = ("O" if first else "X")

	request.session['tictactoe'] = [
		0,0,0,
		0,0,0,
		0,0,0]

	context = {
		'name':          request.session.get("playerName"), 
		'first':         ("on" if first else ""),
		'human_data':    ("X" if first else "O"),
		'computer_data': ("O" if first else "X")
	}

	if not first:
		request.session['tictactoe'][0] = computer_data
		context['move'] = 1

	request.session['start'] = True
	return render(request, 'play.html', context)

def move(request):
	resp_data = {}

	data  = request.session.get('tictactoe')
	cell  = int(request.GET.get('cell'))
	first = request.session.get('playerFirst')

	human_data    = ("X" if first else "O"),
	computer_data = ("O" if first else "X")

	if cell > 0 and cell <= len(data):
		if data[cell -1]:
			resp_data['error'] = {
				message: "Server out of synch and thinks that cell is in use.",
				critical: True}
		else:
			data[cell -1] = human_data

			for i in range(0,8):
				if data[i] == 0:
					data[i] = computer_data
					resp_data['move'] = {'cell': i+1}
					break

	found = False

	for i in range(0,8):
		if data[i] == 0:
			found = True

	if not found :
		resp_data['status'] = "cat win"

	request.session['tictactoe'] = data

	return HttpResponse(json.dumps(resp_data), content_type="application/json")
