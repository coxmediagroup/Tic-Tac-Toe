#!/usr/bin/env python

# =========================
# = Tic-Tac-Toe Challenge =
# =========================

# Main script to test Board class via CLI
import curses
from Board import Board

def display(screen, line_number, msg, x_pos=2, **kwargs):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    is_error = kwargs.get('error', False)
    if is_error:
        screen.addstr(line_number, x_pos, msg, curses.color_pair(1))
    else:
        screen.addstr(line_number, x_pos, msg)
    screen.refresh()
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

    # Make a new game board
    b = Board(P0=' ')

    # game states
    number_view = False
    toggle_move_text = False
    this_player = None
    next_player = None
    game_width = 60
    line_separator = '-' * (game_width - 4)

    # Collect input errors
    errors = []

    while True:

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

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

        # Spacer
        line_number += 1

        # Divider
        line_number = display(screen, line_number, line_separator)

        # Spacer
        line_number += 2

        # Show game Board
        line_number = show_board(screen, b, line_number, number_view)

        # Spacer
        line_number += 2

        # Error Messages
        if errors:
            while errors:
                msg = errors.pop()
                line_number = display(screen, line_number, msg, error=True)
            line_number += 1

        # Player input or notice
        if not this_player:
            player_query = "Who goes first? (1) You, (2) Computer:"
            line_number = display(screen, line_number, player_query)
        else:
            msg = 'Turn: Player "{}"!'.format(this_player)
            line_number = display(screen, line_number, msg)

            if toggle_move_text:
                curses.echo()
                curses.nocbreak()
                curses.curs_set(2)
                msg = 'Enter an integer (0-{}): '.format(b.last_space_index())
                line_number = display(screen, line_number, msg)
                board_index = screen.getstr(line_number-1, 2+len(msg), 3)
                board_index = board_index.strip()
                try:
                    board_index = int(board_index)
                    if b.player_to_spot(this_player, board_index):
                        next_player, this_player = this_player, next_player
                    else:
                        errors.append('"{}" not a valid move!'.format(
                            board_index))
                except:
                    errors.append('"{}" not valid, please try again!'.format(
                        board_index))
                finally:
                    curses.noecho()
                    curses.cbreak()
                    curses.curs_set(0)
                    toggle_move_text = False
                    number_view = False

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