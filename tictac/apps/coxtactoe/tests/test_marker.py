# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'
import unittest

from apps.coxtactoe import tictactoe as ttt
from apps.coxtactoe import const as C

import logging as log
log.basicConfig(level=log.INFO)


class MarkerTests(unittest.TestCase):
    def setUp(self):
        self._ = ttt.Marker('_')
        self.x = ttt.Marker('X')
        self.o = ttt.Marker('O')

    def test_marker_initializes(self):
        _ = self._
        self.assertIsInstance(_, ttt.Marker)
        self.assertEquals(_, C._)
        self.assertEquals(repr(_), '_')
        self.assertEquals(_.bits, '00')

    def test_x_marker_initializes(self):
        x = self.x
        self.assertIsInstance(x, ttt.Marker)
        self.assertEquals(repr(x), 'X')
        self.assertEquals(x.bits, '01')
        self.assertEquals(x, C.X)

    def test_o_marker_initializes(self):
        o = self.o
        self.assertIsInstance(o, ttt.Marker)
        self.assertEquals(repr(o), 'O')
        self.assertEquals(o.bits, '10')
        self.assertEquals(o, C.O)

    def test_marker_initializes_with_base_2(self):
        _ = ttt.Marker('00', base=2)
        x = ttt.Marker('01', base=2)
        o = ttt.Marker('10', base=2)
        self.assertEquals(_, self._)
        self.assertEquals(x, self.x)
        self.assertEquals(o, self.o)

    def test_marker_init_only_accepts_valid_values(self):
        self.assertRaises(ValueError, ttt.Marker, '0')
        self.assertRaises(ValueError, ttt.Marker, 'z')
        self.assertRaises(ValueError, ttt.Marker, '.')
        self.assertRaises(ValueError, ttt.Marker, -1)
        self.assertRaises(ValueError, ttt.Marker, 3)
        self.assertRaises(ValueError, ttt.Marker, '00')
        self.assertRaises(ValueError, ttt.Marker, '01')
        self.assertRaises(ValueError, ttt.Marker, '10')

    def test_marker_opponent(self):
        self.assertIsNone(self._.opponent)
        self.assertEquals(self.o, self.x.opponent)
        self.assertEquals(self.x, self.o.opponent)