from django.shortcuts import render
from django.http import HttpResponse

#handles the "start game" view
def start_game(request):
    context = {}
    return render(request, 'game/startgame.html', context)

#handles when player presses "Start Game" button
def launch(request):
    context = {}
    return render(request, 'game/game.html', context)

#loads the current game based on settings in memory
def game_page(request):
    context = {}
    return render(request, 'game/game.html', context)

def ajax_make_move(request):
    context = {}
    return render(request, 'game/game.html', context)

