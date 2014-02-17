"""
Everything to do with the game play within curses

"""
import curses

from tic_tac_toe.board import Board, BoardMoveException

# screen mode constants
SPLASH_SCREEN_MODE = 'splash'
GAME_SCREEN_MODE = 'game'
QUIT_SCREEN_MODE = 'quit'

# Styling
PADDING = 2
GAME_WIDTH = 64
LINE_SEPARATOR = '-' * (GAME_WIDTH - (PADDING * 2))

# Game texts
MSG_GAME_TITLE = 'Code Challenge'
MSG_KEY_NUMBER_VIEW_MODE = 'v = number view'
MSG_KEY_QUIT = 'q = quit'
MSG_QUIT_CONFIRM = '(Are you sure? press "y" to quit or "n" to go back)'
MSG_START_GAME = '(press "p" to play or "q" to quit)'
MSG_PLAYER_START = 'Who goes first? (1) You, (2) Computer:'
MSG_PLAYER_1_SCORE = '"{}" (You)       = {}'
MSG_PLAYER_2_SCORE = '"{}" (Computer)  = {}'
MSG_PLAYER_0_SCORE = 'Draw            = {}'
MSG_PLAY_AGAIN = '(play again? press "y" to play or "n" to reset game)'
MSG_PLAYER_TURN = '** Player "{}" Turn **'
MSG_NOT_VALID = '"{}" is not a valid move, please try again!'
MSG_ENTER_MOVE = 'Enter an integer (1-{}): '
MSG_GAME_WIN = 'Player "{}" is the winner!'
MSG_GAME_DRAW = "Cat's game (Draw)"
MSG_ALERT_PLAYER_TO_MOVE = '(press "m" to enter a move)'
MSG_PRESS_ANY_KEY = '(press any key)'

# High scores
HIGH_SCORES = [[2, "sframe@gmail.com"]]

def _disable_cursor_input():
    """
    Don't echo back character what user presses
    Enter one value without pressing return
    hide the text cursor

    """
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

def _enable_cursor_input():
    """
    Echo back characters what user presses
    Do not enter text unless pressing enter (entering multi-key values)
    Show the text cursor

    """
    curses.echo()
    curses.nocbreak()
    curses.curs_set(2)

class GameScreenException(Exception):
    """Exceptions during gameplay"""
    pass

