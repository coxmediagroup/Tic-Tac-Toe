import curses
from Board import Board

class GameScreenException(Exception):
    pass

class GameScreen(object):
    """
    Game settings for game played through curses
    
    """
    # Current line when writing lines to screen
    line_number = 0
    
    # screen mode constants
    SPLASH_SCREEN_MODE = 'splash'
    GAME_SCREEN_MODE = 'game'
    QUIT_SCREEN_MODE = 'quit'

    # Game screen states
    screen_mode = SPLASH_SCREEN_MODE
    last_screen_mode = screen_mode
    number_view_mode = False
    ask_player_for_move = False
    round_over_status = None
    winning_player = None
    errors = []
    high_scores = [[2, "sframe@gmail.com"]]

    # Styling
    PADDING = 2
    GAME_WIDTH = 64
    LINE_SEPARATOR = '-' * (GAME_WIDTH - (PADDING * 2))
    
    # Game texts
    MSG_GAME_TITLE = 'Code Challenge'
    MSG_KEY_number_view_mode = 'v = number view'
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
    
    def __init__(self, *args, **kwargs):
        self.screen = args[0]
        self.DEFAULT_LINE_NUMBER = kwargs.get('line_number', self.line_number)
        self.reset_line_number()
        self.make_game_board(p0=' ', p2_ai=True)
        self._game_styles()
        self.DEBUG = kwargs.get('debug', False)
        self.game_is_running = True
        self.high_scores = kwargs.get('high_scores', self.high_scores)
    
    def disable_cursor_input(self):
        """
        
        """
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
    
    def enable_cursor_input(self):
        """
        
        """
        curses.echo()
        curses.nocbreak()
        curses.curs_set(2)
    
    def make_game_board(self, **kwargs):
        """
        
        """
        self.board = Board(**kwargs)
    
    def reset_line_number(self):
        """
        
        """
        self.line_number = self.DEFAULT_LINE_NUMBER
    
    def display(self, msg, styles=[]):
        """
        Write to screen and keep track of line count
        
        """
        self.set_style(styles)
        self.screen.addstr(self.line_number, self.PADDING, msg)
        self.set_style(styles, unstyle=True)
        self.line_number += 1
    
    def set_style(self, styles=[], unstyle=False):
        """
        Set or unset global styles for display
        
        """
        for style in styles:
            if unstyle:
                self.screen.attroff(style)
            else:
                self.screen.attron(style)
    
    def _game_styles(self):
        """
        After curses.initscr()
        
        """
        # Error msgs
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        self.ERROR_COLORS = curses.color_pair(1)

        # player winning spaces
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.WINNING_COLORS = curses.color_pair(2)

        # computer winning spaces
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.LOSING_COLORS = curses.color_pair(3)

        # visual indicator of a previous move
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.LAST_MOVE_COLORS = curses.color_pair(4)
    
    def _write_spacer(self, lines=1):
        """
        
        """
        self.line_number += lines
    
    def _write_divider(self, lines=1):
        """
        
        """
        for x in range(lines):
            self.display(self.LINE_SEPARATOR)
    
    def display_debug(self):
        """
        
        """
        if self.DEBUG:
            self._write_divider()
            self.display('DEBUG:')
            self._write_divider()
            
            # Game states

            msg = '* screen_mode         = {}'
            self.display(msg.format(self.screen_mode))
            
            msg = '* last_screen_mode    = {}'
            self.display(msg.format(self.last_screen_mode))
            
            msg = '* number_view_mode    = {}'
            self.display(msg.format(self.number_view_mode))

            msg = '* ask_player_for_move = {}'
            self.display(msg.format(self.ask_player_for_move))

            msg = '* round_over_status   = {}'
            self.display(msg.format(self.round_over_status))

            msg = '* winning_player      = {}'
            self.display(msg.format(self.winning_player))
            
            msg = '* current_player      = {}'
            self.display(msg.format(self.board.current_player))
            
            self._write_divider()
        
    
    def game_title(self):
        self.screen.clear()
        self.reset_line_number()
        self.disable_cursor_input()
        self.display_debug()
        self._write_spacer(lines=self.PADDING)
        self.display(self.MSG_GAME_TITLE)
        self._write_spacer()
        self._write_divider()
        
    def draw_quit_game_screen(self):
        """

        """
        # Title
        self.game_title()
        self.display(self.MSG_QUIT_CONFIRM)
    
    def draw_splash_screen(self):
        """
        
        """
        # Title
        self.game_title()
        
        # show high score Top 10
        
        self.display(self.MSG_START_GAME)
    
    def draw_game_screen(self):
        """
        
        """
        # Title
        self.game_title()

        # Help section
        self.display(self.MSG_KEY_number_view_mode)
        self.display(self.MSG_KEY_QUIT)

        # Divider
        self._write_divider()
        self._write_spacer()

        # Score Board
        msg = self.MSG_PLAYER_1_SCORE
        msg = msg.format(self.board.P1, self.board.score_board[self.board.P1])
        self.display(msg)

        msg = self.MSG_PLAYER_2_SCORE
        msg = msg.format(self.board.P2, self.board.score_board[self.board.P2])
        self.display(msg)

        msg = self.MSG_PLAYER_0_SCORE
        msg = msg.format(self.board.score_board[self.board.P0])
        self.display(msg)
        self._write_spacer()

        # Divider
        self._write_divider()
        self._write_spacer(lines=2)

        # Show game Board
        self._draw_game_board()
        self._write_spacer(lines=2)
        
        # Show player turn
        if self.board.current_player:
            msg = self.MSG_PLAYER_TURN.format(self.board.current_player)
            self.display(msg)
            self._write_spacer()
        
        # Error Messages
        if self.errors:
            styles = [self.ERROR_COLORS]
            while self.errors:
                msg = self.errors.pop()
                self.display(msg, styles=styles)
            self._write_spacer()

    def _draw_game_board(self):
        """
        Draw the game board
        
        """
        row_separator = (u'--- ' * self.board.COLS).strip()

        i = 0
        for row in self.board.board:
            msg =  ''
            letter_position = self.PADDING
            for x, space in enumerate(row):
                styles = []                        
                if self.number_view_mode and space.player == self.board.P0:
                    if self.ask_player_for_move:
                        styles.append(curses.A_BLINK)
                    value = space.board_index
                else:
                    value = space.player
                if space.winner:
                    if self.winning_player == self.board.P1:
                        styles.append(self.WINNING_COLORS)
                    else:
                        styles.append(self.LOSING_COLORS)
                elif space.last_move:
                    styles.append(self.LAST_MOVE_COLORS)
                self.set_style(styles)
                msg = str(value).center(3, ' ')
                self.screen.addstr(self.line_number, letter_position, msg)
                self.set_style(styles, unstyle=True)
                letter_position += len(msg)
                if x < len(row)-1:
                    msg = '|'
                    self.screen.addstr(self.line_number, letter_position, msg)
                    letter_position += len(msg)
            self._write_spacer()

            if i < (self.board.ROWS -1):
                self.display(row_separator)
            i += 1

    def key_events(self):
        """
        Evaluates player's choices
        
        Return False to exit game loop.
        
        """
        # key events
        key_event = self.screen.getch()
        
        # Toggle debug mode
        if key_event == ord("D"):
            self.DEBUG = not self.DEBUG
        
        # Hard quit game
        if key_event == ord("Q"):
            return False
        
        # Quit game confirmation
        if not self.screen_mode == self.QUIT_SCREEN_MODE:
            if key_event == ord("q"):
                self.last_screen_mode = self.screen_mode
                self.screen_mode = self.QUIT_SCREEN_MODE
            
        # Quit screen keys
        if self.screen_mode == self.QUIT_SCREEN_MODE:
            if key_event == ord("y"):
                return False
            elif key_event == ord("n"):
                self.screen_mode = self.last_screen_mode
        
        # Spash screen keys
        if self.screen_mode == self.SPLASH_SCREEN_MODE:
            
            if key_event == ord("p"):
                self.last_screen_mode = self.screen_mode
                self.screen_mode = self.GAME_SCREEN_MODE
        
        # Game screen keys
        if self.screen_mode == self.GAME_SCREEN_MODE:
            
            # Which player goes first
            if not self.board.current_player:
                if key_event == ord("1"):
                    self.board.current_player = self.board.P1
                    self.board.next_player = self.board.P2
                elif key_event == ord ("2"):
                    self.board.current_player = self.board.P2
                    self.board.next_player = self.board.P1
            
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
                            self.board.P0: 0,
                            self.board.P1: 0,
                            self.board.P2: 0,
                        }
                        # return to splash screen
                        self.screen_mode = self.SPLASH_SCREEN_MODE
            
            # toggle view numbers
            if key_event == ord("v"):
                self.number_view_mode = not self.number_view_mode
        
        return True
        
    def game_is_ready(self):
        """
        Game is ready when there is a defined starting player
        
        """
        if not self.board.current_player:
            self.display(self.MSG_PLAYER_START)
            return False
        else:
            return True
    
    def round_over(self):
        """
        When a player has an nth-in-a-row move then the round is over.
        
        """
        if self.round_over_status:
            return True
        else:
            return False
    
    def display_winner(self):
        """
        Display the "round_over_status" message to who won the round.
        
        """
        styles = []
        if self.winning_player == self.board.P1:
            styles = [self.WINNING_COLORS]
        elif self.winning_player == self.board.P2:
            styles = [self.LOSING_COLORS]
        self.display(self.round_over_status, styles=styles)

    def play_again(self):
        """
        
        """        
        # show winner
        self.display_winner()
        
        # diplay play again message
        # (key events ="y": resets board, "n": resets game)
        self.display(self.MSG_PLAY_AGAIN)
    
    def player_ai(self):
        """
        
        """
        if self.board.current_player == self.board.P1:
            return self.board.P1_AI
        elif self.board.current_player == self.board.P2:
            return self.board.P2_AI

    def valid_player_move(self, this_space):
        
        # validate player choice
        try:
            # make this an integer
            this_space = int(this_space)
            # try to place move
            current_player = self.board.current_player
            if not self.board.move_player(current_player, this_space):
                raise GameScreenException
        except:
            self.errors.append(self.MSG_NOT_VALID.format(this_space))
            return False
        return True

    def player_move_query(self):
        """
        
        """
        if self.ask_player_for_move:
            
            # prompt player to enter value between 1 - (total board spaces)
            board_space_count = self.board.last_space_number()
            player_query_msg = self.MSG_ENTER_MOVE.format(board_space_count)
            self.display(player_query_msg)
        
            # get player choice
            self.enable_cursor_input()
            input_start = self.PADDING + len(player_query_msg)
            this_line = self.line_number-1
            this_space = self.screen.getstr(this_line, input_start, 3)
            this_space = this_space.strip()
            self.disable_cursor_input()
            
            # Dont ask again unless prompted
            self.ask_player_for_move = False
            
            return self.valid_player_move(this_space)
            
        else:
            
            # prompt the player to enter a move
            self.display(self.MSG_ALERT_PLAYER_TO_MOVE)
        
        return False
    
    def player_turn(self):
        """
        
        """
        # current player turn: human or computer?
        if self.player_ai(): # computer
            # Computer: always makes a valid move - right? :)
            valid_move = self.board.ai(self.board.current_player)
            self.display(self.MSG_PRESS_ANY_KEY)
        else:
            # Human: choose a valid move
            valid_move = self.player_move_query()
        
        # last move a valid move?
        if valid_move:
            
            # current player move make a winning move?
            player_wins = self.board.player_win_round(self.board.current_player)
            if player_wins:
                #   Note which player was winner
                self.winning_player = self.board.current_player
                #   add point for current player
                self.board.score_board[self.board.current_player] += 1
        
            # swap player turns
            self.board.swap_players()
        
            # (max-in-a-row for round over?)
            if player_wins:
                # [Round over] (Player wins)
                msg = self.MSG_GAME_WIN.format(self.winning_player)
                self.round_over_status = msg

            # (space available to keep playing?)
            if not self.board.remaining_spaces():
                # add point for draw
                self.board.score_board[self.board.P0] += 1
                # [Round over] (Draw)
                self.round_over_status == True
                
            
            self.screen.refresh()
        