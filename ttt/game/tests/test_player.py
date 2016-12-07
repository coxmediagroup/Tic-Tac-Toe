from django.test import TestCase

import unittest

import json

from game.models import *
from game.player import Computer

from datetime import datetime
from django.utils.timezone import utc


class ComputerTest(TestCase):
    def test_first_move_as_x(self):
        g = Game.create_new(is_user_x=False)
        move = Computer.determine_move(g, PLAYER_X, PLAYER_O)
        assert move == (1, 1)

    def test_first_move_as_o(self):
        g = Game.create_new(is_user_x=True)
        g[0][0] = PLAYER_X
        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (1, 1)

    def test_first_move_as_o_with_x_in_center(self):
        g = Game.create_new(is_user_x=True)
        g[1][1] = PLAYER_X
        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (0, 0)

    def test_vertical_block(self):
        g = Game.create_new(is_user_x=True)
        g[1][1] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (0, 0)
        g[move[0]][move[1]] = PLAYER_O

        g[1][0] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (1, 2)

    def test_horizontal_block(self):
        g = Game.create_new(is_user_x=True)
        g[1][1] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (0, 0)
        g[move[0]][move[1]] = PLAYER_O

        g[0][1] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (2, 1)

    def test_diagonal_block(self):
        g = Game.create_new(is_user_x=True)
        g[1][1] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (0, 0)
        g[move[0]][move[1]] = PLAYER_O

        g[2][0] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (0, 2)

    @unittest.expectedFailure
    def test_guaranteed_win_scenario(self):
        g = Game.create_new(is_user_x=False)
        move = Computer.determine_move(g, PLAYER_X, PLAYER_O)
        assert move == (1, 1)
        g[move[0]][move[1]] = PLAYER_X

        # any center border cell will do here
        # this first move by the opposite player guarantees a win
        g[0][1] = PLAYER_O

        # the next move should be in an adjacent corner
        move = Computer.determine_move(g, PLAYER_X, PLAYER_O)
        assert move == (0, 0) or move == (0, 2)
        g[move[0]][move[1]] = PLAYER_X

        # This move has created a potential win right away
        winning_move = g.winning_move(for_player=PLAYER_X)
        assert winning_move == (2, 0) or winning_move == (2, 2)

        g[winning_move[0]][winning_move[1]] = PLAYER_O

        # the computer's next move should be adjacent to his two previous plays
        move = Computer.determine_move(g, PLAYER_X, PLAYER_O)
        assert move == (1, 0) or move == (1, 2)

        #if we have gotten here, then we know the algorithms are working
