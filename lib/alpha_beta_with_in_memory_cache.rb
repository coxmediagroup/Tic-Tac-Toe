#
#  class:                   AlphaBetaWithInMemoryCache
#  extends:                 AlphaBeta
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe
  #
  #  Extend the standard minimax with a/b pruning algorithm with a
  #  transposition-sensitive in-memory state => value caching facility.
  #
  class AlphaBetaWithInMemoryCache < AlphaBeta
    include InMemoryStateValueCache
  end
end