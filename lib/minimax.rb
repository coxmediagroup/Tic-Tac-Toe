#
#  class:     Minimax
#  extends:   AbstractStrategy
#  module:    TicTacToe
#  author:    Joseph Weissman, <jweissman1986@gmail.com>
#

module TicTacToe


  #
  #   Recursively calculates the value of the minimax tree for a given state
  #
  class Minimax < AbstractStrategy



    #
    #   Sum minimax trees for a given state on behalf of player.
    #
    def value(state, player=1, depth=0,alpha=nil, beta=nil,color=nil)

      return endgame_score(state,player,depth) if terminal?(state)

      successors_values = []
      each_immediate_successor_state(state) do |successor|
        successor_value = value(successor, player, depth-1)
        successors_values << successor_value
      end

      score = 0
      if state.current_player == player
        score = successors_values.max
      else
        score = successors_values.min
      end
      score
    end


  end
end