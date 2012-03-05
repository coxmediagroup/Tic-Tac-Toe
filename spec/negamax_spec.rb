# To change this template, choose Tools | Templates
# and open the template in the editor.

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