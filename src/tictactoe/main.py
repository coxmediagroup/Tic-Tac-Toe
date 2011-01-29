'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski
'''

import sys

from game import Game

def main():
    #TODO: Get player choice X/O
    game = Game()
    game.start()
    
    while not game.is_over():
        #Play the game
        pass
    
    return 0

if __name__ == '__main__':
    sys.exit(main())