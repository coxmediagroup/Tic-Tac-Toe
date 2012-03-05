#
#  class:                   Negamax
#  extends:                 AbstractStrategy
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe
  #
  #   Negamax offers a coding simplification over minimax: rather than handling
  #   min'ing and max'ing players differently, we keep track of an alternating
  #   'color' and directly select the max over subtree values every time.
  #
  class Negamax < AbstractStrategy
    #
    #  Perform a negamax over the state tree (determine the value of a given
    #  node with provided color.)
    #
    def value(state, player=1, depth=0, alpha=-INFINITY, beta=INFINITY, color=1)
      color = -color
      return color*endgame_score(state,player,depth) if terminal? state

      score = -INFINITY
      each_immediate_successor_state(state) do |succ|
        subalpha = -value(succ, player, depth-1, -beta, -alpha, color)
        score    = [score, subalpha].max
        alpha    = [alpha, subalpha].max
        break unless beta > alpha
      end
      score
    end

    #
    #  Override best_move -- the negamax implementation above indicates the LOWEST
    #  value as the best one.
    #
    def best_move(state, player=1, debug=true)
      best_val = INFINITY
      best_position = nil

      each_immediate_successor_state_with_index(state) do |succ, i|
        move_value = value(succ, player, 0)
        if move_value <= best_val
          best_val = move_value
          best_position = i
        end
      end
      best_position
    end
  end
end