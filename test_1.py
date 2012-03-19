#! /usr/bin/env python
import copy
import pdb
import sys
import unittest
from unittest import TestCase
from game import TicTacToe, InvalidMove
from bitarray import bitarray


class TicTacToeTest(TestCase):
    '''Test the game '''

    depth = 0
    recurse_level = 0

    def setUp(self):
        self.game = TicTacToe()
        self.game.reset()

    def tearDown(self):
        del self.game
        self.game = None

    def test_board(self):
        self.game.player_one = bitarray('100100100')
        self.game.player_two = bitarray('010010010')
        self.assertEqual(bitarray('100100100')|bitarray('010010010'), self.game.board())

    def test_reset(self):
        self.game.player_one = bitarray('100100100')
        self.game.player_two = bitarray('010010010')
        self.assertEqual(bitarray('100100100')|bitarray('010010010'), self.game.board())
        self.game.reset()
        self.assertEqual(bitarray('000000000'), self.game.player_one)
        self.assertEqual(bitarray('000000000'), self.game.player_two)

    def test_parse(self):
        try:
            self.game.parse_move('ag4')
        except InvalidMove:
            pass
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        try:
            self.game.parse_move('d3')
            raise Exception('Should Error')
        except InvalidMove:
            pass
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        try:
            self.game.parse_move('a0')
            raise Exception('Should Error')
        except InvalidMove:
            pass
        except:
            raise Exception('Should Error')
        self.assertEqual(self.game.parse_move('a1'),(0,0))

    def test_move(self):
        self.assertTrue(self.game.move(self.game.player_two, 'b1'))
        self.assertFalse(self.game.move(self.game.player_one, 'b1'))
        self.assertTrue(self.game.move(self.game.player_one, 'c1'))
        self.assertEqual(self.game.board(), bitarray('000100100'))

    def test_possible_moves(self):
        #self.game.reset()
        #print self.game.player_one
        self.assertEqual(self.game.possible_moves(), [0,1,2,3,4,5,6,7,8])
        self.assertTrue(self.game.move(self.game.player_two, 'b1'))
        self.assertTrue(self.game.move(self.game.player_one, 'c1'))
        self.assertEqual(self.game.possible_moves(), [0,1,2,4,5,7,8])

    def test_is_there_a_winning_move(self):
        self.game.player_two[0] = True
        self.game.player_two[2] = True
        result = self.game.is_there_a_winning_move(self.game.player_two, optional_block = -1)
        self.assertEqual(result, 1)
        self.game.player_one = bitarray('000000000') # machine
        self.game.player_two = bitarray('000000000') # opponent

    def test_move_that_results_with_two_winning_options(self):
        self.game.player_two[0] = True
        self.game.player_two[8] = True
        self.game.player_one[1] = True
        self.game.player_one[4] = True
        result = self.game.move_that_results_with_two_winning_options(self.game.player_two)
        #print self.game.player_two
        self.assertEqual(result,6)
        self.game.reset()
        self.game.player_two[2] = True
        self.game.player_two[6] = True
        self.game.player_one[1] = True
        self.game.player_one[4] = True
        result = self.game.move_that_results_with_two_winning_options(self.game.player_two)
        self.assertEqual(result,8)
        self.game.reset()
        self.game.player_two[2] = True
        self.game.player_two[6] = True
        self.game.player_one[1] = True
        self.game.player_one[2] = True
        result = self.game.move_that_results_with_two_winning_options(self.game.player_two)
        self.assertEqual(result,0)

    def test_most_winning_options(self):
        self.game.reset()
        self.game.player_two[0] = True
        self.game.player_two[1] = True
        self.game.player_one[2] = True
        self.game.player_one[4] = True
        best_move, win_count = self.game.most_winning_options(self.game.player_two)
        # This appears incorrect
        self.assertEqual(win_count, 2)
        self.assertEqual(best_move, 5)

    def test_row1_player_have_a_winner(self):
        self.game.player_one = bitarray('111000000')
        self.assertTrue(self.game.is_it_a_winner(self.game.player_one))
        self.game.player_one = bitarray('101000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))
        self.game.player_one = bitarray('001000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))
        self.game.player_one = bitarray('010000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))
        self.game.player_one = bitarray('011000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))
        self.game.player_one = bitarray('110000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))
        self.game.player_one = bitarray('000000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))

    def test_row2_player_have_a_winner(self):
        self.game.player_one = bitarray('000111000')
        self.assertTrue(self.game.is_it_a_winner(self.game.player_one))
        self.game.player_one = bitarray('101001000')
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))
        self.game.player_one = bitarray('001010000')
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))
        self.game.player_one = bitarray('011100000')
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))
        self.game.player_one = bitarray('110011000')
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))
        self.game.player_one = bitarray('110101000')
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))

    def test_row3_player_have_a_winner(self):
        self.game.player_one = bitarray('000000111')
        self.assertTrue(self.game.is_it_a_winner(self.game.player_one))

    def test_col1_player_have_a_winner(self):
        self.game.player_one = bitarray('100100100')
        self.assertTrue(self.game.is_it_a_winner(self.game.player_one))

    def test_col2_player_have_a_winner(self):
        self.game.player_one = bitarray('010010010')
        self.assertTrue(self.game.is_it_a_winner(self.game.player_one))

    def test_col3_player_have_a_winner(self):
        self.game.player_one = bitarray('001011001')
        self.assertTrue(self.game.is_it_a_winner(self.game.player_one))

    def test_diag1_player_have_a_winner(self):
        self.game.player_one = bitarray('001010101')
        self.assertTrue(self.game.is_it_a_winner(self.game.player_one))

    def test_diag2_player_have_a_winner(self):
        self.game.player_one = bitarray('101010001')
        self.assertTrue(self.game.is_it_a_winner(self.game.player_one))

    def test_no_player_have_a_winner(self):
        self.game.player_one = bitarray('011100101')
        #print self.game.is_it_a_winner(self.game.player_one)
        self.assertFalse(self.game.is_it_a_winner(self.game.player_one))

    def test_recurse_attack(self):
        """
        Lets see if we can beat it
        """
        self.game.reset()
        is_there_a_winner, game = self._recurse_attack(self.game)
        if is_there_a_winner is not False:
            try:
                print "The winner is"
                print 'player_one', game.player_one
                print 'player_two', game.player_two
            except:
                print "No winners"
                print 'player_one', game.player_one
                print 'player_two', game.player_two

    def _recurse_attack(self, tg):
