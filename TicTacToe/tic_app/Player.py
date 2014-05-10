'''
Created on May 9, 2014

@author: reza
'''
from __builtin__ import super
#an abstract class represented an agent in the real world.
class Agent:
    def __init__(self,game_state,type): 
        self.game_state = game_state;
        self.type = type;
        self.opponent_type = 'o' if self.type == 'x' else 'x'    
        self.win_states = ((1,4,7),(2,5,8),(3,6,9),(1,2,3),(4,5,6),(7,8,9),(1,5,9),(3,5,7))
    def check_win(self,game_state):
        for state in self.win_states:
            try:
                if game_state[state[0]-1]!='0' and game_state[state[0]-1]== game_state[state[1]-1] and game_state[state[1]-1]== game_state[state[2]-1]:
                    return game_state[state[0]-1];
            except:
                pass
        return -1;
    def next_move(self,game_state):
        pass
    
#an ai agent class which has some kind of intelligent to play tic-tac-toe
class AIAgent(Agent):
    def __init__(self,game_state,type):
        Agent.__init__(self,game_state,type)
