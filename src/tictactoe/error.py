'''
Created on Feb 4, 2011

@author: Krzysztof Tarnowski (krzysztof.tarnowski@ymail.com)
'''

import engine

class InvalidGameState(Exception):
    ''' Signals invalid game state.
    
    Attributes:
        state: The state that is invalid.
        valid_states: A list of valid state values.
    
    Class attributes:
        _MESSAGE: Message format for pretty-printing.
    '''

    _MESSAGE = 'Invalid state: {0}. Expected one of {1}'
    _STATE_TO_STR = {
                        engine.NOT_STARTED: 'NOT_STARTED',
                        engine.IN_PROGRESS: 'IN_PROGRESS',
                        engine.P1_WON: 'P1_WON',
                        engine.P2_WON: 'P2_WON',
                        engine.DRAW: 'DRAW'
                     }

    def __init__(self, state, valid_states):
        ''' Constructor.
        
        Args:
            state: Invalid state.
            valid_states: A list of valid state values.
        '''
        
        self.state = state
        self.valid_states = valid_states
        
        valid_states_str = [self._STATE_TO_STR[valid_state] for valid_state in valid_states]
        
        Exception.__init__(self, self._MESSAGE.format(self._STATE_TO_STR[state], valid_states_str))
        

class InvalidMove(Exception):
    ''' Signals an attempt to play invalid _move.
    
    Attributes:
        _move: Illegal _move that was played.
        legal_moves: A list of expected values/moves - tuples (x, y)
        
    Class attributes:
        _MESSAGE: Message format for pretty-printing.
    '''
    
    _MESSAGE = 'Invalid _move: {0}. Expected one of {1}.'
    
    def __init__(self, move, legal_moves):
        ''' 
        
        Args:
            _move: Illegal _move.
            legal_moves: A list of legal moves.
        '''
        
        self._move = move
        self.lega_moves = legal_moves
        Exception.__init__(self, self._MESSAGE.format(move, legal_moves))
