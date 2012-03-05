#
#  class:                   NegamaxWithInMemoryCache
#  extends:                 AbstractStrategy
#  module:                  TicTacToe
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#

module TicTacToe
  #
  #  Augments negamax algorithm with a transposition-aware cache.
  #
  class NegamaxWithInMemoryCache < Negamax
    include InMemoryStateValueCache
  end
end