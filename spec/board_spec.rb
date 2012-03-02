#
#
#    Specifications for the TicTacToe::Board class.
#
#
require 'board'

module TicTacToe

  describe Board, "constructor interface" do
    it "may be constructed without options" do
      @board = Board.new

      # should have sane defaults
      @board.field.should == Array.new(9) {0}
    end
=begin
    it "may be constructed with optional :size parameter" do
      @board = Board.new :size => [4,4]
      @board.matrix.length.should    be 4
      @board.matrix[0].length.should be 4
    end
=end
  end

  #
  #  A board should be able to manage inscriptions and construct
  #  a plaintext representation of the current game state.
  #
  describe Board, "inscription handling" do
    before(:each) do
      @board = Board.new
    end

    it "should accept and erase inscriptions" do
      @board.turn = 1
      @board.inscribe! [0, 0]
      @board.get(0,0).should be 1
      @board.erase! [0,0]
      @board.get(0,0).should be 0

      @board.turn = 2
      @board.inscribe! [2, 1]
      @board.get(2,1).should be 2
      @board.erase! [2,1]
      @board.get(2,1).should be 0
    end

    it "should format an empty board for display" do
      @board.pretty.should == "   |   |   \n-----------\n   |   |   \n-----------\n   |   |   \n"
    end

    it "should format an inscribed board for display" do
      # make a few marks
      @board.inscribe! [0,1]
      @board.turn = 2
      @board.inscribe! [1,2]
      @board.pretty.should == "   | X |   \n-----------\n   |   | O \n-----------\n   |   |   \n"
    end
  end
  


  #
  #  A board should provide introspection and game analysis facilities.
  #
  describe Board, "game analysis" do

    it "should construct a game matrix" do
      @board = Board.new(:field => [
        0,2,1,
        1,1,2,
        2,2,0
      ]).matrix.should == [
        [0,2,1],
        [1,1,2],
        [2,2,0]
      ]
    end

    it "should correctly identify diagonals" do
      @board = Board.new(:field => [
        0,2,1,
        1,1,2,
        2,2,0
      ])

      @board.diagonals.should == [
        [0,1,0],[1,1,2]
      ]

      @board.rows_columns_and_diagonals.should == [
        [0,2,1],
        [1,1,2],
        [2,2,0],

        [0,1,2],
        [2,1,2],
        [1,2,0],

        [0,1,0],
        [1,1,2]
      ]
    end

    it "should gather legal moves" do
      @board = Board.new(:field => [
        0,2,1,
        1,1,2,
        2,2,0
      ]).unmarked_positions.should == [[0,0],[2,2]]
    end
    
    it "should gather legal next states" do
      @board = Board.new(:field => [
        0,2,1,
        1,1,2,
        2,2,0
      ], :turn => 1)

      b = @board

      next_states = @board.legal_next_states

      next_states.collect(&:field).should == [
       [1,2,1,
        1,1,2,
        2,2,0],
       [0,2,1,
        1,1,2,
        2,2,1]      
      ]

      next_states.collect(&:turn).should == [ 2, 2 ]

      # ensure we haven't possibly mutated the original board config
      b.field.should == @board.field
      b.turn.should == @board.turn
    end
=begin
    it "should gather legal future states" do
      Board.new(:matrix => [
        [0,2,1],
        [1,1,2],
        [2,2,1]
      ]).legal_future_states(1).map(&:matrix).should == [
       [[1,2,1],
        [1,1,2],
        [2,2,1]]
      ]
    end
=end
  end


  #
  #  A board should be able to detect various end-game conditions.
  #
  describe Board, "end game detection" do

    it "should recognize when a game is incomplete" do
      @board = Board.new :turn => 2, :field => [
        2,1,0,
        1,2,1,
        1,2,1
      ]

      @board.done?.should == false
      # @board.winner.should raise ArgumentError
    end

    it "should detect a draw" do
      @board = Board.new :field => [
        2,2,1,
        1,1,2,
        2,2,1
      ]
      @board.done?.should == true
      @board.winner.should be 0
    end

    it "should detect a horizontal win" do
      @board = Board.new :field => [
        2,2,1,
        1,1,2,
        2,2,2
      ]
      @board.winner.should be 2
    end

    it "should detect a diagonal win" do
      @board = Board.new :field => [
        2,2,1,
        2,1,2,
        1,2,2
      ]
      @board.winner.should be 1

    end

  end



end