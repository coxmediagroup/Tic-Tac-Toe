'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''

import numpy

import engine
from error import InvalidGameState
from error import InvalidMove


class Game(object):
    ''' This class encapsulates generic game logic and its interfaces.

    Attributes:
        _engine: Game engine to use for calculating the next move.
        _state: The current game state. Can be either NO_STARTED, IN_PROGRESS,
                P1_WON or P2_WON.
        board: Numpy two dimensional array representing Tic-Tac-Toe's game
               board. Valid values for fields are P1, P2 and EMPTY. By default
               the board is filled with EMPTY values upon creation.
        player: Tells which player should make the next move.
    '''

    def __init__(self, game_engine=engine.RulesBasedEngine()):
        ''' Constructor.

        Player 1 (P1) is the first one to make a move at the beginning
        of the game.

        Args:
            game_engine: Specifies the game engine to use. Default is the
            rules-based engine.
        '''
        self._engine = game_engine
        self._state = engine.NOT_STARTED
        self.board = numpy.zeros((3, 3), dtype=numpy.int16)
        self.player = engine.P1

    def start(self):
        ''' Initializes the Tic-Tac-Toe game.

        Raises:
            InvalidGameState: The game is in invalid state.
        '''

        if self._state != engine.NOT_STARTED:
            raise InvalidGameState(self._state, [engine.IN_PROGRESS])

        self._state = engine.IN_PROGRESS

    def reset(self):
        ''' Resets the game. '''
        self.__init__()

    def play(self, move=None, game_engine=None):
        ''' Makes a move

        Args:
            move: Move to make. If None is given, either internal game engine
                  or passed game engine instance is used to generate the next
                  move. Default is None.
            game_engine: Allows to override the game engine used in this turn.

        Raises:
            InvalidGameState: Game is not in progress, i.e. has either not
                                started or has ended.
            InvalidMove: The move is not valid for the current game state.
        '''

        if self._state != engine.IN_PROGRESS:
            raise InvalidGameState(self._state, [engine.IN_PROGRESS])

        game_engine = game_engine and game_engine or self._engine

        if move == None:
            move = game_engine.next_move(self.board, self.player)
        else:
            legal_moves = game_engine.get_legal_moves(self.board)
            if not move in legal_moves:
                raise InvalidMove(move, legal_moves)

        self.board[move[0], move[1]] = self.player
        self.player = game_engine.get_opponent(self.player)
        self._state = game_engine.get_state(self.board)

    def is_over(self):
        ''' Checks whether the game has ended.

        Returns: True if the game is in one of final states. False otherwise.
        '''

        return (self._state != engine.NOT_STARTED
                and self._state != engine.IN_PROGRESS)

    def is_draw(self):
        ''' Checks whether the game ended in a draw.

        Returns: True if the game ended in a draw.
        '''

        return self._state == engine.DRAW

    def has_cross_won(self):
        ''' Checks whether player 1 (X) has won the game.

        Returns: True if player 1 has won.
        '''

        return self._state == engine.P1_WON

    def is_valid(self, move):
        ''' Checks if the given move is legal for the current game state.

        Returns: True if the move is valid.
        '''

        return move in self._engine.get_legal_moves(self.board)
