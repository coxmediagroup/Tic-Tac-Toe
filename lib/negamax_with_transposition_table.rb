#
#  specified class:         NegamaxWithTranspositionTable
#  extends:                 Negamax
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe
  #
  #  Integrates a transposition table into the negamax algorithm.
  #
  class NegamaxWithTranspositionTable < Negamax
    include TranspositionTable
  end
end
