import sys
'''
         Do the tic tac toe game!
'''

class Board:
   """Contains the board's state"""
   pass

class Game:
   """Contains a board and other game state"""
   def __init__( self ):
      self._test()
   def _test( self ):
   
      def assert_true(cond, msg):
         if not cond:
            print msg
            sys.exit()
   
      print "Testing starting."

      # testing Board.is_full
      b = Board()
      assert_true(not b.is_full(), "Error, Board.is_full incorrect.")
      for x in range(8):
         b.move_X(x)
         assert_true(not b.is_full(), "Error, Board.is_full incorrect: " + str(x))
         for e in range(x + 1):
            assert_true(not b.spot_empty(e), "spot " + str(e) + " should not be empty")
         for e in range(x + 1, 9):
            assert_true(b.spot_empty(e), "spot " + str(e) + " should be empty")
         assert_true(not b.is_full(), "board should not be full: " + str(b))
      b.move_X(8)
      assert_true(b.is_full(), "Error, Board.is_full incorrect: 8")
      assert_true(b.is_full(), "board should be full: " + str(b))

      # testing Board.get_opposite_and_other_empty_corners
      b = Board()
      ls = b.get_opposite_and_other_empty_corners('X')
      for x in [0, 2, 6, 8]:
         assert_true(x in ls, "%s should be an empty corner" % x)
      ls = b.get_opposite_and_other_empty_corners('O')
      for x in [0, 2, 6, 8]:
         assert_true(x in ls, "%s should be an empty corner" % x)

      # make first move, into NW corner
      b.move_X(0)
      ls = b.get_opposite_and_other_empty_corners('X')
      for x in [2, 6, 8]:
         assert_true(x in ls, "%s should be an empty corner" % x)
      assert_true(0 not in ls, "%s should not be an empty corner: %s" % (0, ls))
      assert_true(8 == ls[0], "%s should be the opposite corner: %s" % (8, ls))

      ls = b.get_opposite_and_other_empty_corners('X')
      for x in [2, 6, 8]:
         assert_true(x in ls, "%s should be an empty corner" % x)
      assert_true(0 not in ls, "%s should not be an empty corner: %s" % (0, ls))

      # make second move, into NE corner
      b.move_O(2)
      ls = b.get_opposite_and_other_empty_corners('X')
      assert_true(ls[0] == 8, "opposite empty corner should be 8, not %s" % ls[0])
      assert_true(ls[1] == 6, "other empty corner should be 6, not %s" % ls[1])
      assert_true(len(ls) == 2, "empty corners length should be 2, not %s" % len(ls))

      ls = b.get_opposite_and_other_empty_corners('O')
      assert_true(ls[0] == 6, "opposite empty corner should be 6, not %s" % ls[0])
      assert_true(ls[1] == 8, "other empty corner should be 8, not %s" % ls[1])
      assert_true(len(ls) == 2, "empty corners length should be 2, not %s" % len(ls))

      # make third move, into SW corner
      b.move_X(6)
      ls = b.get_opposite_and_other_empty_corners('X')
      assert_true(ls == [8], "only empty corner should be 8, not %s" % ls)
      ls = b.get_opposite_and_other_empty_corners('O')
      assert_true(ls == [8], "only empty corner should be 8, not %s" % ls)

      # make fourth move, into SE corner
      b.move_X(8)
      ls = b.get_opposite_and_other_empty_corners('X')
      assert_true(ls == [], "should be no empty corners left, not %s" % ls)
      ls = b.get_opposite_and_other_empty_corners('O')
      assert_true(ls == [], "should be no empty corners left, not %s" % ls)

      # testing find_winner
      for moves in [[0, 1, 2], [3, 4, 5], [6, 7, 8], 
                    [0, 3, 6], [1, 4, 7], [2, 5, 8],
                    [0, 4, 8], [2, 4, 6]]:
         b = Board()
         b.move_X(moves[0])
         assert_true(None == b.find_winner(), "Should have no winner, only moved once.")
         b.move_X(moves[1])
         assert_true(None == b.find_winner(), "Should have no winner, only moved twice.")
         b.move_X(moves[2])
         w = b.find_winner()
         assert_true('X' == w, "Should have X winner, not %s" % w)

      for moves in [[0, 1, 2], [0, 2, 1], [2, 1, 0]]:
         b = Board()
         b.move_X(moves[0])
         w = b.find_two_index('X')
         assert_true(None == w, "Should have no almost win, only moved once, not %s" % w)
         b.move_X(moves[1])
         w = b.find_two_index('X')
         assert_true(moves[2] == w, "Should have %s almost win, not %s" % (moves[2], w))

      print "Testing done."

Game()
