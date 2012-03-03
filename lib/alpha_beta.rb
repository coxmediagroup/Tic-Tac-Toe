#
#
#  alpha/beta pruning -- under construction
#
module TicTacToe
  class AlphaBeta < Minimax
    # def initialize; end


    #
    #   walk minimax tree for a given state on behalf of player.
    #
    #   use a/b pruning to optimize search.
    #
    #   assumes state.successors is a hash of moves => successor states
    #
    #   NOTE: under construction
    #   TODO investigate
    #
=begin
    def AlphaBeta.value(state, player=1, depth=0, observe=StateObserver.new,alpha=1,beta=-1) # , cutoff_depth=-Infinity)

      if observe.terminal?(state)
        return 0 if observe.draw?(state)
        score = observe.evaluate(state, player)
        if depth >= -2
         score = score * INFINITY
        end
        return score
      end

      Tree.new(state).generate_successors if state.successors.empty?

      # 'sum' the minimax trees of successor states
      player_up = state.current_player == player
      # score = player_up ? -INFINITY : INFINITY
      if player_up
        state.successors.values.each do |succ|
          minimax = AlphaBeta.value(succ, player, depth-1, observe, alpha, beta)
          alpha = [alpha, minimax].max
          break if beta <= alpha
        end
        return alpha
      else
        state.successors.values.each do |succ|
          minimax = AlphaBeta.value(succ, player, depth-1, observe, alpha, beta)
          beta = [beta, minimax].min
         break if alpha <= beta
        end
        return beta
      end
    end
=end
  end
end
