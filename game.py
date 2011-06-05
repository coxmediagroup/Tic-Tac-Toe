#!/usr/bin/env python

import board

WIN = 1
LOSE = -1
DRAW = 0

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
            move = int(
                raw_input('Please enter your move %s: ' % possible_moves)
            )
        except ValueError:
            print 'Please enter a number for your move.'
            continue
        if move not in possible_moves:
            print 'Sorry, %s is not available.  Please try again.' % move
            continue
        return move

def get_computer_move(current_board, player, possible_moves):
    raise NotImplementedError('Please implement get_computer_move().')

def analyze_board(subject_board, player_number):
    '''Find the possible outcomes for each move.'''
    spaces = subject_board.available_moves()
    results = [None] * 9
    for space in spaces:
        temp_board = subject_board.copy()
        temp_board.move(board.players[player_number], space)
        if temp_board.winner():
            results[space] = WIN
        elif not temp_board.available_moves():
            results[space] = DRAW
        else:
            # If the other player can force a win, this is a losing
            # possibility for us.  If the other player can force a draw,
            # this branch is also a draw for us.  Otherwise, we can force
            # a win.
            other_player = (player_number + 1) % 2
            union = set(analyze_board(temp_board, other_player))
            results[space] = -max(union)
    return results

if __name__ == '__main__':
    main()
