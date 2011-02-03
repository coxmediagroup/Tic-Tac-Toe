'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski (krzysztof.tarnowski@ymail.com)
'''

import sys

import util
import engine
from game import Game

def read_move():
    ''' Reads user move from STDIN.
    
    The method expects the input to be formated as "x, y".

    Currently no sanity checks are performed.
    
    Returns:
        A two-item list representing field to capture. For example [0, 0].
    '''
    #TODO(krzysztof.tarnowski@ymail.com): Sanitize the input 
    sys.stdout.write('Your move [x, y]: ')
    move = [int(c) for c in sys.stdin.readline().split(',')]
    return move

def main():
    ''' Entry method of the Tic-Tac-Toe application. '''
    sys.stdout.write('Cross or nought? [default: O]: ')
    player_choice = sys.stdin.readline().strip().upper()
    human = (player_choice == 'X') and engine.P1 or engine.P2
    
    game = Game()
    game.start()
    
    # Print the board only if human player plays the 'X'
    if human == engine.P1:
        print(util.board_to_str(game.board))
    
    while not game.is_over():
        if game.player == human:
            move = read_move()
        else:
            move = None
        
        # If the move is None, get move from AI engine
        game.play(move)

        print(util.board_to_str(game.board))
    
    message = ['The game is over. ']
    
    if game.is_draw():
        message.append('It\'s a draw!')
    else:
        if game.has_cross_won():
            message.append('Player 1 has won!')
        else:
            message.append('Player 2 has won!')
            
    print(''.join(message))
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
