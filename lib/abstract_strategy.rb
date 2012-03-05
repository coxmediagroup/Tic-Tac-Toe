#
#  class:                   AbstractStrategy
#  extends:                 --
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe

  #
  #   Abstract superclass for the various implementations
  #   of different gameplaying algorithms
  #
  class AbstractStrategy < StateObserver


    #
    #  Invoke the best move possible -- will invoke a method "value" on
    #  self providing as arguments the successor state, the current player
    #  and the initial depth (0). We select the best-ranking move.
    #
    def best_move(state, player=1, debug=true)

      pp state if debug
      best_val = -INFINITY
      best_position = nil

      each_immediate_successor_state_with_index(state) do |succ, i|
        move_value = value(succ, player, 0)
        if move_value >= best_val
          best_val = move_value
          best_position = i
        end
        puts "--- move #{i} has value #{move_value}" if debug
      end

      puts "===== best position: #{best_position}" if debug
      
      # return best position
      best_position

    end

    protected

    #
    #  Calculate the final score for a terminal board state.
    #
    def endgame_score(state, player, depth)
        return 0 if draw?(state)
        score = evaluate(state, player)
        if depth >= -1
          score = score * INFINITY
        end
        return score
    end
  end
end
