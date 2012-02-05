#!/usr/bin/python
# Bernhardt, Russell
# russell.bernhardt@gmail.com

""" This module contains semi-graphical elements and controls drawing the
screen.
"""

import os
from engine import TTTEngine, TTTError, TTTEndGame

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


# starter -- not ideal here, but not sure where else to put it.
game = GameUI()
game.redrawScreen()
in_play = True
while( in_play ):
    var = raw_input('Enter the number of an open space or "q" to quit: ')

    if var == 'q':
        print 'Thanks for playing!'
        in_play = False
        
    elif var.isdigit() and len(var) == 1 and int(var) > 0:
        try:
            game.applyMove( int(var) - 1 )
            game.applyMove( game.getBestMove() )
            game.redrawScreen()
        
        except TTTError as e:
            print str(e)
            _ = raw_input('Press ENTER to try again...')
            game.redrawScreen()
            
        except TTTEndGame as e:
            # draw the screen one last time so you can actually see the result
            game.redrawScreen()
            print str(e)
            in_play = False
        
    else:
        # invalid input
        print 'Please enter either a single digit or the letter "q"...'

