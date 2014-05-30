'''Django admin config for tictactoe app'''
from django.contrib import admin

from .models import Game

admin.site.register(Game)
