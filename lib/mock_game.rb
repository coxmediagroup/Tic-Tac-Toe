#
#  class:                   StateObserver
#  extends:                 --
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe

  #
  #     Performs a mock run through a game, playing an AI against
  #     itself, with or without debug output indicating the state
  #     of the mock game being played.
  #
  class MockGame < StateObserver
    attr_accessor :ai

    #
    #   The constructor takes the algorithm to be used in the game
    #
    def initialize(algorithm=AlphaBetaWithTranspositionTable.new)
      raise StandardError.new("algorithm must subclass AbstractStrategy -- provided #{algorithm.name}") unless algorithm.is_a? AbstractStrategy
      @ai = algorithm
    end

    #
    #   Play mock games for all successors of a given state up
    #   to the specified depth.
    #
    def play_successors(state, depth=1, debug=true)
      scores = [0,0,0]
      return scores if terminal? state
      each_immediate_successor_state(state) do |successor|
        new_scores = [0,0,0]

        unless depth > 0
          game_result = play(successor, debug)
          new_scores[game_result] += 1
        else
          new_scores = play_successors(successor, depth-1, debug)
        end

        # sum pairs of array entries
        scores = scores.zip(new_scores).map { |e| e[0] + e[1] }
      end
      scores
    end

    #
    #   Play mock games for the immediate successors of a given
    #   game state.
    #
    def play_immediate_successors(state, debug=true)
      scores = [0,0,0]
      each_immediate_successor_state(state) do |successor|
        scores[play(successor, debug)] += 1
      end
      puts "==== draws: #{scores[0]} / wins: #{scores[1]} / losses: #{scores[2]} ===" if debug
      scores
    end

    #
    #     Simulate play of an AI player against itself.
    #
    def play(state, debug=true)
      puts '*' * 80 if debug
      # puts "--- playing game..." if debug

      first_player = state.current_player
      second_player = 3 - first_player

      # play game out
      until terminal? state
        state = move!(state, first_player, debug)
        state = move!(state, second_player, debug) unless terminal? state
      end
      puts '===== game complete ======' if debug

      return winner(state)
    end

    #
    #    Perform a single move in a simulated game.
    #
    def move!(state, player, debug=true)
      if debug
        puts '=' * 30
        puts
        pp state
        puts
      end
      move = @ai.best_move(state, player, debug)
      state.successor move
    end

  end
end
