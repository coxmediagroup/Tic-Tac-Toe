#
#  class:         MinimaxSpec
#  extends:       --
#  module:        TicTacToe
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
#

require 'state_observer'
require 'abstract_strategy'
require 'abstract_strategy_spec'
require 'minimax'
require 'state'
require 'mock_game'

module TicTacToe
  #
  #   Provides a specification for the Minimax implementation powering the
  #   engine. (Note: these tests have been moved up to a shared test group
  #   at 'abstract_strategy_spec'.)
  #
  describe Minimax do
    it_should_behave_like "a strategy"
  end
end