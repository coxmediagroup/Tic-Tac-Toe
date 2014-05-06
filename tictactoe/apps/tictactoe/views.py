from django.shortcuts import render
from tictactoe.forms import UsernameForm
from tictactoe.models import Player



def index(request):
    ctx = {}
    return render(request, 'index.html', ctx)

def play_game(request):
	ctx = {}
	if request.method == 'GET':
		username_form = UsernameForm()
		ctx.update({'form':username_form})
	if request.method == 'POST':
		username_form = UsernameForm(request.POST)
		if username_form.is_valid():
			un = username_form.cleaned_data['username']
			request.session['username'] = un
			player, created = Player.objects.get_or_create(username=un)
		else:
			ctx.update({'form':username_form})

	return render(request, 'game.html', ctx)
