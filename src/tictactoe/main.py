'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''

import sys

from game import Game

def read_move():
    sys.stdout.write('Your move [x y]: ')
    move = [int(c) for c in sys.stdin.readline().split(',')]
    return move

def main():
    ''' doc '''
    sys.stdout.write('Cross or nought? [default: O]: ')
    player_choice = sys.stdin.readline().strip().upper()
    human = (player_choice == 'X') and Game.P1 or Game.P2
    
    game = Game()
    game.start()
    
    while not game.is_over():
        if game.get_turn() == human:
            move = read_move()
        else:
            move = None
        
        game.play(move)
    
    if game.is_draw():
        pass
    
    if game.has_cross_won():
        pass
    else:
        pass
    
    return 0

if __name__ == '__main__':
    sys.exit(main())