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

file = open("output.txt","w")

class Node(object):
   
    def __init__(self, position=0, state=[], score=0, links=[]):
        self.position = position
        self.state = state
        self.score = score
        self.links = links
        
    def __str__(self):
        return " " + str(self.state[0]) + " | " + str(self.state[1]) + " | " + str(self.state[2]) + "\n" + \
               " " + str(self.state[3]) + " | " + str(self.state[4]) + " | " + str(self.state[5]) + "\n" + \
               " " + str(self.state[6]) + " | " + str(self.state[7]) + " | " + str(self.state[8]) + "\n" + \
               str(self.score) +  "\n\n"
        
def foo(current_state, ai_player, current_player):
    open_positions = findRemainingPositions(current_state)
    
    if len(open_positions) == 1:
        position = open_positions.pop()
        new_state = copy.deepcopy(current_state)
        new_state[position] = current_player
        score = 0
        if ( ai_player == 'x' and testForWinner(new_state, 'x') == True ) or \
           ( ai_player =='o' and testForWinner(new_state, 'o') == True ):
            score = 1
        elif ( ai_player == 'x' and testForWinner(new_state, 'o') == True ) or \
             ( ai_player =='o' and testForWinner(new_state, 'x') == True ):
            score = -1
        node = Node(position, new_state, score)
        file.write( str(node) )
        return [node]

    nodes = []
    for position in open_positions:
        new_state = copy.deepcopy(current_state)
        new_state[position] = current_player
        score = 0
        if ( ai_player == 'x' and testForWinner(new_state, 'x') == True ) or \
           ( ai_player =='o' and testForWinner(new_state, 'o') == True ):
            score = 1
        elif ( ai_player == 'x' and testForWinner(new_state, 'o') == True ) or \
             ( ai_player =='o' and testForWinner(new_state, 'x') == True ):
            score = -1
        links = []
        if score == 0:
            score = 1
            next_player = None
            if current_player == 'x':
                next_player = 'o'
            else:
                next_player = 'x'
            links = foo(new_state, ai_player, next_player)
            for link in links:
                if link.score < score:
                    score = link.score
        else:
            node = Node(position, new_state, score, links)
            file.write( str(node) )
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
    a = foo(state, 'x', 'x')
    
file.close()
