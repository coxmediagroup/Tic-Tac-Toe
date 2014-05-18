from optparse import make_option
import logging

from django.core.management.base import BaseCommand

from tictactoe.board import Board
from tictactoe.strategy import RandomStrategy, MinimaxStrategy


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--iterations', '-i', dest='iterations', type='int',
            help='Number of games to play', default=10000),)
    help = 'Test the MinimaxStrategy against the RandomStrategy'

    def handle(self, *args, **options):
        iterations = options['iterations']
        self.vs_random(iterations)
        self.vs_minimax(iterations)
        self.stdout.write(
            "A strange game. The only winning move is not to play.")

    def vs_random(self, iterations):
        random_wins, minimax_wins, ties = 0, 0, 0
        rs = RandomStrategy()
        ms = MinimaxStrategy()
        for i in xrange(iterations):
            msg = "Game {}:".format(i)
            if i % 2:
                msg += "Random is X, Minimax is O, "
                board = self.play_game(rs, ms)
                minimax_win = (board.winner() == Board.O_WINS)
            else:
                msg += "Minimax is X, Random is O, "
                board = self.play_game(ms, rs)
                minimax_win = (board.winner() == Board.X_WINS)
            if board.winner() == Board.TIE:
                msg += "Tie."
                logger.info(msg)
                ties += 1
            elif minimax_win:
                msg += "Minimax Wins."
                logger.info(msg)
                minimax_wins += 1
            else:
                msg += "Random Wins!"
                logging.error(msg)
                logging.error('\n' + str(board))
                random_wins += 1
        self.stdout.write(
            "{} games, Random wins {}, Minimax wins {}, {} ties".format(
                iterations, random_wins, minimax_wins, ties))

    def vs_minimax(self, iterations):
        wins, ties = 0, 0
        ms = MinimaxStrategy()
        for i in xrange(iterations):
            msg = "Game {}: Minimax vs. Minimax, ".format(i)
            board = self.play_game(ms, ms)
            if board.winner() == Board.TIE:
                msg += "Tie."
                logger.info(msg)
                ties += 1
            else:
                msg += "Winner!"
                logging.error(msg)
                logging.error('\n' + str(board))
                wins += 1
        self.stdout.write(
            "{} games, Minimax vs. Minimax, {} wins, {} ties".format(
                iterations, wins, ties))

    def play_game(self, player1, player2):
        board = Board()
        for turn in range(9):
            player = player2 if (turn % 2) else player1
            board.move(player.next_move(board))
            if board.winner():
                return board
