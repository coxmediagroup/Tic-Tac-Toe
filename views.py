from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Would you like to play a game?")
