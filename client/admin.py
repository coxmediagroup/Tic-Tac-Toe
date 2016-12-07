from django.contrib import admin
from .models import Game, Move

class GameAdmin(admin.ModelAdmin):
    pass

class MoveAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'x_position', 'y_position', 'created')
    list_filter = ('game__name',)

admin.site.register(Game, GameAdmin)
admin.site.register(Move, MoveAdmin)
