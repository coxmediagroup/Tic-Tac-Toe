# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'
import unittest
import random

from coxtactoe import tictactoe as ttt
from coxtactoe import const as C
from coxtactoe.exceptions import InvalidMoveError

import logging as log
log.basicConfig(level=log.INFO)


class BoardTests(unittest.TestCase):
    def setUp(self):
        self._ = ttt.Marker()
        self.x = ttt.Marker('X')
        self.o = ttt.Marker('O')
        self.board = ttt.Board()

    def test_board_initializes(self):
        self.assertIsInstance(self.board, ttt.Board)
        self.assertEqual(repr(self.board), '[_, _, _, _, _, _, _, _, _]')

    def test_board_cast_to_int(self):
        board_int = int(self.board)
        self.assertIs(type(board_int), int)
        self.assertEquals(board_int, 0)

    def test_board_len(self):
        board_length_in_bits = self.board.SQUARES * self.board.BITS_PER_SQUARE
        self.assertEquals(len(self.board), board_length_in_bits)

    def test_board_bits(self):
        self.assertEquals(self.board.bits, '000000000000000000')

    def test_board_key(self):
        self.assertEquals(self.board.key, 0)
        self.board.place(self.x, 0)
        self.assertEquals(self.board.key, 1)
        self.board.place(self.o, 1)
        self.assertEquals(self.board.key, 9)

    def test_board_reset(self):
        initial_board = self.board
        self.board.place(self.x, 0)
        self.board.reset()
        self.assertEquals(self.board, initial_board)

    def test_board_square_offset(self):
        for i in range(self.board.SQUARES):
            offset = self.board.square_offset(i)
            self.assertEquals(offset, (i * self.board.BITS_PER_SQUARE))

    def test_board_square_mask(self):
        b = self.board
        self.assertEquals(b.offset_mask(0),  int('000000000000000011', base=2))
        self.assertEquals(b.offset_mask(2),  int('000000000000001100', base=2))
        self.assertEquals(b.offset_mask(4),  int('000000000000110000', base=2))
        self.assertEquals(b.offset_mask(6),  int('000000000011000000', base=2))
        self.assertEquals(b.offset_mask(8),  int('000000001100000000', base=2))
        self.assertEquals(b.offset_mask(10), int('000000110000000000', base=2))
        self.assertEquals(b.offset_mask(12), int('000011000000000000', base=2))
        self.assertEquals(b.offset_mask(14), int('001100000000000000', base=2))
        self.assertEquals(b.offset_mask(16), int('110000000000000000', base=2))

    def test_initial_board_squares_are_unmarked(self):
        for i in range(self.board.SQUARES):
            marker = self.board.square(i)
            self.assertIsInstance(marker, ttt.Marker)
            self.assertEquals(marker, C._)
            self.assertEquals(repr(marker), '_')
            self.assertEquals(marker.bits, '00')

    def test_placing_markers_on_board(self):
        for m in self.x, self._, self.o:
            for i in range(self.board.SQUARES):
                self.board.turn = m
                self.board.place(m, i)
                marker = self.board.square(i)
                self.assertIsInstance(marker, ttt.Marker)
                self.assertEquals(marker, m)
                self.assertEquals(repr(marker), repr(m))
                self.assertEquals(marker.bits, m.bits)

    def test_placing_marker_in_occupied_square_raises_error(self):
        self.board.place(self.x, 0)
        self.board.place(self.o, 4)
        for marker in self.x, self.o:
            self.assertRaises(InvalidMoveError, self.board.place, marker, 0)
            self.assertRaises(InvalidMoveError, self.board.place, marker, 4)

    def test_no_winner(self):
        self.assertIsNone(self.board.winner)

    def _winner_across(self, player, across=0):
        opponent = player.opponent
        opponent_offset = 1 if across < 2 else -1
        self.board.place(player, 3 * across)
        self.board.place(opponent, 3 * (across + opponent_offset))
        self.board.place(player, 3 * across + 1)
        self.board.place(opponent, 3 * (across + opponent_offset) + 1)
        self.board.place(player, 3 * across + 2)
        self.assertEquals(self.board.winner, player)

    def test_winner_is_x_on_first_row(self):
        self._winner_across(self.x, 0)

    def test_winner_is_x_on_second_row(self):
        self._winner_across(self.x, 1)

    def test_winner_is_x_on_third_row(self):
        self._winner_across(self.x, 2)

    def test_winner_is_o_on_first_row(self):
        self._winner_across(self.x, 0)

    def test_winner_is_o_on_second_row(self):
        self._winner_across(self.x, 1)

    def test_winner_is_o_on_third_row(self):
        self._winner_across(self.x, 2)

    def test_playing_a_random_choice_game(self):
        log.debug("In test_playing_a_random_choice_game()")
        game_state = self.board.SQUARES * [self._]
        marker = self.x
        squares_available = range(self.board.SQUARES)

        while squares_available:
            log.debug("  squares_available: %r" % squares_available)
            log.debug("  game_state: %r" % game_state)
            # Place marker on an available square
            square = random.choice(squares_available)
            log.debug("  square: %r" % square)
            squares_available.remove(square)
            self.board.place(marker, square)
            # Update what game state should look like
            game_state[square] = marker
            if self.board.game_over:
                break
            # Next player's turn
            marker = self.o if marker == self.x else self.x

        self.assertEquals(repr(self.board), repr(game_state))


