#
#
#     Naive implementation of minimax algorithm for tic-tac-toe.
#
#     Wishlist:
#       - a/b pruning
#       - transposition table
#       - iterative deepening
#
#
#

module TicTacToe

  INFINITY = 1.0/0

  class Minimax




    #
    #   walk minimax tree for a given state on behalf of player.
    #
    #   assumes state.successors is a hash of moves => successor states
    #
    def Minimax.value(state, player=1, depth=0, observe=StateObserver.new) #,alpha=-INFINITY,beta=INFINITY) # , cutoff_depth=-Infinity)
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

      # min/max!
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
      # raise StandardError("cannot play ")
      Tree.new(state).generate_successors if state.successors.empty?

      best_position = state.successors.max_by { |m,succ|
        Minimax.value(succ, player, 0, observe)
      }.first

      # return best position
      best_position # _and_successor.first
    end # end Minimax.best_move



#    def Minimax.zobrist(matrix)
#
#      # should seed...
#      r ||= Array.new(3) { |i| Array.new(3) { |j| Array.new(3) { |k| rand } } }
#
#      key = 0
#      matrix.each_with_index do |row, x|
#        row.each_with_index do |value, y|
#          key ^= r[x][y][value][player] # observe.matrix(state)
#        end
#      end
#
#      key
#    end
#
#    def Minimax.value(state, player=1, depth=0, observe=StateObserver.new)
#
#      @@transpositions ||= {}
#
#      matrix             = observe.matrix(state)
#      transpose          = observe.transpose(state)
#      inverse            = observe.flip_vertical(state)
#      inverse_horizontal = observe.flip_horizontal(state)
#      rotated            = observe.rotate(state)
#      rotated_ccw        = observe.rotate_ccw(state)
#      transpositions     = [ matrix, transpose, inverse,
#                             inverse_horizontal, rotated, rotated_ccw ]
#
#      val = nil
#      state_hashes = transpositions.map { |t| Minimax.hash(t,player) }
#      state_hashes.each do |state_hash|
#        val = @@transpositions[state_hash] if @@transpositions.has_key? state_hash
#      end
#
#      val = _value(state, player, depth, observe)
#
#      state_hashes.each do |state_hash|
#        @@transpositions[state_hash] = val
#      end
#
#      val
#    end

  end
end