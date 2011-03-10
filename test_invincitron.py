'''
tests for invincitron

'''

import random

import invincitron as I

# notes
# first move should be x
# 2nd should be a corner
# 3rd should be a corner

# in good vs good, should be ties?
# in good vs random, random should never win

def play_n_games(n,player1_cls,player2_cls):
    return [I.play_game(player1_cls(),player2_cls()) for ii in xrange(n)]
    

class test_good_vs_good(object):
    @classmethod
    def setup_class(cls):
        cls.games = play_n_games(2000,I.GoodPlayer,I.GoodPlayer)

    def test_all_first_move_is_center(self):
        for winner,game,moves in self.games: 
            assert moves[0] == 4

    def test_all_2nd_move_is_corner(self):
        corners = set([0,2,6,8])
        for winner,game,moves in self.games:
            assert moves[1] in corners, "boo!  %s %s %s" % (winner,game,moves)

    def test_all_3rd_move_is_opposite_corner(self):
        for winner,game,moves in self.games:
            assert (moves[1] + moves[2]) == 8  # too clever by half

    def test_all_ties(self):
        assert all((x[0] == 'TIE' for x in self.games))


class test_good_vs_random(object):
    @classmethod
    def setup_class(cls):
        cls.games1 = play_n_games(1000,I.GoodPlayer,I.RandomPlayer)
        cls.games2 = play_n_games(1000,I.RandomPlayer,I.GoodPlayer)

    def test_random_never_wins(self):
        assert all((x[0] != 'O' for x in self.games1))
        assert all((x[1] != 'X' for x in self.games2))
 
