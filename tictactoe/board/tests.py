from django.test import TestCase
from models import Player, Game, Move
from django.db import IntegrityError
import unittest

class SavingMoveModelTestCase(TestCase):
  '''
     Testing custom integrity checks for the Move model.
  '''

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

  def test_save_move_duplicate_positions(self):
    ''' Tests second move in same x/y position from different player.
        Expected: An exception is raised with message for unique together (game, x, y).
    '''
    game = Game.objects.get(id=1)
    player1 = Player.objects.get(id=1)
    player2 = Player.objects.get(id=2)
    move = Move(game=game, player=player1, position_x=1, position_y=1)
    move2 = Move(game=game, player=player2, position_x=1, position_y=1)
    move.save()
    from_db = Move.objects.get(id=1)
    self.assertEqual(from_db.position_x, 1)
    with self.assertRaises(IntegrityError) as context:
      move2.save()
    self.assertEqual(context.exception.message, 'columns game_id, position_x, position_y are not unique')

  def test_save_same_player_immediate_succession(self):
    ''' Tests same player making otherwise valid moves back to back.
        Expected: An exception is raised with message for consecutive moves.
    '''
    game = Game.objects.get(id=1)
    player1 = Player.objects.get(id=1)
    player2 = Player.objects.get(id=2)
    move = Move(game=game, player=player1, position_x=1, position_y=1)
    move2 = Move(game=game, player=player1, position_x=1, position_y=2)
    move.save()
    from_db = Move.objects.get(id=1)
    self.assertEqual(from_db.position_x, 1)
    with self.assertRaises(IntegrityError) as context:
      move2.save()
    self.assertEqual(context.exception.message, 'Same player cannot make consecutive moves in the same game')

  def test_invalid_positions(self):
    ''' Tests for positions outside of possible values.
        Expected: Exception raised
    '''
    game = Game.objects.get(id=1)
    player1 = Player.objects.get(id=1)
    invalid_position = 7
    move = Move(game=game, player=player1, position_x=invalid_position, position_y=1)
    with self.assertRaises(IntegrityError) as context:
      move.save()
    self.assertEqual(context.exception.message, 'position_x, %s is outside of valid range,0-2' % invalid_position)
    move.position_x = 0
    move.position_y = invalid_position
    with self.assertRaises(IntegrityError) as context:
      move.save()
    self.assertEqual(context.exception.message, 'position_y, %s is outside of valid range,0-2' % invalid_position)

