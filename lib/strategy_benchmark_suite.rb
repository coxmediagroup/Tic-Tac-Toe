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
require 'minimax'
require 'alpha_beta'
require 'state'
require 'hashing_provider'
require 'transposition_table'
require 'minimax_with_transposition_table'
require 'alpha_beta_with_transposition_table'

require 'stringio'
require 'benchmark'

module TicTacToe
  

  def self.mock_games(algorithm)
    MockGame.new(algorithm).play_successors(State.new,1,false)
  end

  Benchmark.bm(1) do |algorithm|

    algorithm.report("minimax") { TicTacToe.mock_games(Minimax.new) }
    algorithm.report("minimax + table") do
      TicTacToe.mock_games(MinimaxWithTranspositionTable.new)
    end

    algorithm.report("alpha-beta") { TicTacToe.mock_games(AlphaBeta.new) }
    algorithm.report("alpha-beta + table") do
      TicTacToe.mock_games(AlphaBetaWithTranspositionTable.new)
    end
  end
end