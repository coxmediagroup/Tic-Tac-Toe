"""
Copyright (C) 2014 Ryan Hansen.  All rights reserved.
This source code (including its associated software) is owned by Ryan Hansen and
is protected by United States and international intellectual property law, including copyright laws, patent laws,
and treaty provisions.
"""

import itertools

from core.const import PLAYERS, WIN_VECTORS


class Game(object):
    x = []
    o = []

    def available(self, board=None):
        """
        Return a list of available moves based on the position already held by both players
        """
        if not board:
            board = self.x + self.o
        moves = []
        p = 0
        for p in range(0, 9):
            if p not in board:
                moves.append(p)
            p += 1
        return moves

    def take(self, player, pos):
        """
        Assign the chose position to the given player
        """
        attr = self.__getattribute__(PLAYERS[player])
        attr.append(pos)

    def eval_game(self, player, depth=0):
        """
        Determine the next move based on the implementation of the famous minimax algorithm
        """
        depth += 1  # Recursion depth, incrementing by one with each pass
        score = 0  # The minimax score for the move being evaluated
        scores = {}  # The collection of scores for each of the moves evaluated
        opponent = self.switch_player(player)  # opponent gets passed to next_move for minimax recursion
        if self.winner(opponent):
            if depth % 2 == 0:
                return 10 - depth
            else:
                return depth - 10
        board = self.available()  # get available moves
        # If no moves left, the game is over and we have had no winners, so it's a draw.  Return a score of 0
        if len(board) == 0:
            return 0
        for m in board:  # Start evaluating available moves
            self.take(player, m)  # Take the proposed move
            score = self.eval_game(opponent, depth)  # play out the game and return the score of the proposed move
            self.clear(player, m)  # Once scored, roll back the move
            scores[m] = score  # Add the score to the collection
        if depth % 2 == 0:
            return min(scores, key=scores.get)  # Return the lowest scoring move
        else:
            return max(scores, key=scores.get)  # Return the highest scoring move


    def winner(self, player):
        """
        Check to see if <player> has won the game
        """
        # Get the occupied positions held by <player>
        occupied = self.__getattribute__(PLAYERS[player])
        # Loop over all 3-digit permutations of <player>'s positions, comparing each one against known win vectors.
        # If we find a match, we have a winner.
        for p in itertools.permutations(occupied, 3):
            if p in WIN_VECTORS:
                return p
        return False

    def winnable(self, player):
        """
        Test if the current game state is winnable by <player>.  If true, return the winning position.
        Obviously, if the game is winnable for <player>, it is also blockable for the opponent, so this same function
        may be used for either detection depending on whose turn it is.
        """
        # Get the occupied positions for the player
        occupied = self.__getattribute__(PLAYERS[player])
        # Get the occupied position for the opponent
        opp = self.__getattribute__(PLAYERS[self.switch_player(player)])
        # Loop frenzy. I'll buy lunch for whoever comes up with the list comprehension for this sucker. I gave up.
        for v in WIN_VECTORS:  # Loop the win vectors
            for perm in itertools.permutations(v, 2):  # Loop through all 2-digit permutations of each vector
                vector = list(perm)  # Listify each permutation
                for p in itertools.permutations(occupied, 2):  # Loop through all 2-digit permutations of occupied
                    if list(p) == vector:
                        # At this point, we know the player holds two positions that match one of the win vectors
                        # which means we have a possible winner.  We then return the position that will result in the
                        # win (or block, as the case may be).  Easy enough using some "set" magic.
                        win = list(set(v) - set(vector))[0]
                        # Now we make sure win move is not held by the opponent
                        if win not in opp:
                            return win
        return False

    def switch_player(self, player):
        """
        Return the opponent of <player>.  This becomes useful for the back-and-forth nature of minimax.
        """
        return [k for k, v in PLAYERS.iteritems() if k != player][0]

    def clear(self, player, pos):
        """
        Clear a give move from <player>'s occupied positions
        """
        moves = self.__getattribute__(PLAYERS[player])
        moves.remove(pos)

    def reset(self):
        self.x = []
        self.o = []


if __name__ == '__main__':
    g = Game()
    move = g.eval_game('machine')
    print move