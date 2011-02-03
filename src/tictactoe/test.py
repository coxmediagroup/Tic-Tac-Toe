'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''
import unittest
import numpy

from engine import *
import util

class GameEngineTest(object):
    
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
        ''' '''
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
        ''' '''
        for scenario in scenarios:
            board = scenario['board']
            expected_state = scenario['expected_state']
            
            state = self._engine.get_state(board)
            
            self.assertEqual(state, expected_state, 
                             self._MESSAGE_STATE_TEST.format(self._STATE_NAMES[expected_state],
                                                  self._STATE_NAMES[state], 
                                                  util.board_to_str(board)))
    
    def test_state_evaluation(self):
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
    
    def setUp(self):
        self._engine = NegamaxEngine()
        
class RulesBasedEngineTest(unittest.TestCase, GameEngineTest):
    
    def setUp(self):
        self._engine = RulesBasedEngine()
        
    def test_play_win(self):
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