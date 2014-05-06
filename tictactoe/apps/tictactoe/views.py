from django.shortcuts import render



def index(request):
    ctx = {}
    return render(request, 'index.html', ctx)

def play_game(request):
	ctx = {}
	return render(request, 'game.html', ctx)
