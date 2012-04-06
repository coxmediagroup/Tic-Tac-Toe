#!/usr/bin/python
# Bernhardt, Russell
# russell.bernhardt@gmail.com

""" This module contains semi-graphical elements and controls drawing the
screen.
"""

import os
from engine import TTTEngine, TTTError, TTTEndGame

# Add a UI method to TTTBoard.
class GameUI(TTTEngine):
    
    # Clears the screen and redraws the current board layout.
    def redraw_screen(self):
        if os.sys.platform == 'win32':
            print '\n' * 25 # cheat for Windows
            
        else:
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


# Launcher; not ideal here, but not sure where else to put it.
game = GameUI()
game.redraw_screen()
in_play = True
while( in_play ):
    var = raw_input('Enter the number of an open space or "q" to quit: ')

    if var == 'q':
        print 'Thanks for playing!'
        in_play = False
        
    elif var.isdigit() and len(var) == 1 and int(var) > 0:
        try:
            game.apply_move( int(var) - 1 )
            game.apply_move( game.get_best_move() )
            game.redraw_screen()
        
        except TTTError as e:
            print str(e)
            _ = raw_input('Press ENTER to try again...')
            game.redraw_screen()
            
        except TTTEndGame as e:
            # draw the screen one last time so you can actually see the result
            game.redraw_screen()
            print str(e)
            in_play = False
        
    else:
        # invalid input
        print 'Please enter either a single digit or the letter "q"...'

