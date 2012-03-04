#
#  specified class:  MinimaxWithTranspositionsTable
#  extends:          --
#  module:           TicTacToe
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe

  #
  #
  #     Wrap a transposition table around the minimax implementation
  #
  class MinimaxWithTranspositionTable < Minimax
    
    include TranspositionTable

    # redefine value
    alias :_value :value

    def value(state, player=1, depth=0)
      return lookup(state) if depth < -4 and recognized? state
      val = _value(state, player, depth)
      memorize(state, val) if depth < -4
      val
    end
  end
end