#! /usr/bin/env python
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
    player_one = bitarray('000000000')
    player_two = bitarray('000000000')

    def board(self):
        return self.player_one | self.player_two

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
                return self.player_one
            if (win & self.player_two)==win:
                return self.player_two
        return False

    def choose_move(self, player):
        '''simplest solution first, find the first empty cell'''
        for a_index in range(0, len(player)):
            if self.board()[a_index] is False:
                player[a_index] = True
                return True
        return False #no moves left

class TitTacToeTest(TestCase):
    '''Test the game '''

    def setUp(self):
        self.game = TicTacToe()

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

    def test_row1_win(self):
        self.game.player_one = bitarray('110000000')
        self.game.player_two = bitarray('000110000')
        self.game.move(self.game.player_one, 'a3')
        self.assertEqual(self.game.player_one, self.game.is_there_a_winner())

    def test_row2_win(self):
        self.game.player_one = bitarray('000111000')
        self.game.player_two = bitarray('110000000')
        self.assertEqual(self.game.player_one, self.game.is_there_a_winner())

    def test_row3_win(self):
        self.game.player_one = bitarray('000000111')
        self.game.player_two = bitarray('110000000')
        self.assertEqual(self.game.player_one, self.game.is_there_a_winner())

    def test_col1_win(self):
        self.game.player_one = bitarray('100100100')
        self.game.player_two = bitarray('010011000')
        self.assertEqual(self.game.player_one, self.game.is_there_a_winner())

    def test_col1_win(self):
        self.game.player_one = bitarray('010010010')
        self.game.player_two = bitarray('000101000')
        self.assertEqual(self.game.player_one, self.game.is_there_a_winner())



    def test_basic(self):
        self.assertEquals(1+1, 2)

def main():
    test_Basic()

if __file__ == "__main__":
    unittest.main()


