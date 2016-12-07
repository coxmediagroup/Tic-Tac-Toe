from itertools import combinations

import random
import sys

class TicTacToe(object):
    '''
    A tictactoe game that will let user chooses to be an X or an O.
    '''
    def __init__(self):
        '''
        Set default values
        '''
        self.layout = [0,1,2,3,4,5,6,7,8]
        self.available = [0,1,2,3,4,5,6,7,8]
        self.definition = [8,1,6,3,5,7,4,9,2]
        self.corners = [0,2,6,8]

        self.winning_position = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        self.winning_sum = 15

        self.players = ['X', 'O']
        self.challenger = None
        self.computer = None
        self.challenger_path = []
        self.computer_path = []
        self.finished = False
    
    def get_highest_value(self):
        '''
        Based on self.definition, the winning sum for all position is 15.
        So, this function will check which ones are closer to winning sum.
        '''
        big_to_small = sorted(self.definition, reverse=True)

        for i in big_to_small:

            if self.layout[self.definition.index(i)] in self.available:
                return self.definition.index(i)
    
    def who_wins(self):
        '''
        Check who won based on pre-defined winning position possibilities.
        '''
        for i in self.winning_position:
            
            if self.layout[i[0]] == self.layout[i[1]] == self.layout[i[2]]:
                self.finished = True
                return self.layout[i[0]]
        
        if not self.available:
            self.finished = True
            return True
        
        return False
    
    def make_a_move(self, pos, sign='X'):
        '''
        This function is the actual position assignment. When that spot is filled,
        remove them from the available choices.
        '''
        self.layout[pos] = sign
        self.available.remove(pos)

        if sign == self.challenger:
            self.challenger_path.append(pos)
        else:
            self.computer_path.append(pos)
        self.who_wins()
        return pos
    
    def counter_move(self, sign='X'):
        '''
        This is the main AI of computer moves. It will check (hopefully) every possibilities
        to either win or draw.
        '''
        if not self.available:
            return False
        options = []
        value = None
        
        # when the computer goes first, make sure the centered square is filled
        if self.computer == 'X' and self.layout[4] == 4:
            value = 4
        
        # when the computer is defending, check if the fist move is on a corner,
        # or an edge. If it was on a corner, fill the centered square, else,
        # the computer will choose the spot beside it.
        elif len(self.challenger_path) < 2 and self.computer == 'O':
            options = [i for i in self.corners if i in self.available]
            
            if self.challenger_path[0] not in self.corners:
                
                for i in options:
                    if i + 1 == self.challenger_path[0] or i -1 == self.challenger_path:
                        value = i
                        break
            else:
                value = 4
        
        # when the computer is on offense, grab the centered square. However,
        # if it is already filled, choose any of available corners.
        elif len(self.challenger_path) < 2 and self.computer == 'X':
            
            if self.layout[4] == 4:
                value = 4
            else:
                value = [i for i in self.corners if i in self.available][0]

        else:
            # as the game goes on, the computer will calculate priorities
            # on which spots have the biggest chance to win. Winning is preferred
            # when there are options between winning and blocking.
            try:
                combine_computer = combinations(self.computer_path, 2)
            
            except ValueError:
                combine_computer = []
            
            try:
                combine_challenger = combinations(self.challenger_path, 2)
            
            except ValueError:
                combine_computer = []

            for x in combine_computer:
                diff =  self.winning_sum - (self.definition[x[0]] + 
                        self.definition[x[1]])
                options.append({'pos': diff, 
                                'remain': self.winning_sum - diff})

            for x in combine_challenger:
                diff =  self.winning_sum - (self.definition[x[0]] + 
                        self.definition[x[1]])
                options.append({'pos': diff, 
                              'remain': self.winning_sum - diff})
            priority = sorted(options, key=lambda x: x['remain'])
            
            for i in priority:

                try:
                    y = self.definition.index(i['pos'])

                    if y in self.available:
                        value = y
                        break

                except:
                    pass
            else:
                # if it cannot find any priority, it will check which ones
                # are closer to winning. If it cannot find any, just choose the
                # first one available on the board, since at this point, the aim
                # is only for a draw. 
                if self.get_highest_value():
                    value = self.get_highest_value()

                else:
                    value = self.available[0]
        return self.make_a_move(value, sign)