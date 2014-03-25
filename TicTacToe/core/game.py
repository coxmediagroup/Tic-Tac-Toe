# Copyright (C) 2014 Ryan Hansen.  All rights reserved.
# This source code (including its associated software) is owned by Ryan Hansen and
# is protected by United States and international intellectual property law, including copyright laws, patent laws,
# and treaty provisions.

import itertools

from core.const import PLAYERS, WIN_VECTORS


class Game(object):
    x = []
    o = []

    def available(self):
        moves = []
        p = 0
        for p in range(0, 9):
            if p not in self.x and p not in self.o:
                moves.append(p)
            p += 1
        return moves

    def take(self, player, pos):
        attr = self.__getattribute__(PLAYERS[player])
        attr.append(pos)

    def move(self, player, board, depth, score):
        for i in range(8):
            pass

    def win(self, player):
        # check x
        attr = self.__getattribute__(PLAYERS[player])
        for p in itertools.permutations(attr, 3):
            if p in WIN_VECTORS:
                return p
        return False