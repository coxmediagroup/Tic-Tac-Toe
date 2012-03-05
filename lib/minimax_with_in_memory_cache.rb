#
#  specified class:         MinimaxWithInMemoryCache
#  extends:                 Minimax
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#

module TicTacToe
  #
  #  Integrates a transpositionally-aware in-memory cache into the minimax
  #  algorithm.
  #
  class MinimaxWithInMemoryCache < Minimax
    include InMemoryStateValueCache
  end
end
