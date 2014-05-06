from django.shortcuts import render
from tictactoe.forms import UsernameForm
from tictactoe.models import Player



def index(request):
    ctx = {}
    un = request.session.get('username',None)
    if un:
    	player_qs = Player.objects.filter(
    		username=un
    		)
    	if player_qs.count() > 0:
    		player = player_qs[0]
    		rank = Player.objects.all(
    			).filter(
    			plays__gte=player.plays
    			).exclude(
    			username=player.username
    			).order_by(
    			'-plays'
    			).count() + 1
    		ctx.update({'player':player,
    			'player_rank':rank})

    players = Player.objects.all().order_by('-plays')[:10]
    ctx.update({'players':players})

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
