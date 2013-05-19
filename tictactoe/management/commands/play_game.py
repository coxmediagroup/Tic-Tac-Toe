import sys
import itertools
from django.core.management.base import NoArgsCommand
from tictactoe import Board, naught_bot
from tictactoe import exceptions as ex


class Command(NoArgsCommand):
    args = None
    help = 'Start a new game of Tic Tac Toe'

    def handle_noargs(self, **options):
        board = Board()
        try:
            while True:
                while True:
                    try:
                        user_selection = raw_input("\nEnter a valid open cell number:")
                        idx = int(user_selection)
                        assert 8 >= idx >= 0, "cell must be 0-8"
                        board[int(user_selection)] = board.CROSS
                        self.stdout.write(chr(27) + "[2J")
                        self.stdout.write(str(board))
                        break
                    except (AssertionError, TypeError, ex.TicTacToeError) as exc:
                        if isinstance(exc, ex.GameOver):
                            self.stdout.write(str(exc))
                            sys.exit(0)

                        self.stderr.write(str(exc))

                board[naught_bot(board)] = board.NAUGHT
                self.stdout.write(chr(27) + "[2J")
                self.stdout.write(str(board))
        except KeyboardInterrupt:
            self.stderr.write("\nExiting...")