# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import random

from math import floor

from apps.coxtactoe.models import TicTacToeMoveModel
from apps.coxtactoe.tictactoe import Marker, Board
from apps.coxtactoe import const as C

import logging as log
log.basicConfig(level=log.INFO)


_ = Marker(C._)
X = Marker(C.X)
O = Marker(C.O)

__docformat__ = 'restructuredtext en'


class MinMaxPlayer(object):
    """Implements a MinMax 3,3,3-game player.

        With some small modification it would be able to play any m,n,k-game.
        The MinMax approach works because "no player can profit from deviating
        from the strategy for one period and then reverting to the strategy."

        Source: http://en.wikipedia.org/wiki/One-Shot_deviation_principle

    """
    def __init__(self, player, board=Board()):
        self.board = board
        self.player = player
        self.minmax_ai = player
        self.wins = {X: 0, O: 0}
        self.ties = {X: 0, O: 0}
        self.loses = {X: 0, O: 0}
        self.recent_wins = {X: 0, O: 0}
        self.recent_ties = {X: 0, O: 0}
        self.recent_loses = {X: 0, O: 0}

    def save_move(self, player, board, move):
        """Saves moves for faster decisions later"""
        TicTacToeMoveModel.objects.get_or_create(
            player=repr(player), prev_board=board.key, move=move)

    def get_saved_move(self, player, board):
        """Retrieves a move for the current board state if available.

            Assuming a B-tree for the DB implementation, this
            gives us O(log n) performance once a move has been saved.
        """
        try:
            move = TicTacToeMoveModel.objects.get(
                player=repr(player), prev_board=board.key)
        except TicTacToeMoveModel.DoesNotExist:
            return None
        else:
            return move

    def score(self, player, board):
        """Scores the game"""
        if board.winner == player:
            return C.WIN
        if board.winner is not None:
            return C.LOSS
        return C.TIE

    def get_best_move(self, player=None, board=None):
        moves = []
        if player is None:
            player = self.player
        if board is None:
            board = self.board

        # Look up saved move and take it if we find one for current board state
        if self.board.key == board.key:
            saved_move = self.get_saved_move(player, board)
            if saved_move is not None:
                return saved_move.move

        # Return the score for the game once it ends
        if board.game_over:
            return self.score(self.player, board)

        # Simulate placing moves on the board for every open square
        for square in board.open_squares:
            next_board = Board(board.key, turn=player)
            next_board.place(player, square)
            next_player = X if player == O else O
            score = self.get_best_move(next_player, next_board)
            moves.append((square, score))

            # Poor man's alpha-beta pruning
            # See http://en.wikipedia.org/wiki/Alpha–beta_pruning
            if self.player != player and score == C.LOSS:
                break
            if self.player == player and score >= C.TIE:
                break

        # Save the move we found for future play before returning it
        if self.board.key == board.key:
            move = max(moves, key=lambda m: m[C.SCORE_IDX])[C.MOVE_IDX]
            self.save_move(player, board, move)
            return move

        # Return max move if current player's turn, else return min move
        if self.player == player:
            return max(moves, key=lambda m: m[C.SCORE_IDX])[C.SCORE_IDX]
        else:
            return min(moves, key=lambda m: m[C.SCORE_IDX])[C.SCORE_IDX]


    # TESTING METHODS
    ###########################################################################
    # The code below this point was intended to be disposable; for helping me
    # debug the program and verify its behavior while I was developing it.
    # I decided to leave it in and use it as a game play driver for automated
    # testing of the AI code. If this were code anyone would have to maintain,
    # it would make the sort list for refactoring.
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def reset_game(self):
        self.player = X
        self.board.reset()

    def move(self):
        if self.board.turn == self.minmax_ai:
            move = self.get_best_move(self.player, self.board)
        else:
            move = random.choice(self.board.open_squares)
        self.board.place(self.player, move)
        self.player = self.player.opponent

    def print_recent_game_stats(self):
        x_wins = (float(self.recent_wins[X]) / 100.0)
        x_ties = (float(self.recent_ties[X]) / 100.0)
        x_loss = (float(self.recent_loses[X]) / 100.0)
        x_comb = x_wins + x_ties

        o_wins = (float(self.recent_wins[O]) / 100.0)
        o_ties = (float(self.recent_ties[O]) / 100.0)
        o_loss = (float(self.recent_loses[O]) / 100.0)
        o_comb = o_wins + o_ties

        print "\n"
        print "X win rate: {}%".format(int(floor(x_wins * 100)))
        print "X tie rate: {}%".format(int(floor(x_ties * 100)))
        print "X loss rate: {}%\n".format(int(floor(x_loss * 100)))

        print "O win rate: {}%".format(int(floor(o_wins * 100)))
        print "O tie rate: {}%".format(int(floor(o_ties * 100)))
        print "O loss rate: {}%\n".format(int(floor(o_loss * 100)))

        print "X WIN+TIE RATE: {}%".format(int(floor(x_comb * 100)))
        print "O WIN+TIE RATE: {}%".format(int(floor(o_comb * 100)))

    def play(self):
        print("How about a nice game of chess? No? Tic-Tac-Toe? Allons-y!")

        sys.stdout.write("\nPlaying")
        try:
            game_subcount = 0
            games_played = 0
            while games_played < 1000:
                finished_game = False
                finished_game_reset = False

                for i in range(9):
                    self.move()
                    sys.stdout.write('.')
                    if not self.board.game_over:
                        continue
                    if self.board.winner == X:
                        self.wins[X] += 1
                        self.loses[O] += 1
                        self.recent_wins[X] += 1
                        self.recent_loses[O] += 1
                        sys.stdout.write(repr(X))
                    if self.board.winner == O:
                        self.wins[O] += 1
                        self.loses[X] += 1
                        self.recent_wins[O] += 1
                        self.recent_loses[X] += 1
                        sys.stdout.write(repr(O))
                    break
                if not self.board.winner:
                    self.ties[X] += 1
                    self.ties[O] += 1
                    self.recent_ties[X] += 1
                    self.recent_ties[O] += 1
                    sys.stdout.write('T')
                games_played += 1
                finished_game = True

                game_subcount += 1
                if game_subcount == 100:
                    self.print_recent_game_stats()
                    # Reset last 100 game stats & counter
                    game_subcount = 0
                    for player in O, X:
                        self.recent_wins[player] = 0
                        self.recent_ties[player] = 0
                        self.recent_loses[player] = 0

                self.reset_game()
                finished_game_reset = True
        except KeyboardInterrupt:
            if not finished_game:
                pass
            if not finished_game_reset:
                self.reset_game()
        finally:
            print("\nTotal Games: %d" % games_played)
            print("\n[ X ]=---------")
            print("WINS:   %d" % self.wins[X])
            print("TIES:   %d" % self.ties[X])
            print("LOSES:  %d" % self.loses[X])
            print("\n[ O ]=---------")
            print("WINS:   %d" % self.wins[O])
            print("TIES:   %d" % self.ties[O])
            print("LOSES:  %d" % self.loses[O])

            assert self.loses[self.minmax_ai] == 0
            assert self.wins[self.minmax_ai.opponent] == 0
