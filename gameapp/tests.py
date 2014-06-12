from django.test import TestCase

from gameapp.game import GameBoard
from gameapp.player import PlayerRandom, PlayerMinimax, minimax, get_max, get_value

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
      
class PlayerRandomTest(TestCase):
   def test_random_play(self):
      board=GameBoard()
      count = len(board.get_valid_moves())
      board.move(*PlayerRandom.choose_move(board))
      self.assertEqual(len(board.get_valid_moves()), count - 1)
      
   def test_random_play_last(self):
      board=GameBoard('XXOOO_XOX')
      count = len(board.get_valid_moves())
      board.move(*PlayerRandom.choose_move(board))
      self.assertEqual(len(board.get_valid_moves()), count - 1)
   
class PlayerMinimaxTest(TestCase):
   def test_get_max_better(self):
      choices = [1, 2]
      bestVal = -1
      val = 0
      choice = 3
      self.assertEqual((0, [3]), get_max(bestVal, val, choices, choice))
      
   def test_get_max_same(self):
      choices = [1, 2]
      bestVal = 0
      val = 0
      choice = 3
      self.assertEqual((0, [1,2,3]), get_max(bestVal, val, choices, choice))
      
   def test_get_max_worse(self):
      choices = [1, 2]
      bestVal = 0
      val = -1
      choice = 3
      self.assertEqual((0, [1,2]), get_max(bestVal, val, choices, choice))
      
   def test_get_value(self):

      self.assertEqual(0, get_value(GameBoard()))
      
      # XXX
      # OO 
      #
      self.assertEqual(1, get_value(GameBoard('XXXOO____')))
      
      # XX
      # OOO 
      # X
      self.assertEqual(-1, get_value(GameBoard('XX_OOOX__')))
      
      self.assertEqual(0, get_value(GameBoard('XO_______')))
   
   def test_minimax_win(self):
      # XX
      # OO
      #
      self.assertEqual( (1, [(0,2)]), minimax(GameBoard('XX_OO____'), 1, 1) )
      
      # XX
      # OO
      #
      self.assertEqual( (1, [(0,2)]), minimax(GameBoard('XX_OO____'), 1, 1) )
      
      # X
      # XO
      # O X
      # Counter-intuitive, but this is the first square that allows a win
      # TODO: optimize for winning in fewer turns
      self.assertEqual( (1, [(0,1)]), minimax(GameBoard('X__XO_O_X'), 6, -1) )
   
   def test_minimax_block(self):
      # X X
      #  O
      #    
      self.assertEqual( (0, [(0,1)]), minimax(GameBoard('X_X_O____'), 2, -1) )
      
   def test_minimax_dont_lose(self):
      self.assertEqual( (0, [(1,1)]), minimax(GameBoard('X________'), 6, -1) )
      
      self.assertEqual( (0, [(0,0), (0,2), (2,0), (2,2)]), minimax(GameBoard('____X____'), 6, -1) )
      
      
      