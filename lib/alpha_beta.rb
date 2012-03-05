#
#  class:         AlphaBeta
#  extends:       AbstractStrategy
#  module:        TicTacToe
#  author:        Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe
  #
  #  Encapsulates an alpha-beta pruning approach to speeding up
  #  the computation of the minimax.
  #
  class AlphaBeta < AbstractStrategy
    #
    #   Walk minimax tree for a given state on behalf of player,
    #   using alpha/beta pruning to optimize search.
    #
    def value(state, player=1, depth=0, alpha=-INFINITY,beta=INFINITY,color=nil)

      return endgame_score(state,player,depth) if terminal?(state)

      player_up = state.current_player == player
      score = 0

      if player_up
        each_immediate_successor_state(state) do |succ|
          subalpha = value(succ, player, depth-1, alpha, beta)
          alpha = [alpha, subalpha].max
          break if beta <= alpha
        end
        score = alpha
      else
        each_immediate_successor_state(state) do |succ|
          subbeta = value(succ, player, depth-1, alpha, beta)
          beta = [beta, subbeta].min
          break if beta <= alpha
        end
        score = beta
      end

      score

    end
  end
end