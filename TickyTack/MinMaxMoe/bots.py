"""
Bots to play tic tac toe.
"""
from MinMaxMoe.tictactoe import otherSide
from MinMaxMoe.gentree import NodeScore, fact

class MinMaxMoeBot(object):
    """
    Uses the minimax algorithm from game theory.

    That is, it compares the opponent's maximum payoff given
    each possible move, and chooses the move that minimizes
    this value.

    Scores for each node are precomputed in gentree.py
    and stored in an external anydbm-compatable mapping.
    See that file for complete details.
    """
    name = 'MinMaxMoe'
    def __init__(self, dbm, verbose=False):
        """
        @param dbm a anydbm instance (see gentree.py)
        """
        self.dbm = dbm
        self.verbose = verbose

    def log(self, note):
        if self.verbose:
            print note

    def getScore(self, root, branch):
        string = self.dbm['%s.%s' % (root, branch)]
        return NodeScore(*map(int, string.split()))
        
    def choose(self, game):
        root = game.path
        self.log('analyzing node: %s' % root)
        choices = [(branch, self.getScore(root, branch))
                  for branch in game.moves]
        opponent = otherSide(game.toPlay)

        # !! we'll track two numbers because we have to consider
        # both the number of paths where the opponent wins AND
        # the number of paths where we tie. The initial value here
        # is incredibly pessimistic (opponent wins every time).
        minMax = (fact(9), 0)

        best = None
        for branch, nodeScore in choices:
            score = (getattr(nodeScore, opponent), nodeScore.Tie)
            self.log('  .%s -> %6s' % (branch, score))
            if score < minMax:
                minMax = score
                best = branch
        assert best is not None, "Something went terribly wrong!"
        return best



class DumbBot(object):
    """
    Always chooses the first available move.
    This was basically just for testing the UI.
    """
    name = 'DumbBot'
    def choose(self, game):
        return game.moves[0]

