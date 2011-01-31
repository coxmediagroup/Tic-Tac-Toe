"""
This performs a brute force and very naive walk of the game tree
for tic tac toe.

Rationale
=========

The basic idea here is that there are 9 squares, chosen in sequence,
so there can be no more than 9! (==362880) possible lines of play.

In fact, there are far fewer lines than this, because many lines
are trimmed early due to one player winning.

Since Tic Tac Toe is a game of complete information, it doesn't matter
which sequence of moves lead to a particular board configuration. It
is possible to model the game as 3^9 (==39366) states: X, O, or _
for each of the 9 squares (you also need to know whose turn it is,
but this is easily deduced by comparing the number of Xs and Os).

The game tree could be even further trimmed by considering states that
are the same except for rotation or mirroring. For example, the nine
possible first moves could be trimmed down to three: center, corner,
side.

However, 9! is a small enough number that walking the entire tree
is fairly painless, and the path based approach works well with
the magic accessor methods (.XA1.OA2, etc) in the TicTacToe class.


Scoring
=======

Each node in the tree is given three scores, corresponding to the
total number of sub-paths through its child nodes that lead to a
win for X, a win for O, or a tie.

The scores are normalized for comparison, so that for any node n
at depth d in the tree:

   X + O + Tie == (9-d)!
       where (X, O, Tie) = score(n)

Example:

    >>> from MinMaxMoe.tictactoe import TicTacToe
    >>> node = TicTacToe().XB2.OA1.XA2.OB1.XC2
    >>> node
    TicTacToe().XB2.OA1.XA2.OB1.XC2 # [ O O _ | X X X | _ _ _ ], X wins.
    >>> node.depth
    5
    >>> score(node)
    NodeScore(X=24, O=0, Tie=0)

Here the score for X is 24 because there are 4! (==24) ways the four
empty cells could have been filled.

Normalizing the scores at each level of the tree makes it trivial for
the minimax algorithm to choose between moves.
    
"""
import sys
from MinMaxMoe.tictactoe import TicTacToe, X, O, kTie
from collections import namedtuple
import operator
import datetime
import anydbm


kDbmName = 'gametree.dbm'


NodeScoreBase = namedtuple('NodeScore', ('X', 'O', 'Tie'))
class NodeScore(NodeScoreBase):
    """
    A named tuple for representing the three score values for each
    game tree node. This is the output of the score() function.
    """
    def __add__(self, other):
        """
        >>> NodeScore(1, 2, 3) + NodeScore(10, 20, 30)
        NodeScore(X=11, O=22, Tie=33)
        """
        return NodeScore(X = self.X + other.X,
                         O = self.O + other.O,
                         Tie = self.Tie + other.Tie)


fact = lambda n : reduce(operator.mul, range(1, n+1), 1)
assert fact(5) == 120


def score(node, collector=None):

    if node.isOver:
        points = fact(9-node.depth)
        winner = node.winner

        result = NodeScore(X = points if winner == X else 0,
                         O = points if winner == O else 0,
                         Tie = points if winner == kTie else 0)

    else:
        children = [getattr(node, move) for move in node.moves]
        result = sum((score(child, collector) for child in children),
                     NodeScore(0, 0, 0))

    if collector is not None:
        collector.save(node.path, result)

    return result



class PrintCollector(object):
    """
    This just prints the scores as they're calculated.
    """
    def save(self, path, score):
        print path, "=>", score
    def done(self):
        print "-" * 60


class DictCollector(object):
    """
    This saves the values to any mapping/dict-style object.
    """
    def __init__(self, data):
        self.dict = data
    def save(self, path, score):
        self.dict[path] = score
    def done(self):
        pass

class AnyDbmCollector(object):
    """
    This saves the values to a dbm. It will overwrite the
    dbm file if already present.

    The X, O, and Tie scores are flattened to space-delimited
    string, since anydbm values must always be strings.
    """
    def __init__(self, filename):
        self.dbm = anydbm.open(filename, 'n')
    def save(self, path, score):
        self.dbm[path] = '%s %s %s' % score
    def done(self):
        self.dbm.close()



def main(collector):
    started = datetime.datetime.now()
    print '[%s] generating tree to %s. This may take a few minutes...' \
        % (started, kDbmName)
    score(TicTacToe(), collector)
    collector.done()
    ended = datetime.datetime.now()
    print "[%s] tree walked in %s seconds" % (ended, (ended-started).seconds)


if __name__=="__main__":
    if "-t" in sys.argv:
        import doctest
        doctest.testmod()
    elif "-p" in sys.argv:
        main(PrintCollector())
    else:
        main(AnyDbmCollector(kDbmName))
