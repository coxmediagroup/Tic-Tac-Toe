from django.test import TestCase

from gameapp.game import GameBoard

class GameBoardTest(TestCase):
   def test_game_init(self):
      self.assertEqual("_________", GameBoard().get_state())
      self.assertEqual("X________", GameBoard("X________").get_state())
      self.assertEqual("_X_O_____", GameBoard("_X_O_____").get_state())
      
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
      
