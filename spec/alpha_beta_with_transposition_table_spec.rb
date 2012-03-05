#
#  specified class:         AlphaBetaWithTranspositionsTable
#  extends:                 --
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
require 'state_observer'
require 'abstract_strategy'
require 'mock_game'
require 'alpha_beta'
require 'state'
require 'abstract_strategy_spec'
require 'infinity'
require 'transposition_table'
require 'alpha_beta_with_transposition_table'

module TicTacToe
  describe AlphaBetaWithTranspositionTable do
    it_should_behave_like 'a strategy'
  end
end