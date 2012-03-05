#
#  specified class:         TranspositionTable
#  extends:                 --
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
require 'state'
require 'state_observer'
require 'abstract_strategy'
require 'negamax'
require 'infinity'
require 'transposition_table'
require 'mock_game'
require 'benchmark'
require 'abstract_strategy_spec'

module TicTacToe

  #
  #     Provides a specification for the transposition table functionality.
  #
  describe TranspositionTable do

    class NegamaxPlusTranspositionTable < Negamax
      include TranspositionTable
    end
  
    before(:each) do
      @observe = NegamaxPlusTranspositionTable.new

      @state                     = State.new [ 1,2,0, 0,0,0, 0,0,0 ]
      @transposed_state          = State.new [ 1,0,0, 2,0,0, 0,0,0 ]
      @inverted_state            = State.new [ 0,0,0, 0,0,0, 1,2,0 ]
      @inverted_horizontal_state = State.new [ 0,2,1, 0,0,0, 0,0,0 ]
      @rotated_state             = State.new [ 0,0,1, 0,0,2, 0,0,0 ]
      @rotated_ccw_state         = State.new [ 0,0,0, 2,0,0, 1,0,0 ]
      @rotated_180_state         = State.new [ 0,0,0, 0,0,0, 0,2,1 ]
    end

    it "should apply transformations" do
      m = @observe.matrix(@state)

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
        @observe.apply_transformation(txf,m).flatten.should == state.board
      end
    end

    it "should identify transpositionally unique successor states" do
      @observe.open_positions(State.new).should have(3).items
      original_matrix = @observe.matrix(@state)
      for transformation in TranspositionTable::TRANSPOSITIONS
        for other_transformation in TranspositionTable::TRANSPOSITIONS
          unless transformation == other_transformation
            transposed_matrix = @observe.apply_transformation(transformation, original_matrix)
            transposed_other_matrix = @observe.apply_transformation(other_transformation, original_matrix)
            @observe.are_transpositionally_isomorphic?(original_matrix,transposed_matrix).should be true
            @observe.are_transpositionally_isomorphic?(original_matrix,transposed_other_matrix).should be true
            transposed_matrix.should_not == transposed_other_matrix
          end
        end
      end
    end


    describe NegamaxPlusTranspositionTable do
      it_should_behave_like "an optimization"
    end
  end
end