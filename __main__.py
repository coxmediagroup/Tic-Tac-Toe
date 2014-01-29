#!/usr/bin/env python

# =========================
# = Tic-Tac-Toe Challenge =
# =========================

# Main script to test Board class via CLI
import curses
from Board import Board

def main(screen):
    
    b = Board()
    
    # screen = curses.newwin(height, width, begin_y, begin_x)
    screen.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    
    while True:
        
        screen.clear()
        
        begin_x = 20
        begin_y = 30
        height = 0
        width = 0
        
        screen = curses.newwin(begin_x, begin_y, height, width)
        
        screen.border(0)
        
        # Title
        screen.addstr(0, 1, ' Code Challenge ')
        
        # Help
        screen.addstr(2, 2, 'q = quit')
        
        # Score Board
        screen.addstr(4, 2, 'Player 1 = {}'.format(0))
        screen.addstr(5, 2, 'Player 2 = {}'.format(0))
        screen.addstr(6, 2, 'Draw     = {}'.format(0))
        screen.addstr(7, 2, '------------------------'.format(0))
        
        # Raw Board
        screen.addstr(10, 2,  '[X]|   | O '.format(0))
        screen.addstr(11, 2,  '--- --- ---'.format(0))
        screen.addstr(12, 2,  '   |[X]| O '.format(0))
        screen.addstr(13, 2,  '--- --- ---'.format(0))
        screen.addstr(14, 2,  '   |   |[X]'.format(0))
        
        # key key event value
        key_event = screen.getch()
        
        # quit game
        if key_event == ord("q"):
            break
        

if __name__ == "__main__":
    curses.wrapper(main)