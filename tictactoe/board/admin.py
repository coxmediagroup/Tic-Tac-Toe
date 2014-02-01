from django.contrib import admin
from board.models import Game
from board.models import Move
from board.models import Player


class GameAdmin(admin.ModelAdmin):
  list_display = ('player1_name', 'player2_name', 'is_over', 'winner')
  def player1_name(self, obj):
    if obj.player_1:
      return obj.player_1.name
  player1_name.admin_order_field = 'player_1__name'
  player1_name.admin_short_description = 'player 1'

  def player2_name(self, obj):
    if obj.player_2:
      return obj.player_2.name
  player2_name.admin_order_field = 'player_2__name'
  player2_name.admin_short_description = 'player 2'


class PlayerAdmin(admin.ModelAdmin):
  list_display = ('name', 'humanity',)
  def humanity(self, obj):
    return 'HUMAN' if obj.is_human else 'COMPUTER'
  humanity.admin_order_field = 'is_human'
  humanity.admin_short_description = 'Humanity'



admin.site.register(Game, GameAdmin)
admin.site.register(Move)
admin.site.register(Player, PlayerAdmin)
