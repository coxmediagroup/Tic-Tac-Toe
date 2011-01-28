#!/usr/bin/python
from itertools import combinations
import sys

layout = [0,1,2,3,4,5,6,7,8]
available = [0,1,2,3,4,5,6,7,8]
definition = [8,1,6,3,5,7,4,9,2]

winning_position = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6]
]

winning_sum = 15
corners = [0,2,6,8]
challenger_path = []
computer_path = []

def board():
    print " "
    print "  %s  |  %s  |  %s" % (layout[0], layout[1], layout[2])
    print "-----|-----|----"
    print "  %s  |  %s  |  %s" % (layout[3], layout[4], layout[5])
    print "-----|-----|----"
    print "  %s  |  %s  |  %s" % (layout[6], layout[7], layout[8])
    print " "

def is_winning(pos, sign):
    possibilities = [i for i in winning_position if pos in i]
    
    winner = [True for i in possibilities 
              if layout[i[0]] == layout[i[1]] == layout[i[2]] == sign]
    
    if not available:
        board()
        sys.exit('Draw.')
    
    if winner:
        board()
        if sign == 'X':
            print 'You won.'
        else:
            print 'You lost. Sorry.'
        sys.exit()
    return False

def get_highest_value():
    big_to_small = sorted(definition, reverse=True)
    
    for i in big_to_small:
        
        if layout[definition.index(i)] in available:
            return definition.index(i)
    
def make_a_move(pos, sign='X'):
    layout[pos] = sign
    available.remove(pos)
    
    if sign == 'X':
        challenger_path.append(pos)
    else:
        computer_path.append(pos)
    is_winning(pos, sign)
    return True

def available_corner():
    
    for i in corners:
        if i in available:
            return i

def counter_move(pos):
    # available = [i for i, v in enumerate(layout) if i == v]
    options = []
    best_chances = None
    value = None
    
    if layout[4] == 4:
        value = 4
    
    elif len(challenger_path) < 2 and challenger_path[0] == 4:
        value = available_corner()
    
    else:
        combine_computer = combinations(computer_path, 2)
        combine_challenger = combinations(challenger_path, 2)
        
        for x in combine_computer:
            diff =  winning_sum - (definition[x[0]] + definition[x[1]])
            options.append(diff)
        
        for x in combine_challenger:
            diff =  winning_sum - (definition[x[0]] + definition[x[1]])
            options.append(diff)
        
        priority = sorted(options)
        
        for i in priority:
            
            try:
                y = definition.index(i)
                
                if y in available:
                    best_chances = y
                    break
            except:
                pass
        
        if best_chances:
            value = best_chances
        
        else:
            
            if get_highest_value():
                value = get_highest_value()
            
            else:
                value = available[0]
    make_a_move(value, 'O')

def choose_position():
    position = raw_input('Choose your position: ')
    
    if not position.isdigit():
        print 'ERROR: Choose a layout number.'
    
    elif int(position) not in range(0,9):
        print 'ERROR: Invalid Position.'

    else:

        if not make_a_move(int(position), 'X'):
            print 'ERROR: That position has been filled'
        else:
            counter_move(int(position))

def main():
    counter = 1
    while counter == 1:
        board()
        choose_position()

if __name__ == "__main__":
    sys.exit(main())