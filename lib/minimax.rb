#
#  specified class:         Minimax
#  extends:                 --
#  module:                  TicTacToe
#
#   description:
#
#   Recursively calculates the value of the minimax tree for a given
#   state, and recommends a best move to a player.
#   
#   The implementation is for now a very simple no-frills MiniMax,
#   which does seem to work effectively. It's a bit slow, of course.
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
#

module TicTacToe

  INFINITY = 1.0/0

  class Minimax

    #
    #   sum minimax trees for a given state on behalf of player.
    #
    #   note that we do assume state.successors is a hash of moves => successor states
    #
    def Minimax.value(state, player=1, depth=0, observe=StateObserver.new)
      if observe.terminal?(state)
        return 0 if observe.draw?(state)
        score = observe.evaluate(state, player)
        if depth >= -1
          score = score * INFINITY
        end
        return score
      end

      Tree.new(state).generate_successors if state.successors.empty?

      # 'sum' the minimax trees of successor states
      successors_values = state.successors.values.map do |succ|
        Minimax.value(succ, player, depth-1, observe)
      end

      score = 0
      if state.current_player == player
        score = successors_values.max
      else
        score = successors_values.min
      end
      score
    end

    
    #
    #   select the best move by ranking minimax trees
    #   for each potential next game state
    #
    def Minimax.best_move(state, player=1, observe=StateObserver.new)
      Tree.new(state).generate_successors if state.successors.empty?

      best_position = state.successors.max_by do |m,succ|
        Minimax.value(succ, player, 0, observe) 
      end.first

      # return best position
      best_position
      
    end # end Minimax.best_move



  end
end