class GameScreen(object):
    """
    Game settings for game played through curses

    """
    def __init__(self, *args, **kwargs):
        self.screen = args[0]
        self.default_line_number = kwargs.get('line_number', 0)
        self._reset_line_number()
        self.make_game_board(player0=' ', player2_ai=True)
        self._game_styles()
        self.debug = kwargs.get('debug', False)
        self._game_is_running = True
        self.high_scores = kwargs.get('high_scores', HIGH_SCORES)

        # Game screen states
        self.screen_mode = SPLASH_SCREEN_MODE
        self.last_screen_mode = self.screen_mode
        self.number_view_mode = False
        self.ask_player_for_move = False
        self.round_over_status = None
        self.winning_player = None
        self.errors = []

    def make_game_board(self, **kwargs):
        """
        Intantiate the Board, possibly re-configuring it for different types
        of games

        """
        self.board = Board(**kwargs)

    def _reset_line_number(self):
        """
        Different parts of game screen are written to a line number and then
        the line number is incremented. Reseting the line number allows
        re-drawing from the top of the screen again

        """
        self.line_number = self.default_line_number

    def _display(self, msg, styles=()):
        """
        Write to screen and increment the line number

        """
        self._set_style(styles)
        self.screen.addstr(self.line_number, PADDING, msg)
        self._set_style(styles, unstyle=True)
        self.line_number += 1

    def _set_style(self, styles=(), unstyle=False):
        """
        Set or unset global styles for display. Useful for bracketing inline
        text with separate styles.

        """
        for style in styles:
            if unstyle:
                self.screen.attroff(style)
            else:
                self.screen.attron(style)

    def _game_styles(self):
        """
        Initiate different styles for text display within this curses screen

        """
        # Error msgs
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        self.error_colors = curses.color_pair(1)

        # player winning spaces
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.winning_colors = curses.color_pair(2)

        # computer winning spaces
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.losing_colors = curses.color_pair(3)

        # visual indicator of a previous move
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.last_move_colors = curses.color_pair(4)

    def _write_spacer(self, lines=1):
        """
        Simple way of "writing" a blank line

        """
        self.line_number += lines

    def _write_divider(self, lines=1):
        """
        Simple way of "writing" a visual divider

        """
        line_counter = 0
        while line_counter < lines:
            self._display(LINE_SEPARATOR)
            line_counter += 1

    def _display_debug(self):
        """
        Show some variables during game play

        """
        if self.debug:
            self._write_divider()
            self._display('debug:')
            self._write_divider()

            # Game states

            msg = '* screen_mode         = {}'
            self._display(msg.format(self.screen_mode))

            msg = '* last_screen_mode    = {}'
            self._display(msg.format(self.last_screen_mode))

            msg = '* number_view_mode    = {}'
            self._display(msg.format(self.number_view_mode))

            msg = '* ask_player_for_move = {}'
            self._display(msg.format(self.ask_player_for_move))

            msg = '* round_over_status   = {}'
            self._display(msg.format(self.round_over_status))

            msg = '* winning_player      = {}'
            self._display(msg.format(self.winning_player))

            msg = '* this_player         = {}'
            self._display(msg.format(self.board.this_player))

            self._write_divider()

    def _game_title(self):
        """
        Common top section of the game screen

        """
        self.screen.clear()
        self._reset_line_number()
        _disable_cursor_input()
        self._display_debug()
        self._write_spacer(lines=PADDING)
        self._display(MSG_GAME_TITLE)
        self._write_spacer()
        self._write_divider()

    def _draw_quit_game_screen(self):
        """
        The quit screen confirmation page

        """
        # Title
        self._game_title()
        self._display(MSG_QUIT_CONFIRM)

    def _draw_splash_screen(self):
        """
        The game introduction page

        """
        # Title
        self._game_title()

        # Show high score Top 10

        self._display(MSG_START_GAME)

    def _draw_game_screen(self):
        """
        The gameplay screen

        """
        # Title
        self._game_title()

        # Help section
        self._display(MSG_KEY_NUMBER_VIEW_MODE)
        self._display(MSG_KEY_QUIT)

        # Divider
        self._write_divider()
        self._write_spacer()

        # Score Board
        msg = MSG_PLAYER_1_SCORE
        msg = msg.format(self.board.player1,
                         self.board.score_board[self.board.player1])
        self._display(msg)

        msg = MSG_PLAYER_2_SCORE
        msg = msg.format(self.board.player2,
                         self.board.score_board[self.board.player2])
        self._display(msg)

        msg = MSG_PLAYER_0_SCORE
        msg = msg.format(self.board.score_board[self.board.player0])
        self._display(msg)
        self._write_spacer()

        # Divider
        self._write_divider()
        self._write_spacer(lines=2)

        # Show game Board
        self._draw_game_board()
        self._write_spacer(lines=2)

        # Show player turn
        if self.board.this_player:
            msg = MSG_PLAYER_TURN.format(self.board.this_player)
            self._display(msg)
            self._write_spacer()

        # Error Messages
        if self.errors:
            styles = [self.error_colors]
            while self.errors:
                msg = self.errors.pop()
                self._display(msg, styles=styles)
            self._write_spacer()

    def _draw_game_board(self):
        """
        Draw the actual game board grid itself

        """
        row_separator = (u'--- ' * self.board.cols).strip()

        i = 0
        for row in self.board.board:
            msg = ''
            letter_position = PADDING
            for row_count, space in enumerate(row):
                styles = []
                if self.number_view_mode and space.player == self.board.player0:
                    if self.ask_player_for_move:
                        styles.append(curses.A_BLINK)
                    value = space.board_index
                else:
                    value = space.player
                if space.winner:
                    if self.winning_player == self.board.player1:
                        styles.append(self.winning_colors)
                    else:
                        styles.append(self.losing_colors)
                elif space.last_move:
                    styles.append(self.last_move_colors)
                self._set_style(styles)
                msg = str(value).center(3, ' ')
                self.screen.addstr(self.line_number, letter_position, msg)
                self._set_style(styles, unstyle=True)
                letter_position += len(msg)
                if row_count < len(row)-1:
                    msg = '|'
                    self.screen.addstr(self.line_number, letter_position, msg)
                    letter_position += len(msg)
            self._write_spacer()

            if i < (self.board.rows -1):
                self._display(row_separator)
            i += 1

    def _keys_splash_screen(self, key_event):
        """
        Keys pressed during splash screen

        """
        if key_event == ord("p"):
            self.last_screen_mode = self.screen_mode
            self.screen_mode = GAME_SCREEN_MODE

    def _keys_quitgame_screen(self, key_event):
        """
        Keys pressed to go to quit game confirmation screen

        """
        if key_event == ord("q"):
            self.last_screen_mode = self.screen_mode
            self.screen_mode = QUIT_SCREEN_MODE

    def _keys_quitconfirm_screen(self, key_event):
        """
        Keys pressed during quit game screen

        """
        if key_event == ord("y"):
            # Confirmed to quit game
            return True
        elif key_event == ord("n"):
            # Don't quit just yet
            self.screen_mode = self.last_screen_mode
            return False

    def _keys_game_screen(self, key_event):
        """
        Keys pressed during game screen

        """
        # Which player goes first
        if not self.board.this_player:
            if key_event == ord("1"):
                self.board.this_player = self.board.player1
                self.board.next_player = self.board.player2
            elif key_event == ord("2"):
                self.board.this_player = self.board.player2
                self.board.next_player = self.board.player1

        # Interact with player
        else:

            # player turn, prompt to enter a move value
            if not self.ask_player_for_move and key_event == ord("m"):
                self.ask_player_for_move = True

            # round over! play again?
            if self.round_over_status:

                if key_event in [ord("y"), ord("n")]:
                    # reset game board
                    self.round_over_status = ''
                    self.winning_player = ''
                    self.board.clear_board()

                if key_event == ord("n"):
                    # reset game board and score
                    self.board.score_board = {
                        self.board.player0: 0,
                        self.board.player1: 0,
                        self.board.player2: 0,
                    }
                    # return to splash screen
                    self.screen_mode = SPLASH_SCREEN_MODE

        # toggle view numbers
        if key_event == ord("v"):
            self.number_view_mode = not self.number_view_mode

    def _key_events(self):
        """
        Evaluates the player's choices during different screens

        Returning False will exit the main game loop.

        """
        # key events
        key_event = self.screen.getch()

        # Toggle debug mode
        if key_event == ord("D"):
            self.debug = not self.debug

        # Hard quit game
        if key_event == ord("Q"):
            return False

        # Quit game confirmation
        if not self.screen_mode == QUIT_SCREEN_MODE:
            self._keys_quitgame_screen(key_event)

        # Quit screen keys
        if self.screen_mode == QUIT_SCREEN_MODE:
            if self._keys_quitconfirm_screen(key_event):
                return False

        # Spash screen keys
        if self.screen_mode == SPLASH_SCREEN_MODE:
            self._keys_splash_screen(key_event)

        # Game screen keys
        if self.screen_mode == GAME_SCREEN_MODE:
            self._keys_game_screen(key_event)

        return True

    def _game_is_ready(self):
        """
        Game is ready when there is a defined starting player. Every round
        there after the starting player is opposite of the last player from
        the previous game.

        """
        if not self.board.this_player:
            self._display(MSG_PLAYER_START)
            return False
        else:
            return True

    def _round_over(self):
        """
        When a player has an nth-in-a-row move then the round is over.

        """
        if self.round_over_status:
            return True
        else:
            return False

    def _display_winner(self):
        """
        Display the "round_over_status" message of who won the round.

        """
        styles = []
        if self.winning_player == self.board.player1:
            styles = [self.winning_colors]
        elif self.winning_player == self.board.player2:
            styles = [self.losing_colors]
        self._display(self.round_over_status, styles=styles)

    def _play_again(self):
        """
        Display the game winner and prompt player if they would like to play
        again. If the yes then board will reset and the scores will persist,
        if no then the game will reset, the scores will reset and the player
        will be presented with the splash screen again.

        """
        # show winner
        self._display_winner()

        # diplay play again message
        # (key events ="y": resets board, "n": resets game)
        self._display(MSG_PLAY_AGAIN)

    def _player_ai(self):
        """
        AI status for player is set during intit. Possibly could be dynamic.

        """
        if self.board.this_player == self.board.player1:
            return self.board.player1_ai
        elif self.board.this_player == self.board.player2:
            return self.board.player2_ai

    def _valid_player_move(self, this_space):
        """
        Check that the input itself is an integer and whether or not the
        proposed move is legal.

        """
        # validate player choice
        try:
            # make this an integer
            this_space = int(this_space)
            # try to place move
            this_player = self.board.this_player
            self.board.move_player(this_player, this_space)
        except (ValueError, BoardMoveException):
            self.errors.append(MSG_NOT_VALID.format(this_space))
            return False
        return True

    def _player_move_query(self):
        """
        Only to allow multi-character cursor input if the player is ready
        to enter a position. Especially for larger game boards where multiple
        digits for spaces are necessary.

        """
        if self.ask_player_for_move:

            # prompt player to enter value between 1 - (total board spaces)
            board_space_count = self.board.last_space_number()
            player_query_msg = MSG_ENTER_MOVE.format(board_space_count)
            self._display(player_query_msg)

            # get player choice
            _enable_cursor_input()
            input_start = PADDING + len(player_query_msg)
            this_line = self.line_number-1
            this_space = self.screen.getstr(this_line, input_start, 3)
            this_space = this_space.strip()
            _disable_cursor_input()

            # Dont ask again unless prompted
            self.ask_player_for_move = False

            return self._valid_player_move(this_space)

        else:

            # prompt the player to enter a move
            self._display(MSG_ALERT_PLAYER_TO_MOVE)

        return False

    def _player_turn(self):
        """
        Display the game play between players.

        Display an error if the move is not valid

        Assign point if there is winning move or a draw

        Swap player turns

        """
        # current player turn: human or computer?
        if self._player_ai(): # computer
            # Computer: always makes a valid move - right? :)
            self.board.ai_move()
            valid_move = True
            self._display(MSG_PRESS_ANY_KEY)
        else:
            # Human: choose a valid move
            valid_move = self._player_move_query()

        # last move a valid move?
        if valid_move:

            # current player move make a winning move?
            player_wins = self.board.player_win_round(self.board.this_player)
            if player_wins:
                #   Note which player was winner
                self.winning_player = self.board.this_player
                #   add point for current player
                self.board.score_board[self.board.this_player] += 1

            # swap player turns
            self.board.swap_players()

            # (max-in-a-row for round over?)
            if player_wins:
                # [Round over] (Player wins)
                msg = MSG_GAME_WIN.format(self.winning_player)
                self.round_over_status = msg

            # (space available to keep playing?)
            if not self.board.remaining_spaces():
                # add point for draw
                self.board.score_board[self.board.player0] += 1
                # [Round over] (Draw)
                self.round_over_status = MSG_GAME_DRAW

    def run_game(self):
        """
        Main game loop and interaction between different game screens

        """
        # Game Loop
        while self._game_is_running:

            # If splash screen
            if self.screen_mode == SPLASH_SCREEN_MODE:

                # Show splash screen
                self._draw_splash_screen()

            # if game screen
            elif self.screen_mode == GAME_SCREEN_MODE:

                # Show the score and game board
                self._draw_game_screen()

                # game ready? (which player goes first)
                if self._game_is_ready():

                    # game rounds (until round over)
                    if self._round_over():

                        # play another round?
                        self._play_again()

                    else:

                        # (current player makes a move)
                        self._player_turn()

            # if quit screen
            elif self.screen_mode == QUIT_SCREEN_MODE:

                # show the quit confirmation screen
                self._draw_quit_game_screen()

            # Check for key presses
            self._game_is_running = self._key_events()
        