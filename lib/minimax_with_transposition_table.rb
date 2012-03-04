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
  end
end