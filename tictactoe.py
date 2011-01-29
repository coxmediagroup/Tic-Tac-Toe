from itertools import combinations

import random
import sys

class TicTacToe:
    
    def __init__(self):
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
    
    def board(self):
        print "  %s  |  %s  |  %s" % (self.layout[0], self.layout[1], self.layout[2])
        print "-----|-----|----"
        print "  %s  |  %s  |  %s" % (self.layout[3], self.layout[4], self.layout[5])
        print "-----|-----|----"
        print "  %s  |  %s  |  %s" % (self.layout[6], self.layout[7], self.layout[8])
    
    def get_highest_value(self):
        big_to_small = sorted(self.definition, reverse=True)

        for i in big_to_small:

            if self.layout[self.definition.index(i)] in self.available:
                return self.definition.index(i)
    
    def check_for_a_win(self, pos, sign):
        possibilities = [i for i in self.winning_position if pos in i]

        win = [True for i in possibilities 
               if self.layout[i[0]] == self.layout[i[1]] == self.layout[i[2]] == sign]

        if not self.available:
            self.board()
            sys.exit('Draw.')

        if win:
            self.board()

            if win[0] == self.challenger:
                sys.exit('You won.')
            else:
                sys.exit('You lost. Sorry.')
        return False

    def ask_for_position(self):
        try:
            position = raw_input('Choose your position: ')

            if not position.isdigit():
                print 'ERROR: Choose a layout number.'

            elif int(position) not in self.available:
                print 'ERROR: Invalid Position.'

            else:
                return int(position)
        except KeyboardInterrupt:
            sys.exit("\nBye.")
        return False
    
    def make_a_move(self, pos, sign='X'):
        self.layout[pos] = sign
        self.available.remove(pos)

        if sign == 'X':
            self.challenger_path.append(pos)
        else:
            self.computer_path.append(pos)
        self.check_for_a_win(pos, sign)
        return True
    
    def counter_move(self, sign='X'):
        options = []
        best_chances = None
        value = None

        if self.layout[4] == 4:
            value = 4

        elif len(self.challenger_path) < 2 and \
                 self.challenger_path[0] == 4:
            value = [i for i in self.corners if i in self.available][0]

        else:
            combine_computer = combinations(self.computer_path, 2)
            combine_challenger = combinations(self.challenger_path, 2)

            for x in combine_computer:
                diff =  self.winning_sum - (self.definition[x[0]] + 
                        self.definition[x[1]])
                options.append(diff)

            for x in combine_challenger:
                diff =  self.winning_sum - (self.definition[x[0]] + 
                        self.definition[x[1]])
                options.append(diff)

            priority = sorted(options)

            for i in priority:

                try:
                    y = self.definition.index(i)

                    if y in self.available:
                        best_chances = y
                        break

                except:
                    pass

            if best_chances:
                value = best_chances

            else:

                if self.get_highest_value():
                    value = self.get_highest_value()

                else:
                    value = available[0]
        self.make_a_move(value, sign)
    
    def play(self):
        '''
        
        '''
        while not self.finished:
            # use one of the corners if the computer has to make the first move
            if self.challenger_path == self.computer_path and \
                self.challenger == 'O':
                self.counter_move(self.computer)
            
            else:
                self.board()
                new_pos = self.ask_for_position()
                
                self.make_a_move(new_pos, self.challenger)
                self.counter_move(self.computer)

if __name__ == "__main__":
    game = TicTacToe()
    
    while not game.challenger:
        
        try:
            user_input = raw_input('Choose whether you want to be an "X" or an "O": ')
        
            if user_input not in game.players:
                print 'ERROR: Please choose either "X" or "O"'
        
            else:
                game.challenger = user_input
                game.computer = [i for i in game.players if i != user_input][0]
                game.play()
        
        except KeyboardInterrupt:
            sys.exit("\nBye.")