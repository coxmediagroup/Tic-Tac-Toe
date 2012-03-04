#
#  class:         AlphaBetaWithTranspositionsTable
#  extends:       --
#  module:        TicTacToe
#  author:        Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe
  #
  #  Extends the existing alpha/beta pruning technique with
  #  transposition tables.
  #
  class AlphaBetaWithTranspositionTable < AlphaBeta
    include TranspositionTable
  end
end
