require 'state'
require 'hashing_provider'
require 'transposition_table'

module TicTacToe
  describe TranspositionTable, "tracks a map of states => values up to state isomorphy" do
    #  before(:each) do
    #    @transposition_table = TranspositionTable.new
    #  end

    class ExampleTranspositionTableUtilizingClass
      include TranspositionTable
    end
  
    before(:each) do
      @sample = ExampleTranspositionTableUtilizingClass.new
      @state = State.new [
        1,2,0,
        0,0,0,
        0,0,0
      ]

      @transposed_state = State.new [
        1,0,0,
        2,0,0,
        0,0,0
      ]
    
      @inverted_state = State.new [
        0,0,0,
        0,0,0,
        1,2,0
      ]

      @inverted_horizontal_state = State.new [
        0,2,1,
        0,0,0,
        0,0,0

      ]

      @rotated_state = State.new [
        0,0,0,
        2,0,0,
        1,0,0
      ]

      # try to prevent test leakage here (think it was causing failures when running spec suite?)
      TranspositionTable.clear! # = {}
    end

    it "should apply transformations" do
      @sample.apply(TranspositionTable::TRANSPOSE, @state).board.should == @transposed_state.board
      @sample.apply(TranspositionTable::INVERSE, @state).board.should == @inverted_state.board
      @sample.apply(TranspositionTable::INVERSE_HORIZ, @state).board.should == @inverted_horizontal_state.board
      @sample.apply(TranspositionTable::ROTATE, @state).board.should == @rotated_state.board
    end


    it "should remeber, recognize and lookup states" do
      @sample.recognized?(@state).should be false
      @sample.memorize(@state,1)

      @sample.recognized?(@inverted_state).should be true
      @sample.recognized?(@state).should be true
      @sample.recognized?(@rotated_state).should be true
      @sample.recognized?(@inverted_horizontal_state).should be true

      @sample.lookup(@state).should be 1
      @sample.lookup(@inverted_state).should be 1
      @sample.lookup(@rotated_state).should be 1
      @sample.lookup(@inverted_horizontal_state).should be 1
    end
  end

end