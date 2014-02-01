from django.test import TestCase
from models import Player, Game, Move
from django.db import IntegrityError
import unittest

class SavingModelsTestCase(TestCase):
  def setUp(self):
    player_1 = Player.objects.create(name="Person1", is_human=True)
    player_2 = Player.objects.create(name="Person2", is_human=False)
    Game.objects.create(player_1=player_1, player_2=player_2)

  def test_save_move_normal(self):
    ''' Tests a simple move to valid location.
        Expected: no exceptions.
    '''
    game = Game.objects.get(id=1)
    player1 = Player.objects.get(id=1)
    move = Move(game=game, player=player1, position_x=1, position_y=1)
    move.save()
    from_db = Move.objects.get(id=1)
    self.assertEqual(from_db.position_x, 1)

