#!/usr/bin/env python

import board

def main():
    import os, sys
    b = board.Board()
    players = board.players
    player_number = 0
    winner = None
    movers = (
        get_human_move,
        get_human_move,
    )
    possible_moves = b.available_moves()
    while possible_moves and not winner:
        player = players[player_number]
        current_move = movers[player_number](b, player, possible_moves)
        b.move(player, current_move)
        winner = b.winner()
        player_number = (player_number + 1) % 2
        possible_moves = b.available_moves()
    print b
    if winner:
        print 'The winner is: %s' % winner
    else:
        print 'There was no winner.'

def get_human_move(current_board, player, possible_moves):
    while True:
        print current_board
        try:
            move = int(raw_input('Please enter your move %s: ' % possible_moves))
        except ValueError:
            print 'Please enter a number for your move.'
            continue
        if move not in possible_moves:
            print 'Sorry, %s is not available.  Please try again.' % move
            continue
        return move

def get_computer_move(current_board, player, possible_moves):
    raise NotImplementedError('Please implement get_computer_move().')

if __name__ == '__main__':
    main()
