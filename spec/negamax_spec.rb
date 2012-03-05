#
#  specified class:         Negamax
#  extends:                 --
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
require 'state_observer'
require 'abstract_strategy'
require 'abstract_strategy_spec'
require 'state'
require 'infinity'
require 'mock_game'
require 'negamax'

module TicTacToe
  describe Negamax do
   it_should_behave_like 'a strategy'
  end
end