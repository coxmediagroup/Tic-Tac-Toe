#
#  file:             strategy_benchmark_suite.rb
#  description:
#
#     Performs a benchmarking suite of the available algorithms.
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
#
require 'state'
require 'state_observer'
require 'abstract_strategy'
require 'mock_game'
require 'state'
require 'infinity'
require 'transposition_table'
require 'in_memory_state_value_cache'

require 'minimax'
require 'minimax_with_transposition_table'
require 'minimax_with_in_memory_cache'

require 'alpha_beta'
require 'alpha_beta_with_transposition_table'
require 'alpha_beta_with_in_memory_cache'

require 'negamax'
require 'negamax_with_transposition_table'
require 'negamax_with_in_memory_cache'

require 'stringio'
require 'benchmark'

module TicTacToe
  def self.mock_games(algorithm)
    MockGame.new(algorithm).play_successors(State.new,1,false)
  end

  Benchmark.bm(20) do |algorithm|

    # negamax
    algorithm.report("negamax") { TicTacToe.mock_games(Negamax.new) }

    algorithm.report("negamax + table") {
      TicTacToe.mock_games(NegamaxWithTranspositionTable.new)
    }

    algorithm.report("negamax + cache") do
      TicTacToe.mock_games(NegamaxWithInMemoryCache.new)
    end

    # minimax + a/b pruning
    algorithm.report("a/b") { TicTacToe.mock_games(AlphaBeta.new) }

    algorithm.report("a/b + table") do
      TicTacToe.mock_games(AlphaBetaWithTranspositionTable.new)
    end
    algorithm.report("a/b + cache") do
      TicTacToe.mock_games(AlphaBetaWithInMemoryCache.new)
    end


    # minimax
    algorithm.report("minimax") { TicTacToe.mock_games(Minimax.new) }

    algorithm.report("minimax + table") do
      TicTacToe.mock_games(MinimaxWithTranspositionTable.new)
    end

    algorithm.report("minimax + cache") do
      TicTacToe.mock_games(MinimaxWithInMemoryCache.new)
    end
  end
end