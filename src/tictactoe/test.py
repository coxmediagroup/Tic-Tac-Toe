#!/usr/bin/env python
'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski (krzysztof.tarnowski@ymail.com)
'''
import unittest
import copy

import util
from engine import *


class GameEngineTest(object):
    ''' Generic class for game engine tests.

    The class provides helper methods for running test scenarios given
    as dictionaries. For example:

        scenarios = [
                        {
                            'board': [],
                            'expected_value': 0
                        }
                    ]

    Attributes:
        _engine: Game engine tested by scenarios. Subclasses should set this
                 attribute in their setUp() method.

    Class attributes:
        _MESSAGE_STATE_TEST: String format for text printed in case the state
                             test fails for a scenario.

        _STATE_NAMES: Dictionary of print-friendly game state names.

        _MESSAGE_PLAY_TEST: String format for text printed in case the run
                            test fails for a scenario.

        _PLAYER_CHAR: Mapping player => character (X or O)

        _MESSAGE_UNBEATALBE_TEST: String format for text printed in case the
                                  test_unbeatable_{} fails.
    '''

    _MESSAGE_STATE_TEST = 'Expected {0}, got {1}.\n{2}'

    _STATE_NAMES = {
                        P1_WON: 'player 1 (X) win',
                        P2_WON: 'player 2 (O) win',
                        DRAW: 'draw',
                        IN_PROGRESS: 'in progress'
                    }

    _MESSAGE_PLAY_TEST = 'Expected one of {0}, got {1}.\n{2}'

    _PLAYER_CHAR = {P1: 'X', P2: 'O'}

    _MESSAGE_UBEATABLE_TEST = '''
    Computer lost when playing {0}.\nMove history: {1}.\n{2}
    '''

    def setUp(self):
        self._engine = None

    def _run_play_scenarios(self, scenarios):
        ''' Runs 'play' test scenarios.

        This method verifies whether the engine outputs expected values (move)
        for the specified board arrangements.

        Args:
            scenarios: A list of test scenarios given as dictionaries:

                           {
                               'board': *numpy array of arrays with values
                                         P1, P2 or EMPTY*,
                               'player': *current player: P1 or P2*,
                               'expected_moves': *list of moves given as
                                                  tuples (x, y)*
                           }
        '''

        for scenario in scenarios:
            board = scenario['board']
            player = scenario['player']
            expected_moves = scenario['expected_moves']

            move = self._engine.next_move(board, player)

            self.assertTrue(move in expected_moves,
                             self._MESSAGE_PLAY_TEST.format(expected_moves,
                                                  move,
                                                  util.board_to_str(board)))

    def _run_state_scenarios(self, scenarios):
        ''' Runs 'state' scenarios.

        This method verifies whether the engine correctly analyzes the current
        state of the game (board).

        Args:
            scenarios: A list of test scenarios given as dictionaries:

                           {
                               'board': numpy array of arrays with values
                                         P1, P2 or EMPTY,
                               'expected_state': either P1_WON, P2_WON or DRAW
                           }
        '''

        for scenario in scenarios:
            board = scenario['board']
            expected_state = scenario['expected_state']

            state = self._engine.get_state(board)
            msg = self._MESSAGE_STATE_TEST.format(
                             self._STATE_NAMES[expected_state],
                             self._STATE_NAMES[state],
                             util.board_to_str(board))

            self.assertEqual(state, expected_state, msg)

    def test_state_evaluation(self):
        ''' Tests game engine's game state/board evaluation. '''

        scenarios = [
                        {
                            'board': numpy.array([
                                                    [EMPTY, EMPTY, EMPTY],
                                                    [EMPTY, EMPTY, EMPTY],
                                                    [EMPTY, EMPTY, EMPTY],
                                                  ]),
                            'expected_state': IN_PROGRESS
                        },
                        {
                            'board': numpy.array([
                                                    [P1, P1, P1],
                                                    [P2, P2, P1],
                                                    [P2, P2, EMPTY],
                                                  ]),
                            'expected_state': P1_WON
                        },
                        {
                            'board': numpy.array([
                                                    [P1, P2, P1],
                                                    [P1, P1, P1],
                                                    [P2, P2, EMPTY],
                                                  ]),
                            'expected_state': P1_WON
                        },
                        {
                            'board': numpy.array([
                                                    [P1, P1, P2],
                                                    [P2, P2, P1],
                                                    [P1, P1, P1],
                                                  ]),
                            'expected_state': P1_WON
                        },
                        {
                            'board': numpy.array([
                                                    [P1, P1, P2],
                                                    [P1, P2, P1],
                                                    [P1, P2, P1],
                                                  ]),
                            'expected_state': P1_WON
                        },
                        {
                            'board': numpy.array([
                                                    [P1, P1, P2],
                                                    [P2, P1, P1],
                                                    [P2, P1, P1],
                                                  ]),
                            'expected_state': P1_WON
                        },
                        {
                            'board': numpy.array([
                                                    [P1, P2, P1],
                                                    [P2, P2, P1],
                                                    [P1, P1, P1],
                                                  ]),
                            'expected_state': P1_WON
                        },
                        {
                            'board': numpy.array([
                                                    [P1, P2, P1],
                                                    [P2, P1, P1],
                                                    [P2, P2, P1],
                                                  ]),
                            'expected_state': P1_WON
                        },
                        {
                            'board': numpy.array([
                                                    [P1, P2, P1],
                                                    [P2, P1, P2],
                                                    [P1, P2, P1],
                                                  ]),
                            'expected_state': P1_WON
                        },
                        {
                            'board': numpy.array([
                                                    [P1, P1, P2],
                                                    [P2, P2, P2],
                                                    [P1, P1, P1],
                                                  ]),
                            'expected_state': P2_WON
                        },
                        {
                            'board': numpy.array([
                                                    [P1, P1, P2],
                                                    [P2, P2, P1],
                                                    [P1, P2, P1],
                                                  ]),
                            'expected_state': DRAW
                        },
                     ]

        self._run_state_scenarios(scenarios)