#        print "recurse_level", self.recurse_level
        game = copy.deepcopy(tg)
        self.recurse_level += 1
        self.assertLess(self.recurse_level, 10)
        #print "level", self.recurse_level
        #print "player_one here", self.game.player_one
        #print "player_two here", self.game.player_two
        for move in range(0,9):
            reset_game = copy.deepcopy(game)
            if (game.player_one[move]==True) | (game.player_two[move]==True):
                continue
            game.player_two[move] = True
            self.assertFalse(game.is_it_a_winner(game.player_two))
            game.make_the_best_move()
            if game.is_it_a_winner(game.player_one):
                """Not a good move for player_two, as player_one wins. So try a different move"""
                game = copy.deepcopy(reset_game)
#                print "player one wins"
#                print "player one", game.player_one
#                print "player two", game.player_two
                continue
            """No winners so lets recurse another level"""
#            print "no_win"
#            print "player_one", game.player_one
#            print "player_two", game.player_two
            result, game = self._recurse_attack(game)
            self.assertFalse(result)
        return False, game

    def test_row1_win(self):
        self.game.player_one = bitarray('110000000')
        self.game.player_two = bitarray('000110000')
        self.game.move(self.game.player_one, 'a3')
        self.assertEqual((self.game.player_one, bitarray('111000000')), self.game.is_there_a_winner())

    def test_row2_win(self):
        self.game.player_one = bitarray('000111000')
        self.game.player_two = bitarray('110000000')
        self.assertEqual((self.game.player_one, bitarray('000111000')), self.game.is_there_a_winner())

    def test_row3_win(self):
        self.game.player_one = bitarray('000000111')
        self.game.player_two = bitarray('110000000')
        self.assertEqual((self.game.player_one, bitarray('000000111')), self.game.is_there_a_winner())

    def test_col1_win(self):
        self.game.player_one = bitarray('100100100')
        self.game.player_two = bitarray('010011000')
        self.assertEqual((self.game.player_one, bitarray('100100100')), self.game.is_there_a_winner())

    def test_col2_win(self):
        self.game.player_one = bitarray('010010010')
        self.game.player_two = bitarray('000101000')
        self.assertEqual((self.game.player_one, bitarray('010010010')), self.game.is_there_a_winner())

    def test_col3_win(self):
        self.game.player_one = bitarray('001011001')
        self.game.player_two = bitarray('010100010')
        self.assertEqual((self.game.player_one, bitarray('001001001')), self.game.is_there_a_winner())

    def test_diag1_win(self):
        self.game.player_one = bitarray('001010101')
        self.game.player_two = bitarray('100101010')
        self.assertEqual((self.game.player_one, bitarray('001010100')), self.game.is_there_a_winner())

    def test_diag2_win(self):
        self.game.player_one = bitarray('101010001')
        self.game.player_two = bitarray('010101010')
        self.assertEqual((self.game.player_one, bitarray('100010001')), self.game.is_there_a_winner())

    def test_no_win(self):
        self.game.player_one = bitarray('011100101')
        self.game.player_two = bitarray('100011000')
#        print self.game.is_there_a_winner()
        self.assertFalse(self.game.is_there_a_winner())

    def test_choose_move(self):
        empty = bitarray('000000000')
        self.game.player_one = bitarray('000000000')
        self.game.player_two = bitarray('000000000')
        index = 0
        for index in range(0,9):
            for move_x in range(0,9):
                if move_x%2:
                    self.game.choose_move(self.game.player_one, offset=index)
                else:
                    self.game.choose_move(self.game.player_two, offset=index)
                self.assertEqual(self.game.player_two & self.game.player_one, empty)
#            print "player_one", self.game.player_one
#            print "player_two", self.game.player_two
            self.game.player_one = bitarray('000000000')
            self.game.player_two = bitarray('000000000')

if __file__ == "__main__":
    unittest.main()


