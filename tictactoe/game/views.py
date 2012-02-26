import logging
import os
from django.shortcuts import render


def index(request):
    '''This is the initial view placeholder when the application is first entered
    '''
    return render(request, 'game/index.html')