from django.test import TestCase

from gameapp.game import GameBoard

class GameBoardTest(TestCase):
   def test_game_init(self):
      self.assertEqual('_________', GameBoard().get_state())
      self.assertEqual('X________', GameBoard('X________').get_state())
      self.assertEqual('_X_O_____', GameBoard('_X_O_____').get_state())
      
      #test board length
      self.assertRaises(ValueError, GameBoard, ''           )
      self.assertRaises(ValueError, GameBoard, 'XO______'   )
      self.assertRaises(ValueError, GameBoard, '__________' )
      
      #test board integrity
      self.assertRaises(ValueError, GameBoard, 'XX_______'  )
      self.assertRaises(ValueError, GameBoard, 'O________'  )
      self.assertRaises(ValueError, GameBoard, 'A________'  )
      
   def test_get_player(self):
      self.assertEqual("X", GameBoard().get_player())
      self.assertEqual("O", GameBoard('X________').get_player())
      
   def test_move(self):
      board = GameBoard()
      
      #test out-of-bounds
      self.assertRaises(IndexError, board.move, *(0, 3))
      self.assertRaises(IndexError, board.move, *(0, -1))
      self.assertRaises(IndexError, board.move, *(-1, 0))
      self.assertRaises(IndexError, board.move, *(3, 2))
      
      #test valid moves
      board.move(1, 0)
      self.assertEqual('___X_____', board.get_state())
      self.assertRaises(ValueError, board.move, *(1, 0))
      
      board.move(2, 2)
      self.assertEqual('___X____O', board.get_state())
      self.assertRaises(ValueError, board.move, *(2, 2))
      
   def test_game_over(self):
      #game start
      self.assertEqual(False, GameBoard().is_game_over())
      
      #game in progress
      self.assertEqual(False, GameBoard('X___O____').is_game_over())
      
      #game ended
      self.assertEqual(True, GameBoard('X__OOOX_X').is_game_over())
      self.assertEqual(True, GameBoard('XOO_X___X').is_game_over())
      self.assertEqual(True, GameBoard('XOOX__X__').is_game_over())
      self.assertEqual(True, GameBoard('XXOOOXXOX').is_game_over())
      
   def test_get_winner(self):
      self.assertEqual('O',  GameBoard('X__OOOX_X').get_winner())
      self.assertEqual('X',  GameBoard('XOO_X___X').get_winner())
      self.assertEqual(True, GameBoard('OXXOX_O__').is_game_over())
      self.assertEqual(None, GameBoard('XXOOOXXOX').get_winner())
      
      #game not finished
      self.assertEqual(None, GameBoard('X___O____').get_winner())
      
      