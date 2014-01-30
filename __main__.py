#!/usr/bin/env python

# =========================
# = Tic-Tac-Toe Challenge =
# =========================

# Main script to test Board class via CLI
import curses
from Board import Board

def display(screen, line_number, msg, x_pos=2):
    screen.addstr(line_number, x_pos, msg)
    line_number += 1
    return line_number

def show_board(screen, board, line_number, number_view):
    
    row_separator = (u'--- ' * board.COLS).strip()
    
    i = 0
    for row in board.board:
        msg =  ''
        for space in row:
            if number_view:
                value = space.board_index
            else:
                value = space.player
            msg += '{}|'.format(str(value).center(3, ' '))
        msg = msg.strip('|')
        line_number = display(screen, line_number, msg)
        if i < (board.ROWS -1):
            line_number = display(screen, line_number, row_separator)
        i += 1
    
    return line_number

def main(screen):
    
    b = Board(P0=' ')
        
    # screen.keypad(1)
    # curses.noecho()
    
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    
    # game states
    number_view = False
    toggle_move_text = False
    this_player = None
    next_player = None
    game_width = 60
    line_separator = '-' * (game_width - 4)
    
    while True:
        
        screen.clear()
        line_number = 2
        
        
        # Title
        msg =  'Code Challenge'
        line_number = display(screen, line_number, msg)
        line_number += 1
        
        # Divider
        line_number = display(screen, line_number, line_separator)
        
        # Help section
        line_number = display(screen, line_number, 'n = number view')
        line_number = display(screen, line_number, 'q = quit')
        
        # Divider
        line_number = display(screen, line_number, line_separator)
        
        
        # spacer
        line_number += 1
        
        # Score Board
        msg = '"{}" (You)       = {}'.format(b.P1, b.P1_score)
        line_number = display(screen, line_number, msg)
        msg = '"{}" (Computer)  = {}'.format(b.P2, b.P2_score)
        line_number = display(screen, line_number, msg)
        msg = 'Draw            = {}'.format(b.P2_score)
        line_number = display(screen, line_number, msg)
        
        # spacer
        line_number += 1
        
        # Divider
        line_number = display(screen, line_number, line_separator)
        
        # Spacer
        line_number += 2
        
        # Show game Board
        line_number = show_board(screen, b, line_number, number_view)
        
        # spacing (if errors?)
        line_number += 2
        
        # Error Messages
        # curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        # screen.addstr(16, 2, ' Error Message Here! '.format(0), curses.color_pair(1))
        
        # Player input or notice
        if not this_player:
            player_query = "Who goes first? (1) Human, (2) Computer:"
            line_number = display(screen, line_number, player_query)
        else:
            msg = 'Turn: Player "{}"!'.format(this_player)
            line_number = display(screen, line_number, msg)
            
            if toggle_move_text:
                toggle_move_text = False
                number_view = False
                curses.echo()
                curses.nocbreak()
                curses.curs_set(2)
                msg = 'Enter an integer (0-9): '
                line_number = display(screen, line_number, msg)
                move_index = screen.getstr(line_number-1, len(msg)+2, 3)
                line_number = display(screen, line_number, move_index)
                curses.noecho()
                curses.cbreak()
                curses.curs_set(0)
            else:
                msg = '(press "m" to enter a move)'
                line_number = display(screen, line_number, msg)
            
        # key events
        key_event = screen.getch()
        
        # quit game
        if key_event == ord("q"):
            break
            
        # toggle view numbers
        elif key_event == ord("n"):
            if number_view:
                number_view = False
            else:
                number_view = True
        
        if not this_player:
            if key_event == ord("1"):
                this_player = b.P1
                next_player = b.P2
            elif key_event == ord ("2"):
                this_player = b.P2
                next_player = b.P1
        else:
            if not toggle_move_text and key_event == ord("m"):
                toggle_move_text = True


if __name__ == "__main__":
    curses.wrapper(main)