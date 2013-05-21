import sys
from django.core.management.base import NoArgsCommand
from tictactoe import Board, naught_bot, NAUGHT, CROSS
from tictactoe import exceptions as ex


class Command(NoArgsCommand):
    args = None
    help = 'Would you like to play a game?'

    def clear_stdout(self):
        # clears the terminal (I had no idea how to do this so I googled).
        self.stdout.write(chr(27) + "[2J")

    def render_board(self):
        self.clear_stdout()
        self.stdout.write(str(self.board))

    def handle_noargs(self, **options):
        self.board = Board()
        self.render_board()
        try:
            while True:
                while True:
                    try:
                        user_selection = raw_input("\nEnter a cell number:")
                        idx = int(user_selection)
                        assert 8 >= idx >= 0, "cell must be 0-8"
                        self.board[int(user_selection)] = CROSS
                        break
                    except (AssertionError, TypeError, ex.MoveError) as exc:
                        self.stderr.write(str(exc))

                # After the player's mark is set, let the bot look at
                # the board.
                self.board[naught_bot(self.board)] = NAUGHT
                self.render_board()
        except ex.GameOver as exc:
            self.render_board()
            self.stderr.write(str(exc))
        except KeyboardInterrupt:
            self.stderr.write("\nExiting...")
