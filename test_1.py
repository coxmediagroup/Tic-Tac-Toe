#! /usr/bin/env python
import copy
import pdb
import sys
import unittest
from unittest import TestCase
from game import TicTacToe, InvalidMove
from bitarray import bitarray
from time import sleep
from optparse import OptionParser

verbose = False


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
        self.game.machine = bitarray('100100100')
        self.game.opponent = bitarray('010010010')
        self.assertEqual(bitarray('100100100') | bitarray('010010010'), self.game.board())

    def test_reset(self):
        self.game.machine = bitarray('100100100')
        self.game.opponent = bitarray('010010010')
        self.assertEqual(bitarray('100100100') | bitarray('010010010'), self.game.board())
        self.game.reset()
        self.assertEqual(bitarray('000000000'), self.game.machine)
        self.assertEqual(bitarray('000000000'), self.game.opponent)

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
        self.assertEqual(self.game.parse_move('a1'), (0, 0))

    def test_move(self):
        self.assertTrue(self.game.move(self.game.opponent, 'b1'))
        self.assertFalse(self.game.move(self.game.machine, 'b1'))
        self.assertTrue(self.game.move(self.game.machine, 'c1'))
        self.assertEqual(self.game.board(), bitarray('000100100'))

    def test_possible_moves(self):
        #self.game.reset()
        #print self.game.machine
        self.assertEqual(self.game.possible_moves(), [0, 1, 2, 3, 4, 5, 6, 7, 8])
        self.assertTrue(self.game.move(self.game.opponent, 'b1'))
        self.assertTrue(self.game.move(self.game.machine, 'c1'))
        self.assertEqual(self.game.possible_moves(), [0, 1, 2, 4, 5, 7, 8])

    def test_is_there_a_winning_move(self):
        self.game.opponent[0] = True
        self.game.opponent[2] = True
        result = self.game.is_there_a_winning_move(self.game.opponent, optional_block=-1)
        self.assertEqual(result, 1)
        self.game.machine = bitarray('000000000')   # machine
        self.game.opponent = bitarray('000000000')   # opponent

    def test_move_that_results_with_two_winning_options(self):
        self.game.opponent[0] = True
        self.game.opponent[8] = True
        self.game.machine[1] = True
        self.game.machine[4] = True
        result = self.game.move_that_results_with_two_winning_options(self.game.opponent)
        #print self.game.opponent
        self.assertEqual(result, 6)
        self.game.reset()
        self.game.opponent[2] = True
        self.game.opponent[6] = True
        self.game.machine[1] = True
        self.game.machine[4] = True
        result = self.game.move_that_results_with_two_winning_options(self.game.opponent)
        self.assertEqual(result, 8)
        self.game.reset()
        self.game.opponent[2] = True
        self.game.opponent[6] = True
        self.game.machine[1] = True
        self.game.machine[2] = True
        result = self.game.move_that_results_with_two_winning_options(self.game.opponent)
        self.assertEqual(result, 0)

    def test_most_winning_options(self):
        self.game.reset()
        self.game.opponent[0] = True
        self.game.opponent[1] = True
        self.game.machine[2] = True
        self.game.machine[4] = True
        best_move, win_count = self.game.most_winning_options(self.game.opponent)
        # This appears incorrect
        self.assertEqual(win_count, 2)
        self.assertEqual(best_move, 5)

    def test_row1_player_have_a_winner(self):
        self.game.machine = bitarray('111000000')
        self.assertTrue(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('101000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('001000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('010000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('011000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('110000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('000000000')
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('000000111')
        self.assertTrue(self.game.is_it_a_winner(self.game.machine))

    def test_row2_player_have_a_winner(self):
        self.game.machine = bitarray('000111000')
        self.assertTrue(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('101001000')
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('001010000')
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('011100000')
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('110011000')
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.machine = bitarray('110101000')
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))

    def test_row3_player_have_a_winner(self):
        self.game.machine = bitarray('000000111')
        self.assertTrue(self.game.is_it_a_winner(self.game.machine))

    def test_col1_player_have_a_winner(self):
        self.game.machine = bitarray('100100100')
        self.assertTrue(self.game.is_it_a_winner(self.game.machine))

    def test_col2_player_have_a_winner(self):
        self.game.machine = bitarray('010010010')
        self.assertTrue(self.game.is_it_a_winner(self.game.machine))

    def test_col3_player_have_a_winner(self):
        self.game.machine = bitarray('001011001')
        self.assertTrue(self.game.is_it_a_winner(self.game.machine))

    def test_diag1_player_have_a_winner(self):
        self.game.machine = bitarray('001010101')
        self.assertTrue(self.game.is_it_a_winner(self.game.machine))

    def test_diag2_player_have_a_winner(self):
        self.game.machine = bitarray('101010001')
        self.assertTrue(self.game.is_it_a_winner(self.game.machine))

    def test_no_player_have_a_winner(self):
        self.game.machine = bitarray('011100101')
        #print self.game.is_it_a_winner(self.game.machine)
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))

    def test_print_game(self):
        self.game.machine = bitarray('011100101')
        self.game.opponent = bitarray('100011000')
        state = self.game.print_game()
        test_against = [
            ['x', 'o', 'o'],
            ['o', 'x', 'x'],
            ['o', '-', 'o'],
        ]
        self.assertEqual(state, test_against)

    def test_recurse_attack(self):
        """
        Lets see if we can beat it
        """
        self.game.reset()
        is_there_a_winner, game = self._recurse_attack(self.game)
        try:
            self.games = game.games
        except AttributeError:
            pass
        self.games.append(game)
        if is_there_a_winner is not False:
            try:
                print "The winner is"
                print 'machine', game.machine
                print 'opponent', game.opponent
            except:
                print "No winners"
                print 'machine', game.machine
                print 'opponent', game.opponent

    def _recurse_attack(self, tg, level=0):
#        print "recurse_level", self.recurse_level
        game = copy.deepcopy(tg)
        self.games = []
        recurse_level = 1 + level
        self.assertLess(self.recurse_level, 10)
        #print "level", self.recurse_level
        #print "machine here", self.game.machine
        #print "opponent here", self.game.opponent
        moves = range(0, 9)
        if level == 0:
            moves = (0, 1, 4)
        for move in moves:
            reset_game = copy.deepcopy(game)
            if (game.machine[move] == True) | (game.opponent[move] == True):
                continue
            game.opponent[move] = True
            sleep(5)
            if verbose == True:
                print "opponents move"
                game.print_game()
            try:
                self.assertFalse(game.is_it_a_winner(game.opponent))
            except:
                import pdb
                pdb.set_trace()
            if len(game.possible_moves()) == 0:
                if verbose == True:
                    print "draw"
                game = copy.deepcopy(reset_game)   # should step back 2 moves
                continue
            game.make_the_best_move()
            if game.is_it_a_winner(game.machine):
                """Not a good move for opponent, as machine wins. So try a different move"""
                if verbose == True:
                    print "machine wins"
                    game.print_game()
                game = copy.deepcopy(reset_game)
                continue
            """No winners so lets recurse another level"""
            result, game = self._recurse_attack(game, level=recurse_level)
            try:
                self.games += game.games
            except AttributeError:
                pass
            self.games.append(game)
            game = copy.deepcopy(reset_game)
            self.assertFalse(result)
        if verbose == True:
            print "no more moves"
            game.print_game()
        return False, game

    def test_move_c2(self):
        self.assertTrue(self.game.move(self.game.opponent, 'c2'))

    def test_corner_attack(self):
        self.game.move(self.game.opponent, 'a1')
        self.assertFalse(self.game.is_it_a_winner(self.game.opponent))
        self.game.make_the_best_move()
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.move(self.game.opponent, 'c3')
        self.assertFalse(self.game.is_it_a_winner(self.game.opponent))
        self.game.make_the_best_move()
        self.assertFalse(self.game.is_it_a_winner(self.game.machine))
        self.game.move(self.game.opponent, 'c1')
        self.assertFalse(self.game.is_it_a_winner(self.game.opponent))
        self.game.make_the_best_move()
        self.assertTrue(self.game.is_it_a_winner(self.game.machine))

    def test_row1_win(self):
        self.game.machine = bitarray('110000000')
        self.game.opponent = bitarray('000110000')
        self.game.move(self.game.machine, 'a3')
        self.assertEqual((self.game.machine, bitarray('111000000')), self.game.is_there_a_winner())

    def test_row2_win(self):
        self.game.machine = bitarray('000111000')
        self.game.opponent = bitarray('110000000')
        self.assertEqual((self.game.machine, bitarray('000111000')), self.game.is_there_a_winner())

    def test_row3_win(self):
        self.game.machine = bitarray('000000111')
        self.game.opponent = bitarray('110000000')
        self.assertEqual((self.game.machine, bitarray('000000111')), self.game.is_there_a_winner())
        self.game.opponent = bitarray('100000111')
        self.assertTrue(self.game.is_it_a_winner(self.game.opponent))

    def test_col1_win(self):
        self.game.machine = bitarray('100100100')
        self.game.opponent = bitarray('010011000')
        self.assertEqual((self.game.machine, bitarray('100100100')), self.game.is_there_a_winner())

    def test_col2_win(self):
        self.game.machine = bitarray('010010010')
        self.game.opponent = bitarray('000101000')
        self.assertEqual((self.game.machine, bitarray('010010010')), self.game.is_there_a_winner())

    def test_col3_win(self):
        self.game.machine = bitarray('001011001')
        self.game.opponent = bitarray('010100010')
        self.assertEqual((self.game.machine, bitarray('001001001')), self.game.is_there_a_winner())

    def test_diag1_win(self):
        self.game.machine = bitarray('001010101')
        self.game.opponent = bitarray('100101010')
        self.assertEqual((self.game.machine, bitarray('001010100')), self.game.is_there_a_winner())

    def test_diag2_win(self):
        self.game.machine = bitarray('101010001')
        self.game.opponent = bitarray('010101010')
        self.assertEqual((self.game.machine, bitarray('100010001')), self.game.is_there_a_winner())

    def test_no_win(self):
        self.game.machine = bitarray('011100101')
        self.game.opponent = bitarray('100011000')
#        print self.game.is_there_a_winner()
        self.assertFalse(self.game.is_there_a_winner())

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-v", "--verbose",
        action="store_true", dest="verbose",
        help="Print additional messages to the user", default=False)
    (options, args) = parser.parse_args()
    if options.verbose == True:
        verbose = True

    unittest.main()
