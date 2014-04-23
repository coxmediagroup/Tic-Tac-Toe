
from django.shortcuts import render
from tictac.models import Game

# Create your views here.

def welcome(request):
    return render(request, 'welcome.html', {})

def game_board(request):
    accept = request.META.get('HTTP_ACCEPT', '*/*')
    if 'application/json' in accept or '*/*' in accept:
        template = 'game_board.json'
    else:
        template = 'game_board.html'

    # game = Game.objects.new_game(players=[{ 'name' : 'Baron' },])
    game = Game.objects.get(pk=1)

    return render(request, template, {
        'game' : game }, content_type='application/json')


