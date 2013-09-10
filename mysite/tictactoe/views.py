from django.http import HttpResponse
from django.shortcuts import render

def startgame(request):
    return HttpResponse("Start Hello, world. You're at the games index.")

def index(request):
    return render(request, 'tictactoe/index.html')