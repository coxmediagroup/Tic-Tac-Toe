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

    INFINITY = 1.0/0

    #
    #  Invoke the best move possible -- will invoke a method "value" on
    #  self with each successor state, the current player and the initial depth (0),
    #  selecting the best-ranking move.
    #
    def best_move(state, player=1, debug=false)

      best_val = -INFINITY
      best_position = nil
      pp state if debug
      each_immediate_successor_state_with_index(state) do |succ, i|
        move_value = value(succ, player, 0) # , self)

        # puts "--- #{self.class.name} got move value #{move_value} for move #{i}" if debug

        if move_value >= best_val
          best_val = move_value
          best_position = i
        end
      end

     # puts "=== #{self.class.name} returning #{best_position} as best position" if debug

      # return best position
      best_position

    end

    protected

    #
    #  calculate the final score for a terminal board state
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
