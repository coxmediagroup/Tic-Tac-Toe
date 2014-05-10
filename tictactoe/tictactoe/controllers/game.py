from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from tictactoe.models import *

def index(request):
    return render_to_response("game.html",dict(board=None, user=None))