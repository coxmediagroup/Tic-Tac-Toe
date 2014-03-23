from django.shortcuts import render
from django.views.generic import View


class TicTacToe(View):
    template = 'games/base.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template)


class TicTacToeStart(View):
    template = 'games/game.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template)

