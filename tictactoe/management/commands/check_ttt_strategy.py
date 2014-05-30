'''Django management command to run many Tic-Tac-Toe games with robots'''
from optparse import make_option
import logging

from django.core.management.base import BaseCommand

from tictactoe.board import Board
from tictactoe.strategy import RandomStrategy, MinimaxStrategy


def play_game(player1, player2):
    '''Play a game with two robots'''
    board = Board()
    for turn in range(9):
        player = player2 if (turn % 2) else player1
        board.move(player.next_move(board))
        if board.winner():
            return board


class Command(BaseCommand):
    '''Run many Tic-Tac-Toe games with robots as players'''
    option_list = BaseCommand.option_list + (
        make_option(
            '--iterations', '-i', dest='iterations', type='int',
            help='Number of games to play', default=10000),)
    help = 'Test the MinimaxStrategy against the RandomStrategy'
    _logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        iterations = options['iterations']
        self.vs_random(iterations)
        self.vs_minimax(iterations)
        self.stdout.write(
            "A strange game. The only winning move is not to play.")

    def vs_random(self, iterations):
        '''
        Play the RandomStrategy vs. the MinimaxStrategy

        It is expected that the RandomStrategy will never win a game.
        '''
        random_wins, minimax_wins, ties = 0, 0, 0
        random_s = RandomStrategy()
        minimax_s = MinimaxStrategy()
        for i in xrange(iterations):
            msg = "Game {}:".format(i)
            if i % 2:
                msg += "Random is X, Minimax is O, "
                board = play_game(random_s, minimax_s)
                minimax_win = (board.winner() == Board.O_WINS)
            else:
                msg += "Minimax is X, Random is O, "
                board = play_game(minimax_s, random_s)
                minimax_win = (board.winner() == Board.X_WINS)
            if board.winner() == Board.TIE:
                msg += "Tie."
                self._logger.info(msg)
                ties += 1
            elif minimax_win:
                msg += "Minimax Wins."
                self._logger.info(msg)
                minimax_wins += 1
            else:
                msg += "Random Wins!"
                self._logger.error(msg)
                self._logger.error('\n' + str(board))
                random_wins += 1
        self.stdout.write(
            "{} games, Random wins {}, Minimax wins {}, {} ties".format(
                iterations, random_wins, minimax_wins, ties))

    def vs_minimax(self, iterations):
        '''
        Play the MinimaxStrategy vs. MinimaxStrategy

        The expectation is that all games are ties
        '''
        wins, ties = 0, 0
        minimax_s = MinimaxStrategy()
        for i in xrange(iterations):
            msg = "Game {}: Minimax vs. Minimax, ".format(i)
            board = play_game(minimax_s, minimax_s)
            if board.winner() == Board.TIE:
                msg += "Tie."
                self._logger.info(msg)
                ties += 1
            else:
                msg += "Winner!"
                self._logger.error(msg)
                self._logger.error('\n' + str(board))
                wins += 1
        self.stdout.write(
            "{} games, Minimax vs. Minimax, {} wins, {} ties".format(
                iterations, wins, ties))
