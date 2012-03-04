require 'state_observer'
require 'abstract_strategy'
require 'mock_game'
require 'alpha_beta'
require 'state'
require 'abstract_strategy_spec'

module TicTacToe
  describe AlphaBeta do
    it_should_behave_like 'a strategy'
  end
end