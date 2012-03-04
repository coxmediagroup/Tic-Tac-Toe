#
#  class:                   Minimax
#  extends:                 --
#  module:                  TicTacToe
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#

module TicTacToe


  #
  #   Recursively calculates the value of the minimax tree for a given state
  #
  class Minimax < AbstractStrategy



    #
    #   Sum minimax trees for a given state on behalf of player.
    #
    def value(state, player=1, depth=0) # , observe=StateObserver.new)

      return endgame_score(state,player,depth) if terminal?(state)
#        return 0 if draw?(state)
#        score = evaluate(state, player)
#        if depth >= -1
#          score = score * INFINITY
#        end
#        return score
#      end

      successors_values = []
      each_immediate_successor_state(state) do |successor|
        successor_value = value(successor, player, depth-1)
        successors_values << successor_value
      end

      score = 0
      # p successors_values
      if state.current_player == player
        score = successors_values.max
      else
        score = successors_values.min
      end
      score
    end


  end
end