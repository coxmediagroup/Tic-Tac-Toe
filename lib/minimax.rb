module TicTacToe

  INFINITY = 1.0/0

  class Minimax

    #
    #   walk minimax tree for a given state on behalf of player.
    #
    #   assumes state.successors is a hash of moves => successor states
    #
    def Minimax.value(state, player=1, depth=0, observe=StateObserver.new) # , cutoff_depth=-Infinity)
      raise StandardError.new("argument three is depth!") unless depth.is_a? Integer
      if observe.terminal?(state)
        score = observe.evaluate(state, player)
        score *= INFINITY if depth == 0
        # puts "=== minimax [depth=#{depth}, score=#{score}]"
        return score
      end

      Tree.new(state).generate_successors if state.successors.empty?

      successors_values = state.successors.map do |m, succ|
        Minimax.value(succ, player, depth-1, observe)
      end

      # minimax
      score = 0
      # puts "current player: #{state.current_player} (#{player})"
      if state.current_player == player
        score = successors_values.max
        # puts "max #{score}"
      else
        score = successors_values.min
        # puts "min #{score}"
      end
      # puts "--- minimax [depth=#{depth}, score=#{score}]"
      score

    end

    #
    #   select the best move
    #
    def Minimax.best_move(state, player=1, observe=StateObserver.new)
      raise ArgumentError.new("first argument must be a State object") unless state.is_a? State
      raise StandardError.new("state must be playable") if observe.terminal?(state)

      # pick the first square if board is empty
      # p state
      return 0 if state.empty?

      # build successors tree if not already present
      Tree.new(state).generate_successors if state.successors.empty? 

      puts "===="
      best_position_and_successor = state.successors.max_by do |m, succ|

        score = Minimax.value(succ, player, 0, observe)
        puts "--- scored move #{m} (#{score})"
        score
      end

      # return best position
      best_position_and_successor.first
    
    end # end Minimax.best_move

  end
end