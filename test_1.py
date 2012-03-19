#! /usr/bin/env python
import copy
import pdb
import sys
import unittest
from unittest import TestCase
from bitarray import bitarray
from exceptions import Exception

row_wins = (bitarray('111000000'), bitarray('000111000'), bitarray('000000111'))
col_wins = (bitarray('100100100'), bitarray('010010010'), bitarray('001001001'))
diag_wins =(bitarray('100010001'), bitarray('001010100'))

wins = row_wins + col_wins + diag_wins
row_dict = {'a':0, 'b':3, 'c': 6}
col_dict = {'1': 0, '2':2, '3':2}

class InvalidMove(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class TicTacToe(object):
    ''' This is the Game
    '''
    player_one = bitarray('000000000') # machine
    player_two = bitarray('000000000') # opponent
    blank_board =  bitarray('000000000')

    def board(self):
        return self.player_one | self.player_two

    def reset(self):
        self.player_one = bitarray('000000000') # machine
        self.player_two = bitarray('000000000') # opponent

    def parse_move(self, move):
        try:
            return row_dict[move[0]], col_dict[move[1]]
        except:
            raise InvalidMove(move)

    def move(self, player, move):
        row, col = self.parse_move(move)
        if self.board()[row+col]==True :
            return False
        player[row+col]=True
        return True

    def legal_move(self, move):
        row, col = self.parse_move(move)
        try:
            if self.board()[row+col]==False:
                return True
        except:
            return False
        return False

    def is_there_a_winner(self):
        for win in wins:
            if (win & self.player_one)==win:
                return self.player_one, win
            if (win & self.player_two)==win:
                return self.player_two, win
        return False

    def is_it_a_winner(self, player):
        """Does this player have a winner"""
        for win in wins:
            if (win & player)==win:
                return True
        return False

    def choose_move(self, player, offset=0):
        '''simplest solution first, find the first empty cell'''
        for a_index in range(0, len(player)):
            position = (a_index + offset) % 9
            if self.board()[position] is False:
                player[position] = True
                return True
        return False #no moves left

    def may_move_lead_to_win(self, move, player):
        '''check if all possible rows, columns or  diags are blocked
        '''
        pass

    def possible_moves(self, board=None):
        """What moves are available."""
        if board is None:
            board = self.board()
        choices = []
        for position in range(0, 9):
            if board[position]==False:
                choices.append(position)
        return choices

    def is_there_a_winning_move(self, player, optional_block = -1):
        """If there is such a move return it. Otherwise return false."""
        t_play = player
        pos = self.possible_moves()
        for position in pos:
            if position == optional_block:
                continue
            t_play[position] = True
            if self.is_it_a_winner(t_play):
                t_play[position] = False
                return position
            t_play[position] = False
        return False

    def move_that_results_with_two_winning_options(self, player):
        """If there is such a move return it. Otherwise return false."""
        choices = self.possible_moves()
        count = 0
        for choice in choices:
            player[choice] = True
            result = self.is_there_a_winning_move(player)
            if result is not False:
                count += 1
                """Check for another winning play using this move"""
                result = self.is_there_a_winning_move(player, result)
                if result is not False:
                    player[choice] = False
                    return choice
            player[choice] = False
        return False

    def wins_for_position(self, position):
        p_wins = []
        for w in wins:
            if w[position] == True:
                p_wins.append(w)
        return p_wins

    def most_winning_options(self, player):
        """
        player is opposing player
        """
        choices = self.possible_moves()
        win_count_for_choice = {}
        best = (choices[0], 0)
        for choice in choices:
            """find wins"""
            wins_for_choice = self.wins_for_position(choice)
            win_count = 0
            for w in wins_for_choice:
                if w & player==bitarray('000000000'):
                    win_count += 1
            if win_count>best[1]:
                best = (choice, win_count)
        return best

    def make_the_best_move(self):
        """Find the best possible move. Start by checking if there is a winning move for us"""
        #pdb.set_trace()
        result = self.is_there_a_winning_move(self.player_one)
        if result is not False:
            self.player_one[result] = True
            return result
        '''Check if opponent has a winning move, if so block it'''
        result = self.is_there_a_winning_move(self.player_two)
        if result is not False:
            self.player_one[result] = True
            return result
        '''Is there a move that gives two immediate chances to win'''
        result = self.move_that_results_with_two_winning_options(self.player_one)
        if result is not False:
            self.player_one[result] = True
            return result
        '''Does the opponent have a move that will give them two chance'''
        result = self.move_that_results_with_two_winning_options(self.player_two)
        if result is not False:
            self.player_one[result] = True
            return result
        '''Find the move that gives us the most chances to win and our opponent the least '''
        my_best_move, my_win_count = self.most_winning_options(self.player_two)
        opponents_best_move, opp_win_count = self.most_winning_options(self.player_two)
        if (my_win_count + opp_win_count)==0:
            return False
        if my_win_count>=opp_win_count:
            self.player_one[my_best_move] = True
            return (my_best_move, my_win_count)
        else:
            self.player_one[opponents_best_move] = True
            return (opponents_best_move, opp_win_count)

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

    def test_possible_moves(self):
        #self.game.reset()
        #print self.game.player_one
        self.assertEqual(self.game.possible_moves(), [0,1,2,3,4,5,6,7,8])

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

    def test_parse(self):
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

    def test_recurse_attack(self):
        """
        Lets see if we can beat it
        """
        self.game.reset()
        is_there_a_winner, game = self.recurse_attack(self.game)
        if is_there_a_winner is not False:
            try:
                print "The winner is"
                print 'player_one', game.player_one
                print 'player_two', game.player_two
            except:
                print "No winners"
                print 'player_one', game.player_one
                print 'player_two', game.player_two

    def recurse_attack(self, tg):
#        print "recurse_level", self.recurse_level
        game = copy.deepcopy(tg)
        self.recurse_level += 1
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
            result, game = self.recurse_attack(game)
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


