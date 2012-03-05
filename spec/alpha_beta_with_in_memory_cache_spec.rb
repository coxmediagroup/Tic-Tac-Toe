#
#  specified class:         AlphaBetaWithInMemoryCache
#  extends:                 --
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
#
require 'state_observer'
require 'abstract_strategy'
require 'mock_game'
require 'alpha_beta'
require 'state'
require 'abstract_strategy_spec'
require 'infinity'
require 'transposition_table'
require 'in_memory_state_value_cache'
require 'alpha_beta_with_in_memory_cache'

module TicTacToe
  describe AlphaBetaWithInMemoryCache do
    it_should_behave_like 'a strategy'
  end
end

