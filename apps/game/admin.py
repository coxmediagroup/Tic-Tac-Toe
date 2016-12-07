from django.contrib import admin
from django.contrib.sessions.models import Session
from game.models import Game

admin.site.register(Game)
admin.site.register(Session)