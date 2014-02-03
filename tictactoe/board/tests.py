from django.test import TestCase
from tastypie.test import ResourceTestCase, TestApiClient
from models import Player, Game, Move
from django.db import IntegrityError
import json
import unittest

#TODO- split to different py files...

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




class ApiTestCase(ResourceTestCase):
  '''
     Testing custom integrity checks for the Move model.
  '''

  def setUp(self):
    self.api_client = TestApiClient()
    player_1 = Player.objects.create(name="Person1", is_human=True)
    player_2 = Player.objects.create(name="Person2", is_human=False)
    Game.objects.create(player_1=player_1, player_2=player_2)

  def move_dict(self, game_id, player_id, x, y):
    return {"game": { "id": game_id }, "player": { "id": player_id }, "position_x": x, "position_y": y}

  def test_winner_found(self):
    '''
       Tests winner and is_over are updated on game when three coordinates in a row are one player's.
       Tests winner and is_over are not updated before that.
    '''

    self.api_client.get('/api/v1/move/', format='json')

    game = Game.objects.get(id=1)
    player1 = Player.objects.get(id=1)
    player2 = Player.objects.get(id=2)
    Move(game=game, player=player1, position_x=1, position_y=1).save()
    Move(game=game, player=player2, position_x=0, position_y=0).save()
    Move(game=game, player=player1, position_x=1, position_y=0).save()
    move_post = self.move_dict(game.id, player2.id, 0, 2)
    self.api_client.post('/api/v1/move/', data=move_post)
    
    game = Game.objects.get(id=1)

    self.assertFalse(game.is_over or game.winner)
    move_post = self.move_dict(game.id, player1.id, 1, 2)

    self.api_client.post('/api/v1/move/', data=move_post)


    self.api_client.get('/api/v1/move/', format='json')
    resp = json.loads(self.api_client.get('/api/v1/game/1/', format='json').content)

    game = Game.objects.get(id=1)
    self.assertTrue(game.is_over)
    self.assertTrue(resp['is_over'])
    self.assertEqual(game.winner, player1)
    self.assertEqual(resp['winner']['name'], player1.name)

    
  def test_tie(self):
    '''
       Tests is_over is updated on game when all coordinates have been taken.
       Tests is_over is not updated before that.
       Tests that winner is never set for this scenario.
    '''

    self.api_client.get('/api/v1/move/', format='json')

    game = Game.objects.get(id=1)
    player1 = Player.objects.get(id=1)
    player2 = Player.objects.get(id=2)
    Move(game=game, player=player1, position_x=1, position_y=1).save()
    Move(game=game, player=player2, position_x=1, position_y=0).save()
    Move(game=game, player=player1, position_x=2, position_y=0).save()
    Move(game=game, player=player2, position_x=2, position_y=2).save()
    Move(game=game, player=player1, position_x=0, position_y=0).save()
    Move(game=game, player=player2, position_x=0, position_y=1).save()
    Move(game=game, player=player1, position_x=1, position_y=2).save()
    move_post = self.move_dict(game.id, player2.id, 0, 2)
    self.api_client.post('/api/v1/move/', data=move_post)
    
    game = Game.objects.get(id=1)

    self.assertFalse(game.is_over or game.winner)
    move_post = self.move_dict(game.id, player1.id, 2, 1)
    self.api_client.post('/api/v1/move/', data=move_post)

    resp = json.loads(self.api_client.get('/api/v1/game/1/', format='json').content)

    game = Game.objects.get(id=1)
    self.assertTrue(game.is_over)
    self.assertTrue(resp['is_over'])
    self.assertFalse(game.winner)
    self.assertFalse(resp['winner'])


