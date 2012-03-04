require 'state_observer'
require 'abstract_strategy'
require 'mock_game'
require 'alpha_beta'
require 'state'
require 'abstract_strategy_spec'

require 'hashing_provider'
require 'transposition_table'
require 'alpha_beta_with_transpositions_table'

module TicTacToe
  describe AlphaBetaWithTranspositionsTable do
    it_should_behave_like 'a strategy'
  end
end