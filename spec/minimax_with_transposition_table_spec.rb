#
#  specified class:         MinimaxWithTranspositionTable
#  extends:                 --
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
require 'state_observer'
require 'abstract_strategy'
require 'minimax'
require 'mock_game'
require 'alpha_beta'
require 'state'
require 'abstract_strategy_spec'
require 'transposition_table'
require 'minimax_with_transposition_table'

module TicTacToe
  describe MinimaxWithTranspositionTable do
    it_should_behave_like 'a strategy'
  end
end