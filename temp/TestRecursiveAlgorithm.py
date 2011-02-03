#!/usr/bin/env python
# encoding: utf-8
"""
TestRecursiveAlgorithm.py

Created by Fredrick Stakem on 2011-01-31.
Copyright (c) 2011 __Stakem Research__. All rights reserved.
"""

import sys
import os
import copy


class Node(object):
   
    def __init__(self, position=0, state=[], score=0, links=[]):
        self.position = position
        self.state = state
        self.score = score
        self.links = links
        
    def __str__(self):
        return str(self.position) + " :: " + str(self.score)
        
def foo(current_state, player):
    open_positions = findRemainingPositions(current_state)
    if len(open_positions) == 1:
        position = open_positions.pop()
        new_state = copy.deepcopy(current_state)
        new_state[position] = player
        score = 0
        if ( player == 'x' and testForWinner(new_state, 'x') == True ) or \
           ( player =='o' and testForWinner(new_state, 'o') == True ):
            score = 1
        elif ( player == 'x' and testForWinner(new_state, 'o') == True ) or \
             ( player =='o' and testForWinner(new_state, 'x') == True ):
            score = -1
        node = Node(position, new_state, score)
        return [node]

    nodes = []
    for position in open_positions:
        new_state = copy.deepcopy(current_state)
        new_state[position] = player
        new_player = None
        if player == 'x':
            new_player = 'o'
        else:
            new_player = 'x'
        links = foo(new_state, new_player)
        score = 1
        for link in links:
            if link.score < score:
                score == link.score
        node = Node(position, new_state, score, links)
        nodes.append(node)
    
    return nodes

def findRemainingPositions(current_state):
    open_positions = []
    for i, state in enumerate(current_state):
        if state == '-':
            open_positions.append(i)
    return open_positions
    
def testForWinner(state, player):
    if state[0] == player and state[1] == player and state[2] == player:
        return True
    elif state[0] == player and state[4] == player and state[8] == player:
        return True
    elif state[0] == player and state[3] == player and state[6] == player:
        return True
    elif state[2] == player and state[4] == player and state[6] == player:
        return True
    elif state[2] == player and state[5] == player and state[8] == player:
        return True
    elif state[3] == player and state[4] == player and state[5] == player:
        return True
    elif state[6] == player and state[7] == player and state[8] == player:
        return True
    elif state[1] == player and state[4] == player and state[7] == player:
        return True
    
    return False
     
if __name__ == '__main__':
    state = [ 'x', '-', '-',
              '-', 'o', '-',
              '-', '-', '-' ]
    a = foo(state, 'x')

