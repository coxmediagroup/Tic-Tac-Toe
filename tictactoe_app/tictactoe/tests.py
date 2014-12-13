from django.test import TestCase

from tictactoe.models import GameState, PersistentGameState
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


from django.test import Client
import json
from pprint import pprint as pp


class PostTest(TestCase):
  def test_one_move(self):
    c = Client()
    resp = c.get('/tictactoe/game/')
    jresp = json.loads(resp.content.decode('utf-8'))
    game_id = jresp["game"]["gameId"]
    resp2 = c.post('/tictactoe/game/%s/'%(game_id,), {'player':'X', 'position':'0'}, follow=True)
    jresp2 = json.loads(resp2.content.decode('utf-8'))
    self.assertEqual(len(jresp2['game']['moves']), 2, "computer should have played")


class GameTest(TestCase):
  def setUp(self):
    c = Client()
    resp = c.get('/tictactoe/game/')
    jresp = json.loads(resp.content.decode('utf-8'))
    self.game_id = jresp["game"]["gameId"]

  def do_move(self, player, pos):
    c = Client()
    url = '/tictactoe/game/%s/'%(self.game_id,)
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
    pp(resp)
    self.assertEqual(resp['isDrawn'], True, "Game should be drawn")


