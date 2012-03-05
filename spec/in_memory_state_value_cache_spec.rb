#
#  specified class:         InMemoryStateValueCache
#  extends:                 --
#  module:                  TicTacToe
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
#
require 'benchmark'

require 'state'
require 'state_observer'
require 'abstract_strategy'
require 'negamax'
require 'infinity'
require 'transposition_table'
require 'mock_game'
require 'abstract_strategy_spec'
require 'in_memory_state_value_cache'

module TicTacToe
  #
  #  Test class for specifying module contract.
  #
  class NegamaxPlusInMemoryCache < Negamax
    include InMemoryStateValueCache
  end

  describe InMemoryStateValueCache do
    it "should memorize and recall states" do

      @observe = NegamaxPlusInMemoryCache.new
      @observe.clear_state_value_table!

      @state                     = State.new [ 1,2,0, 0,0,0, 0,0,0 ]
      @transposed_state          = State.new [ 1,0,0, 2,0,0, 0,0,0 ]
      @inverted_state            = State.new [ 0,0,0, 0,0,0, 1,2,0 ]
      @inverted_horizontal_state = State.new [ 0,2,1, 0,0,0, 0,0,0 ]
      @rotated_state             = State.new [ 0,0,1, 0,0,2, 0,0,0 ]
      @rotated_ccw_state         = State.new [ 0,0,0, 2,0,0, 1,0,0 ]
      @rotated_180_state         = State.new [ 0,0,0, 0,0,0, 0,2,1 ]

      @transpositions = [ @transposed_state, @inverted_state, @inverted_horizontal_state,
                          @rotated_state,   @rotated_ccw_state, @rotated_180_state ]

      player, depth, color, value = 1, 0, 1, 0
      m = @observe.matrix(@state)

      @observe.collect_state_values.should be_empty
      @observe.recognized?(m).should be false
      @observe.memorize(m, player, depth, color, value)

      @observe.recognized?(m).should be value
      @transpositions.each do |transposition|
        m = @observe.matrix(transposition)
        @observe.recognized?(m).should be value
      end
    end
  end

  describe NegamaxPlusInMemoryCache do
    it_should_behave_like 'an optimization'
  end
end
