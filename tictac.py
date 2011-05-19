#!/usr/bin/env python

from itertools import combinations
import logging, random, collections

# This is the winning combinations
winning=[0,1,2,3,4,5,6,7,8,0,3,6,1,4,7,2,5,8,0,4,8,2,4,6]
spots = range(0,9)

def printboard():
    '''Utility function to display the state as an ascii-art game board.'''
    print '\n'.join([
        ' %s | %s | %s',
        '-----------',
        ' %s | %s | %s',
        '-----------',
        ' %s | %s | %s',
    ]) % tuple(spots)


def moveHandler(board,spots,winning,player,n):
    print winning
    # set X for player one, or O for player 2
    if player==1:
            check="X"
    else:   
            check="O"
            
    # Remove block from spaces array
    spots[n] = check
    
    #for s in spots:
    #    print type(s)
    
    #print [pos for pos in spots if isinstance(pos, int )]

    # Replace block with check mark in board
    board=board.replace(str(n),check)

    # Replace space with check mark in checkboard array
    for c in range(len(winning)):
        #print winning
        if winning[c]==n:
            winning[c]=check

    # Run the checkwinner function
    status = winner(winning,check)
    return board,status
            
def playing(player):
    '''display the correct player'''
    if player == 'x':
        return 'o'
    return 'x'

def whoplayed(player):
    '''let'\s find out who played last'''
    pass
    
def winner(winning,check):
    '''Set the array element variables'''
    x,y,z=0,1,2

    # Loop through to check winner
    while x<=21:
        combo = [winning[x],winning[y],winning[z]]
        print combo

        # If we have three 'X' or 'O' we have a winner
        if combo.count(check) == 3:
                status =1
                break
        else:
                status =0

        # Loop through the next combo
        x+=3
        y+=3
        z+=3
        
    return status

def game(player):
    try:
        key = int(raw_input('\n\nPlayer ' + str(player) + ': Please select a space numbered (0,8) '))
        # Check if block is used.
        while spots.count(key)==0:
            print "\nInvalid Space"
            key=game(player)
    except:
        print "Invalid Space"
        key = game(player)
    return key


# The game (no not the one on BET!)
while True:
    player = len(spots)%2 +1
    if player == 1:
            player = 2
    else:
            player =1
    
    board = str(printboard())
    key = game(player)
    board,status =moveHandler(board,spots,winning,player,key)

    if status == 1:
            print '\n\nPlayer ' + str(player) + ' is the winner!!!'
            print board
            break
    elif len(spots)==0:
            print "No more spaces left. Game ends in a TIE!!!"
            print board
            break
    else:
            continue

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4