#!/usr/bin/env python

# =========================
# = Tic-Tac-Toe Challenge =
# =========================

# Main script to test Board class via CLI
import curses
from Board import Board

def set_style(screen, styles, unstyle=False):
    for style in styles:
        if unstyle:
            screen.attroff(style)
        else:
            screen.attron(style)

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
    game_over_status = ''
    winning_player = ''

    # Collect input errors
    errors = []

    # ==========
    # = Styles =
    # ==========

    # Error msgs
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    ERROR_COLORS = curses.color_pair(1)

    # player winning spaces
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    WINNING_COLORS = curses.color_pair(2)

    # computer winning spaces
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    LOSING_COLORS = curses.color_pair(3)

    # visual indicator of a previous move
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    LAST_MOVE_COLORS = curses.color_pair(4)

    def display(screen, line_number, msg, letter_position=2, styles=[]):
        set_style(screen, styles)
        screen.addstr(line_number, letter_position, msg)
        set_style(screen, styles, unstyle=True)
        line_number += 1
        return line_number

    def show_board(screen, board, line_number, number_view):

        row_separator = (u'--- ' * board.COLS).strip()

        i = 0
        for row in board.board:
            msg =  ''
            letter_position = 2
            for x, space in enumerate(row):
                styles = []
                if number_view:
                    value = space.board_index
                else:
                    value = space.player
                    if space.winner:
                        if winning_player == b.P1:
                            styles.append(WINNING_COLORS)
                        else:
                            styles.append(LOSING_COLORS)
                    elif space.last_move:
                        styles.append(LAST_MOVE_COLORS)
                set_style(screen, styles)
                msg = str(value).center(3, ' ')
                screen.addstr(line_number, letter_position, msg)
                set_style(screen, styles, unstyle=True)
                letter_position += len(msg)
                if x < len(row)-1:
                    msg = '|'
                    screen.addstr(line_number, letter_position, msg)
                    letter_position += len(msg)
            line_number += 1

            if i < (board.ROWS -1):
                line_number = display(screen, line_number, row_separator)
            i += 1

        return line_number

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
        msg = '"{}" (You)       = {}'.format(b.P1, b.score_board[b.P1])
        line_number = display(screen, line_number, msg)

        msg = '"{}" (Computer)  = {}'.format(b.P2, b.score_board[b.P2])
        line_number = display(screen, line_number, msg)

        msg = 'Draw            = {}'.format(b.score_board[b.P0])
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
                styles = [ERROR_COLORS]
                line_number = display(screen, line_number, msg, styles=styles)
            line_number += 1

        # Player input or notice
        if not this_player:
            player_query = "Who goes first? (1) You, (2) Computer:"
            line_number = display(screen, line_number, player_query)
        else:
            if game_over_status:
                if winning_player == b.P1:
                    styles = [WINNING_COLORS]
                elif winning_player == b.P2:
                    styles = [LOSING_COLORS]
                msg = game_over_status
                line_number = display(screen, line_number, msg, styles=styles)
                msg = '(press "p" to play again)'
                line_number = display(screen, line_number, msg)
            else:
                msg = 'Turn: Player "{}"!'.format(this_player)
                line_number = display(screen, line_number, msg)

                if toggle_move_text:
                    curses.echo()
                    curses.nocbreak()
                    curses.curs_set(2)
                    msg = 'Enter an integer (1-{}): '
                    msg = msg.format(b.last_space_index())
                    line_number = display(screen, line_number, msg)
                    board_index = screen.getstr(line_number-1, 2+len(msg), 3)
                    board_index = board_index.strip()
                    msg = '"{}" is not valid, please try again!'
                    try:
                        board_index = int(board_index)
                        if b.move_player_to_space(this_player, board_index):
                            # did player make a winning move?
                            if b.player_won(this_player):
                                b.score_board[this_player] += 1
                                msg = 'Player "{}" is the winner!'
                                game_over_status = msg.format(this_player)
                                winning_player = this_player
                            elif not b.remaining_spaces():
                                b.score_board[b.P0] += 1
                                game_over_status = "Cat's game (Draw)"

                            # continue to swap players after win?
                            next_player, this_player = this_player, next_player
                        else:
                            errors.append(msg.format(board_index))
                    except:
                        errors.append(msg.format(board_index))
                    finally:
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

            if game_over_status and key_event == ord("p"):
                game_over_status = ''
                winning_player = ''
                b.clear_board()

if __name__ == "__main__":
    curses.wrapper(main)