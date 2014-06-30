from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User as DjangoUser

from game.models import Game, PlayerProfile


def welcome(request):
	
	if request.POST:
		xplayer = request.POST.get('xplayer')
		xplayer_email = ''.join([xplayer,'@tictactoe_game.us'])
		xplayer_password = ''.join([xplayer,'password'])
		player, created = DjangoUser.objects.get_or_create(username=xplayer,
														   email=xplayer_email,
														   password=xplayer_password)
		player_profile, created = PlayerProfile.objects.get_or_create(player=player,player_type=1)
		return redirect(reverse('titctactoe_game',
								args=(xplayer,)))

	return render(request,
				  'game/welcome.html')


def game(request, xplayer):
	
	playerProfile = get_object_or_404(PlayerProfile, player__username=xplayer)
	context = {'xplayer': xplayer,
			   'oplayer': 'sion'}
	return render(request,
				  'game/board.html',
				  context)


