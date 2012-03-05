#
#  specified class:         TranspositionTable
#  extends:                 --
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
require 'state'
require 'state_observer'
require 'abstract_strategy'
require 'alpha_beta'
require 'infinity'
require 'transposition_table'
require 'mock_game'

require 'abstract_strategy_spec'

module TicTacToe

  #
  #     Provides a specification for the transposition table functionality.
  #
  #     TODO specify override behavior 
  #
  describe TranspositionTable do

    class AlphaBetaPlusTranspositionTable < AlphaBeta
      include TranspositionTable
    end
  
    before(:each) do
      @sample = AlphaBetaPlusTranspositionTable.new

      @state                     = State.new [ 1,2,0, 0,0,0, 0,0,0 ]
      @transposed_state          = State.new [ 1,0,0, 2,0,0, 0,0,0 ]
      @inverted_state            = State.new [ 0,0,0, 0,0,0, 1,2,0 ]
      @inverted_horizontal_state = State.new [ 0,2,1, 0,0,0, 0,0,0 ]
      @rotated_state             = State.new [ 0,0,1, 0,0,2, 0,0,0 ]
      @rotated_ccw_state         = State.new [ 0,0,0, 2,0,0, 1,0,0 ]
      @rotated_180_state         = State.new [ 0,0,0, 0,0,0, 0,2,1 ]
    end

    it "should apply transformations" do
      m = @sample.matrix(@state)

      transformations_and_expected_states = {
        TranspositionTable::IDENTITY      => @state,
        TranspositionTable::TRANSPOSE     => @transposed_state,
        TranspositionTable::INVERSE       => @inverted_state,
        TranspositionTable::INVERSE_HORIZ => @inverted_horizontal_state,
        TranspositionTable::ROTATE        => @rotated_state,
        TranspositionTable::ROTATE_CCW    => @rotated_ccw_state,
        TranspositionTable::ROTATE_180    => @rotated_180_state
      }

      transformations_and_expected_states.each do |txf, state|
        @sample.apply_transformation(txf,m).should == state.board
      end
    end


    it "should identify transpositionally unique successor states" do
      @sample.open_positions(State.new).should have(3).items

      # TODO assert that none of the transpositions is actually the SAME as
      #      any of the others and that they ARE transpositionally identical
    end


    it "should integrate safely into and optimize over an existing algorithm" do
      describe AlphaBetaPlusTranspositionTable do
        it_should_behave_like "an optimization"
      end
    end
  end

end