class NegamaxEngineTest(unittest.TestCase, GameEngineTest):
    ''' Test case for Negamax game engine. '''

    def setUp(self):
        self._engine = NegamaxEngine()


class RulesBasedEngineTest(unittest.TestCase, GameEngineTest):
    ''' Test case for rules-based game engine. '''

    def setUp(self):
        self._engine = RulesBasedEngine()

    def test_play_win(self):
        ''' Tests whether the algorithm performs winning move. '''

        scenarios = [
                        {
                            'board': numpy.array([
                                                    [P1, EMPTY, EMPTY],
                                                    [P1, P2, P2],
                                                    [EMPTY, P2, P1],
                                                  ]),
                            'player': P1,
                            'expected_moves': [(2, 0)]
                        },
                        {
                            'board': numpy.array([
                                                    [P1, EMPTY, EMPTY],
                                                    [EMPTY, P2, EMPTY],
                                                    [EMPTY, P2, P1],
                                                  ]),
                            'player': P1,
                            'expected_moves': [(0, 1)]
                        },
                    ]
        self._run_play_scenarios(scenarios)

    def test_play_block(self):
        ''' Tests whether the algorithm attempts to blocks opponents win. '''

        scenarios = [
                        {
                            'board': numpy.array([
                                                    [P1, EMPTY, EMPTY],
                                                    [EMPTY, P2, P2],
                                                    [EMPTY, P2, P1],
                                                  ]),
                            'player': P1,
                            'expected_moves': [(0, 1), (1, 0)]
                        },
                        {
                            'board': numpy.array([
                                                    [P1, EMPTY, EMPTY],
                                                    [EMPTY, P2, EMPTY],
                                                    [EMPTY, P2, P1],
                                                  ]),
                            'player': P1,
                            'expected_moves': [(0, 1)]
                        },
                    ]
        self._run_play_scenarios(scenarios)

    def test_play_fork(self):
        ''' Tests whether the algorithm attempts to create fork. '''

        scenarios = [
                        {
                            'board': numpy.array([
                                                    [P1, EMPTY, P2],
                                                    [EMPTY, EMPTY, P1],
                                                    [EMPTY, P2, EMPTY],
                                                  ]),
                            'player': P1,
                            'expected_moves': [(1, 0)]
                        },
                        {
                            'board': numpy.array([
                                                    [P1, EMPTY, EMPTY],
                                                    [EMPTY, P2, EMPTY],
                                                    [EMPTY, EMPTY, P1],
                                                  ]),
                            'player': P1,
                            'expected_moves': [(2, 0), (0, 2)]
                        },
                    ]
        self._run_play_scenarios(scenarios)

    def test_unbeatable_cross(self):
        ''' Tests whether the engine is unbeatable given that it opens the
            game.

            This test recursively generates whole game tree, i.e. examines all
            possible moves for non-AI player.
        '''
        # TODO (krzysztof.tarnowski@ymail.com): Move to GameEngineTest later.
        # This test would take too long to finish for NegamaxEngine.

        board = numpy.zeros((3, 3), dtype=numpy.int16)

        self._run_unbeatable(board, [], P1, P2)

    def test_unbeatable_nough(self):
        ''' Tests whether the engine is unbeatable given that it plays nought.

            This test recursively generates whole game tree, i.e. examines all
            possible moves for non-AI player.
        '''
        # TODO (krzysztof.tarnowski@ymail.com): Move to GameEngineTest later.
        # This test would take too long to finish for NegamaxEngine.

        board = numpy.zeros((3, 3), dtype=numpy.int16)

        self._run_unbeatable(board, [], P1, P1)

    def _run_unbeatable(self, board, move_history, player, human):
        ''' Checks every possible game permutation for computer defeat.

        Args:
            board: The game board represented by numpy 3x3 array of arrays.
            move_history: An ordered list of tuples (x, y) representing moves.
            player: Current player.
            human: Human player.
        '''

        state = self._engine.get_state(board)
        if state != IN_PROGRESS:
            computer = self._engine.get_opponent(human)
            self.assertFalse(self._has_computer_lost(state, human),
                             self._MESSAGE_UBEATABLE_TEST
                             .format(self._PLAYER_CHAR[computer],
                                     move_history,
                                     util.board_to_str(board)))
            return

        if player == human:
            for move in self._engine.get_legal_moves(board):
                new_board = board.copy()
                new_move_history = copy.copy(move_history)

                new_move_history.append(move)
                new_board[move[0], move[1]] = player

                self._run_unbeatable(new_board, new_move_history,
                                     self._engine.get_opponent(player), human)
        else:
            move = self._engine.next_move(board, player)
            move_history.append(move)
            board[move[0], move[1]] = player

            self._run_unbeatable(board, move_history,
                                 self._engine.get_opponent(player), human)

    def _has_computer_lost(self, state, human):
        ''' Checks whether the computer has lost the game.

        Args:
            state: Game state.
            human: Human player (P1 or P2)

        Returns:
            True if computer has lost.
        '''

        if state == P1_WON and human == P1:
            return True
        if state == P2_WON and human == P2:
            return True

        return False


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
