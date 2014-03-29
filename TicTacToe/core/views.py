# Copyright (C) 2014 Ryan Hansen.  All rights reserved.
# This source code (including its associated software) is owned by Ryan Hansen and
# is protected by United States and international intellectual property law, including copyright laws, patent laws,
# and treaty provisions.

from django.shortcuts import render, Http404, HttpResponse

import json
import random

from time import sleep

from core.game import Game


def standard(request, **kwargs):
    move = kwargs.get('move', None)
    if move:
        try:
            g = Game()
            print g.o
            print g.x
            g.take('human', int(move))
            if len(g.available()) == 0:
                return HttpResponse(json.dumps(dict(over=True)), content_type="application/json")
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
            return HttpResponse(json.dumps(dict(move=take, over=False)), content_type="application/json")
        except:
            raise Http404
    return render(request, 'grid.html')