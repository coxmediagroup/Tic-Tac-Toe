'''
Unit Tests for the GameBoard class.

To run all tests, navigate to the base Tic-Tac-Toe folder and run::

    $ python -m unittest discover -v test

Various gameplay scenarios are simulated by
constructing the scenarios by hand with the assumption 
that the gameboard got the first move.  Normally I would use
nose for nicer syntax and ease of writing test generators,
but I didn't want you to have to download any thirdparty
libraries just for an interview problem.

Also, I've never used pytest but it looks pretty awesome
and would probably be more suitable for testing django apps than nose
(although I use only unittest at my current job).

'''
import copy
from unittest import TestCase

from gameboard import GameBoard

new_game = GameBoard('X')

mid_game = GameBoard('X')
mid_game._moves = [16, 256, 1]
mid_game._wins.pop(273)
mid_game._snapshots = {'X': 17, 'O': 256}
mid_game._critical_move = None

draw_game_incomplete = GameBoard('X')
draw_game_incomplete._moves = [16, 256, 1, 64, 4, 2, 8, 32]
draw_game_incomplete._wins = {}
draw_game_incomplete._snapshots = {'X': 29, 'O': 354}
draw_game_incomplete._critical_move = 128

draw_game_complete = GameBoard('X')
draw_game_complete._moves = [16, 256, 1, 64, 4, 2, 8, 32, 128]
draw_game_complete._wins = {}
draw_game_complete._snapshots = {'X': 157, 'O': 354}
draw_game_complete._critical_move = None

winner_game = GameBoard('X')
winner_game._moves = [256, 128, 16, 1, 4, 32, 64]
winner_game._wins = {84: [4, 16, 64]}
winner_game._snapshots = {'X': 340, 'O': 161}
winner_game._critical_move = None

class TestGameBoard(TestCase):

    def setUp(self):
        self.gb = GameBoard('X')

    def test_symbol_required(self):
        self.assertRaises(Exception, GameBoard)
    
    def test_symbol_must_be_x_or_o(self):
        self.assertRaises(Exception, GameBoard, 'Z')

    def test_default_attributes(self):
        self.assertEqual(new_game._symbol, 'X')
        self.assertEqual(new_game._moves, [])
        self.assertEqual(new_game._snapshots, {'X': 0, 'O': 0})
        self.assertIsNone(new_game._critical_move)
    
    def test_moves_available_new_game(self):
        self.assertTrue(new_game.moves_available)
    
    def test_moves_available_mid_game(self):
        self.assertTrue(mid_game.moves_available)
    
    def test_moves_available_draw_game_incomplete(self):
        self.assertFalse(draw_game_incomplete.moves_available)
    
    def test_moves_available_draw_game_complete(self):
        self.assertFalse(draw_game_complete.moves_available)
    
    def test_moves_available_winner_game(self):
        self.assertFalse(winner_game.moves_available)
    
    def test_winner_new_game(self):
        self.assertFalse(new_game.winner)
    
    def test_winner_mid_game(self):
        self.assertFalse(mid_game.winner)
    
    def test_winner_draw_game_incomplete(self):
        self.assertFalse(draw_game_incomplete.winner)
    
    def test_winner_draw_game_complete(self):
        self.assertFalse(draw_game_complete.winner)
    
    def test_winner_winner_game(self):
        self.assertTrue(winner_game.winner)
    
    def test_display_new_game(self):
        self.assertIsInstance(new_game.display, str)
    
    def test_display_mid_game(self):
        self.assertIsInstance(mid_game.display, str)
    
    def test_display_draw_game_incomplete(self):
        self.assertIsInstance(draw_game_incomplete.display, str)
    
    def test_display_draw_game_complete(self):
        self.assertIsInstance(draw_game_complete.display, str)
    
    def test_display_winner_game(self):
        self.assertIsInstance(winner_game.display, str)
    
    def test_make_move_by_index(self):
        orig_wins = copy.copy(self.gb._wins)

        self.gb.make_move_by_index(4, 'O')

        self.assertEqual(self.gb._symbol, 'X')
        self.assertEqual(self.gb._moves, [16])
        self.assertEqual(self.gb._snapshots, {'X': 0, 'O': 16})
        self.assertIsNone(self.gb._critical_move)
        self.assertEqual(self.gb._wins, orig_wins)
    
    def test_move(self):
        orig_wins = copy.copy(self.gb._wins)
        
        self.gb.move()
        
        self.assertEqual(self.gb._symbol, 'X')
        self.assertEqual(self.gb._moves, [16])
        self.assertEqual(self.gb._snapshots, {'X': 16, 'O': 0})
        self.assertIsNone(self.gb._critical_move)
        self.assertEqual(self.gb._wins, orig_wins)
    
    def test_move_critical(self):
        self.gb.make_move_by_index(2, 'O')
        self.gb.move()
        self.gb.make_move_by_index(8, 'O')
        
        self.assertNotIn(32, self.gb._moves)
        self.gb.move()
        self.assertIn(32, self.gb._moves)

