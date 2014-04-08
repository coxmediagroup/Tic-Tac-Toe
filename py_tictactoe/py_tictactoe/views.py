from django.shortcuts import render, redirect

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
	request.session['playerFirst'] = request.GET.get('player-first')
	
	context = {'name':request.session.get("playerName"), 'first':("on" if request.session.get("playerFirst") else "") }
	request.session['start'] = True
	return render(request, 'play.html', context)
