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
        
        #first complete the center and corners then go with other slots
        self.best_moves = (4, 0, 2, 6, 8, 1, 3, 5, 7)
        
#based on game_state which is an array with size 9 containing only '0', 'o' and 'x', it returns tuple (best move, game_is_finished). 
    def next_move(self,game_state):
        empty_slots = self.__find_empty_slots(game_state)
        # if any position making win
        for slot in empty_slots:
            game_state[slot] = self.type
            if(self.check_win(game_state)!=-1):
                return (slot,1);
            game_state[slot] = '0'
        #take an action to prevent the other play being win
        for slot in empty_slots:
            game_state[slot] = self.opponent_type
            if(self.check_win(game_state)!=-1):
                return (slot,0)
            game_state[slot] = '0'
        #find one of the other left moves based on the priority which I gave in best_moves 
        for slot in self.best_moves:
            if game_state[slot]== '0':
                game_state[slot]= self.type
                return (slot,0)
        return (-1,0)

# takes a game state and returns the positions having '0'
    def __find_empty_slots(self,game_state):
        return [i for i in range(len(game_state)) if game_state[i]=='0']
    