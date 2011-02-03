'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''
import unittest
import numpy

from engine import *
import util

class GameEngineTest(object):
    
    _MESSAGE = 'Expected {0}, got {1}.\n{2}'
    _STATE_NAMES = { 
                        P1_WON: 'player 1 (X) win',
                        P2_WON: 'player 2 (O) win',
                        DRAW: 'draw',
                        IN_PROGRESS: 'in progress'
                    }
    
    def setUp(self):
        self._engine = None
        
    def _run_go_scenarios(self, scenarios):
        pass
    
    def _run_state_scenarios(self, scenarios):

        for scenario in scenarios:
            board = scenario['board']
            expected_state = scenario['expected_state']
            
            state = self._engine.get_state(board)
            
            self.assertEqual(state, expected_state, 
                             self._MESSAGE.format(self._STATE_NAMES[expected_state],
                                                  self._STATE_NAMES[state], 
                                                  util.board_to_str(board)))        

    def test_go_for_win(self):
        pass
    
    def test_got_for_block(self):
        pass
    
    def test_go_for_fork(self):
        pass
    
    def test_go_for_fork_block(self):
        pass
    
    def test_go_for_center(self):
        pass
    
    def test_go_for_opposite_corner(self):
        pass
    
    def test_go_for_empty_corner(self):
        pass
    
    def test_go_for_empty_side(self):
        pass
    
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
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()