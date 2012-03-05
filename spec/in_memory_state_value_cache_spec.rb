require 'benchmark'

require 'state'
require 'state_observer'
require 'abstract_strategy'
require 'alpha_beta'
require 'infinity'
require 'transposition_table'
require 'mock_game'
require 'abstract_strategy_spec'
require 'in_memory_state_value_cache'

module TicTacToe
  describe InMemoryStateValueCache do

    class AlphaBetaPlusInMemoryCache < AlphaBeta
      include InMemoryStateValueCache
    end



    before(:each) do
      @sample = AlphaBetaPlusInMemoryCache.new
      @sample.clear_state_value_table!

      @state                     = State.new [ 1,2,0, 0,0,0, 0,0,0 ]
      @transposed_state          = State.new [ 1,0,0, 2,0,0, 0,0,0 ]
      @inverted_state            = State.new [ 0,0,0, 0,0,0, 1,2,0 ]
      @inverted_horizontal_state = State.new [ 0,2,1, 0,0,0, 0,0,0 ]
      @rotated_state             = State.new [ 0,0,1, 0,0,2, 0,0,0 ]
      @rotated_ccw_state         = State.new [ 0,0,0, 2,0,0, 1,0,0 ]
      @rotated_180_state         = State.new [ 0,0,0, 0,0,0, 0,2,1 ]
    end

    it "should remeber, recognize and lookup states" do
      @sample.collect_state_values.should be_empty

      @sample.recognized?(@state).should be false
      @sample.memorize(@state,1)

      @sample.recognized?(@state).should be 1
      @sample.recognized?(@transposed_state).should be 1
      @sample.recognized?(@inverted_state).should be 1
      @sample.recognized?(@rotated_state).should be 1
      @sample.recognized?(@inverted_horizontal_state).should be 1
      @sample.recognized?(@rotated_180_state).should be 1
      @sample.recognized?(@rotated_ccw_state).should be 1
    end

    it "should integrate safely into and optimize over an existing algorithm" do
      describe AlphaBetaPlusInMemoryCache do
        it_should_behave_like 'an optimization'
      end
    end
  end
end
