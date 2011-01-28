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
challenger_path = []
corners = [0,2,6,8]

def board():
    print " "
    print "  %s  |  %s  |  %s" % (layout[0], layout[1], layout[2])
    print "-----|-----|----"
    print "  %s  |  %s  |  %s" % (layout[3], layout[4], layout[5])
    print "-----|-----|----"
    print "  %s  |  %s  |  %s" % (layout[6], layout[7], layout[8])
    print " "

def make_a_move(pos, sign='X'):
    if layout[pos] != pos:
        return False
    layout[pos] = sign
    available.remove(pos)
    
    if not available:
        sys.exit('Done.')
    
    if sign == 'X':
        challenger_path.append(pos)
    return True

def available_corner():
    
    for i in corners:
        if i in available:
            return i

def counter_move(pos):
    # available = [i for i, v in enumerate(layout) if i == v]
    options = []
    best_chances = None
    
    if layout[4] == 4:
        make_a_move(4, 'O')
    
    elif len(challenger_path) < 2:
        
        make_a_move(available_corner(), 'O')
    
    else:
        
        combine_taken = combinations(challenger_path, 2)
        combine_available = combinations(available, 2)
        
        for x in combine_taken:
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
                # print available
                # make_a_move(layout[available[0]], 'O')
                # break
        
        if best_chances:
            value = best_chances
        
        else:
            
            if available_corner():
                value = available_corner()
            
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