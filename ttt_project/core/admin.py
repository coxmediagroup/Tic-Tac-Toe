from django.contrib import admin
from core.models import Game, Move


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'completed')


class MoveAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'space', 'player_move')


admin.site.register(Move, MoveAdmin)
admin.site.register(Game, GameAdmin)
