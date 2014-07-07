# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from apps.coxtactoe import tictactoe as ttt
from apps.coxtactoe.ai import MinMaxPlayer
from apps.coxtactoe import const as C

import logging as log


log.basicConfig(level=log.DEBUG)

__docformat__ = 'restructuredtext en'


class TicTacToeSplashView(TemplateView):
    template_name = "coxtactoe/splash.html"
    http_method_names = ['get', 'post']

    def post(self, request):
        xo_choice = request.POST.get('xo_choice', None)
        if xo_choice not in ('x', 'o'):
            return HttpResponseBadRequest()
        return self.start_game(xo_choice)

    def start_game(self, xo_choice):
        game = ttt.Game()
        if xo_choice == 'o':
            # Have AI make first move
            x = ttt.Marker(C.X)
            ai_player = MinMaxPlayer(x)
            square = ai_player.get_best_move(x, game.board)
            game.board.place(x, square)
        game.save()
        return HttpResponseRedirect(
            reverse(C.VIEW_NAME_GAME, kwargs={C.URL_KEY_GAME_ID: game.id}))

    def get_context_data(self, **kwargs):
        context = super(TicTacToeSplashView, self).get_context_data(**kwargs)
        context['title'] = "cOXtactoe - X or O?"
        context['app'] = ''
        return context



class TicTacToeGameView(TemplateView):
    template_name = "coxtactoe/game.html"

    def get_context_data(self, **kwargs):
        context = super(TicTacToeGameView, self).get_context_data(**kwargs)
        context['title'] = "cOXtactoe - Game"
        context['app'] = 'coxtactoe'
        return context

