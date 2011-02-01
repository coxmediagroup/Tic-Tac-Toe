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
   
    def __init__(self, position=0, score=0, links=[]):
        self.position = position
        self.score = score
        self.links = links
        
def foo(current_state, player):
    open_positions = findRemainingPositions(current_state)
    print "Open positions: " + str(open_positions)
    if len(current_state) == 1:
        new_state = copy.deepcopy(currentState)
        new_state[position] = player
        return [Node(open_positions.pop())]

    nodes = []
    for i, position in enumerate(open_positions):
        new_state = copy.deepcopy(current_state)
        new_state[position] = player
        new_player = None
        if player == 'x':
            new_player = 'o'
        else:
            new_player = 'x'
        links = foo(new_state, new_player)
        node = Node(position, 0, links)
        nodes.append(node)
    
    return nodes

def findRemainingPositions(current_state):
    open_positions = set()
    for i, state in enumerate(current_state):
        if state == '-':
            open_positions.add(i)
    return open_positions

if __name__ == '__main__':
    state = [ 'x', '-', '-',
              '-', 'o', '-',
              '-', '-', '-' ]
    a = foo(state, 'x')

