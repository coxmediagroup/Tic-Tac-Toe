from django.db import models
import datetime
from django.db import IntegrityError
from datetime import timedelta

class Player(models.Model):
  name = models.CharField(max_length=60, null=True, blank=True)
  is_human = models.BooleanField(default=False)

  def __unicode__(self):
    return self.name

  def get_absolute_url(self):
    return "/player/%i/" % self.id

class Game(models.Model):
  '''
     All game state values stored here with a foreign key to moves (see Move model).
  '''
  player_1 = models.ForeignKey(Player, related_name='player_1', null=False, blank=False)
  player_2 = models.ForeignKey(Player, related_name='player_2', null=False, blank=False)
  start_time = models.DateTimeField(default=datetime.datetime.now)
  is_over = models.BooleanField(default=False)
  winner = models.ForeignKey(Player, related_name='winner', null=True, blank=True)

  def __unicode__(self):
    return '%s - %s vs %s' % (self.start_time, self.player_1.name, self.player_2.name)

  def get_absolute_url(self):
    return "/game/%i/" % self.id

class Move(models.Model):
  ''' 
     A move's position is represented by position_x and position_y.
     Ordering is default to game and time desc.
     A uniq constraint is on combination of game and move position (x & y).
     Save is overridden to enforce players take turns and moves are valid.
  '''
  class Meta:
    ordering = ['game', '-time']
    unique_together = (("game", "position_x","position_y"),)

  game = models.ForeignKey(Game, null=False, blank=False)
  player = models.ForeignKey(Player, null=False, blank=False)
  time = models.DateTimeField(default=datetime.datetime.now)
  position_x = models.IntegerField(null=False, blank=False)
  position_y = models.IntegerField(null=False, blank=False)

  def save(self, *args, **kwargs):
    # default ordering is by time descending, see above
    existing_moves = Move.objects.filter(game=self.game)
    if len(existing_moves) > 0 and existing_moves[0].player == self.player and existing_moves[0].id != self.id:
      raise IntegrityError('Same player cannot make consecutive moves in the same game')
    elif self.position_x not in range(0,3):
      raise IntegrityError('position_x, %s is outside of valid range,0-2' % self.position_x)
    elif self.position_y not in range(0,3):
      raise IntegrityError('position_y, %s is outside of valid range,0-2' % self.position_y)
    else:
      super(Move, self).save(*args, **kwargs)

  def __unicode__(self):
    return '%s - %s vs %s | player: %s marked position %s,%s' % (self.time, self.game.player_1.name, self.game.player_2.name, self.player.name, self.position_x, self.position_y)

  def get_absolute_url(self):
    return "/move/%i/" % self.id

