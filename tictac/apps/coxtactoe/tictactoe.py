# -*- coding: utf-8 -*-
import uuid

from apps.coxtactoe import const as C
from apps.coxtactoe.exceptions import InvalidGameError, InvalidMoveError
from apps.coxtactoe.models import TicTacToeGameModel

import logging as log
log.basicConfig(level=log.INFO)


__docformat__ = 'restructuredtext en'


class Marker(int):
    """Implements Tic-Tac-Toe X, O, and empty markers"""
    _ = C._
    X = C.X
    O = C.O

    def __new__(cls, value=0, **kwargs):
        if value in ('00', '01', '10') and kwargs.get('base') is 2:
            pass
        elif value in ('', '_', cls._):
            value = cls._
        elif value in ('x', 'X', cls.X):
            value = cls.X
        elif value in ('o', 'O', cls.O):
            value = cls.O
        else:
            raise ValueError("Must be in ('', '_', 'X', 'O', 0, 1, 2) or in "
                             "('00', '01', '10') when using kwarg 'base=2'")
        return super(Marker, cls).__new__(cls, value, **kwargs)

    def __repr__(self):
        """Returns string representation of marker"""
        if self == self._:  return '_'  #00
        if self == self.X:  return 'X'  #01
        if self == self.O:  return 'O'  #10

    @property
    def bits(self):
        """Returns string representation of marker's binary value"""
        return "{0:0>2b}".format(self)

    @property
    def opponent(self):
        if self == self._:  return None
        if self == self.X:  return Marker(self.O)
        if self == self.O:  return Marker(self.X)


class Board(object):
    """Implements Tic-Tac-Toe board state, rules, and interaction

        Squares are numbered 0 through 8 going left to right, top to bottom:

             0 | 1 | 2
            ---+---+---
             3 | 4 | 5
            ---+---+---
             6 | 7 | 8

    """
    M = N = 3
    SQUARES = M * N
    BITS_PER_SQUARE = 2
    BIT_LEN = SQUARES * BITS_PER_SQUARE

    _ = C._
    X = C.X
    O = C.O

    def __init__(self, board=0, turn=Marker(X)):
        self.board = board
        self.initial_board = board
        self.win_masks = self._win_masks
        self.turn = turn

    def __repr__(self):
        return str([self.square(i) for i in range(self.SQUARES)])

    def __int__(self):
        return self.board

    def __len__(self):
        return self.BIT_LEN

    def __iter__(self):
        for item in ['%s' % repr(self.square(i)) for i in range(self.SQUARES)]:
            yield item

    @property
    def json(self):
        board = ['%s' % repr(self.square(i)) for i in range(self.SQUARES)]
        return '["%s"]' % '","'.join(board)

    @property
    def _win_masks(self):
        wins = {self.X: {'down': [], 'across': [], 'diagonal': []},
                self.O: {'down': [], 'across': [], 'diagonal': []}}

        # Shift down bit pattern by 2 to get every down bit pattern
        x_down = int('000001000001000001', base=2)  # [X,_,_,X,_,_,X,_,_]
        wins[self.X]['down'] = [x_down,
                                x_down << 1 * self.BITS_PER_SQUARE,
                                x_down << 2 * self.BITS_PER_SQUARE]
        # Shift across bit pattern by 6 to get every down bit pattern
        x_across = int('000000000000010101', base=2)  # [X,X,X,_,_,_,_,_,_]
        wins[self.X]['across'] = [x_across,
                                  x_across << 1 * self.BITS_PER_SQUARE * self.N,
                                  x_across << 2 * self.BITS_PER_SQUARE * self.N]
        # Diagonal bit patterns for X in squares 0, 4, 8 and 2, 4, 6
        wins[self.X]['diagonal'] = [int('010000000100000001', base=2),
                                    int('000001000100010000', base=2)]

        # Shift down bit pattern by 2 to get every down bit pattern
        o_down = o_down = x_down << 1  # [O,_,_,O,_,_,O,_,_]
        wins[self.O]['down'] = [o_down,
                                o_down << 1 * self.BITS_PER_SQUARE,
                                o_down << 2 * self.BITS_PER_SQUARE]
        # Shift across bit pattern by 6 to get every down bit pattern
        x_across = o_across = x_across << 1  # [O,O,O,_,_,_,_,_,_]
        wins[self.O]['across'] = [o_across,
                                  o_across << 1 * self.BITS_PER_SQUARE * self.N,
                                  o_across << 2 * self.BITS_PER_SQUARE * self.N]
        # Diagonal bit patterns for O in squares 0, 4, 8 and 2, 4, 6
        wins[self.O]['diagonal'] = [int('100000001000000010', base=2),
                                    int('000010001000100000', base=2)]
        return wins

    @property
    def key(self):
        return self.board

    @property
    def bits(self):
        return "{0:0>{width}b}".format(int(self), width=len(self))

    @property
    def winner(self):
        for player in (self.X, self.O):
            for direction, win_masks in self.win_masks[player].iteritems():
                for win_mask in win_masks:
                    if (int(self.board) & win_mask) == win_mask:
                        return Marker(player)
        return None

    @property
    def open_squares(self):
        return [s for s in range(self.SQUARES) if self.square(s) == self._]

    @property
    def game_over(self):
        if not self.open_squares:
            return True
        if self.winner is not None:
            return True
        return False

    def reset(self):
        """Resets game state for a new game"""
        self.turn = Marker(self.X)
        self.board = self.initial_board

    def offset_mask(self, square_offset):
        """Calculates offset mask for marker at ``square_offset``"""
        return 3 << square_offset

    def square_offset(self, square):
        """Calculates offset for marker bits at ``square``"""
        return (square * self.BITS_PER_SQUARE)

    def square(self, square):
        """Reads current marker at square"""
        offset = self.square_offset(square)
        mask = self.offset_mask(offset)
        return Marker((self.board & mask) >> offset)

    def place(self, marker, square):
        """Places ``marker`` at ``square`` on the game board"""
        if self.turn != marker:
            raise InvalidMoveError("It's not your turn.")

        square_marker = self.square(square)
        if square_marker != self._ and marker != self._:
            raise InvalidMoveError("{0} has already played at square {1}"
                                   .format(repr(square_marker), square))

        offset = self.square_offset(square)
        mask = self.offset_mask(offset)
        self.board = (~mask & self.board) | (marker << offset)
        if self.winner is None:
            self.turn = marker.opponent


class Game(object):
    def __init__(self, id=None):
        if id is not None:
            try:
                game = TicTacToeGameModel.objects.get(gid=id)
            except TicTacToeGameModel.DoesNotExist:
                raise InvalidGameError("Game ID %s does not exist." % id)
            else:
                self.board = Board(board=game.board, turn=Marker(game.turn))
                self.id = id
        else:
            self.id = uuid.uuid4().hex
            self.board = Board()
        self.player = self.board.turn

    @property
    def over(self):
        return self.board.game_over

    @property
    def winner(self):
        return self.board.winner

    def save(self):
        game, created = TicTacToeGameModel.objects.get_or_create(gid=self.id)
        game.turn = repr(self.board.turn)
        game.board = self.board.key
        game.save()

    def reset(self):
        """Resets game state for a new game"""
        self.board.reset()
