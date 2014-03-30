"""
Copyright (C) 2014 Ryan Hansen.  All rights reserved.
This source code (including its associated software) is owned by Ryan Hansen and
is protected by United States and international intellectual property law, including copyright laws, patent laws,
and treaty provisions.
"""

from django.shortcuts import render, Http404, HttpResponse

import json
import random

from time import sleep

from core.const import WIN_VECTORS
from core.game import Game


def index(request):
    return render(request, 'index.html')

def standard(request, **kwargs):
    move = kwargs.get('move', None)
    if move:
        try:
            g = Game()
            over = False
            result = {'result': ''}
            context = dict()
            g.take('human', int(move))
            if len(g.available()) != 0:
                sleep(2)
                # x = request.GET.get('x', None)
                # if x:
                #     g.x = [int(i) for i in x.strip(',').split(',')]
                # o = request.GET.get('o', None)
                # if o:
                #     g.o = [int(i) for i in o.strip(',').split(',')]
                if 4 not in g.o and 4 not in g.x:
                    take = 4
                elif g.o[0] == 4 and len(g.x) == 0:
                    take = 0
                else:
                    win = g.winnable('machine')
                    block = g.winnable('human')
                    if win:
                        take = win
                    elif block:
                        take = block
                    else:
                        take = g.eval_game('machine')
                g.take('machine', take)
                winner = g.winner('machine')
                if winner:
                    over = True
                    result = {'result': list(winner)}
            else:
                take = 9999
                over = True
                result = {'result': 'draw'}
            if over:
                g.reset()
            context['move'] = take
            context['over'] = over
            context['result'] = result
            return HttpResponse(json.dumps(context), content_type="application/json")
        except Exception, ex:
            raise Http404
    return render(request, 'standard.html')


def jerk(request, **kwargs):
    move = kwargs.get('move', None)
    if move:
        winners = []
        sleep(1)
        for v in WIN_VECTORS:
            if int(move) not in v:
                winners.append(list(v))
        winner = winners[random.randint(0, len(winners) - 1)]
        context = dict(
            winner=winner
        )
        return HttpResponse(json.dumps(context), content_type="application/json")
    return render(request, 'jerk.html')