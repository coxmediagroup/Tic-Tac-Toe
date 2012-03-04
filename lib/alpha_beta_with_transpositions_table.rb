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
  class AlphaBetaWithTranspositionsTable < AlphaBeta
    
    include TranspositionTable

    alias :_value :value

    def value(state,player=1,depth=0,alpha=-INFINITY,beta=INFINITY)
      return lookup(state) if depth < -4 and recognized? state
      val = _value(state,player,depth,alpha,beta)
      memorize(state,val)
      val
    end
    
    # TODO could also override open_positions to only show topologically 
    #      UNIQUE successors -- could really help early game, when there's
    #      really only two or three moves to look at, but it 'feels' like
    # =>   8 to the CPU without knowing about the transpositions table


  end
end
