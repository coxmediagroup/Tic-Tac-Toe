#!/usr/bin/env python

# =========================
# = Tic-Tac-Toe Challenge =
# =========================

# Main script to test Board class via CLI
import curses
from Board import Board

def show_board(screen, board, line_number, number_view):
    
    row_separator = (u'--- ' * board.COLS).strip()
    
    i = 0
    for row in board.board:
        line = ''
        for space in row:
            if number_view:
                value = space.board_index
            else:
                value = space.player
            line += ' {} |'.format(value)
        line = line.strip('|')
        screen.addstr(line_number, 2, line)
        line_number += 1
        if i < (board.ROWS -1):
            screen.addstr(line_number, 2, row_separator)
            line_number += 1
        i += 1
    
    return line_number

def main(screen):
    
    b = Board(P0=' ')
    
    # screen = curses.newwin(height, width, begin_y, begin_x)
    screen.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    
    # toggle state
    number_view = False
    line = 0
    
    while True:
        
        screen.clear()
        begin_x = 20; begin_y = 30
        height = 1; width = 2
        screen = curses.newwin(begin_x, begin_y, height, width)
        screen.border(0)
        
        # Title
        screen.addstr(0, 1, ' Code Challenge ')
        
        # Score Board
        screen.addstr(2, 2, 'Player 1 = {}'.format(0))
        screen.addstr(3, 2, 'Player 2 = {}'.format(0))
        screen.addstr(4, 2, 'Draw     = {}'.format(0))
        
        # Divider
        screen.addstr(5, 2, '-' * (begin_y - 4))
        
        line_number = 8
        line_number = show_board(screen, b, line_number, number_view)
        
        # Error Messages
        # curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        # screen.addstr(16, 2, ' Error Message Here! '.format(0), curses.color_pair(1))
        
        # Player input or notice
        
        
        # Help section
        screen.addstr(16, 2, '-' * (begin_y - 4))
        screen.addstr(17, 2, 'n = number view')
        screen.addstr(18, 2, 'q = quit')
        
        
        # key events
        key_event = screen.getch()
        
        # quit game
        if key_event == ord("q"):
            break
            
        # toggle view numbers
        elif key_event == ord("n"):
            screen.clear()
            if number_view:
                number_view = False
            else:
                number_view = True
        

if __name__ == "__main__":
    curses.wrapper(main)