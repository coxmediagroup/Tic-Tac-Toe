#!/usr/bin/python
import sys

layout = [0,1,2,3,4,5,6,7,8]

def board():
    
    print " %s | %s | %s" % (layout[0], layout[1], layout[2])
    print "-----------"
    print " %s | %s | %s" % (layout[3], layout[4], layout[5])
    print "-----------"
    print " %s | %s | %s" % (layout[6], layout[7], layout[8])
    print " "

def challenger_move(pos):

    if layout[pos] != pos:
        return False
    layout[pos] = 'X'
    return True

def choose_position():
    position = raw_input('Choose your position: ')
    
    if not position.isdigit():
        print 'ERROR: Choose a layout number.'
    
    elif int(position) not in range(0,9):
        print 'ERROR: Invalid Position.'

    else:
        '''
        - check if the move is valid
        - weigh in for the best option
        - make a counter move based on the best option
        '''
        challenger_move(int(position))

def main():
    counter = 1
    while counter == 1:
        board()
        choose_position()

if __name__ == "__main__":
    sys.exit(main())