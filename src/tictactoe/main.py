'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''

import sys

import util
import engine
from game import Game

def read_move():
    ''' doc '''
    sys.stdout.write('Your move [x, y]: ')
    move = [int(c) for c in sys.stdin.readline().split(',')]
    return move

def main():
    ''' doc '''
    sys.stdout.write('Cross or nought? [default: O]: ')
    player_choice = sys.stdin.readline().strip().upper()
    human = (player_choice == 'X') and engine.P1 or engine.P2
    
    game = Game()
    game.start()
    print(util.board_to_str(game.board))
    
    while not game.is_over():
        if game.player == human:
            move = read_move()
        else:
            move = None
        
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