from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse
import json

from tictactoe.models import *

def index(request):
    response_data = {}
    response_data['board'] = "hello world"
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    #return render_to_response("game.html",dict(board=None, user=None))

def new(request):
    return render_to_response("new.html",dict(board=None, user=None))