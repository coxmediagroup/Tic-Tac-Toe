import logging
import os
from django.shortcuts import render


def index(request):
    '''This is the initial view that lists the few navigation options that this
    application supports.
    '''
    return render(request, 'game/index.html')

def playGame(request):
    '''This is the initial view placeholder for the game itself.
    '''
    return render(request, 'game/playGame.html')