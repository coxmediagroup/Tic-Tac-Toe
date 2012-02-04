#!/usr/bin/python
# Bernhardt, Russell
# russell.bernhardt@gmail.com
""" This module contains semi-graphical elements and controls drawing the
screen.
"""

import os
from engine import TTTEngine, TTTError

""" Slightly override TTTBoard to add UI methods.
"""
class GameUI(TTTEngine):
    
    """ Clears the screen and redraws the current board layout.
    """ 
    def redrawScreen(self):
        # WARNING: untested on Windows:
        _,cols = os.popen('stty size', 'r').read().split()
        print '\n' * int(cols)
        
        # draw the gameboard
        print '''
           %s  |  %s  |  %s
         -----------------
           %s  |  %s  |  %s
         -----------------
           %s  |  %s  |  %s
         ''' % tuple(self.board)


# starter -- not ideal here, but not sure where else to put it yet.
game = GameUI()
game.redrawScreen()
in_play = True
while( in_play ):
    var = raw_input(
        'Enter the number of an open space or "q" to quit: '
    )

    if var == 'q':
        print 'Thanks for playing!'
        in_play = False
        
    elif var.isdigit() and len(var) == 1:
        try:
            game.applyMove( int(var) - 1 )
        
        except TTTError as e:
            print e.message
            _ = raw_input('Press ENTER to try again...')
            
        except TTTEndGame as e:
            print e.message
            in_play = False
        
        game.applyMove( game.getBestMove() )
        game.redrawScreen()
        
    else:
        # invalid input
        print 'Please enter either a single digit or the letter "q"...'

