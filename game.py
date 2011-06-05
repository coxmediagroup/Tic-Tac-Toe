#!/usr/bin/env python

import board

def main():
    import os, sys
    b = board.Board()
    players = board.players
    current_player = 0
    winner = None
    movers = (
        get_human_move,
        get_human_move,
    )
    while b.available_moves() and not winner:
        current_move = movers[current_player]()
        b.move(players[current_player], current_move)
        winner = b.winner()
        current_player = (current_player + 1) % 2
    if winner:
        print 'The winner is: %s' % winner
    else:
        print 'There was no winner.'

def get_human_move():
    raise NotImplementedError('Please implement get_human_move().')

def get_computer_move():
    raise NotImplementedError('Please implement get_computer_move().')

if __name__ == '__main__':
    main()
