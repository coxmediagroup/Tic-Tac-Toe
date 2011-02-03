'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski (krzysztof.tarnowski@ymail.com)
'''
import unittest

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
    '''
    
    _MESSAGE_STATE_TEST = 'Expected {0}, got {1}.\n{2}'

    _STATE_NAMES = { 
                        P1_WON: 'player 1 (X) win',
                        P2_WON: 'player 2 (O) win',
                        DRAW: 'draw',
                        IN_PROGRESS: 'in progress'
                    }
    
    _MESSAGE_PLAY_TEST = 'Expected one of {0}, got {1}.\n{2}'
    
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
                               'board': *numpy array of arrays with values
                                         P1, P2 or EMPTY*,
                               'expected_state': *either P1_WON, P2_WON or DRAW*
                           }        
        '''
        
        for scenario in scenarios:
            board = scenario['board']
            expected_state = scenario['expected_state']
            
            state = self._engine.get_state(board)
            
            self.assertEqual(state, expected_state, 
                             self._MESSAGE_STATE_TEST.format(self._STATE_NAMES[expected_state],
                                                  self._STATE_NAMES[state], 
                                                  util.board_to_str(board)))
    
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

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
