from django.test import TestCase

from tictactoe_api.models import GameState, PersistentGameState, Move
# Create your tests here.


class GameStateTests(TestCase):
  def setUp(self):
    self.game = GameState("some-id")

  def test_making_move(self):
    valid, data = self.game.validate_next("X", 0)
    self.assertTrue(valid, "Should be able to make an initial move")
    if valid:
      self.game.tally_move(*data)
    valid, data = self.game.validate_next("X", 0)
    self.assertFalse(valid, "Shouldnt have been able to move twice")

  def test_win(self):
    self.game.tally_move('X', 0)
    self.game.tally_move('X', 1)
    self.game.tally_move('X', 2)
    self.assertTrue(self.game.isWon(), "Game should be won if there are 3 x's")


class PersistentGameTests(TestCase):
  def setUp(self):
    self.game = PersistentGameState("some-id")

  def test_save(self):
    self.game.save_move('X',0)
    self.game.save_move('O',1)
    game = PersistentGameState.load("some-id")
    self.assertEqual(len(game.movelist), 2, "movelist not loaded")    

  def test_first_move_numbering_assumption(self):
    import uuid
    g = PersistentGameState(uuid.uuid4())
    g.save_move("X",0)
    obj = Move.objects.filter(session_id=g.game_id).order_by('insert_id').first()
    self.assertEqual(obj.insert_id, 1, "expected database to use 1 for first insert; adjust getAllIds to fix")

from django.test import Client
import json
from pprint import pprint as pp


class PostTest(TestCase):
  def test_one_move(self):
    c = Client()
    resp = c.post('/api/game/new')
    jresp = json.loads(resp.content.decode('utf-8'))
    game_id = jresp["game"]["gameId"]
    resp2 = c.post('/api/game/%s/makeMove'%(game_id,), {'player':'X', 'position':'0'}, follow=True)
    jresp2 = json.loads(resp2.content.decode('utf-8'))
    self.assertEqual(len(jresp2['game']['moves']), 2, "computer should have played")


class GameApiTest(TestCase):
  def setUp(self):
    c = Client()
    resp = c.post('/api/game/new')
    jresp = json.loads(resp.content.decode('utf-8'))
    self.game_id = jresp["game"]["gameId"]

  def do_move(self, player, pos):
    c = Client()
    url = '/api/game/%s/makeMove'%(self.game_id,)
    body = {'player': player, 'position': pos}
    resp = c.post(url, body, follow=True)
    #self.assertEqual(resp.status, 200, "Didn't get HTTP OK back")
    jresp = json.loads(resp.content.decode('utf-8'))
    return jresp

  def test_blocks_move(self):
    self.do_move("X", '0')
    jresp = self.do_move("X", '4') # we expect this to be blocked if the minmax alg plays right
    self.assertEqual(jresp['status'], "error", "didnt get error after blocked move")

  def test_perfect_game(self):
    self.do_move("X", "4")
    self.do_move("X", "1")
    self.do_move("X", "6")
    self.do_move("X", "8")
    resp = self.do_move("X", "5")
    self.assertEqual(resp['game']['isDrawn'], True, "Game should be drawn")


